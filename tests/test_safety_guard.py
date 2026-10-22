"""
Unit tests for Source Safety Guard & SSRF Protection
"""
from agent.safety_guard import evaluate_source_safety, sanitize_and_validate_url

def test_block_localhost_ssrf():
    for target in ["http://localhost:8080", "https://127.0.0.1/admin", "http://0.0.0.0"]:
        eval_res = evaluate_source_safety(target)
        assert eval_res["is_official"] is False
        assert eval_res["is_safe"] is False
        assert eval_res["verification_status"] == "blocked"
        assert eval_res["threat_level"] == "CRITICAL"
        assert "Security Violation" in eval_res["reason"]

def test_block_cloud_metadata_endpoints():
    target = "http://169.254.169.254/latest/meta-data/"
    eval_res = evaluate_source_safety(target)
    assert eval_res["is_safe"] is False
    assert eval_res["verification_status"] == "blocked"
    assert eval_res["threat_level"] == "CRITICAL"

def test_block_private_ips():
    for ip in ["http://192.168.1.10", "http://10.0.0.5"]:
        eval_res = evaluate_source_safety(ip)
        assert eval_res["is_safe"] is False
        assert eval_res["verification_status"] == "blocked"

def test_flag_unofficial_agent_broker():
    unofficial_url = "https://quick-pan-agent.com/instant-pan-reissue"
    eval_res = evaluate_source_safety(unofficial_url)
    assert eval_res["is_official"] is False
    assert eval_res["verification_status"] == "unofficial_rejected"
    assert eval_res["threat_level"] == "HIGH_RISK"
    assert eval_res["action"] == "EXCLUDE_FROM_AUTHORITATIVE_GUIDANCE"
    assert "unofficial third-party agent/broker" in eval_res["reason"]

def test_verify_official_domains():
    for official_url in ["https://cbse.gov.in/cbsenew/pariksha_sangam.html",
                          "https://sarathi.parivahan.gov.in",
                          "https://voters.eci.gov.in",
                          "https://myaadhaar.uidai.gov.in"]:
        eval_res = evaluate_source_safety(official_url)
        assert eval_res["is_official"] is True
        assert eval_res["is_safe"] is True
        assert eval_res["verification_status"] == "official_verified"
        assert eval_res["threat_level"] == "NONE"
