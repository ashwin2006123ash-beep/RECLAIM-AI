"""
Unit tests for 10-Step Inspectable Agentic Workflow
"""
from agent.workflow import AgenticRecoveryWorkflow
from database.models import get_session_by_id, get_session_trace, get_session_evidence

def test_workflow_execution_and_trace(app):
    with app.app_context():
        workflow = AgenticRecoveryWorkflow(session_id="TEST-WF-001")
        intake_data = {
            "document_type": "edu_cert",
            "jurisdiction": "Central / All India",
            "issuing_authority": "Central Board of Secondary Education (CBSE)",
            "status_type": "lost",
            "circumstances": "Relocation loss of senior secondary certificate.",
            "has_police_report": True,
            "has_affidavit": True,
            "has_id_proof": True,
            "has_doc_number_or_copy": True
        }
        res = workflow.run_full_intake_and_guidance(intake_data)
        assert res["session_id"] == "TEST-WF-001"
        assert res["workflow_status"] == "awaiting_approval"
        assert "approval_id" in res
        
        # Check SQLite persistence
        session = get_session_by_id("TEST-WF-001")
        assert session is not None
        assert session["document_type"] == "edu_cert"
        assert session["workflow_status"] == "awaiting_approval"
        assert session["readiness_score"] >= 80
        
        # Check trace events
        traces = get_session_trace("TEST-WF-001")
        assert len(traces) == 8 # Steps 1 through 8 logged
        step_names = [t["step_name"] for t in traces]
        assert "STEP 1: INTAKE" in step_names
        assert "STEP 2: CLASSIFY" in step_names
        assert "STEP 3: PLAN" in step_names
        assert "STEP 4: RETRIEVE" in step_names
        assert "STEP 5: VERIFY" in step_names
        assert "STEP 6: APPLY RULES" in step_names
        assert "STEP 7: EXPLAIN" in step_names
        assert "STEP 8: HUMAN APPROVAL" in step_names
        
        # Check evidence vault
        evidence = get_session_evidence("TEST-WF-001")
        assert len(evidence) > 0
        cbse_evidence = next((e for e in evidence if "cbse" in e["source_url"].lower()), None)
        assert cbse_evidence is not None
        assert cbse_evidence["verification_status"] == "official_verified"
