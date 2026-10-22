"""
Pytest suite for Innovation 2: Counterfactual Recovery Simulator
Verifies side-by-side what-if scenario modeling and statutory delta calculations.
"""
import pytest
from agent.counterfactual import CounterfactualSimulator

def test_counterfactual_scenarios_list(client):
    """Verifies that supported scenarios list endpoint returns 200 with 5 scenarios."""
    res = client.get("/api/recovery/counterfactual-scenarios")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert len(data["scenarios"]) == 5

def test_counterfactual_lost_vs_stolen(client):
    """Verifies that stolen document status mandates FIR and reduces readiness if FIR is missing."""
    base_case = {
        "document_type": "driving_licence",
        "issuing_authority": "MoRTH",
        "jurisdiction": "Karnataka",
        "status_type": "lost",
        "has_police_report": True,
        "has_affidavit": False,
        "has_id_proof": True,
        "has_doc_number_or_copy": True
    }
    res = client.post("/api/recovery/counterfactual-simulate", json={
        "case_data": base_case,
        "scenario_id": "scenario_lost_vs_stolen"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["baseline"]["data"]["status_type"] == "lost"
    assert data["modeled"]["data"]["status_type"] == "stolen"
    # Stolen with missing FIR should have lower readiness and more blocked nodes
    assert data["modeled"]["readiness_score"] < data["baseline"]["readiness_score"]
    assert "SIMULATION" in data["statutory_disclaimer"]

def test_counterfactual_copy_available_vs_missing(client):
    """Verifies that missing document copy blocks DigiLocker instant retrieval."""
    base_case = {
        "document_type": "edu_cert",
        "issuing_authority": "CBSE",
        "jurisdiction": "Central / All India",
        "status_type": "lost",
        "has_police_report": True,
        "has_affidavit": True,
        "has_id_proof": True,
        "has_doc_number_or_copy": True
    }
    res = client.post("/api/recovery/counterfactual-simulate", json={
        "case_data": base_case,
        "scenario_id": "scenario_copy_available_vs_missing"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["baseline"]["digilocker_viable"] is True
    assert data["modeled"]["digilocker_viable"] is False
    assert data["comparative_deltas"]["readiness_score_delta"] < 0

def test_counterfactual_authority_known_vs_unknown(client):
    """Verifies that unknown authority halts at Node 1 and flags unverified fee."""
    base_case = {
        "document_type": "edu_cert",
        "issuing_authority": "CBSE",
        "jurisdiction": "Central",
        "status_type": "lost",
        "has_police_report": True,
        "has_affidavit": True,
        "has_id_proof": True,
        "has_doc_number_or_copy": True
    }
    res = client.post("/api/recovery/counterfactual-simulate", json={
        "case_data": base_case,
        "scenario_id": "scenario_authority_known_vs_unknown"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["baseline"]["fee_status"] == "verified"
    assert data["modeled"]["fee_status"] == "not_verified"
    assert "IDENTIFY_AUTHORITY" in data["modeled"]["blocked_nodes"]
