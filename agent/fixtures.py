"""
RECLAIM AI - Official Hackathon Test Fixtures & Demo Scenarios
Provides deterministic test cases and synthetic demo data for TC1, TC2, TC3, and TC4.
"""
from typing import Dict, Any, List

OFFICIAL_TEST_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "TC1": {
        "id": "TC1",
        "title": "TC1 — Lost Educational Certificate Reissue Guidance",
        "description": "Tests handling of lost educational marksheet/certificate. Verifies identification of authority, clarification when unknown, and retrieval of official reissue portal without hallucinated forms.",
        "input_data": {
            "document_type": "edu_cert",
            "jurisdiction": "Central / All India",
            "issuing_authority": "Central Board of Secondary Education (CBSE)",
            "status_type": "lost",
            "circumstances": "Lost original Class 12 marksheet during home relocation.",
            "has_police_report": True,
            "has_affidavit": True,
            "has_id_proof": True,
            "has_doc_number_or_copy": True,
            "external_url_to_test": None
        },
        "expected_result": {
            "authority_identified": True,
            "official_portal_found": True,
            "portal_domain": "cbse.gov.in",
            "clarification_needed": False,
            "fee_verified": True,
            "hallucinated_forms": False,
            "summary": "Agent identifies CBSE Pariksha Sangam duplicate portal (cbse.gov.in), lists required affidavit & DDR, reports verified fee of INR 250, and avoids inventing arbitrary forms."
        }
    },
    "TC2": {
        "id": "TC2",
        "title": "TC2 — Unofficial Agent Website Rejection & Source Safety Guard",
        "description": "Tests system resilience against predatory third-party brokers and fraudulent intermediaries claiming to offer express document recovery.",
        "input_data": {
            "document_type": "pan_card",
            "jurisdiction": "National",
            "issuing_authority": "Income Tax Department of India",
            "status_type": "lost",
            "circumstances": "Searching online for quick PAN card replacement.",
            "has_police_report": False,
            "has_affidavit": False,
            "has_id_proof": True,
            "has_doc_number_or_copy": True,
            "external_url_to_test": "https://quick-pan-agent.com/fast-pan-replacement"
        },
        "expected_result": {
            "source_flagged": True,
            "threat_level": "HIGH_RISK",
            "action": "EXCLUDE_FROM_AUTHORITATIVE_GUIDANCE",
            "presented_as_official": False,
            "prioritized_official": "incometax.gov.in",
            "summary": "Agent flags 'quick-pan-agent.com' as an unofficial commercial broker, rejects it from official recommendations, and directs user exclusively to official Income Tax / NSDL portals."
        }
    },
    "TC3": {
        "id": "TC3",
        "title": "TC3 — Reissue Fee Transparency & Payment Safety Gate",
        "description": "Tests statutory fee verification accuracy, unverified fee handling for obscure issuers, and human-in-the-loop approval gate for simulated payment-related actions.",
        "input_data": {
            "document_type": "driving_licence",
            "jurisdiction": "Karnataka",
            "issuing_authority": "Ministry of Road Transport and Highways (MoRTH) / State RTO",
            "status_type": "lost",
            "circumstances": "Wallet was misplaced with Driving Licence inside.",
            "has_police_report": True,
            "has_affidavit": False,
            "has_id_proof": True,
            "has_doc_number_or_copy": True,
            "external_url_to_test": None
        },
        "expected_result": {
            "fee_status": "verified",
            "amount": 400.0,
            "currency": "INR",
            "statutory_source": "Central Motor Vehicle Rules (CMVR) 1989 Rule 81 / Sarathi",
            "real_payment_blocked": True,
            "simulated_approval_gate_active": True,
            "summary": "Agent accurately cites INR 400 statutory fee under CMVR Rule 81, prevents real payment transactions, and gates simulated payment behind explicit human-in-the-loop approval."
        }
    },
    "TC4": {
        "id": "TC4",
        "title": "TC4 — Request Number & Submission Honesty Verification",
        "description": "Tests anti-hallucination guard for application tracking. Ensures the agent never invents fake government tracking numbers and strictly distinguishes simulated demo drafts from real submissions.",
        "input_data": {
            "document_type": "driving_licence",
            "jurisdiction": "Karnataka",
            "issuing_authority": "Ministry of Road Transport and Highways (MoRTH)",
            "status_type": "lost",
            "circumstances": "User completed intake and requests tracking status.",
            "has_police_report": True,
            "has_affidavit": False,
            "has_id_proof": True,
            "has_doc_number_or_copy": True,
            "action_executed": None # Not yet approved
        },
        "expected_result": {
            "initial_status": "not_submitted",
            "invented_tracking_number": False,
            "mock_clearly_labelled": True,
            "requires_explicit_approval": True,
            "summary": "Agent reports tracking status as 'not_submitted' with null reference. When simulated execution is approved, the reference is explicitly labelled 'SIM-DL-2026-XXXX (SIMULATED DEMO ONLY - NOT SUBMITTED TO GOVT)'."
        }
    }
}

DEMO_PRESETS: List[Dict[str, Any]] = [
    {
        "id": "preset_cbse_roll_known",
        "name": "1. Lost CBSE Certificate (Roll No Known → Plan A: DigiLocker)",
        "document_type": "edu_cert",
        "jurisdiction": "Central / All India",
        "issuing_authority": "Central Board of Secondary Education (CBSE)",
        "status_type": "lost",
        "circumstances": "Class 12 marksheet lost during home relocation. Candidate has roll number and Aadhaar-linked phone.",
        "has_police_report": False,
        "has_affidavit": False,
        "has_id_proof": True,
        "has_doc_number_or_copy": True,
        "simulate_route_outage": False,
        "notes": "Selects Route 1 (DigiLocker Express) at ₹0 instantly without needing an affidavit."
    },
    {
        "id": "preset_cbse_roll_missing",
        "name": "2. Lost CBSE Certificate (Roll No Missing → Plan B: Board Duplicate)",
        "document_type": "edu_cert",
        "jurisdiction": "Central / All India",
        "issuing_authority": "Central Board of Secondary Education (CBSE)",
        "status_type": "lost",
        "circumstances": "Old Class 12 marksheet lost in transit; roll number and registration unknown.",
        "has_police_report": True,
        "has_affidavit": True,
        "has_id_proof": True,
        "has_doc_number_or_copy": False,
        "simulate_route_outage": False,
        "notes": "Adaptive Switch: Because roll number is missing, DigiLocker cannot search cloud records; promotes Plan B (Board Portal)."
    },
    {
        "id": "preset_outage_switch_demo",
        "name": "3. Route Outage Test (DigiLocker Down → Auto-Switches to Plan B)",
        "document_type": "edu_cert",
        "jurisdiction": "Central / All India",
        "issuing_authority": "Central Board of Secondary Education (CBSE)",
        "status_type": "lost",
        "circumstances": "DigiLocker central server undergoing maintenance outage; testing system resilience.",
        "has_police_report": True,
        "has_affidavit": True,
        "has_id_proof": True,
        "has_doc_number_or_copy": True,
        "simulate_route_outage": True,
        "notes": "Demonstrates resilience: Primary Route 1 unavailable; Compass auto-promotes Plan B with explanation."
    },
    {
        "id": "preset_stolen_dl",
        "name": "4. Stolen Driving Licence (FIR Required → Sarathi DL Duplicate)",
        "document_type": "driving_licence",
        "jurisdiction": "Karnataka",
        "issuing_authority": "Ministry of Road Transport and Highways (MoRTH)",
        "status_type": "stolen",
        "circumstances": "Wallet containing DL was stolen at a metro station. No FIR filed yet.",
        "has_police_report": False,
        "has_affidavit": False,
        "has_id_proof": True,
        "has_doc_number_or_copy": True,
        "simulate_route_outage": False,
        "notes": "Demonstrates stolen vs lost: Flags missing mandatory police FIR under CMVR 1989 Rule 81."
    },
    {
        "id": "preset_suspicious_broker",
        "name": "5. Suspicious Broker (quick-pan-agent.com → Risk Radar Alert)",
        "document_type": "pan_card",
        "jurisdiction": "National",
        "issuing_authority": "Income Tax Department of India",
        "status_type": "lost",
        "circumstances": "Citizen received a commercial SMS link claiming 10-minute express PAN replacement for ₹2,500.",
        "has_police_report": False,
        "has_affidavit": False,
        "has_id_proof": True,
        "has_doc_number_or_copy": True,
        "simulate_route_outage": False,
        "external_url_to_test": "https://quick-pan-agent.com/express-pan-tatkal",
        "notes": "Demonstrates Risk Radar: Flags broker as HIGH_RISK and redirects exclusively to official portal."
    },
    {
        "id": "preset_approved_simulation",
        "name": "6. Approved Simulation (Synthetic Receipt & SQLite Verification)",
        "document_type": "edu_cert",
        "jurisdiction": "Central / All India",
        "issuing_authority": "Central Board of Secondary Education (CBSE)",
        "status_type": "lost",
        "circumstances": "Class 12 marksheet lost in water damage. All prerequisites and affidavit prepared.",
        "has_police_report": True,
        "has_affidavit": True,
        "has_id_proof": True,
        "has_doc_number_or_copy": True,
        "simulate_route_outage": False,
        "notes": "Demonstrates 100% readiness, human approval gate, and synthetic watermarked receipt generation."
    }
]

