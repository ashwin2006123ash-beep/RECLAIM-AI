"""
RECLAIM AI - Recovery Readiness Score Calculator
Calculates an explainable 0-100 indicator based on preparation completeness.
Provides transparent item-by-item breakdown and mandatory legal disclaimer.
"""
from typing import Dict, Any, List

READINESS_DISCLAIMER = (
    "DISCLAIMER: This score measures preparation completeness and documentary readiness only. "
    "It is NOT an official government score and does NOT guarantee government approval or document reissue."
)

def calculate_readiness_score(intake_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates evidence completeness and returns a structured 0-100 score
    along with checklist items and actionable missing items.
    """
    checklist: List[Dict[str, Any]] = []
    total_score = 0
    missing_items: List[str] = []
    
    # Item 1: Document Category (15 pts)
    doc_type = intake_data.get("document_type") or intake_data.get("document_category")
    if doc_type:
        total_score += 15
        checklist.append({
            "id": "doc_type",
            "name": "Document Category Specified",
            "points": 15,
            "max_points": 15,
            "status": "complete",
            "detail": f"Category defined as '{doc_type}'."
        })
    else:
        checklist.append({
            "id": "doc_type",
            "name": "Document Category Specified",
            "points": 0,
            "max_points": 15,
            "status": "missing",
            "detail": "No document category selected."
        })
        missing_items.append("Select document type")
        
    # Item 2: Authority & Jurisdiction (15 pts)
    authority = intake_data.get("issuing_authority")
    jurisdiction = intake_data.get("jurisdiction")
    if authority and jurisdiction and authority.lower() not in ["unknown", ""]:
        total_score += 15
        checklist.append({
            "id": "authority",
            "name": "Issuing Authority & Jurisdiction",
            "points": 15,
            "max_points": 15,
            "status": "complete",
            "detail": f"Authority identified as '{authority}' ({jurisdiction})."
        })
    elif authority or jurisdiction:
        total_score += 8
        checklist.append({
            "id": "authority",
            "name": "Issuing Authority & Jurisdiction",
            "points": 8,
            "max_points": 15,
            "status": "partial",
            "detail": "Authority or state jurisdiction partially specified."
        })
        missing_items.append("Clarify specific state or board authority")
    else:
        checklist.append({
            "id": "authority",
            "name": "Issuing Authority & Jurisdiction",
            "points": 0,
            "max_points": 15,
            "status": "missing",
            "detail": "Issuing authority and state jurisdiction unknown."
        })
        missing_items.append("Identify exact issuing university, board, or regional office")
        
    # Item 3: Loss Circumstances & Status (10 pts)
    status_type = intake_data.get("status_type")
    circumstances = intake_data.get("circumstances", "")
    if status_type and status_type in ["lost", "stolen", "damaged"]:
        score_circum = 10 if len(str(circumstances).strip()) > 5 else 6
        total_score += score_circum
        checklist.append({
            "id": "status_circumstances",
            "name": "Loss Status & Circumstances",
            "points": score_circum,
            "max_points": 10,
            "status": "complete" if score_circum == 10 else "partial",
            "detail": f"Status is '{status_type}'. {('Context noted: ' + circumstances[:40] + '...') if circumstances else 'Context details brief.'}"
        })
    else:
        checklist.append({
            "id": "status_circumstances",
            "name": "Loss Status & Circumstances",
            "points": 0,
            "max_points": 10,
            "status": "missing",
            "detail": "Loss status not documented."
        })
        missing_items.append("Specify how the document was lost, stolen, or damaged")
        
    # Item 4: Police Complaint / DDR / NCR / FIR (20 pts)
    has_police_report = intake_data.get("has_police_report", False)
    if has_police_report:
        total_score += 20
        checklist.append({
            "id": "police_report",
            "name": "Police Report (FIR / DDR / Lost Article Report)",
            "points": 20,
            "max_points": 20,
            "status": "complete",
            "detail": "Police incident report or Daily Diary entry available."
        })
    else:
        needs_fir = status_type == "stolen" or doc_type in ["driving_licence", "passport"]
        checklist.append({
            "id": "police_report",
            "name": "Police Report (FIR / DDR / Lost Article Report)",
            "points": 0,
            "max_points": 20,
            "status": "missing",
            "detail": "Police report not yet filed." + (" (Mandatory for this document type/status)" if needs_fir else " (Recommended for loss proof)")
        })
        missing_items.append("Obtain online Police Lost Document Report / DDR or FIR")
        
    # Item 5: Notarized Affidavit (15 pts)
    has_affidavit = intake_data.get("has_affidavit", False)
    if has_affidavit:
        total_score += 15
        checklist.append({
            "id": "affidavit",
            "name": "Notarized Loss Affidavit on Stamp Paper",
            "points": 15,
            "max_points": 15,
            "status": "complete",
            "detail": "Sworn affidavit attested by Notary Public / Magistrate ready."
        })
    else:
        needs_aff = doc_type in ["edu_cert", "passport", "other_cert"]
        checklist.append({
            "id": "affidavit",
            "name": "Notarized Loss Affidavit on Stamp Paper",
            "points": 0,
            "max_points": 15,
            "status": "missing",
            "detail": "Affidavit not prepared." + (" (Required by University / Board / Passport office)" if needs_aff else " (Optional for this category)")
        })
        if needs_aff:
            missing_items.append("Prepare non-judicial stamp paper affidavit attested by Notary")
            
    # Item 6: Government Photo ID Proof (15 pts)
    has_id_proof = intake_data.get("has_id_proof", False)
    if has_id_proof:
        total_score += 15
        checklist.append({
            "id": "id_proof",
            "name": "Government Photo Identity & Address Proof",
            "points": 15,
            "max_points": 15,
            "status": "complete",
            "detail": "Valid secondary government identity proof confirmed available."
        })
    else:
        checklist.append({
            "id": "id_proof",
            "name": "Government Photo Identity & Address Proof",
            "points": 0,
            "max_points": 15,
            "status": "missing",
            "detail": "Secondary photo ID not verified."
        })
        missing_items.append("Keep Aadhaar, Voter ID, or other secondary government photo ID ready")
        
    # Item 7: Original Roll / Registration / Card Number / Copy (10 pts)
    has_doc_number_or_copy = intake_data.get("has_doc_number_or_copy", False)
    if has_doc_number_or_copy:
        total_score += 10
        checklist.append({
            "id": "doc_number",
            "name": "Previous Document Number / Photocopy / DigiLocker record",
            "points": 10,
            "max_points": 10,
            "status": "complete",
            "detail": "Previous document identifier, mark sheet photocopy, or roll number known."
        })
    else:
        checklist.append({
            "id": "doc_number",
            "name": "Previous Document Number / Photocopy / DigiLocker record",
            "points": 0,
            "max_points": 10,
            "status": "missing",
            "detail": "No previous registration number, roll number, or duplicate copy available."
        })
        missing_items.append("Check old records, educational institution transcripts, or DigiLocker for document number")
        
    # Cap total score at 100
    total_score = min(100, max(0, total_score))
    
    return {
        "score": total_score,
        "checklist": checklist,
        "missing_items": missing_items,
        "explanation": READINESS_DISCLAIMER,
        "readiness_level": (
            "Ready for Official Submission" if total_score >= 80
            else "Substantially Prepared (Minor Prerequisites Pending)" if total_score >= 50
            else "Early Preparation Stage (Prerequisites Incomplete)"
        )
    }
