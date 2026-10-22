"""
Pytest suite for Innovation 5: Accessible Civic Copilot
Verifies bilingual conversational processing (English & Tamil), terminology explanations, and grounding.
"""
import pytest
from agent.copilot import AccessibleCivicCopilot

def test_copilot_english_guidance(client):
    """Verifies that English queries return structured civic guidance."""
    res = client.post("/api/copilot/chat", json={
        "message": "What is the first step to recover my lost Class 12 marksheet?",
        "case_data": {
            "document_type": "edu_cert",
            "issuing_authority": "CBSE",
            "status_type": "lost"
        }
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["language"] == "en"
    assert "Police" in data["reply"] or "DigiLocker" in data["reply"]
    assert len(data["suggested_questions"]) >= 2

def test_copilot_tamil_support(client):
    """Verifies that Tamil queries are accurately detected and answered in Tamil."""
    res = client.post("/api/copilot/chat", json={
        "message": "என் ஓட்டுநர் உரிமம் தொலைந்துவிட்டது, நான் என்ன செய்ய வேண்டும்?",
        "case_data": {
            "document_type": "driving_licence",
            "issuing_authority": "MoRTH",
            "status_type": "lost"
        }
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert data["language"] == "ta"
    assert "காவல்" in data["reply"] or "போர்டல்" in data["reply"] or "படி" in data["reply"]

def test_copilot_glossary_explanation(client):
    """Verifies that legal jargon like 'Affidavit' is detected and simplified."""
    res = client.post("/api/copilot/chat", json={
        "message": "Do I really need an affidavit for duplicate certificate?",
        "case_data": {
            "document_type": "edu_cert",
            "issuing_authority": "CBSE"
        }
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert len(data["explained_terms"]) >= 1
    term = data["explained_terms"][0]
    assert "Affidavit" in term["term"]
    assert "Notary" in term["explanation"] or "வாக்குமூலம்" in term["explanation"]
