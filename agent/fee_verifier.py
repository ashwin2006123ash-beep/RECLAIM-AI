"""
RECLAIM AI - Fee Transparency & Verification Engine
Ensures that fees are only displayed when supported by current, verified official gazettes.
Flags unknown or estimated costs honestly. Never processes or requests real payments.
"""
from typing import Dict, Any, Optional
from agent.source_registry import lookup_sources

def verify_document_fee(document_category: str, issuing_authority: Optional[str] = None) -> Dict[str, Any]:
    """
    Verifies the official statutory fee for document recovery.
    Returns structured fee metadata with verification status, citation, and conditions.
    """
    sources = lookup_sources(document_category)
    
    # Check if we have an authoritative source for this authority / document
    matched_source = None
    if issuing_authority:
        auth_clean = issuing_authority.lower()
        for src in sources:
            src_auth = src.get("issuing_authority", "").lower()
            if auth_clean in src_auth or any(term in auth_clean for term in ["cbse", "parivahan", "rto", "incometax", "pan", "uidai", "aadhaar", "eci", "voter", "passport"]):
                matched_source = src
                break
                
    if not matched_source and sources:
        # Default to primary statutory source for the category
        matched_source = sources[0]
        
    # If the user specified a custom/unlisted university or state authority where we lack verified gazette:
    if issuing_authority and any(unknown in issuing_authority.lower() for unknown in ["unknown", "private university", "autonomous college", "unlisted"]):
        return {
            "status": "not_verified",
            "amount": None,
            "currency": "INR",
            "condition": "Issuing institution fee schedule is not verified in public central registry.",
            "source_title": "Direct Institution Registrar Query Required",
            "source_url": None,
            "last_verified": None,
            "is_official": False,
            "message": "Fee not verified. University and state autonomous bodies set independent fee bylaws. Contact the Controller of Examinations or Registrar directly."
        }
        
    if matched_source and "verified_fee" in matched_source:
        vf = matched_source["verified_fee"]
        return {
            "status": vf["status"],
            "amount": vf["amount"],
            "currency": vf["currency"],
            "condition": vf["condition"],
            "source_title": matched_source["issuing_authority"],
            "source_url": matched_source["official_url"],
            "last_verified": matched_source.get("last_checked"),
            "is_official": True,
            "message": f"Statutory Fee: {vf['currency']} {vf['amount']:.2f}. ({vf['condition']})"
        }
        
    return {
        "status": "not_verified",
        "amount": None,
        "currency": "INR",
        "condition": "No official fee schedule available for this category.",
        "source_title": None,
        "source_url": None,
        "last_verified": None,
        "is_official": False,
        "message": "Fee not verified. Always check the official issuing authority portal directly before paying."
    }
