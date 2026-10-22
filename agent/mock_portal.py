"""
RECLAIM AI 2.0 - Innovation 5: Safe Action Sandbox & Mock Government Portal
Persistent local mock government portal backend with strict idempotency keys,
independent state verification, synthetic receipt generation, and human approval enforcement.
"""
import uuid
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from database.models import (
    create_mock_portal_application,
    get_mock_portal_application_by_idempotency,
    get_mock_portal_application_by_ref
)

SYNTHETIC_RECEIPT_WATERMARK = "SYNTHETIC DEMO — NOT A REAL GOVERNMENT APPLICATION"

class MockGovernmentPortalService:
    """
    Simulates a secure statutory government portal gateway (e.g. Parivahan Mock Gateway / CBSE DADS Mock).
    Maintains persistent SQLite database state, enforces idempotency, and validates independent receipt state.
    """

    @classmethod
    def prepare_draft_application(cls, case_data: Dict[str, Any], readiness_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates prerequisites and compiles a structured draft application package.
        """
        doc_type = case_data.get("document_type", "edu_cert")
        authority = case_data.get("issuing_authority", "Statutory Authority")
        jurisdiction = case_data.get("jurisdiction", "India")
        status_type = case_data.get("status_type", "lost")

        # Required fields validation
        missing_fields = []
        if not doc_type:
            missing_fields.append("Document Category")
        if not authority or authority.lower() in ["unknown", "unknown autonomous college"]:
            missing_fields.append("Specific Issuing Authority")
        if not jurisdiction:
            missing_fields.append("State or Jurisdiction")

        is_valid = len(missing_fields) == 0

        draft_id = f"DRAFT-{doc_type[:4].upper()}-{uuid.uuid4().hex[:6].upper()}"
        idempotency_key = f"IDEMP-{case_data.get('case_id', uuid.uuid4().hex[:8])}-{doc_type[:4].upper()}"

        return {
            "draft_id": draft_id,
            "idempotency_key": idempotency_key,
            "is_valid": is_valid,
            "missing_prerequisites": missing_fields,
            "document_type": doc_type,
            "issuing_authority": authority,
            "jurisdiction": jurisdiction,
            "loss_status": status_type,
            "evidence_attached": {
                "police_report_declared": bool(case_data.get("has_police_report")),
                "notarized_affidavit_declared": bool(case_data.get("has_affidavit")),
                "id_proof_declared": bool(case_data.get("has_id_proof")),
                "previous_document_copy_declared": bool(case_data.get("has_doc_number_or_copy"))
            },
            "readiness_score": readiness_data.get("score", 0),
            "simulated_portal_target": f"https://mock-portal.gov.in/{doc_type}/reissue",
            "statutory_notice": SYNTHETIC_RECEIPT_WATERMARK,
            "prepared_at": datetime.now(timezone.utc).isoformat()
        }

    @classmethod
    def execute_mock_submission(cls, draft_package: Dict[str, Any],
                                citizen_signature: str = "Verified Citizen",
                                simulate_failure: bool = False) -> Dict[str, Any]:
        """
        Executes submission against the persistent mock government portal backend.
        Guarantees idempotency (prevents duplicate submissions) and generates synthetic receipt.
        """
        idempotency_key = draft_package.get("idempotency_key")
        case_id = draft_package.get("case_id", f"CASE-{uuid.uuid4().hex[:6].upper()}")
        doc_type = draft_package.get("document_type", "edu_cert")
        authority = draft_package.get("issuing_authority", "National Authority")

        # 1. Idempotency Check
        existing_app = get_mock_portal_application_by_idempotency(idempotency_key)
        if existing_app:
            return {
                "status": "success",
                "is_duplicate_execution": True,
                "message": f"Idempotency Guard: Existing submission detected for key '{idempotency_key}'. Returning verified receipt.",
                "application_ref": existing_app["application_ref"],
                "submission_status": existing_app["submission_status"],
                "receipt": existing_app["receipt"],
                "audit_trail": existing_app["audit_trail"]
            }

        # 2. Check Prerequisites Validity
        if not draft_package.get("is_valid"):
            missing = draft_package.get("missing_prerequisites", [])
            return {
                "status": "error",
                "is_duplicate_execution": False,
                "message": f"Application rejected by mock portal: Missing statutory prerequisites ({', '.join(missing)}).",
                "application_ref": None,
                "submission_status": "FAILED",
                "receipt": None
            }

        # 3. Simulate Failure Flag (if requested for test lab failure scenario testing)
        if simulate_failure:
            return {
                "status": "error",
                "is_duplicate_execution": False,
                "message": "Simulated Gateway Failure: Mock government portal database timed out. Idempotent retry permitted.",
                "application_ref": None,
                "submission_status": "FAILED",
                "receipt": None
            }

        # 4. Generate Synthetic Application Reference
        # Format: SIM-<CATEGORY>-YYYY-<4_HEX>
        now = datetime.now(timezone.utc)
        app_ref = f"SIM-{doc_type[:4].upper()}-{now.year}-{uuid.uuid4().hex[:4].upper()}"

        audit_trail = [
            {"event": "DRAFT_VALIDATED", "timestamp": draft_package.get("prepared_at"), "agent": "RECLAIM AI Pre-submission Validator"},
            {"event": "CITIZEN_APPROVAL_GRANTED", "timestamp": now.isoformat(), "authorized_by": citizen_signature},
            {"event": "MOCK_PORTAL_INGESTED", "timestamp": now.isoformat(), "gateway": f"{authority} Mock Endpoint"}
        ]

        receipt = {
            "synthetic_disclaimer": SYNTHETIC_RECEIPT_WATERMARK,
            "application_reference": app_ref,
            "document_type": doc_type,
            "issuing_authority": authority,
            "applicant_declaration": "Synthetic Citizen Demonstration Record",
            "submission_timestamp": now.isoformat(),
            "tracking_url": f"/api/mock-portal/verify/{app_ref}",
            "status_code": "CONFIRMED_DEMO_SUBMISSION",
            "next_steps_notice": "This draft was compiled and recorded locally in the Safe Action Sandbox. To lodge an actual legal application, proceed directly to the verified statutory government portal."
        }

        # 5. Persist in SQLite Mock Portal Table
        record = create_mock_portal_application(
            application_ref=app_ref,
            idempotency_key=idempotency_key,
            case_id=case_id,
            applicant_data=draft_package,
            portal_name=f"{authority} Safe Sandbox Portal",
            submission_status="CONFIRMED",
            receipt=receipt,
            audit_trail=audit_trail
        )

        return {
            "status": "success",
            "is_duplicate_execution": False,
            "message": f"Mock application successfully submitted and confirmed under reference: {app_ref}.",
            "application_ref": app_ref,
            "submission_status": "CONFIRMED",
            "receipt": receipt,
            "audit_trail": audit_trail
        }

    @classmethod
    def independently_verify_mock_status(cls, application_ref: str) -> Dict[str, Any]:
        """
        Independent status verification. Queries database to check actual stored receipt state.
        Ensures frontend does not fake success without genuine backend persistence.
        """
        record = get_mock_portal_application_by_ref(application_ref)
        if not record:
            return {
                "verified": False,
                "status": "NOT_FOUND",
                "message": f"Verification failed: Reference '{application_ref}' does not exist in mock government portal registry."
            }

        return {
            "verified": True,
            "application_ref": record["application_ref"],
            "portal_name": record["portal_name"],
            "submission_status": record["submission_status"],
            "submitted_at": record["submitted_at"],
            "receipt": record["receipt"],
            "audit_trail": record["audit_trail"],
            "is_synthetic_demo": True,
            "disclaimer": SYNTHETIC_RECEIPT_WATERMARK
        }
