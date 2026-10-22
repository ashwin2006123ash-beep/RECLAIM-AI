"""
RECLAIM AI - Official Source Registry
Authoritative repository of verified Indian government and educational issuing authorities
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

OFFICIAL_SOURCE_REGISTRY: List[Dict[str, Any]] = [
    {
        "source_id": "SRC_CBSE_PARIKSHA",
        "document_category": "edu_cert",
        "jurisdiction": "Central / All India",
        "issuing_authority": "Central Board of Secondary Education (CBSE)",
        "official_hostname": "cbse.gov.in",
        "official_url": "https://cbse.gov.in/cbsenew/pariksha_sangam.html",
        "source_type": "Official Examination Portal",
        "information_available": "Duplicate marksheet, passing certificate, migration certificate issuance online through Pariksha Sangam portal.",
        "verified_fee": {
            "status": "verified",
            "amount": 250.0,
            "currency": "INR",
            "condition": "Within 5 years of examination; INR 500 for records older than 5 years."
        },
        "required_documents": [
            "Affidavit on non-judicial stamp paper attested by Notary Public / First Class Magistrate",
            "Copy of Police Daily Diary Report (DDR) / Loss Report",
            "Press clipping of advertisement in national daily newspaper (for duplicate certificate)",
            "Self-attested government photo ID proof (Aadhaar / Voter ID / Passport)"
        ],
        "application_portal": "https://cbseit.in/cbse/web/dads/home.aspx",
        "verification_status": "official_verified",
        "last_checked": "2026-10-15T08:00:00Z"
    },
    {
        "source_id": "SRC_DIGILOCKER_EDU",
        "document_category": "edu_cert",
        "jurisdiction": "All India",
        "issuing_authority": "Ministry of Electronics and Information Technology (MeitY)",
        "official_hostname": "digilocker.gov.in",
        "official_url": "https://digilocker.gov.in",
        "source_type": "Official Digital Document Repository",
        "information_available": "Legally valid digital duplicates of CBSE, CISCE, and state university marksheets under Information Technology Rules 2016.",
        "verified_fee": {
            "status": "verified",
            "amount": 0.0,
            "currency": "INR",
            "condition": "Free of cost digital credential pull via Aadhaar authenticated account."
        },
        "required_documents": [
            "Aadhaar authenticated account",
            "Candidate roll number, year of passing, and exam type"
        ],
        "application_portal": "https://digilocker.gov.in",
        "verification_status": "official_verified",
        "last_checked": "2026-10-18T10:00:00Z"
    },
    {
        "source_id": "SRC_PARIVAHAN_SARATHI",
        "document_category": "driving_licence",
        "jurisdiction": "All India (MoRTH)",
        "issuing_authority": "Ministry of Road Transport and Highways (MoRTH)",
        "official_hostname": "parivahan.gov.in",
        "official_url": "https://sarathi.parivahan.gov.in/sarathiservice/stateSelection.do",
        "source_type": "National Transport Services Portal",
        "information_available": "Duplicate Driving Licence issue (Form LLD) due to loss, theft, mutilation under CMVR 1989 Rule 81.",
        "verified_fee": {
            "status": "verified",
            "amount": 400.0,
            "currency": "INR",
            "condition": "INR 200 issue of duplicate DL + INR 200 smart card fee as per CMVR Rule 81."
        },
        "required_documents": [
            "Form LLD (Application for Duplicate Licence)",
            "Police Report / First Information Report (FIR) / Non-Cognizable Report (NCR) for lost/stolen DL",
            "Self-declaration / Affidavit stating circumstances of loss",
            "Copy of original Driving Licence (if available)",
            "Valid Address & Identity proof"
        ],
        "application_portal": "https://sarathi.parivahan.gov.in",
        "verification_status": "official_verified",
        "last_checked": "2026-10-20T12:00:00Z"
    },
    {
        "source_id": "SRC_INCOMETAX_PAN",
        "document_category": "pan_card",
        "jurisdiction": "National / Central Board of Direct Taxes",
        "issuing_authority": "Income Tax Department of India",
        "official_hostname": "incometax.gov.in",
        "official_url": "https://www.incometax.gov.in/iec/foportal/",
        "source_type": "Official Central Tax Portal",
        "information_available": "Reprint of PAN Card without data change or application for duplicate PAN card with corrections via authorized NSDL/UTIITSL portals.",
        "verified_fee": {
            "status": "verified",
            "amount": 50.0,
            "currency": "INR",
            "condition": "INR 50 inclusive of taxes for dispatch within India (reprint); INR 959 for dispatch outside India."
        },
        "required_documents": [
            "10-digit PAN number",
            "Aadhaar number (for online OTP e-KYC paperless dispatch)",
            "Proof of Identity & Proof of Address (if applying offline)"
        ],
        "application_portal": "https://www.onlineservices.nsdl.com/paam/ReprintEPan.html",
        "verification_status": "official_verified",
        "last_checked": "2026-10-19T09:30:00Z"
    },
    {
        "source_id": "SRC_UIDAI_AADHAAR",
        "document_category": "aadhaar",
        "jurisdiction": "National (UIDAI)",
        "issuing_authority": "Unique Identification Authority of India (UIDAI)",
        "official_hostname": "uidai.gov.in",
        "official_url": "https://myaadhaar.uidai.gov.in/",
        "source_type": "Official Identity Portal",
        "information_available": "Retrieve lost Aadhaar Number (UID) / Enrollment ID (EID) and order PVC reprint or download password-protected e-Aadhaar.",
        "verified_fee": {
            "status": "verified",
            "amount": 50.0,
            "currency": "INR",
            "condition": "Free for electronic e-Aadhaar download; INR 50 for secure PVC card reprint delivered by Speed Post."
        },
        "required_documents": [
            "Registered mobile number or email linked to Aadhaar (for OTP retrieval)",
            "Demographic details: Full Name, Date of Birth, PIN code"
        ],
        "application_portal": "https://myaadhaar.uidai.gov.in/gen-pvc",
        "verification_status": "official_verified",
        "last_checked": "2026-10-21T11:00:00Z"
    },
    {
        "source_id": "SRC_ECI_VOTER",
        "document_category": "voter_id",
        "jurisdiction": "Election Commission of India",
        "issuing_authority": "Election Commission of India (ECI)",
        "official_hostname": "voters.eci.gov.in",
        "official_url": "https://voters.eci.gov.in/",
        "source_type": "National Voters' Service Portal",
        "information_available": "Form 8 (Application for shifting of residence/correction of entries/replacement of EPIC without correction).",
        "verified_fee": {
            "status": "verified",
            "amount": 0.0,
            "currency": "INR",
            "condition": "Free of cost. Replacement EPIC issued without government fee."
        },
        "required_documents": [
            "Police Report / Lost Document Report copy (mandatory for lost/stolen card; not required for mutilated)",
            "Existing EPIC number (or search in electoral roll by name & state)",
            "Recent passport size color photograph"
        ],
        "application_portal": "https://voters.eci.gov.in/form8",
        "verification_status": "official_verified",
        "last_checked": "2026-10-18T14:00:00Z"
    },
    {
        "source_id": "SRC_PASSPORT_SEVA",
        "document_category": "passport",
        "jurisdiction": "Ministry of External Affairs (MEA)",
        "issuing_authority": "Consular, Passport & Visa Division, MEA",
        "official_hostname": "passportindia.gov.in",
        "official_url": "https://www.passportindia.gov.in/",
        "source_type": "Official Passport Seva Portal",
        "information_available": "Reissue of Passport in lieu of lost, damaged or stolen passport under normal or tatkaal category.",
        "verified_fee": {
            "status": "verified",
            "amount": 3000.0,
            "currency": "INR",
            "condition": "INR 3,000 for 36-page booklet under normal reissue for lost/damaged passport; INR 5,000 under Tatkaal scheme."
        },
        "required_documents": [
            "Police Certificate / First Information Report (FIR) in original",
            "Self-attested affidavit as per Annexure 'F' explaining how and when passport was lost/damaged",
            "Proof of Date of Birth (Birth Certificate / School Transfer Certificate)",
            "Proof of Present Address (Voter ID / Utility bill / Bank passbook)"
        ],
        "application_portal": "https://portal2.passportindia.gov.in/AppOnlineProject/welcomeLink",
        "verification_status": "official_verified",
        "last_checked": "2026-10-17T16:00:00Z"
    }
]

def get_all_sources() -> List[Dict[str, Any]]:
    return OFFICIAL_SOURCE_REGISTRY

def lookup_sources(document_category: str, jurisdiction: Optional[str] = None) -> List[Dict[str, Any]]:
    results = []
    for src in OFFICIAL_SOURCE_REGISTRY:
        if src["document_category"] == document_category:
            results.append(src)
            
    # Always include DigiLocker as a companion official repository for credentials
    if document_category in ["edu_cert", "driving_licence", "pan_card", "voter_id"]:
        digilocker_src = next((s for s in OFFICIAL_SOURCE_REGISTRY if s["source_id"] == "SRC_DIGILOCKER_EDU"), None)
        if digilocker_src and digilocker_src not in results:
            results.append(digilocker_src)
            
    return results

def get_source_by_id(source_id: str) -> Optional[Dict[str, Any]]:
    for src in OFFICIAL_SOURCE_REGISTRY:
        if src["source_id"] == source_id:
            return src
    return None
