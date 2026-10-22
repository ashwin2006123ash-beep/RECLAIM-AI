"""
Unit tests for Step 8 Human Approval Gate & Tracking Integrity
"""
from agent.workflow import AgenticRecoveryWorkflow
from database.models import get_session_by_id, get_session_approvals, get_session_trace

def test_approval_and_execution_lifecycle(app):
    with app.app_context():
        workflow = AgenticRecoveryWorkflow(session_id="TEST-APPR-001")
        intake_data = {
            "document_type": "driving_licence",
            "jurisdiction": "Karnataka",
            "issuing_authority": "MoRTH",
            "status_type": "lost",
            "has_police_report": True,
            "has_affidavit": False,
            "has_id_proof": True,
            "has_doc_number_or_copy": True
        }
        res = workflow.run_full_intake_and_guidance(intake_data)
        approval_id = res["approval_id"]
        
        # Verify pre-approval tracking state
        guidance = res["guidance"]
        assert guidance["tracking"]["status"] == "not_submitted"
        assert guidance["tracking"]["reference"] is None
        
        # User explicitly approves
        exec_res = workflow.execute_user_approval_decision(
            approval_id=approval_id,
            user_decision="approved"
        )
        assert exec_res["approval_status"] == "approved"
        assert exec_res["workflow_status"] == "completed"
        
        tracking = exec_res["tracking"]
        assert tracking["status"] == "simulated_draft_ready"
        assert "SIM-" in tracking["reference"]
        assert "SIMULATED" in tracking["label"]
        assert "NOT SUBMITTED TO GOVERNMENT" in tracking["label"]
        
        # Verify traces for steps 9 and 10 were appended
        traces = get_session_trace("TEST-APPR-001")
        assert len(traces) == 10
        assert traces[8]["step_name"] == "STEP 9: EXECUTE PERMITTED ACTION"
        assert traces[9]["step_name"] == "STEP 10: VERIFY RESULT"

def test_rejection_lifecycle(app):
    with app.app_context():
        workflow = AgenticRecoveryWorkflow(session_id="TEST-REJ-001")
        intake_data = {
            "document_type": "pan_card",
            "jurisdiction": "National",
            "issuing_authority": "Income Tax Department",
            "status_type": "lost",
            "has_police_report": False,
            "has_affidavit": False,
            "has_id_proof": True,
            "has_doc_number_or_copy": True
        }
        res = workflow.run_full_intake_and_guidance(intake_data)
        approval_id = res["approval_id"]
        
        # User REJECTS
        exec_res = workflow.execute_user_approval_decision(
            approval_id=approval_id,
            user_decision="rejected"
        )
        assert exec_res["approval_status"] == "rejected"
        assert exec_res["workflow_status"] == "paused_by_user"
        assert exec_res["tracking"]["reference"] is None
        assert exec_res["tracking"]["status"] == "not_submitted"
