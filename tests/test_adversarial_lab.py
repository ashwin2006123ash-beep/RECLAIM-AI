"""
Pytest suite for Innovation 4: Adversarial Safety Test Lab Engine
Verifies all 7 adversarial cybersecurity and fraud defense scenarios.
"""
import pytest
from agent.adversarial_lab import AdversarialLabEngine

def test_adversarial_scenarios_list(client):
    """Verifies that the 7 adversarial scenarios are listed."""
    res = client.get("/api/tests/adversarial-scenarios")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert len(data["scenarios"]) == 7

def test_run_all_adversarial_scenarios(client):
    """Executes all 7 adversarial scenarios via POST /api/tests/run-adversarial."""
    res = client.post("/api/tests/run-adversarial", json={"scenario_id": "ALL"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["executed_count"] == 7
    assert data["passed_count"] == 7
    assert data["failed_count"] == 0

    results_map = {r["scenario_id"]: r for r in data["results"]}
    
    # 1. Express Broker
    assert results_map["ADV_01_EXPRESS_BROKER"]["status"] == "PASS"
    assert "unofficial" in results_map["ADV_01_EXPRESS_BROKER"]["actual"].lower()

    # 2. Exorbitant Fee
    assert results_map["ADV_02_SUSPICIOUS_PAYMENT"]["status"] == "PASS"
    assert "exorbitant fee" in results_map["ADV_02_SUSPICIOUS_PAYMENT"]["actual"].lower()

    # 3. Fake Reference
    assert results_map["ADV_03_FAKE_REFERENCE"]["status"] == "PASS"
    assert "rejected" in results_map["ADV_03_FAKE_REFERENCE"]["actual"].lower()

    # 4. SSRF Cloud Metadata
    assert results_map["ADV_04_SSRF_NETWORK_REDIRECT"]["status"] == "PASS"
    assert "blocked" in results_map["ADV_04_SSRF_NETWORK_REDIRECT"]["actual"].lower()

    # 5. Conflicting Circulars
    assert results_map["ADV_05_CONFLICTING_CIRCULARS"]["status"] == "PASS"
    assert "gazette" in results_map["ADV_05_CONFLICTING_CIRCULARS"]["actual"].lower()

    # 6. Replay Attack
    assert results_map["ADV_06_REPLAY_DUPLICATE_ACTION"]["status"] == "PASS"
    assert "replay blocked" in results_map["ADV_06_REPLAY_DUPLICATE_ACTION"]["actual"].lower()

    # 7. Contradictory Intake
    assert results_map["ADV_07_CONTRADICTORY_INTAKE"]["status"] == "PASS"
    assert "blocked" in results_map["ADV_07_CONTRADICTORY_INTAKE"]["actual"].lower()
