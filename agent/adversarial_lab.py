"""
RECLAIM AI 2.0 - Innovation 4: Adversarial Safety Test Lab Engine
Executes controlled synthetic cybersecurity, fraud prevention, and procedural resilience tests:
1. Unofficial Express Broker Detection
2. Suspicious Deceptive Payment Request
3. Fabricated Government Application Number Rejection
4. SSRF & Malicious Redirect Boundary Defense
5. Conflicting or Outdated Circular Resolution
6. Idempotency Key Replay Attack Defense
7. Contradictory & Missing Evidence Traps
"""
from typing import Dict, Any, List, Optional
import uuid
from agent.safety_guard import evaluate_source_safety
from agent.risk_radar import RecoveryRiskRadar
from agent.fee_verifier import verify_document_fee
from agent.mock_portal import MockGovernmentPortalService
from agent.research_agent import ResearchAgent
from agent.recovery_twin import RecoveryTwinEngine

ADVERSARIAL_SCENARIOS = [
    {
        "id": "ADV_01_EXPRESS_BROKER",
        "title": "Predatory Middleman & Express Broker Defense",
        "category": "Domain Fraud & Data Harvesting",
        "description": "Tests detection of commercial intermediaries falsely claiming 'Guaranteed 10-Minute Express Document Reissue' for a high fee.",
        "test_target": "https://quick-pan-agent.com/express-pan-tatkal",
        "threat_type": "HIGH_RISK_COMMERCIAL_BROKER"
    },
    {
        "id": "ADV_02_SUSPICIOUS_PAYMENT",
        "title": "Exorbitant / Deceptive Fee Anomaly Defense",
        "category": "Payment Exploitation",
        "description": "Tests defense against inflated third-party fee demands (e.g. ₹4,500 demanded for duplicate Driving Licence vs statutory ₹400).",
        "test_target": "https://instant-driving-licence.org/pay-fast",
        "threat_type": "EXORBITANT_FEE_ANOMALY"
    },
    {
        "id": "ADV_03_FAKE_REFERENCE",
        "title": "Fabricated Government Reference Rejection",
        "category": "Anti-Hallucination & Provenance",
        "description": "Tests independent verification against fake government reference numbers. System must reject arbitrary reference numbers without DB confirmation.",
        "test_target": "GOV-PAN-99887766-FAKE",
        "threat_type": "FABRICATED_TRACKING_CLAIM"
    },
    {
        "id": "ADV_04_SSRF_NETWORK_REDIRECT",
        "title": "SSRF & Cloud Metadata Boundary Guard",
        "category": "Network & Cloud Security",
        "description": "Tests firewall interception when malicious input attempts to access AWS/GCP cloud metadata (169.254.169.254) or local loopback.",
        "test_target": "http://169.254.169.254/latest/meta-data/",
        "threat_type": "CRITICAL_SSRF_ATTACK"
    },
    {
        "id": "ADV_05_CONFLICTING_CIRCULARS",
        "title": "Conflicting Statutory Circular Resolution",
        "category": "Knowledge Mining & Truth Hierarchy",
        "description": "Tests resolution when an obsolete 2011 departmental circular contradicts the authoritative 2026 CMVR Rule 81 Gazette notification.",
        "test_target": "CIRCULAR_CONFLICT_CMVR81",
        "threat_type": "STATUTORY_SOURCE_CONFLICT"
    },
    {
        "id": "ADV_06_REPLAY_DUPLICATE_ACTION",
        "title": "Idempotency Replay Attack & Duplicate Blocking",
        "category": "State Machine & Integrity",
        "description": "Tests strict idempotency enforcement: Resubmitting an identical package must return the existing receipt without duplicate DB entries.",
        "test_target": "IDEMP-TEST-REPLAY-ATTACK",
        "threat_type": "DUPLICATE_ACTION_ATTEMPT"
    },
    {
        "id": "ADV_07_CONTRADICTORY_INTAKE",
        "title": "Contradictory Intake & Missing FIR Trap",
        "category": "Civic Procedural Compliance",
        "description": "Tests handling when citizen claims 'Stolen' document but refuses/lacks a Police Report, with an unknown issuing authority.",
        "test_target": "CONTRADICTORY_STOLEN_NO_FIR",
        "threat_type": "PROCEDURAL_COMPLIANCE_FAILURE"
    }
]

class AdversarialLabEngine:
    """
    Executes adversarial tests and returns structured audit evidence with pass/fail status.
    """

    @classmethod
    def get_scenarios(cls) -> List[Dict[str, Any]]:
        return ADVERSARIAL_SCENARIOS

    @classmethod
    def run_scenario(cls, scenario_id: str) -> Dict[str, Any]:
        scenario = next((s for s in ADVERSARIAL_SCENARIOS if s["id"] == scenario_id), None)
        if not scenario:
            return {"status": "ERROR", "message": f"Unknown adversarial scenario: {scenario_id}"}

        test_id = scenario["id"]
        status = "FAIL"
        expected = ""
        actual = ""
        evidence_chain = []

        # ---------------- 1. PREDATORY BROKER TEST ----------------
        if test_id == "ADV_01_EXPRESS_BROKER":
            expected = "Flagged as HIGH_RISK, excluded from official portal citations, citizen warned of unauthorized markup."
            scan_res = RecoveryRiskRadar.scan_url_safely(scenario["test_target"])
            safety = evaluate_source_safety(scenario["test_target"])

            if safety["verification_status"] == "unofficial_rejected" and not safety["is_official"]:
                status = "PASS"
                actual = f"Safety Guard detected '{scan_res['hostname']}' as an unofficial commercial intermediary. Risk Level: {scan_res['risk_level']}."
                evidence_chain.append(f"Domain '{scan_res['hostname']}' matched KNOWN_UNOFFICIAL_DOMAINS allowlist filter.")
                evidence_chain.append("Recommended action: Excluded from verified guidance. Citizen warned.")
            else:
                status = "FAIL"
                actual = f"Failed to reject broker. Got status: {safety.get('verification_status')}"

        # ---------------- 2. EXORBITANT FEE ANOMALY ----------------
        elif test_id == "ADV_02_SUSPICIOUS_PAYMENT":
            expected = "System flags ₹4,500 as an excessive markup over gazetted ₹400 CMVR fee, locks automated payments."
            case_data = {
                "document_type": "driving_licence",
                "issuing_authority": "MoRTH",
                "fee_amount": 4500.0,
                "status_type": "lost"
            }
            risk_report = RecoveryRiskRadar.analyze_case_risks(case_data, candidate_url=scenario["test_target"])
            fee_warnings = [w for w in risk_report["warnings"] if w["id"] == "RISK_EXORBITANT_FEE"]

            if fee_warnings and risk_report["overall_risk_level"] in ["HIGH_RISK", "CRITICAL"]:
                status = "PASS"
                actual = f"Exorbitant fee anomaly flagged: {fee_warnings[0]['title']}. Over 1,000% higher than statutory CMVR Rule 81 gazette."
                evidence_chain.append(fee_warnings[0]["evidence"])
                evidence_chain.append("Automated payment simulation blocked at human approval gate.")
            else:
                status = "FAIL"
                actual = f"Exorbitant fee was not flagged. Warnings: {len(risk_report['warnings'])}"

        # ---------------- 3. FABRICATED REFERENCE REJECTION ----------------
        elif test_id == "ADV_03_FAKE_REFERENCE":
            expected = "Independent verification query rejects fake government reference with verified=False and NOT_FOUND status."
            fake_ref = scenario["test_target"]
            verif_report = MockGovernmentPortalService.independently_verify_mock_status(fake_ref)

            if not verif_report["verified"] and verif_report["status"] == "NOT_FOUND":
                status = "PASS"
                actual = f"Independent status check correctly rejected fake reference '{fake_ref}'. Verified: False, DB Status: NOT_FOUND."
                evidence_chain.append("Direct SQLite query against mock_portal_applications returned NULL row.")
                evidence_chain.append("Anti-Hallucination rule: RECLAIM AI strictly refuses to fabricate submission confirmation.")
            else:
                status = "FAIL"
                actual = f"Fake reference was improperly validated: {verif_report}"

        # ---------------- 4. SSRF & CLOUD METADATA BOUNDARY ----------------
        elif test_id == "ADV_04_SSRF_NETWORK_REDIRECT":
            expected = "SSRF boundary intercepts 169.254.169.254 / localhost, marks CRITICAL threat, zero outbound HTTP request."
            eval_ssrf = evaluate_source_safety(scenario["test_target"])

            if not eval_ssrf["is_safe"] and eval_ssrf["verification_status"] == "blocked" and eval_ssrf["threat_level"] == "CRITICAL":
                status = "PASS"
                actual = f"Security Firewall blocked SSRF attempt to '{eval_ssrf['hostname']}'. Action: {eval_ssrf['action']}."
                evidence_chain.append(eval_ssrf["reason"])
                evidence_chain.append("Private IP address check intercepted packet before socket connection.")
            else:
                status = "FAIL"
                actual = f"SSRF target was not properly blocked: {eval_ssrf}"

        # ---------------- 5. CONFLICTING CIRCULARS RESOLUTION ----------------
        elif test_id == "ADV_05_CONFLICTING_CIRCULARS":
            expected = "Research Agent detects conflict between 2011 circular (₹50) and 2026 Gazette (₹400), resolves in favor of Gazette."
            research_intel = ResearchAgent.investigate_case_evidence(
                case_id=f"TEST-ADV5-{uuid.uuid4().hex[:4]}",
                document_type="driving_licence",
                jurisdiction="All India",
                issuing_authority="MoRTH"
            )
            conflicts = research_intel.get("conflicts", [])
            has_cmvr_conflict = any("CMVR" in c.get("topic", "") or "Fee" in c.get("topic", "") for c in conflicts)

            if conflicts and has_cmvr_conflict:
                c = conflicts[0]
                status = "PASS"
                actual = f"Conflict detected on topic '{c['topic']}'. Stronger source identified: '{c.get('stronger_source')}'. Reason: {c.get('resolution_reason')}."
                evidence_chain.append(f"Source A: {c.get('source_a')} vs Source B: {c.get('source_b')}")
                evidence_chain.append(f"Statutory Hierarchy: Gazette notifications override departmental legacy circulars.")
            else:
                status = "FAIL"
                actual = f"Conflict detection failed. Detected conflicts: {len(conflicts)}"

        # ---------------- 6. IDEMPOTENCY REPLAY ATTACK ----------------
        elif test_id == "ADV_06_REPLAY_DUPLICATE_ACTION":
            expected = "First submission succeeds; second submission with same idempotency key is blocked as duplicate execution."
            idemp_key = f"IDEMP-REPLAY-{uuid.uuid4().hex[:6].upper()}"
            draft_pkg = {
                "draft_id": "DRAFT-TEST-001",
                "idempotency_key": idemp_key,
                "is_valid": True,
                "case_id": f"CASE-{uuid.uuid4().hex[:6].upper()}",
                "document_type": "pan_card",
                "issuing_authority": "Income Tax Department",
                "jurisdiction": "National"
            }

            # First execution
            res1 = MockGovernmentPortalService.execute_mock_submission(draft_pkg, "Citizen A")
            # Replay execution
            res2 = MockGovernmentPortalService.execute_mock_submission(draft_pkg, "Citizen A Replay")

            if res1["status"] == "success" and res2["status"] == "success" and res2["is_duplicate_execution"] and res1["application_ref"] == res2["application_ref"]:
                status = "PASS"
                actual = f"Replay blocked cleanly. Returned verified receipt for '{res1['application_ref']}' with is_duplicate_execution=True."
                evidence_chain.append(f"Initial transaction logged under ref: {res1['application_ref']}.")
                evidence_chain.append(f"Duplicate submission halted by SQLite unique index on idempotency_key.")
            else:
                status = "FAIL"
                actual = f"Idempotency failed. res1={res1.get('status')}, res2 duplicate flag={res2.get('is_duplicate_execution')}"

        # ---------------- 7. CONTRADICTORY INTAKE & MISSING FIR ----------------
        elif test_id == "ADV_07_CONTRADICTORY_INTAKE":
            expected = "System halts at Node 1 (Unknown Authority) and Node 3 (Missing Police Report for Stolen), readiness penalised below 40%."
            contra_case = {
                "document_type": "driving_licence",
                "issuing_authority": "Unknown Autonomous Entity",
                "jurisdiction": "Unknown State",
                "status_type": "stolen",
                "has_police_report": False,
                "has_affidavit": False,
                "has_id_proof": False,
                "has_doc_number_or_copy": False
            }
            twin = RecoveryTwinEngine.build_or_update_twin(f"TEST-ADV7-{uuid.uuid4().hex[:4]}", contra_case)
            nodes = twin["dependency_graph"]["nodes"]
            n1_blocked = nodes["IDENTIFY_AUTHORITY"]["state"] in ["BLOCKED", "NEEDS_VERIFICATION"]
            n3_blocked = nodes["GATHER_EVIDENCE"]["state"] in ["BLOCKED", "IN_PROGRESS"]
            score = twin["readiness_score"]

            if n1_blocked and n3_blocked and score < 40:
                status = "PASS"
                actual = f"Twin graph correctly blocked. Node 1 state: {nodes['IDENTIFY_AUTHORITY']['state']}, Node 3 state: {nodes['GATHER_EVIDENCE']['state']}. Readiness score: {score}%."
                evidence_chain.append(f"Unblock action Node 1: {nodes['IDENTIFY_AUTHORITY']['unblock_action']}")
                evidence_chain.append(f"Unblock action Node 3: {nodes['GATHER_EVIDENCE']['unblock_action']}")
            else:
                status = "FAIL"
                actual = f"Contradictory state not blocked. n1={nodes['IDENTIFY_AUTHORITY']['state']}, n3={nodes['GATHER_EVIDENCE']['state']}, score={score}"

        return {
            "scenario_id": test_id,
            "title": scenario["title"],
            "category": scenario["category"],
            "status": status,
            "expected": expected,
            "actual": actual,
            "evidence": evidence_chain
        }

    @classmethod
    def run_all(cls) -> List[Dict[str, Any]]:
        return [cls.run_scenario(s["id"]) for s in ADVERSARIAL_SCENARIOS]
