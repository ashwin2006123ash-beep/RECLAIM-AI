"""
RECLAIM AI - Gemini AI Client & Deterministic Fallback Engine
Integrates the Google Gemini API (Interactions / google-genai SDK)
with a robust deterministic fallback when no API key is provided or offline.
"""
import os
import json
import logging
from typing import Dict, Any, Optional
from config import Config

logger = logging.getLogger(__name__)

def is_gemini_available() -> bool:
    """Returns True if a non-empty GEMINI_API_KEY is configured."""
    return bool(Config.GEMINI_API_KEY and len(Config.GEMINI_API_KEY.strip()) > 8)

def call_gemini_api(prompt: str) -> Optional[str]:
    """
    Invokes Google Gemini using the official google-genai SDK.
    Returns response text or None on failure.
    """
    if not is_gemini_available():
        return None
        
    try:
        from google import genai
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=prompt,
            config={
                "temperature": 0.2,
                "response_mime_type": "application/json"
            }
        )
        return response.text
    except Exception as e:
        logger.warning(f"Gemini API invocation failed: {str(e)}. Falling back to deterministic reasoning.")
        return None

def build_deterministic_recovery_plan(intake_data: Dict[str, Any],
                                      verified_sources: list,
                                      fee_info: Dict[str, Any],
                                      readiness_info: Dict[str, Any],
                                      flagged_sources: list) -> Dict[str, Any]:
    """
    High-fidelity deterministic agent reasoning engine.
    Produces structured, source-backed recovery roadmap adhering to statutory rules.
    """
    doc_type = intake_data.get("document_type", "edu_cert")
    authority = intake_data.get("issuing_authority", "Central/State Authority")
    jurisdiction = intake_data.get("jurisdiction", "India")
    status_type = intake_data.get("status_type", "lost")
    
    # Missing information detection
    missing_info = []
    if not intake_data.get("issuing_authority") or authority.lower() in ["unknown", ""]:
        missing_info.append("Specific educational board, university, or regional RTO name")
    if not intake_data.get("jurisdiction") or jurisdiction.lower() in ["unknown", "unknown state"]:
        missing_info.append("State or union territory of initial issue")
    if not intake_data.get("has_police_report") and status_type in ["stolen", "lost"]:
        missing_info.append("Online Police Lost Article Report (DDR/NCR/FIR number)")
    if not intake_data.get("has_doc_number_or_copy"):
        missing_info.append("Previous document registration/roll number or photocopy")
        
    # Build Next Steps sequence
    next_steps = []
    step_num = 1
    
    # Step 1: Authority Identification
    if missing_info and ("Specific educational board" in missing_info[0] or "State or union" in missing_info[0]):
        next_steps.append({
            "step": step_num,
            "action": "Clarify Issuing Authority & Affiliation",
            "reason": "Reissue procedures and bylaws vary by university or state authority. Cannot proceed to official application without exact issuer.",
            "source_ids": [],
            "status": "pending_clarification"
        })
        step_num += 1
    else:
        next_steps.append({
            "step": step_num,
            "action": f"Confirm Issuing Authority ({authority})",
            "reason": f"Official duplicate request must be filed through the jurisdiction of {jurisdiction}.",
            "source_ids": [s.get("source_id") for s in verified_sources if s.get("source_id")],
            "status": "complete"
        })
        step_num += 1
        
    # Step 2: Police Report / DDR
    if status_type in ["stolen", "lost"]:
        next_steps.append({
            "step": step_num,
            "action": "File Police Lost Document / Daily Diary Report (DDR/NCR) Online",
            "reason": "A statutory loss report protects against identity theft and is required by government issuing authorities.",
            "source_ids": [s.get("source_id") for s in verified_sources if s.get("source_id")],
            "status": "complete" if intake_data.get("has_police_report") else "action_required"
        })
        step_num += 1
        
    # Step 3: Notarized Affidavit (for edu_cert, passport, or damaged items)
    if doc_type in ["edu_cert", "passport", "other_cert"]:
        next_steps.append({
            "step": step_num,
            "action": "Execute Notarized Loss Affidavit on Non-Judicial Stamp Paper",
            "reason": "Sworn statement before a Notary Public or Executive Magistrate affirming the loss and undertaking not to misuse the document.",
            "source_ids": [s.get("source_id") for s in verified_sources if s.get("source_id")],
            "status": "complete" if intake_data.get("has_affidavit") else "action_required"
        })
        step_num += 1
        
    # Step 4: Digital Retrieval via DigiLocker
    next_steps.append({
        "step": step_num,
        "action": "Attempt Instant Electronic Pull via DigiLocker",
        "reason": "DigiLocker documents carry legal equivalence to original physical certificates under Section 9A of the IT Act 2000.",
        "source_ids": ["SRC_DIGILOCKER_EDU"],
        "status": "recommended_immediate"
    })
    step_num += 1
    
    # Step 5: Official Reissue Application
    portal_name = verified_sources[0]["source_type"] if verified_sources else "Official Portal"
    next_steps.append({
        "step": step_num,
        "action": f"Submit Reissue Application via {portal_name}",
        "reason": "Legitimate reissue can only be processed through the verified statutory portal or designated facilitation center.",
        "source_ids": [s.get("source_id") for s in verified_sources if s.get("source_id")],
        "status": "ready_for_approval" if readiness_info.get("score", 0) >= 50 else "blocked_by_missing_evidence"
    })
    step_num += 1
    
    # Required documents aggregation
    required_docs = []
    for s in verified_sources:
        for doc in s.get("required_documents", []):
            if doc not in required_docs:
                required_docs.append(doc)
                
    if not required_docs:
        required_docs = [
            "Online Police Lost Document Entry (DDR/NCR/FIR)",
            "Self-attested Government Photo ID (Aadhaar / Voter ID / Passport)",
            "Notarized Affidavit on non-judicial stamp paper",
            "Photocopy or roll/registration number of lost document"
        ]
        
    # Proposed Action for Human-in-the-Loop Gate
    primary_portal = verified_sources[0].get("official_url") if verified_sources else None
    proposed_action = {
        "action_id": "ACT_PREPARE_RECOVERY_DOSSIER",
        "name": "Prepare Official Application Dossier & Safe Portal Link",
        "description": f"Compile pre-filled application dossier for {authority} and prepare navigation to verified portal {primary_portal or 'official portal'}.",
        "requires_approval": True,
        "consequences": (
            "Will generate a structured recovery checklist package and open the verified official portal in a secure window. "
            "No actual government fees will be debited and no external database will be modified without your direct submission on the government website."
        )
    }
    
    return {
        "document_type": doc_type,
        "jurisdiction": jurisdiction,
        "issuing_authority": authority,
        "workflow_status": "guidance_prepared",
        "engine_mode": "DETERMINISTIC_FALLBACK_AI",
        "next_steps": next_steps,
        "required_documents": required_docs,
        "missing_information": missing_info,
        "fees": fee_info,
        "sources": verified_sources,
        "flagged_sources": flagged_sources,
        "readiness": readiness_info,
        "proposed_action": proposed_action,
        "tracking": {
            "status": "not_submitted",
            "reference": None,
            "tracking_note": "Application has not been submitted to any government portal. Antigravity/RECLAIM AI does not invent simulated tracking numbers without explicit user approval."
        }
    }

def generate_agent_recovery_guidance(intake_data: Dict[str, Any],
                                     verified_sources: list,
                                     fee_info: Dict[str, Any],
                                     readiness_info: Dict[str, Any],
                                     flagged_sources: list) -> Dict[str, Any]:
    """
    Main orchestration entry point:
    Attempts Gemini API structured generation first; if unavailable, uses the deterministic engine.
    """
    # If Gemini is configured, attempt live call
    if is_gemini_available():
        prompt = f"""
You are the RECLAIM AI agent guiding a citizen whose document was lost/stolen/damaged.
Input Data: {json.dumps(intake_data)}
Verified Sources Available: {json.dumps(verified_sources)}
Fee Information: {json.dumps(fee_info)}
Readiness Score: {json.dumps(readiness_info)}
Flagged Unofficial Sources: {json.dumps(flagged_sources)}

Follow these strict civic AI rules:
1. Do not invent government fees or arbitrary form names.
2. Flag unofficial third-party broker websites.
3. If issuing authority is missing or unknown, mark it as missing information and ask for clarification.
4. Output must be strictly valid JSON matching this schema:
{{
  "document_type": string,
  "jurisdiction": string,
  "issuing_authority": string,
  "workflow_status": "guidance_prepared",
  "engine_mode": "LIVE_GEMINI_AI",
  "next_steps": [{{"step": int, "action": string, "reason": string, "source_ids": [string], "status": string}}],
  "required_documents": [string],
  "missing_information": [string],
  "fees": {{"status": string, "amount": number or null, "currency": "INR", "condition": string, "message": string}},
  "sources": list,
  "flagged_sources": list,
  "readiness": object,
  "proposed_action": {{"action_id": string, "name": string, "description": string, "requires_approval": true, "consequences": string}},
  "tracking": {{"status": "not_submitted", "reference": null, "tracking_note": string}}
}}
"""
        response_text = call_gemini_api(prompt)
        if response_text:
            try:
                parsed = json.loads(response_text)
                parsed["engine_mode"] = "LIVE_GEMINI_AI"
                return parsed
            except Exception as e:
                logger.warning(f"Failed to parse Gemini response: {e}. Falling back.")
                
    # Deterministic reasoning fallback
    return build_deterministic_recovery_plan(
        intake_data, verified_sources, fee_info, readiness_info, flagged_sources
    )
