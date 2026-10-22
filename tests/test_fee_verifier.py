"""
Unit tests for Fee Verification & Transparency
"""
from agent.fee_verifier import verify_document_fee

def test_verified_driving_licence_fee():
    fee = verify_document_fee("driving_licence", "Ministry of Road Transport and Highways (MoRTH)")
    assert fee["status"] == "verified"
    assert fee["amount"] == 400.0
    assert fee["currency"] == "INR"
    assert fee["is_official"] is True
    assert "CMVR" in fee["condition"] or "Rule 81" in fee["condition"]

def test_verified_voter_id_fee_is_zero():
    fee = verify_document_fee("voter_id", "Election Commission of India")
    assert fee["status"] == "verified"
    assert fee["amount"] == 0.0
    assert "Free of cost" in fee["condition"]

def test_unverified_fee_for_unknown_authority():
    fee = verify_document_fee("edu_cert", "Unknown Autonomous College")
    assert fee["status"] == "not_verified"
    assert fee["amount"] is None
    assert fee["is_official"] is False
    assert "Fee not verified" in fee["message"]
