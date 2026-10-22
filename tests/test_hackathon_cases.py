"""
Automated Pytest Suite for the 4 Official Hackathon Scenarios:
TC1 — Lost Certificate
TC2 — Unofficial Agent Website
TC3 — Reissue Fee
TC4 — Request Number Received
"""
import json

def test_api_run_all_hackathon_test_cases(client):
    """Executes the full test suite via POST /api/tests/run."""
    response = client.post("/api/tests/run", json={"scenario_id": "ALL"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["executed_count"] == 4
    
    results_map = {r["scenario_id"]: r for r in data["results"]}
    
    # 1. Verify TC1 (Lost Certificate)
    tc1 = results_map["TC1"]
    assert tc1["status"] == "PASS", f"TC1 failed: {tc1.get('actual')}"
    assert "cbse.gov.in" in tc1["actual"]
    assert "250" in tc1["actual"]
    
    # 2. Verify TC2 (Unofficial Agent Website)
    tc2 = results_map["TC2"]
    assert tc2["status"] == "PASS", f"TC2 failed: {tc2.get('actual')}"
    assert "quick-pan-agent.com" in tc2["actual"]
    assert "HIGH_RISK" in tc2["actual"]
    
    # 3. Verify TC3 (Reissue Fee)
    tc3 = results_map["TC3"]
    assert tc3["status"] == "PASS", f"TC3 failed: {tc3.get('actual')}"
    assert "400.00" in tc3["actual"]
    assert "CMVR" in tc3["actual"]
    
    # 4. Verify TC4 (Request Number Received & Tracking Honesty)
    tc4 = results_map["TC4"]
    assert tc4["status"] == "PASS", f"TC4 failed: {tc4.get('actual')}"
    assert "not_submitted" in tc4["actual"]
    assert "SIMULATED" in tc4["actual"]

def test_tc1_individual(client):
    response = client.post("/api/tests/run", json={"scenario_id": "TC1"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["results"][0]["status"] == "PASS"

def test_tc2_individual(client):
    response = client.post("/api/tests/run", json={"scenario_id": "TC2"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["results"][0]["status"] == "PASS"

def test_tc3_individual(client):
    response = client.post("/api/tests/run", json={"scenario_id": "TC3"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["results"][0]["status"] == "PASS"

def test_tc4_individual(client):
    response = client.post("/api/tests/run", json={"scenario_id": "TC4"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["results"][0]["status"] == "PASS"
