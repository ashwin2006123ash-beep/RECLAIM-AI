"""
RECLAIM AI 2.0 - Unified Agentic Workflow Engine
Integrates the 5 Core Innovations into one coordinated, inspectable agent loop:
OBSERVE -> BUILD RECOVERY TWIN -> INVESTIGATE -> REASON -> ASSESS RISK -> ACT SAFELY -> VERIFY -> LEARN
"""
import uuid
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from config import Config
from agent.source_registry import lookup_sources, get_all_sources
from agent.safety_guard import evaluate_source_safety
from agent.fee_verifier import verify_document_fee
from agent.readiness import calculate_readiness_score
from agent.gemini_client import generate_agent_recovery_guidance
from agent.recovery_twin import RecoveryTwinEngine
from agent.research_agent import ResearchAgent
from agent.adaptive_planner import AdaptiveRecoveryPlanner
from agent.risk_radar import RecoveryRiskRadar
from agent.mock_portal import MockGovernmentPortalService, SYNTHETIC_RECEIPT_WATERMARK
from database.models import (
    create_or_update_session,
    get_session_by_id,
    add_trace_event,
    add_evidence,
    create_approval_request,
    resolve_approval_request,
    get_session_trace,
    get_session_evidence,
    get_session_approvals,
    update_session_workflow
)

class AgenticRecoveryWorkflow:
    """
    Coordinated Agent Loop executing:
    Stage 1: OBSERVE & INTAKE
    Stage 2: BUILD RECOVERY TWIN & CLASSIFY
    Stage 3: INVESTIGATE & PROOF-OF-TRUTH RESEARCH
    Stage 4: REASON & ADAPTIVE MULTI-ROUTE PLANNING
    Stage 5: ASSESS RISK & CYBERSECURITY RADAR
    Stage 6: ACT SAFELY (Draft Compilation & Step 8 Approval Gate)
    Stage 7: EXECUTE PERMITTED ACTION (Safe Action Sandbox)
    Stage 8: VERIFY & LEARN FROM RESULT (Independent Verification)
    """

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"REC-{uuid.uuid4().hex[:8].upper()}"

    def run_full_intake_and_guidance(self, intake_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes Stages 1 through 6 (Intake to Human Approval Gate).
        Stages 7 and 8 are executed upon explicit citizen approval.
        """
        session_id = self.session_id
        
        # ---------------- STAGE 1 / STEP 1: OBSERVE & INTAKE ----------------
        doc_type = intake_data.get("document_type", "edu_cert")
        jurisdiction = intake_data.get("jurisdiction", "")
        issuing_authority = intake_data.get("issuing_authority", "")
        status_type = intake_data.get("status_type", "lost")
        external_url = intake_data.get("external_url_to_test")
        
        intake_valid = bool(doc_type)
        missing_inputs = []
        if not jurisdiction:
            missing_inputs.append("State or Jurisdiction")
        if not issuing_authority:
            missing_inputs.append("Issuing Authority")
            
        add_trace_event(
            session_id=session_id,
            step_number=1,
            step_name="STEP 1: INTAKE",
            status="complete" if intake_valid else "flagged",
            input_summary=f"Doc Type: {doc_type}, Jurisdiction: {jurisdiction or 'Unspecified'}, Status: {status_type}",
            decision="Accept input and initialize Recovery Twin" if intake_valid else "Reject incomplete intake",
            reason=f"Validated required fields. Missing: {', '.join(missing_inputs) if missing_inputs else 'None'}.",
            evidence_ref="Citizen Intake Declaration",
            action_taken="Parsed intake payload and created persistent case state",
            outcome="Case intake registered"
        )
        
        # ---------------- STAGE 2 / STEP 2: CLASSIFY & BUILD RECOVERY TWIN ----------------
        cat_meta = next((c for c in Config.DOCUMENT_CATEGORIES if c["id"] == doc_type), None)
        category_name = cat_meta["name"] if cat_meta else doc_type
        
        # Build live digital Recovery Twin with dynamic dependency graph
        recovery_twin = RecoveryTwinEngine.build_or_update_twin(
            case_id=session_id,
            case_data=intake_data
        )

        add_trace_event(
            session_id=session_id,
            step_number=2,
            step_name="STEP 2: CLASSIFY",
            status="complete",
            input_summary=f"Category: {category_name}, Status: {status_type}",
            decision=f"Constructed Recovery Twin with {len(recovery_twin['dependency_graph']['nodes'])} dependency nodes",
            reason="Every lost document has statutory dependency prerequisites (bylaws, police loss reports, sworn affidavits).",
            evidence_ref="Statutory Category Mapping Registry",
            action_taken=f"Initialized Recovery Twin #{session_id}; Next Best Action: {recovery_twin['next_best_action']}",
            outcome=f"Twin Status: {recovery_twin['current_status']}"
        )
        
        # ---------------- STAGE 3 / STEP 3: PLAN ROADMAP ----------------
        add_trace_event(
            session_id=session_id,
            step_number=3,
            step_name="STEP 3: PLAN",
            status="complete",
            input_summary=f"Authority: {issuing_authority or 'Pending Lookup'}",
            decision="Formulated 5-stage official reissue progression roadmap",
            reason="Citizens require an explainable roadmap to bypass predatory middlemen and costly mistakes.",
            evidence_ref="Civic Reissue Blueprint",
            action_taken="Structured sequential recovery path: Verify Authority -> File Police Loss -> Notarize Affidavit -> Digital Pull -> Reissue Application",
            outcome="Recovery sequence ready for source retrieval"
        )
        
        # ---------------- STAGE 4 / STEP 4: INVESTIGATE & RETRIEVE (RESEARCH AGENT) ----------------
        # Innovation 2: Proof-of-Truth Research Agent
        research_intel = ResearchAgent.investigate_case_evidence(
            case_id=session_id,
            document_type=doc_type,
            jurisdiction=jurisdiction,
            issuing_authority=issuing_authority,
            external_url=external_url
        )

        candidate_sources = lookup_sources(doc_type, jurisdiction)
        all_candidates = list(candidate_sources)
        if external_url:
            all_candidates.append({
                "source_id": "SRC_EXTERNAL_USER_CANDIDATE",
                "document_category": doc_type,
                "jurisdiction": jurisdiction or "External",
                "issuing_authority": "Third-Party Candidate / Web Source",
                "official_hostname": external_url,
                "official_url": external_url,
                "source_type": "External Search Candidate",
                "information_available": "Claims document reissue assistance",
                "verification_status": "unverified"
            })
            
        add_trace_event(
            session_id=session_id,
            step_number=4,
            step_name="STEP 4: RETRIEVE",
            status="complete",
            input_summary=f"Retrieved {len(all_candidates)} sources, {research_intel['claims_count']} claims, {research_intel['conflicts_count']} conflicts",
            decision=f"Mined statutory evidence claims from official registry" + (f" and candidate URL ({external_url})" if external_url else ""),
            reason="Authoritative sources must be verified prior to making procedural claims.",
            evidence_ref="Proof-of-Truth Research Agent",
            action_taken="Extracted claims, assigned provenance tags (LIVE_VERIFIED / CACHED / UNVERIFIED), and evaluated conflicts",
            outcome=f"Evidence Vault populated with {research_intel['claims_count']} claims"
        )
        
        # ---------------- STAGE 5 / STEP 5: VERIFY & ASSESS RISK (RISK RADAR) ----------------
        verified_sources = []
        flagged_sources = []
        
        for cand in all_candidates:
            target_url = cand.get("official_url") or cand.get("official_hostname")
            safety_eval = evaluate_source_safety(target_url)
            
            if safety_eval["is_official"]:
                verified_sources.append(cand)
                add_evidence(
                    session_id=session_id,
                    source_id=cand.get("source_id", "SRC_VERIFIED"),
                    source_title=cand.get("issuing_authority", "Official Portal"),
                    source_url=cand.get("official_url", target_url),
                    verification_status="official_verified",
                    extracted_summary=cand.get("information_available", "Official reissue portal guidelines."),
                    decision_supported=f"Used to define legitimate application process for {doc_type}."
                )
            else:
                flagged_info = {
                    "source_id": cand.get("source_id", "SRC_FLAGGED"),
                    "title": cand.get("issuing_authority", target_url),
                    "url": target_url,
                    "threat_level": safety_eval["threat_level"],
                    "reason": safety_eval["reason"],
                    "action": safety_eval["action"]
                }
                flagged_sources.append(flagged_info)
                add_evidence(
                    session_id=session_id,
                    source_id=cand.get("source_id", "SRC_FLAGGED"),
                    source_title=cand.get("issuing_authority", target_url),
                    source_url=target_url,
                    verification_status=safety_eval["verification_status"],
                    extracted_summary=safety_eval["reason"],
                    decision_supported="Excluded from recommendations; flagged as unofficial/untrusted."
                )

        # Innovation 4: Recovery Risk Radar Scan
        risk_radar_result = RecoveryRiskRadar.analyze_case_risks(
            case_data=intake_data,
            evidence_claims=research_intel["claims"],
            candidate_url=external_url
        )

        # If risk radar identified critical threats, update recovery twin
        if risk_radar_result["blocked_nodes"]:
            recovery_twin = RecoveryTwinEngine.build_or_update_twin(
                case_id=session_id,
                case_data=intake_data,
                external_risk_flags=risk_radar_result["warnings"]
            )
                
        verification_status_step = "flagged" if (flagged_sources or risk_radar_result["warnings"]) else "complete"
        add_trace_event(
            session_id=session_id,
            step_number=5,
            step_name="STEP 5: VERIFY",
            status=verification_status_step,
            input_summary=f"Risk Level: {risk_radar_result['overall_risk_level']} (Score: {risk_radar_result['risk_score']}/100)",
            decision=(
                f"Approved {len(verified_sources)} official government portals. "
                f"Flagged {len(flagged_sources)} unofficial brokers. Active Risk Warnings: {risk_radar_result['warning_count']}."
            ),
            reason="Strict domain allowlist enforcement and Risk Radar protect citizens against fraudulent fees and data harvesting.",
            evidence_ref="Recovery Risk Radar & Safety Guard",
            action_taken="Filtered candidate URLs through SSRF checker, allowlist, and 9-point threat scanner",
            outcome=f"{len(verified_sources)} sources verified; {len(flagged_sources)} excluded"
        )
        
        # ---------------- STAGE 6 / STEP 6: APPLY RULES & REASON (ADAPTIVE PLANNER) ----------------
        fee_info = verify_document_fee(doc_type, issuing_authority)
        readiness_info = calculate_readiness_score(intake_data)
        
        # Innovation 3: Adaptive Recovery Multi-Route Decision Engine
        route_planning = AdaptiveRecoveryPlanner.evaluate_and_compare_routes(
            case_data=intake_data,
            readiness_data=readiness_info,
            risk_data=risk_radar_result
        )

        rule_summary = (
            f"Readiness: {readiness_info['score']}/100. "
            f"Recommended Route: {route_planning['recommended_route']['name'] if route_planning['recommended_route'] else 'Pending Authority Clarification'}. "
            f"Fee Status: {fee_info['status']} ({fee_info.get('currency', 'INR')} {fee_info.get('amount') or 'N/A'})."
        )
        
        add_trace_event(
            session_id=session_id,
            step_number=6,
            step_name="STEP 6: APPLY RULES",
            status="complete",
            input_summary=f"Readiness Score: {readiness_info['score']}%, Fee: {fee_info['status']}",
            decision="Evaluated statutory rules across 3 comparative recovery routes",
            reason="Different routes have distinct trade-offs (e.g. DigiLocker is free & instant; Official portal delivers physical smart card).",
            evidence_ref="Adaptive Recovery Decision Engine",
            action_taken="Compared Route 1 (DigiLocker), Route 2 (Statutory Portal), and Route 3 (Physical Counter)",
            outcome=rule_summary
        )
        
        # ---------------- STAGE 7 / STEP 7: EXPLAIN ----------------
        guidance_result = generate_agent_recovery_guidance(
            intake_data=intake_data,
            verified_sources=verified_sources,
            fee_info=fee_info,
            readiness_info=readiness_info,
            flagged_sources=flagged_sources
        )

        # Attach 2.0 Innovations to guidance payload
        guidance_result["recovery_twin"] = recovery_twin
        guidance_result["research_intelligence"] = research_intel
        guidance_result["route_planning"] = route_planning
        guidance_result["risk_radar"] = risk_radar_result
        
        add_trace_event(
            session_id=session_id,
            step_number=7,
            step_name="STEP 7: EXPLAIN",
            status="complete",
            input_summary=f"Engine Mode: {guidance_result.get('engine_mode', 'DETERMINISTIC_FALLBACK_AI')}",
            decision="Synthesized explainable multi-route recovery guidance with 'Why did the agent choose this?' matrix",
            reason="Citizen must clearly understand what to do next, why each route was chosen or deferred, and statutory citations.",
            evidence_ref="AI Explanation Generator & Decision Matrix",
            action_taken="Generated transparent next steps, required documents list, route comparison, and readiness breakdown",
            outcome="Guidance synthesized and ready for citizen review"
        )
        
        # ---------------- STAGE 8 / STEP 8: HUMAN APPROVAL GATE (SAFE ACTION SANDBOX) ----------------
        # Prepare Draft for Sandbox
        sandbox_draft = MockGovernmentPortalService.prepare_draft_application(
            case_data=intake_data,
            readiness_data=readiness_info
        )
        sandbox_draft["case_id"] = session_id
        guidance_result["sandbox_draft"] = sandbox_draft

        proposed = guidance_result.get("proposed_action", {
            "action_id": "ACT_PREPARE_RECOVERY_DOSSIER",
            "name": "Prepare Official Application Dossier & Safe Portal Link",
            "description": f"Compile prefilled recovery dossier for {issuing_authority or 'Official Authority'}.",
            "requires_approval": True,
            "consequences": (
                "Will execute a verified simulation against the Safe Action Sandbox and generate an official recovery dossier. "
                "No actual government fees will be debited and no external database will be modified without your direct submission on the government website."
            )
        })
        
        approval_id = create_approval_request(
            session_id=session_id,
            proposed_action=f"{proposed['name']}: {proposed['description']}",
            consequences=proposed["consequences"]
        )
        
        add_trace_event(
            session_id=session_id,
            step_number=8,
            step_name="STEP 8: HUMAN APPROVAL",
            status="awaiting_approval",
            input_summary=f"Proposed Action: {proposed['name']}",
            decision="Halted automated execution; presented proposed action to citizen for explicit consent",
            reason="Human-in-the-loop gate ensures no action is executed without informed citizen authorization.",
            evidence_ref="Civic AI Safety Protocol / Step 8 Gate",
            action_taken=f"Created pending approval request #{approval_id}",
            outcome="Waiting for user decision (Approve / Reject)"
        )
        
        # Persist session state in SQLite
        create_or_update_session(
            session_id=session_id,
            document_type=doc_type,
            jurisdiction=jurisdiction,
            issuing_authority=issuing_authority,
            status_type=status_type,
            workflow_status="awaiting_approval",
            readiness_score=readiness_info["score"],
            fee_status=fee_info["status"],
            fee_amount=fee_info.get("amount"),
            fee_currency=fee_info.get("currency", "INR"),
            payload={
                "intake": intake_data,
                "guidance": guidance_result,
                "approval_id": approval_id,
                "recovery_twin": recovery_twin,
                "sandbox_draft": sandbox_draft
            }
        )
        
        return {
            "session_id": session_id,
            "workflow_status": "awaiting_approval",
            "approval_id": approval_id,
            "guidance": guidance_result,
            "recovery_twin": recovery_twin,
            "route_planning": route_planning,
            "risk_radar": risk_radar_result
        }

    def execute_user_approval_decision(self, approval_id: int, user_decision: str,
                                      notes: Optional[str] = None,
                                      simulate_failure: bool = False) -> Dict[str, Any]:
        """
        Executes Step 9 (EXECUTE PERMITTED ACTION) and Step 10 (VERIFY RESULT).
        Runs against the persistent Mock Government Portal with idempotency protection.
        """
        session_id = self.session_id
        session = get_session_by_id(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found.")
            
        payload = session.get("payload", {})
        guidance = payload.get("guidance", {})
        intake_data = payload.get("intake", {})
        sandbox_draft = payload.get("sandbox_draft", {})
        doc_type = session.get("document_type", "edu_cert")
        authority = session.get("issuing_authority", "Authority")
        
        if user_decision.lower() in ["reject", "rejected", "cancel", "cancelled"]:
            # User declined the action
            resolve_approval_request(
                approval_id=approval_id,
                user_decision="rejected",
                approval_status="rejected",
                execution_result="Citizen declined proposed action. Workflow paused safely with no external changes."
            )
            
            add_trace_event(
                session_id=session_id,
                step_number=9,
                step_name="STEP 9: EXECUTE PERMITTED ACTION",
                status="cancelled",
                input_summary="Citizen Decision: REJECT",
                decision="Execution aborted per citizen preference",
                reason="Citizen withheld approval; system strictly respects human boundary.",
                evidence_ref="Human-in-the-Loop Decision Log",
                action_taken="Cancelled proposed execution",
                outcome="Workflow stopped safely"
            )
            
            add_trace_event(
                session_id=session_id,
                step_number=10,
                step_name="STEP 10: VERIFY RESULT",
                status="complete",
                input_summary="Action: None (User Aborted)",
                decision="Workflow status marked as 'paused_by_user'",
                reason="Audit log updated to reflect user rejection.",
                evidence_ref="Session State Verification",
                action_taken="Persisted paused state",
                outcome="Clean stop verified"
            )
            
            update_session_workflow(session_id, workflow_status="paused_by_user")

            # Update twin state
            intake_data["approval_status"] = "rejected"
            twin = RecoveryTwinEngine.build_or_update_twin(case_id=session_id, case_data=intake_data)
            
            return {
                "session_id": session_id,
                "workflow_status": "paused_by_user",
                "approval_status": "rejected",
                "execution_result": "Action declined. You can adjust your information and re-run whenever you wish.",
                "recovery_twin": twin,
                "tracking": {
                    "status": "not_submitted",
                    "reference": None,
                    "tracking_note": "Application was rejected by citizen. Nothing has been submitted."
                }
            }
            
        # Citizen APPROVED the action:
        # STEP 9: EXECUTE PERMITTED ACTION against Safe Action Sandbox / Mock Portal
        sandbox_res = MockGovernmentPortalService.execute_mock_submission(
            draft_package=sandbox_draft,
            citizen_signature="Authenticated Citizen (Demo Session)",
            simulate_failure=simulate_failure
        )

        if sandbox_res["status"] == "error":
            # Handle failure honestly (no fake success!)
            failure_msg = sandbox_res["message"]
            resolve_approval_request(
                approval_id=approval_id,
                user_decision="approved",
                approval_status="failed",
                execution_result=failure_msg
            )
            add_trace_event(
                session_id=session_id,
                step_number=9,
                step_name="STEP 9: EXECUTE PERMITTED ACTION",
                status="failed",
                input_summary="Execution Target: Mock Government Portal",
                decision=f"Sandbox Execution Failed: {failure_msg}",
                reason="System detected mock portal validation error or simulated downtime.",
                evidence_ref="Mock Portal Backend Status Response",
                action_taken="Halted submission; recorded honest error report",
                outcome="Submission rejected by backend"
            )
            add_trace_event(
                session_id=session_id,
                step_number=10,
                step_name="STEP 10: VERIFY RESULT",
                status="failed",
                input_summary="Outcome: FAILURE",
                decision="Verified failure state: No synthetic reference issued",
                reason="Never display placeholder success messages for failed transactions.",
                evidence_ref="Independent State Verification Engine",
                action_taken="Marked workflow state as 'failed'",
                outcome="Failure verified honestly"
            )
            update_session_workflow(session_id, workflow_status="failed")
            return {
                "session_id": session_id,
                "workflow_status": "failed",
                "approval_status": "failed",
                "execution_result": failure_msg,
                "tracking": {
                    "status": "submission_failed",
                    "reference": None,
                    "label": "SUBMISSION FAILED",
                    "note": failure_msg
                }
            }

        # Submission Successful in Mock Portal
        simulated_ref = sandbox_res["application_ref"]
        receipt = sandbox_res["receipt"]

        primary_source = None
        if guidance.get("sources"):
            primary_source = guidance["sources"][0]
        portal_url = primary_source.get("official_url") if primary_source else "https://digilocker.gov.in"

        execution_text = (
            f"Successfully compiled recovery dossier for {authority}. "
            f"Simulated local draft confirmed under ID: '{simulated_ref}' ({SYNTHETIC_RECEIPT_WATERMARK}). "
            f"Prepared secure gateway redirect to official portal: {portal_url}."
        )
        
        resolve_approval_request(
            approval_id=approval_id,
            user_decision="approved",
            approval_status="approved",
            execution_result=execution_text
        )
        
        add_trace_event(
            session_id=session_id,
            step_number=9,
            step_name="STEP 9: EXECUTE PERMITTED ACTION",
            status="complete",
            input_summary="Citizen Decision: APPROVED",
            decision="Executed authorized action against Safe Action Sandbox with Idempotency Key",
            reason="Explicit citizen approval received with timestamped audit record.",
            evidence_ref=f"Approval Record #{approval_id}",
            action_taken=f"Ingested draft into Mock Portal; generated confirmed receipt '{simulated_ref}'",
            outcome="Simulated application confirmed"
        )
        
        # STEP 10: INDEPENDENT VERIFICATION & LEARN
        # Independently verify mock backend state
        independent_verification = MockGovernmentPortalService.independently_verify_mock_status(simulated_ref)

        add_trace_event(
            session_id=session_id,
            step_number=10,
            step_name="STEP 10: VERIFY RESULT",
            status="complete",
            input_summary=f"Queried Mock Gateway for ref '{simulated_ref}'",
            decision=f"Independently Verified: Status={independent_verification['submission_status']} in persistent database",
            reason="Anti-Hallucination & Provenance Rule: RECLAIM AI independently queries backend state and strictly labels demo receipts.",
            evidence_ref="Mock Portal Backend Audit Registry",
            action_taken="Updated application tracking state with verified synthetic receipt",
            outcome="Execution verified and state finalized"
        )
        
        update_session_workflow(session_id, workflow_status="completed")

        # Update recovery twin state to confirmed
        intake_data["approval_status"] = "approved"
        mock_submission_state = {
            "application_ref": simulated_ref,
            "submission_status": "CONFIRMED"
        }
        twin = RecoveryTwinEngine.build_or_update_twin(
            case_id=session_id,
            case_data=intake_data,
            mock_submission_state=mock_submission_state
        )
        
        return {
            "session_id": session_id,
            "workflow_status": "completed",
            "approval_status": "approved",
            "execution_result": execution_text,
            "execution_details": {
                "dossier_generated": True,
                "simulated_draft_id": simulated_ref,
                "target_portal": portal_url,
                "portal_authority": authority,
                "dossier_checklist": guidance.get("required_documents", []),
                "simulated_submission_disclaimer": SYNTHETIC_RECEIPT_WATERMARK,
                "idempotency_key": sandbox_draft.get("idempotency_key"),
                "is_duplicate_execution": sandbox_res.get("is_duplicate_execution", False)
            },
            "receipt": receipt,
            "independent_verification": independent_verification,
            "recovery_twin": twin,
            "tracking": {
                "status": "simulated_draft_ready",
                "reference": simulated_ref,
                "label": "SIMULATED DEMO REFERENCE - NOT SUBMITTED TO GOVERNMENT",
                "target_portal": portal_url,
                "official_authority": authority,
                "note": "This is a demonstration reference number generated locally in the Safe Action Sandbox. To complete actual statutory filing, proceed directly to the verified official government portal."
            }
        }
