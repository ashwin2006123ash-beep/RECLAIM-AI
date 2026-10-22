"""
Pytest suite for Innovation 3: Provenance Graph Engine
Verifies end-to-end 7-tier DAG generation, node linking, and assumption tracking.
"""
import pytest
from agent.provenance_graph import ProvenanceGraphEngine

def test_provenance_graph_structure(client):
    """Verifies that the provenance graph endpoint returns a complete 7-tier graph."""
    # First submit an intake to have a valid session
    intake_res = client.post("/api/recovery/intake", json={
        "document_type": "driving_licence",
        "jurisdiction": "Karnataka",
        "issuing_authority": "Ministry of Road Transport and Highways (MoRTH)",
        "status_type": "lost",
        "has_police_report": True,
        "has_affidavit": False,
        "has_id_proof": True,
        "has_doc_number_or_copy": True
    })
    assert intake_res.status_code == 200
    session_id = intake_res.get_json()["data"]["session_id"]

    # Fetch provenance graph
    res = client.get(f"/api/recovery/{session_id}/provenance-graph")
    assert res.status_code == 200
    graph = res.get_json()

    assert graph["status"] == "success"
    assert len(graph["tier_metadata"]) == 7
    assert graph["node_count"] >= 10
    assert graph["edge_count"] >= 8
    assert graph["provenance_traceability_score"] >= 80

    # Verify tiers present in nodes
    tiers_present = {n["tier"] for n in graph["nodes"]}
    assert {1, 2, 3, 4, 5, 6, 7}.issubset(tiers_present)

def test_provenance_graph_unsupported_claim_highlighting(client):
    """Verifies that an unknown authority case correctly highlights unverified assumptions."""
    graph = ProvenanceGraphEngine.build_graph_for_case("TEST-UNVERIFIED", case_data={
        "intake": {
            "document_type": "edu_cert",
            "jurisdiction": "Unknown",
            "issuing_authority": "Unknown Autonomous College",
            "status_type": "lost"
        }
    })
    assert graph["unsupported_claim_count"] > 0
    # Confirm at least one node has is_unsupported_or_stale = True
    unsupported_nodes = [n for n in graph["nodes"] if n["is_unsupported_or_stale"]]
    assert len(unsupported_nodes) >= 1
    assert any("Authority" in n["label"] or "Fee" in n["label"] for n in unsupported_nodes)
