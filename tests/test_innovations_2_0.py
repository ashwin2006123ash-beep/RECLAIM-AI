"""
Automated Pytest Suite for RECLAIM AI 2.0 Innovations:
- Innovation 1: Recovery Twin & Dependency Graph
- Innovation 2: Proof-of-Truth Research Agent & Conflict Resolution
- Innovation 3: Adaptive Multi-Route Planner
- Innovation 4: Recovery Risk Radar
- Innovation 5: Safe Action Sandbox & Mock Government Portal
"""
import pytest
from agent.recovery_twin import RecoveryTwinEngine
from agent.research_agent import ResearchAgent
from agent.adaptive_planner import AdaptiveRecoveryPlanner
from agent.risk_radar import RecoveryRiskRadar
from agent.mock_portal import MockGovernmentPortalService, SYNTHETIC_RECEIPT_WATERMARK
from database.models import get_recovery_twin

def test_recovery_twin_dynamic_recalculation(app):
    with app.app_context():
        case_id = "TWIN-TEST-001"
        # Case 1: Incomplete evidence (missing police report and affidavit)
        case_data_initial = {
            "document_type": "driving_licence",
            "jurisdiction": "Karnataka",
            "issuing_authority": "MoRTH",
            "status_type": "stolen",
            "has_police_report": False,
            "has_affidavit": False,
            "has_id_proof": True,
            "has_doc_number_or_copy": False
        }
        twin_1 = RecoveryTwinEngine.build_or_update_twin(case_id, case_data_initial)
        nodes_1 = twin_1["dependency_graph"]["nodes"]
        
        # In stolen DL without police report, GATHER_EVIDENCE should be IN_PROGRESS / BLOCKED
        assert nodes_1["GATHER_EVIDENCE"]["state"] in ["IN_PROGRESS", "BLOCKED"]
        assert "Police" in nodes_1["GATHER_EVIDENCE"]["blocked_reason"]
        assert nodes_1["PREPARE_APPLICATION"]["state"] == "BLOCKED"
        
        # Case 2: Citizen obtains Police Report and adds it
        case_data_updated = dict(case_data_initial)
        case_data_updated["has_police_report"] = True
        case_data_updated["has_doc_number_or_copy"] = True
        
        twin_2 = RecoveryTwinEngine.build_or_update_twin(case_id, case_data_updated)
        nodes_2 = twin_2["dependency_graph"]["nodes"]
        
        # Now GATHER_EVIDENCE and PREPARE_APPLICATION should be COMPLETED
        assert nodes_2["GATHER_EVIDENCE"]["state"] == "COMPLETED"
        assert nodes_2["PREPARE_APPLICATION"]["state"] == "COMPLETED"
        assert nodes_2["OBTAIN_APPROVAL"]["state"] == "READY"
        assert twin_2["readiness_score"] > twin_1["readiness_score"]

def test_missing_authority_blocks_graph_and_routes(app):
    with app.app_context():
        case_id = "TWIN-UNKNOWN-AUTH"
        case_data = {
            "document_type": "edu_cert",
            "jurisdiction": "",
            "issuing_authority": "Unknown Autonomous College",
            "status_type": "lost",
            "has_police_report": True,
            "has_affidavit": True,
            "has_id_proof": True,
            "has_doc_number_or_copy": True
        }
        twin = RecoveryTwinEngine.build_or_update_twin(case_id, case_data)
        nodes = twin["dependency_graph"]["nodes"]
        assert nodes["IDENTIFY_AUTHORITY"]["state"] in ["BLOCKED", "NEEDS_VERIFICATION"]
        assert nodes["VERIFY_PROCESS"]["state"] == "BLOCKED"
        
        # Route planner should pause recommendation
        route_plan = AdaptiveRecoveryPlanner.evaluate_and_compare_routes(case_data, twin["readiness_breakdown"])
        assert route_plan["is_blocked_by_missing_authority"] is True
        assert route_plan["recommended_route"] is None
        assert "authority is unknown" in route_plan["decision_summary"].lower()

def test_proof_of_truth_claims_and_conflicts(app):
    with app.app_context():
        case_id = "RESEARCH-TEST-001"
        intel = ResearchAgent.investigate_case_evidence(
            case_id=case_id,
            document_type="driving_licence",
            jurisdiction="Karnataka",
            issuing_authority="MoRTH"
        )
        assert intel["claims_count"] > 0
        claims = intel["claims"]
        assert any(c["source_tag"] == "LIVE_VERIFIED" for c in claims)
        
        # Conflict detection between legacy circular and CMVR Rule 81
        assert intel["conflicts_count"] > 0
        conflict = intel["conflicts"][0]
        assert "CMVR" in conflict["stronger_source"] or "Central Motor Vehicles Rules" in conflict["stronger_source"]
        assert conflict["is_resolved"] is True

def test_adaptive_multi_route_comparison(app):
    with app.app_context():
        case_data = {
            "document_type": "driving_licence",
            "jurisdiction": "Karnataka",
            "issuing_authority": "MoRTH",
            "status_type": "lost",
            "has_police_report": True,
            "has_affidavit": True,
            "has_id_proof": True,
            "has_doc_number_or_copy": True
        }
        twin = RecoveryTwinEngine.build_or_update_twin("ROUTE-TEST-001", case_data)
        route_plan = AdaptiveRecoveryPlanner.evaluate_and_compare_routes(case_data, twin["readiness_breakdown"])
        
        assert len(route_plan["all_routes"]) == 3
        route_ids = [r["route_id"] for r in route_plan["all_routes"]]
        assert "ROUTE_DIGITAL_DIGILOCKER" in route_ids
        assert "ROUTE_OFFICIAL_ONLINE_PORTAL" in route_ids
        assert "ROUTE_IN_PERSON_COUNTER" in route_ids
        
        rec = route_plan["recommended_route"]
        assert rec is not None
        assert "ROUTE_OFFICIAL_ONLINE_PORTAL" == rec["route_id"]
        assert len(route_plan["why_chosen_matrix"]) >= 2

def test_recovery_risk_radar_detection(app):
    with app.app_context():
        # Test 1: Stolen document without police report
        case_data = {
            "document_type": "driving_licence",
            "status_type": "stolen",
            "has_police_report": False,
            "fee_amount": 5000.0 # Exorbitant fee anomaly
        }
        radar = RecoveryRiskRadar.analyze_case_risks(
            case_data=case_data,
            candidate_url="https://quick-pan-agent.com/express-pan"
        )
        assert radar["overall_risk_level"] in ["HIGH_RISK", "CRITICAL"]
        categories = [w["category"] for w in radar["warnings"]]
        assert "UNAPPROVED_OR_SUSPICIOUS_DOMAIN" in categories
        assert "MISSING_REQUIRED_EVIDENCE" in categories
        assert "UNVERIFIED_FEE_REQUEST" in categories
        
        # Test safe url scanner
        scan = RecoveryRiskRadar.scan_url_safely("https://parivahan.gov.in")
        assert scan["is_official_government"] is True
        assert scan["risk_level"] == "SAFE_OFFICIAL"

def test_mock_portal_idempotency_and_verification(app):
    with app.app_context():
        draft = {
            "case_id": "MOCK-CASE-99",
            "idempotency_key": "IDEMP-TEST-KEY-12345",
            "is_valid": True,
            "document_type": "driving_licence",
            "issuing_authority": "MoRTH",
            "prepared_at": "2026-10-22T08:00:00Z"
        }
        # First submission
        res1 = MockGovernmentPortalService.execute_mock_submission(draft)
        assert res1["status"] == "success"
        assert res1["is_duplicate_execution"] is False
        app_ref = res1["application_ref"]
        assert app_ref.startswith("SIM-")
        assert SYNTHETIC_RECEIPT_WATERMARK in res1["receipt"]["synthetic_disclaimer"]
        
        # Second submission with same idempotency key (must detect duplicate!)
        res2 = MockGovernmentPortalService.execute_mock_submission(draft)
        assert res2["status"] == "success"
        assert res2["is_duplicate_execution"] is True
        assert res2["application_ref"] == app_ref
        
        # Independent status query from database
        verify_res = MockGovernmentPortalService.independently_verify_mock_status(app_ref)
        assert verify_res["verified"] is True
        assert verify_res["submission_status"] == "CONFIRMED"
        assert verify_res["is_synthetic_demo"] is True

def test_mock_portal_simulated_failure(app):
    with app.app_context():
        draft = {
            "case_id": "MOCK-FAIL-01",
            "idempotency_key": "IDEMP-FAIL-TEST",
            "is_valid": True,
            "document_type": "edu_cert",
            "issuing_authority": "CBSE"
        }
        res = MockGovernmentPortalService.execute_mock_submission(draft, simulate_failure=True)
        assert res["status"] == "error"
        assert res["submission_status"] == "FAILED"
        assert "Simulated Gateway Failure" in res["message"]
