"""
RECLAIM AI — Recovery Compass Tests
Tests for Adaptive Route Selection, Route Outage Handling, Missing Information adaptation,
Plan B fallback switching, and Statutory Fee Transparency.
"""
import pytest
from agent.adaptive_planner import AdaptiveRecoveryPlanner
from agent.readiness import calculate_readiness_score
from agent.fee_verifier import verify_document_fee
from agent.workflow import AgenticRecoveryWorkflow

def test_compass_primary_route_selection():
    """When roll number is present and authority is CBSE, Route 1 (DigiLocker) is recommended for immediate zero-cost pull."""
    case_data = {
        "document_type": "edu_cert",
        "jurisdiction": "Central",
        "issuing_authority": "Central Board of Secondary Education (CBSE)",
        "status_type": "lost",
        "has_police_report": False,
        "has_affidavit": False,
        "has_id_proof": True,
        "has_doc_number_or_copy": True,
        "primary_route_available": True
    }
    readiness = calculate_readiness_score(case_data)
    result = AdaptiveRecoveryPlanner.evaluate_and_compare_routes(case_data, readiness)

    assert result["recommended_route"] is not None
    assert result["recommended_route"]["route_id"] == "ROUTE_DIGITAL_DIGILOCKER"
    assert result["plan_b"] is not None
    assert result["plan_b"]["route_id"] == "ROUTE_OFFICIAL_ONLINE_PORTAL"

def test_compass_adaptive_plan_b_on_missing_roll_number():
    """When roll number is missing, DigiLocker cannot search MeitY cloud, so Compass automatically promotes Plan B (Board Portal)."""
    case_data = {
        "document_type": "edu_cert",
        "jurisdiction": "Central",
        "issuing_authority": "Central Board of Secondary Education (CBSE)",
        "status_type": "lost",
        "has_police_report": False,
        "has_affidavit": False,
        "has_id_proof": True,
        "has_doc_number_or_copy": False, # Missing roll number
        "primary_route_available": True
    }
    readiness = calculate_readiness_score(case_data)
    result = AdaptiveRecoveryPlanner.evaluate_and_compare_routes(case_data, readiness)

    assert result["recommended_route"] is not None
    assert result["recommended_route"]["route_id"] == "ROUTE_OFFICIAL_ONLINE_PORTAL"
    assert "Roll/Registration number is missing" in result["adaptive_switch_reason"]
    # Check that DigiLocker is marked with score 55 and deferral reason
    r1 = next(r for r in result["all_routes"] if r["route_id"] == "ROUTE_DIGITAL_DIGILOCKER")
    assert r1["feasibility_score"] == 55

def test_compass_adaptive_plan_b_on_route_outage():
    """When primary route experiences outage (simulate_route_outage=True), Compass promotes Plan B."""
    case_data = {
        "document_type": "edu_cert",
        "jurisdiction": "Central",
        "issuing_authority": "Central Board of Secondary Education (CBSE)",
        "status_type": "lost",
        "has_police_report": False,
        "has_affidavit": False,
        "has_id_proof": True,
        "has_doc_number_or_copy": True,
        "simulate_route_outage": True
    }
    readiness = calculate_readiness_score(case_data)
    result = AdaptiveRecoveryPlanner.evaluate_and_compare_routes(case_data, readiness)

    assert result["primary_route_available"] is False
    assert result["recommended_route"]["route_id"] == "ROUTE_OFFICIAL_ONLINE_PORTAL"
    assert "unavailable" in result["adaptive_switch_reason"].lower()

def test_compass_user_switch_to_plan_b():
    """When user explicitly chooses preferred_route='ROUTE_OFFICIAL_ONLINE_PORTAL', Compass respects citizen preference."""
    case_data = {
        "document_type": "edu_cert",
        "jurisdiction": "Central",
        "issuing_authority": "Central Board of Secondary Education (CBSE)",
        "status_type": "lost",
        "has_police_report": True,
        "has_affidavit": True,
        "has_id_proof": True,
        "has_doc_number_or_copy": True,
        "preferred_route": "ROUTE_OFFICIAL_ONLINE_PORTAL"
    }
    readiness = calculate_readiness_score(case_data)
    result = AdaptiveRecoveryPlanner.evaluate_and_compare_routes(case_data, readiness)

    assert result["recommended_route"]["route_id"] == "ROUTE_OFFICIAL_ONLINE_PORTAL"
    assert "Citizen switched route" in result["adaptive_switch_reason"]

def test_compass_unknown_authority_blocks_routes():
    """When issuing authority is unknown, Compass safely refuses to invent arbitrary routes."""
    case_data = {
        "document_type": "edu_cert",
        "jurisdiction": "Unknown",
        "issuing_authority": "Unknown Autonomous College",
        "status_type": "lost"
    }
    readiness = calculate_readiness_score(case_data)
    result = AdaptiveRecoveryPlanner.evaluate_and_compare_routes(case_data, readiness)

    assert result["is_blocked_by_missing_authority"] is True
    assert result["recommended_route"] is None
    assert "Decision engine paused" in result["decision_summary"]
