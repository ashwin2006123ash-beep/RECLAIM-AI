"""
RECLAIM AI 2.0 - Innovation 1: Recovery Twin & Dependency Graph Engine
Builds and maintains a structured, live digital representation of every recovery case
with a topological dependency graph, dynamic state transitions, and unblocking rules.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from agent.readiness import calculate_readiness_score
from agent.source_registry import lookup_sources
from agent.fee_verifier import verify_document_fee
from database.models import save_recovery_twin, get_recovery_twin

# Valid Graph Node States
NODE_STATES = ["BLOCKED", "READY", "IN_PROGRESS", "COMPLETED", "NEEDS_VERIFICATION"]

class RecoveryTwinEngine:
    """
    Manages the Digital Twin of a lost document case.
    Recalculates the topological dependency graph upon any case modification.
    """

    NODE_DEFINITIONS = [
        {
            "id": "IDENTIFY_AUTHORITY",
            "name": "Identify Issuing Authority",
            "description": "Establish the specific board, university, RTO, or government department responsible for reissue.",
            "dependencies": []
        },
        {
            "id": "VERIFY_PROCESS",
            "name": "Verify Official Recovery Process",
            "description": "Retrieve official circulars, statutory gazettes, and verified government portal routes.",
            "dependencies": ["IDENTIFY_AUTHORITY"]
        },
        {
            "id": "GATHER_EVIDENCE",
            "name": "Gather Required Evidence",
            "description": "Assemble mandatory evidence (Police Loss Report/DDR, Notarized Affidavit, Identity Proof, Previous Copy).",
            "dependencies": ["VERIFY_PROCESS"]
        },
        {
            "id": "CONFIRM_FEE",
            "name": "Confirm Applicable Statutory Fee",
            "description": "Verify official government fee schedule from gazette or flag unverified costs.",
            "dependencies": ["VERIFY_PROCESS"]
        },
        {
            "id": "PREPARE_APPLICATION",
            "name": "Prepare Recovery Application",
            "description": "Synthesize application dossier and prefilled submission package.",
            "dependencies": ["GATHER_EVIDENCE", "CONFIRM_FEE"]
        },
        {
            "id": "OBTAIN_APPROVAL",
            "name": "Obtain Citizen Approval",
            "description": "Pause execution at Step 8 Human Approval Gate for explicit user review and authorization.",
            "dependencies": ["PREPARE_APPLICATION"]
        },
        {
            "id": "EXECUTE_SUBMISSION",
            "name": "Execute Simulated Submission",
            "description": "Submit application to Safe Action Sandbox / Mock Government Portal with idempotency key.",
            "dependencies": ["OBTAIN_APPROVAL"]
        },
        {
            "id": "VERIFY_STATUS",
            "name": "Verify Resulting Status",
            "description": "Independently query mock portal backend to verify receipt and confirmed demo state.",
            "dependencies": ["EXECUTE_SUBMISSION"]
        }
    ]

    @classmethod
    def build_or_update_twin(cls, case_id: str, case_data: Dict[str, Any],
                             external_risk_flags: Optional[List[Dict[str, Any]]] = None,
                             mock_submission_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Builds or updates the digital recovery twin with categorized facts,
        evaluated dependencies, node states, and next recommended action.
        """
        doc_type = case_data.get("document_type", "edu_cert")
        jurisdiction = case_data.get("jurisdiction", "")
        authority = case_data.get("issuing_authority", "")
        status_type = case_data.get("status_type", "lost")
        has_police_report = bool(case_data.get("has_police_report"))
        has_affidavit = bool(case_data.get("has_affidavit"))
        has_id_proof = bool(case_data.get("has_id_proof"))
        has_doc_number = bool(case_data.get("has_doc_number_or_copy"))

        # 1. Structure Case Facts
        verified_facts = []
        user_facts = []
        uncertain_claims = []

        if doc_type:
            user_facts.append(f"Document category specified as '{doc_type}'")
        if status_type:
            user_facts.append(f"Loss condition declared as '{status_type}'")
        if has_police_report:
            user_facts.append("Police Report / Lost Document Entry declared available")
        if has_affidavit:
            user_facts.append("Notarized loss affidavit declared prepared")
        if has_id_proof:
            user_facts.append("Secondary government photo ID declared available")
        if has_doc_number:
            user_facts.append("Previous document registration/roll number or scan available")

        # Evaluate authority fact authenticity
        authority_is_known = bool(authority and authority.strip().lower() not in ["", "unknown", "unknown autonomous college", "unlisted"])
        jurisdiction_is_known = bool(jurisdiction and jurisdiction.strip().lower() not in ["", "unknown", "unknown state"])

        if authority_is_known and jurisdiction_is_known:
            verified_facts.append(f"Issuing authority identified as '{authority}' in jurisdiction '{jurisdiction}'")
        elif authority or jurisdiction:
            uncertain_claims.append("Authority or jurisdiction is vague / partially unverified")
        else:
            uncertain_claims.append("Issuing authority and state jurisdiction are completely unknown")

        # Check sources & fees
        sources = lookup_sources(doc_type, jurisdiction)
        fee_info = verify_document_fee(doc_type, authority)
        if fee_info.get("status") == "verified":
            verified_facts.append(f"Statutory fee verified: INR {fee_info.get('amount'):.2f} via {fee_info.get('source_title', 'Gazette')}")
        else:
            uncertain_claims.append("Statutory fee is unverified for this issuing institution")

        # 2. Evaluate Readiness Score
        readiness = calculate_readiness_score(case_data)

        # 3. Dynamic Dependency Graph Evaluation
        nodes: Dict[str, Dict[str, Any]] = {}

        # --- Node 1: IDENTIFY_AUTHORITY ---
        if authority_is_known and jurisdiction_is_known:
            n1_state = "COMPLETED"
            n1_blocked_reason = None
            n1_unblock_action = None
        elif authority_is_known or jurisdiction_is_known:
            n1_state = "NEEDS_VERIFICATION"
            n1_blocked_reason = "Partial authority details provided."
            n1_unblock_action = "Provide exact state department, board, or university name."
        else:
            n1_state = "BLOCKED"
            n1_blocked_reason = "Issuing authority and state are missing."
            n1_unblock_action = "Specify the exact issuing board (e.g. CBSE), university, or state RTO."

        nodes["IDENTIFY_AUTHORITY"] = {
            "id": "IDENTIFY_AUTHORITY",
            "name": "Identify Issuing Authority",
            "state": n1_state,
            "blocked_reason": n1_blocked_reason,
            "unblock_action": n1_unblock_action,
            "evidence_linked": [f"Authority: {authority or 'Unknown'}", f"State: {jurisdiction or 'Unknown'}"]
        }

        # --- Node 2: VERIFY_PROCESS ---
        if n1_state != "COMPLETED":
            n2_state = "BLOCKED"
            n2_blocked_reason = "Cannot verify process until issuing authority is identified."
            n2_unblock_action = "Complete Node 1: Identify Issuing Authority."
        else:
            has_official_source = any(s.get("verification_status") == "official_verified" for s in sources)
            if has_official_source:
                n2_state = "COMPLETED"
                n2_blocked_reason = None
                n2_unblock_action = None
            else:
                n2_state = "NEEDS_VERIFICATION"
                n2_blocked_reason = "No official gazetted process found in central registry."
                n2_unblock_action = "Query university registrar or regional transport office for local circular."

        nodes["VERIFY_PROCESS"] = {
            "id": "VERIFY_PROCESS",
            "name": "Verify Official Recovery Process",
            "state": n2_state,
            "blocked_reason": n2_blocked_reason,
            "unblock_action": n2_unblock_action,
            "evidence_linked": [s.get("issuing_authority") for s in sources if s.get("official_url")]
        }

        # --- Node 3: GATHER_EVIDENCE ---
        needs_fir = status_type == "stolen" or doc_type in ["driving_licence", "passport"]
        needs_affidavit = doc_type in ["edu_cert", "passport", "other_cert"]

        missing_evidence = []
        if needs_fir and not has_police_report:
            missing_evidence.append("Police Lost Document Entry (DDR/NCR/FIR)")
        if needs_affidavit and not has_affidavit:
            missing_evidence.append("Notarized Loss Affidavit on Stamp Paper")
        if not has_id_proof:
            missing_evidence.append("Government Photo Identity Proof")

        if n2_state == "BLOCKED":
            n3_state = "BLOCKED"
            n3_blocked_reason = "Prerequisite process verification incomplete."
            n3_unblock_action = "Complete Node 2: Verify Official Recovery Process."
        elif missing_evidence:
            n3_state = "IN_PROGRESS"
            n3_blocked_reason = f"Missing mandatory evidence: {', '.join(missing_evidence)}."
            n3_unblock_action = f"Obtain and verify: {missing_evidence[0]}."
        else:
            n3_state = "COMPLETED"
            n3_blocked_reason = None
            n3_unblock_action = None

        nodes["GATHER_EVIDENCE"] = {
            "id": "GATHER_EVIDENCE",
            "name": "Gather Required Evidence",
            "state": n3_state,
            "blocked_reason": n3_blocked_reason,
            "unblock_action": n3_unblock_action,
            "evidence_linked": [f"Police Report: {has_police_report}", f"Affidavit: {has_affidavit}", f"ID Proof: {has_id_proof}"]
        }

        # --- Node 4: CONFIRM_FEE ---
        if n2_state == "BLOCKED":
            n4_state = "BLOCKED"
            n4_blocked_reason = "Authority not established."
            n4_unblock_action = "Resolve Node 1 & 2."
        elif fee_info.get("status") == "verified":
            n4_state = "COMPLETED"
            n4_blocked_reason = None
            n4_unblock_action = None
        else:
            n4_state = "NEEDS_VERIFICATION"
            n4_blocked_reason = "Statutory fee is unverified from public gazette."
            n4_unblock_action = "Check official gazette or student accounts section directly."

        nodes["CONFIRM_FEE"] = {
            "id": "CONFIRM_FEE",
            "name": "Confirm Applicable Statutory Fee",
            "state": n4_state,
            "blocked_reason": n4_blocked_reason,
            "unblock_action": n4_unblock_action,
            "evidence_linked": [fee_info.get("message", "Fee pending")]
        }

        # --- Node 5: PREPARE_APPLICATION ---
        # Blocked if critical evidence is missing or external risk flags are critical
        critical_risk = any(r.get("severity") in ["CRITICAL", "HIGH"] for r in (external_risk_flags or []))
        if n3_state != "COMPLETED":
            n5_state = "BLOCKED"
            n5_blocked_reason = f"Mandatory evidence incomplete ({', '.join(missing_evidence)})."
            n5_unblock_action = "Complete gathering required supporting documents."
        elif critical_risk:
            n5_state = "NEEDS_VERIFICATION"
            n5_blocked_reason = "High cybersecurity risk detected on target portal/intermediary."
            n5_unblock_action = "Review Recovery Risk Radar warnings before application preparation."
        else:
            n5_state = "COMPLETED"
            n5_blocked_reason = None
            n5_unblock_action = None

        nodes["PREPARE_APPLICATION"] = {
            "id": "PREPARE_APPLICATION",
            "name": "Prepare Recovery Application",
            "state": n5_state,
            "blocked_reason": n5_blocked_reason,
            "unblock_action": n5_unblock_action,
            "evidence_linked": ["Prefilled Dossier ready" if n5_state == "COMPLETED" else "Dossier blocked"]
        }

        # --- Node 6: OBTAIN_APPROVAL ---
        approval_status = case_data.get("approval_status", "pending")
        if n5_state != "COMPLETED":
            n6_state = "BLOCKED"
            n6_blocked_reason = "Application dossier has not been successfully prepared."
            n6_unblock_action = "Satisfy prerequisites in Node 5."
        elif approval_status == "approved":
            n6_state = "COMPLETED"
            n6_blocked_reason = None
            n6_unblock_action = None
        elif approval_status == "rejected":
            n6_state = "BLOCKED"
            n6_blocked_reason = "Citizen explicitly rejected or paused the proposed action."
            n6_unblock_action = "Citizen may review and grant approval when ready."
        else:
            n6_state = "READY"
            n6_blocked_reason = "Awaiting explicit citizen authorization at Step 8 Gate."
            n6_unblock_action = "Review consequences and click 'Approve & Proceed'."

        nodes["OBTAIN_APPROVAL"] = {
            "id": "OBTAIN_APPROVAL",
            "name": "Obtain Citizen Approval",
            "state": n6_state,
            "blocked_reason": n6_blocked_reason,
            "unblock_action": n6_unblock_action,
            "evidence_linked": [f"Citizen Decision: {approval_status.upper()}"]
        }

        # --- Node 7: EXECUTE_SUBMISSION ---
        has_mock_submission = mock_submission_state and mock_submission_state.get("submission_status") in ["CONFIRMED", "SUBMITTED"]
        if n6_state != "COMPLETED":
            n7_state = "BLOCKED"
            n7_blocked_reason = "Execution halted: Citizen approval not granted."
            n7_unblock_action = "Obtain approval at Node 6."
        elif has_mock_submission:
            n7_state = "COMPLETED"
            n7_blocked_reason = None
            n7_unblock_action = None
        else:
            n7_state = "READY"
            n7_blocked_reason = "Ready to execute against Safe Action Sandbox."
            n7_unblock_action = "Trigger sandbox submission with idempotency key."

        nodes["EXECUTE_SUBMISSION"] = {
            "id": "EXECUTE_SUBMISSION",
            "name": "Execute Simulated Submission",
            "state": n7_state,
            "blocked_reason": n7_blocked_reason,
            "unblock_action": n7_unblock_action,
            "evidence_linked": [f"Sandbox Status: {mock_submission_state.get('submission_status') if mock_submission_state else 'Not Executed'}"]
        }

        # --- Node 8: VERIFY_STATUS ---
        has_verified_ref = mock_submission_state and mock_submission_state.get("application_ref") and mock_submission_state.get("submission_status") == "CONFIRMED"
        if n7_state != "COMPLETED":
            n8_state = "BLOCKED"
            n8_blocked_reason = "No confirmed simulated execution to verify."
            n8_unblock_action = "Complete Node 7."
        elif has_verified_ref:
            n8_state = "COMPLETED"
            n8_blocked_reason = None
            n8_unblock_action = None
        else:
            n8_state = "IN_PROGRESS"
            n8_blocked_reason = "Awaiting backend confirmation receipt."
            n8_unblock_action = "Run independent mock portal status check."

        nodes["VERIFY_STATUS"] = {
            "id": "VERIFY_STATUS",
            "name": "Verify Resulting Status",
            "state": n8_state,
            "blocked_reason": n8_blocked_reason,
            "unblock_action": n8_unblock_action,
            "evidence_linked": [f"Receipt: {mock_submission_state.get('application_ref') if has_verified_ref else 'None'}"]
        }

        # 4. Next Best Action determination
        next_best_action = "Review recovery guidance"
        for node_id in ["IDENTIFY_AUTHORITY", "VERIFY_PROCESS", "GATHER_EVIDENCE", "CONFIRM_FEE", "PREPARE_APPLICATION", "OBTAIN_APPROVAL", "EXECUTE_SUBMISSION", "VERIFY_STATUS"]:
            node = nodes[node_id]
            if node["state"] in ["BLOCKED", "NEEDS_VERIFICATION", "IN_PROGRESS", "READY"]:
                next_best_action = node["unblock_action"] or node["name"]
                break

        # 5. Overarching Case Status
        if nodes["VERIFY_STATUS"]["state"] == "COMPLETED":
            current_status = "RECOVERY_SIMULATION_CONFIRMED"
        elif nodes["OBTAIN_APPROVAL"]["state"] == "READY":
            current_status = "AWAITING_CITIZEN_APPROVAL"
        elif n1_state == "BLOCKED":
            current_status = "CLARIFICATION_REQUIRED"
        elif n3_state == "IN_PROGRESS":
            current_status = "EVIDENCE_GATHERING"
        else:
            current_status = "GUIDANCE_ACTIVE"

        twin_data = {
            "case_id": case_id,
            "document_type": doc_type,
            "jurisdiction": jurisdiction,
            "issuing_authority": authority,
            "status_type": status_type,
            "facts": {
                "verified_facts": verified_facts,
                "user_provided_facts": user_facts,
                "uncertain_claims": uncertain_claims
            },
            "dependency_graph": {
                "nodes": nodes,
                "node_order": [d["id"] for d in cls.NODE_DEFINITIONS],
                "definitions": cls.NODE_DEFINITIONS
            },
            "readiness_score": readiness["score"],
            "readiness_breakdown": readiness,
            "current_status": current_status,
            "next_best_action": next_best_action,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        # Persist in SQLite
        save_recovery_twin(
            case_id=case_id,
            document_type=doc_type,
            jurisdiction=jurisdiction,
            issuing_authority=authority,
            status_type=status_type,
            facts=twin_data["facts"],
            dependency_graph=twin_data["dependency_graph"],
            readiness_score=readiness["score"],
            current_status=current_status
        )

        return twin_data
