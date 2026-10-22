"""
Unit tests for Recovery Readiness Score Calculation
"""
from agent.readiness import calculate_readiness_score, READINESS_DISCLAIMER

def test_full_readiness_score():
    data = {
        "document_type": "edu_cert",
        "jurisdiction": "Central / All India",
        "issuing_authority": "CBSE",
        "status_type": "lost",
        "circumstances": "Relocation loss of senior secondary certificate.",
        "has_police_report": True,
        "has_affidavit": True,
        "has_id_proof": True,
        "has_doc_number_or_copy": True
    }
    result = calculate_readiness_score(data)
    assert result["score"] >= 95
    assert len(result["missing_items"]) == 0
    assert result["readiness_level"] == "Ready for Official Submission"
    assert READINESS_DISCLAIMER in result["explanation"]

def test_partial_readiness_score():
    data = {
        "document_type": "driving_licence",
        "jurisdiction": "Karnataka",
        "issuing_authority": "MoRTH",
        "status_type": "stolen",
        "circumstances": "Lost wallet",
        "has_police_report": False,
        "has_affidavit": False,
        "has_id_proof": True,
        "has_doc_number_or_copy": False
    }
    result = calculate_readiness_score(data)
    # Score should reflect missing police report and missing doc copy
    assert result["score"] < 60
    assert len(result["missing_items"]) >= 2
    assert any("Police Lost Document" in item for item in result["missing_items"])
    assert READINESS_DISCLAIMER in result["explanation"]

def test_zero_readiness_score():
    result = calculate_readiness_score({})
    assert result["score"] == 0
    assert len(result["missing_items"]) >= 4
