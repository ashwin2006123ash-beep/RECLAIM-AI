"""
Regression test suite for /api/risk-radar/scan-url
Verifies that POST, GET, and OPTIONS requests return HTTP 200 with structured JSON and NEVER 405 Method Not Allowed.
"""
import pytest
import json

def test_risk_radar_post_json(client):
    """Verifies that POST with JSON payload returns 200 and structured report."""
    response = client.post("/api/risk-radar/scan-url", json={"url": "https://parivahan.gov.in"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    report = data["scan_report"]
    assert report["is_official_government"] is True
    assert report["risk_level"] == "SAFE_OFFICIAL"
    assert "parivahan.gov.in" in report["hostname"]

def test_risk_radar_post_unofficial_broker(client):
    """Verifies that POST with unofficial broker returns 200 and HIGH_RISK warning."""
    response = client.post("/api/risk-radar/scan-url", json={"url": "https://quick-pan-agent.com/express"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    report = data["scan_report"]
    assert report["is_official_government"] is False
    assert report["risk_level"] in ["HIGH_RISK_BROKER", "HIGH_RISK"]
    assert "quick-pan-agent.com" in report["hostname"]

def test_risk_radar_get_query_param(client):
    """Verifies that GET with query parameter returns 200 (not 405)."""
    response = client.get("/api/risk-radar/scan-url?url=https://cbse.gov.in")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["scan_report"]["is_official_government"] is True

def test_risk_radar_options_preflight(client):
    """Verifies that OPTIONS CORS preflight returns 200 (not 405)."""
    response = client.open("/api/risk-radar/scan-url", method="OPTIONS")
    assert response.status_code == 200

def test_risk_radar_trailing_slash_handling(client):
    """Verifies that trailing slash /api/risk-radar/scan-url/ does not fail with 405."""
    response = client.post("/api/risk-radar/scan-url/", json={"url": "https://incometax.gov.in"})
    assert response.status_code in [200, 308]
    if response.status_code == 308:
        # Follow redirect if issued
        redirect_res = client.post(response.headers["Location"], json={"url": "https://incometax.gov.in"})
        assert redirect_res.status_code == 200
