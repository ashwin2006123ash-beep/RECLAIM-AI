"""
Unit tests for Health Check & Core Metadata endpoints
"""
import json

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "RECLAIM AI" in data["service"]
    assert "Lost a document? Reclaim your next step." in data["tagline"]
    assert data["ai_engine_status"] in ["LIVE_GEMINI_AI", "DETERMINISTIC_FALLBACK_AI"]

def test_document_types(client):
    response = client.get("/api/document-types")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    categories = data["categories"]
    assert len(categories) >= 6
    cat_ids = [c["id"] for c in categories]
    assert "edu_cert" in cat_ids
    assert "driving_licence" in cat_ids
    assert "pan_card" in cat_ids
    assert "aadhaar" in cat_ids
    assert "voter_id" in cat_ids
    assert "passport" in cat_ids

def test_sources_endpoint(client):
    response = client.get("/api/sources")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] > 0
    sources = data["sources"]
    cbse = next((s for s in sources if s["source_id"] == "SRC_CBSE_PARIKSHA"), None)
    assert cbse is not None
    assert "cbse.gov.in" in cbse["official_hostname"]
