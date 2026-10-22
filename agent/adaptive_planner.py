"""
RECLAIM AI 2.0 - Innovation 3: Adaptive Recovery Planner
Explainable Multi-Route Decision Engine with transparent route trade-offs,
comparative feasibility scoring, and an explicit 'Why did the agent choose this?' matrix.
"""
from typing import Dict, Any, List, Optional
from agent.source_registry import lookup_sources
from agent.fee_verifier import verify_document_fee

class AdaptiveRecoveryPlanner:
    """
    Evaluates available case evidence and generates comparative recovery routes:
    - Route A: Instant Digital Credential (DigiLocker)
    - Route B: Statutory Online Reissue Portal (Parivahan / CBSE / NSDL)
    - Route C: Administrative Counter / In-Person Facilitation Center
    """

    @classmethod
    def evaluate_and_compare_routes(cls, case_data: Dict[str, Any],
                                   readiness_data: Dict[str, Any],
                                   risk_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Synthesizes feasible recovery routes, determines the optimal recommendation,
        and provides an auditable decision justification matrix.
        """
        doc_type = case_data.get("document_type", "edu_cert")
        authority = (case_data.get("issuing_authority") or "").strip()
        jurisdiction = (case_data.get("jurisdiction") or "").strip()
        status_type = case_data.get("status_type", "lost")
        has_police_report = bool(case_data.get("has_police_report"))
        has_affidavit = bool(case_data.get("has_affidavit"))
        has_id_proof = bool(case_data.get("has_id_proof"))
        has_doc_number = bool(case_data.get("has_doc_number_or_copy"))

        fee_info = verify_document_fee(doc_type, authority)
        readiness_score = readiness_data.get("score", 0)

        routes: List[Dict[str, Any]] = []

        primary_route_available = case_data.get("primary_route_available", True)
        if case_data.get("simulate_route_outage"):
            primary_route_available = False
        preferred_route = case_data.get("preferred_route")

        # ================= ROUTE 1: INSTANT DIGITAL CREDENTIAL (DIGILOCKER) =================
        digilocker_supported = doc_type in ["edu_cert", "driving_licence", "pan_card", "voter_id", "aadhaar"]
        digilocker_prereqs = ["Aadhaar-linked mobile number for OTP"]
        if not has_doc_number:
            digilocker_prereqs.append("Approximate registration / roll number / year of issue")

        r1_feasible = digilocker_supported and authority.lower() not in ["unknown", "unknown autonomous college"] and primary_route_available
        if not primary_route_available:
            r1_score = 15
            r1_status = "TEMPORARILY_UNAVAILABLE"
            r1_deferral = "Primary digital repository is experiencing simulated downtime or maintenance. Adaptive Recovery Compass has promoted Plan B."
        elif not r1_feasible:
            r1_score = 20
            r1_status = "NOT_AVAILABLE_FOR_CATEGORY"
            r1_deferral = "Issuing authority is unlisted or document category is not integrated with DigiLocker."
        elif not has_doc_number:
            r1_score = 55
            r1_status = "FEASIBLE"
            r1_deferral = "Requires exact roll/registration number to query MeitY database."
        else:
            r1_score = 90
            r1_status = "FEASIBLE"
            r1_deferral = None

        route_1 = {
            "route_id": "ROUTE_DIGITAL_DIGILOCKER",
            "name": "Route 1: Instant Legal Digital Credential (DigiLocker)",
            "channel": "Electronic / Self-Service Cloud Repository",
            "statutory_basis": "Information Technology (Preservation and Retention of Information by Intermediaries Providing Digital Locker Facilities) Rules, 2016 (Rule 9A)",
            "legal_validity": "Legally equivalent to original physical certificate under Section 9A of IT Act 2000.",
            "statutory_fee": {
                "amount": 0.0,
                "currency": "INR",
                "status": "verified",
                "condition": "Free of cost public digital credential pull."
            },
            "prerequisites": digilocker_prereqs,
            "advantages": [
                "Immediate retrieval (zero courier delay)",
                "No statutory fee (100% free of cost)",
                "Does not require notarized stamp-paper affidavit or police DDR for simple digital pull"
            ],
            "limitations": [
                "Requires linked mobile number for Aadhaar OTP authentication",
                "Provides digital PDF / XML credential, not a physical embossed card/mark sheet",
                "Requires authentic roll or document number to locate the issuer record"
            ],
            "feasibility_score": r1_score,
            "status": r1_status,
            "deferral_reason": r1_deferral
        }
        routes.append(route_1)

        # ================= ROUTE 2: STATUTORY ONLINE REISSUE PORTAL =================
        sources = lookup_sources(doc_type, jurisdiction)
        primary_source = sources[0] if sources else None
        portal_name = primary_source.get("issuing_authority") if primary_source else "Central Statutory Portal"
        portal_url = primary_source.get("official_url") if primary_source else None

        needs_fir = status_type == "stolen" or doc_type in ["driving_licence", "passport"]
        needs_affidavit = doc_type in ["edu_cert", "passport", "other_cert"]

        r2_prereqs = ["Valid Identity & Address Proof"]
        if needs_fir and not has_police_report:
            r2_prereqs.append("Mandatory Police Lost Document Entry (DDR/NCR/FIR)")
        if needs_affidavit and not has_affidavit:
            r2_prereqs.append("Notarized Loss Affidavit on non-judicial stamp paper")
        if not has_doc_number:
            r2_prereqs.append("Previous document registration / roll number / card number")

        r2_feasible = bool(portal_url) and authority.lower() not in ["unknown", "unknown autonomous college"]
        r2_score = 85 if (r2_feasible and has_police_report and (has_affidavit or not needs_affidavit)) else (50 if r2_feasible else 10)

        route_2 = {
            "route_id": "ROUTE_OFFICIAL_ONLINE_PORTAL",
            "name": f"Route 2: Statutory Online Reissue Portal ({portal_name})",
            "channel": "Official Government Web Gateway & Speed Post Delivery",
            "statutory_basis": primary_source.get("information_available", "Statutory Citizen Service Guidelines") if primary_source else "Statutory Citizen Service Guidelines",
            "legal_validity": "Issues an authentic replacement physical duplicate / smart card directly from the statutory issuer.",
            "statutory_fee": {
                "amount": fee_info.get("amount"),
                "currency": fee_info.get("currency", "INR"),
                "status": fee_info.get("status", "not_verified"),
                "condition": fee_info.get("condition", "Official gazette fee schedule")
            },
            "prerequisites": r2_prereqs,
            "advantages": [
                "Delivers authentic physical duplicate document via Speed Post",
                "Includes official QR code, hologram, or watermarked security paper",
                "Direct government tracking reference provided"
            ],
            "limitations": [
                "Requires mandatory evidentiary prerequisites (Police DDR / Notarized Affidavit)",
                "Standard government postal dispatch turnaround (7 to 21 working days)",
                "Statutory fee applicable"
            ],
            "feasibility_score": r2_score,
            "status": "FEASIBLE" if r2_feasible else "BLOCKED_PENDING_AUTHORITY",
            "deferral_reason": None if r2_feasible else "Authority or official online reissue gateway is unverified."
        }
        routes.append(route_2)

        # ================= ROUTE 3: IN-PERSON FACILITATION / RTO / REGISTRAR COUNTER =================
        route_3 = {
            "route_id": "ROUTE_IN_PERSON_COUNTER",
            "name": "Route 3: In-Person Facilitation Center / Administrative Counter",
            "channel": "Physical Office Submission (RTO Counter / University Examination Branch / Seva Kendra)",
            "statutory_basis": "Citizen Charter & Offline Administrative Reissue Procedures",
            "legal_validity": "Hand-delivered duplicate document upon manual biometric or file verification.",
            "statutory_fee": {
                "amount": fee_info.get("amount"),
                "currency": fee_info.get("currency", "INR"),
                "status": fee_info.get("status", "not_verified"),
                "condition": "Paid via treasury challan, demand draft, or cash counter."
            },
            "prerequisites": [
                "Physical printout of application form with passport photographs",
                "Original police lost report and original notarized stamp affidavit",
                "Self-attested photocopies of identity proofs"
            ],
            "advantages": [
                "Essential fallback when biometric mismatch, Aadhaar OTP failure, or record spelling discrepancy occurs",
                "Enables direct inquiry with the Public Information Officer or Assistant Registrar"
            ],
            "limitations": [
                "Requires in-person visit during official working hours",
                "Manual queuing and physical treasury challan generation",
                "Higher citizen effort and transit cost"
            ],
            "feasibility_score": 45,
            "status": "FALLBACK_ROUTE",
            "deferral_reason": "Online routes offer lower friction and transparent tracking without physical transit."
        }
        routes.append(route_3)

        # ================= DECISION LOGIC: SELECT RECOMMENDED ROUTE =================
        adaptive_switch_reason = None

        if not authority or authority.lower() in ["unknown", "unknown autonomous college"]:
            recommended = None
            decision_summary = "Decision engine paused: Issuing authority is unknown. Reissue bylaws and fee schedules cannot be determined without authority clarification."
            why_chosen = [
                {"rule": "Authority Rule", "justification": "Reissue procedures are statutory; different universities and boards have distinct bylaws."},
                {"rule": "Safety Guard", "justification": "Refusing to recommend an arbitrary portal prevents misleading the citizen."}
            ]
        elif preferred_route == "ROUTE_OFFICIAL_ONLINE_PORTAL":
            recommended = route_2
            adaptive_switch_reason = "Citizen switched route: Selected official statutory portal for physical dispatch."
            decision_summary = f"Recommended: {route_2['name']} based on user preference for physical document dispatch."
            why_chosen = [
                {"rule": "User Preference Override", "justification": "User selected physical duplicate reissue over digital retrieval."},
                {"rule": "Official Source Rule", "justification": f"Verified portal ({portal_name}) confirmed in authoritative registry."}
            ]
        elif preferred_route == "ROUTE_IN_PERSON_COUNTER":
            recommended = route_3
            adaptive_switch_reason = "Citizen switched route: Selected in-person administrative counter submission."
            decision_summary = f"Recommended: {route_3['name']} for physical counter submission."
            why_chosen = [
                {"rule": "User Preference Override", "justification": "User requested in-person facilitation counter."}
            ]
        elif not primary_route_available:
            # Route 1 is down -> auto adapt to Route 2 (or Route 3)
            recommended = route_2 if r2_feasible else route_3
            adaptive_switch_reason = "Primary Route (DigiLocker) is currently unavailable. Adaptive Compass automatically routed to Plan B (Official Statutory Portal)."
            decision_summary = f"Adaptive Switch Active: {recommended['name']} recommended because primary digital route is unavailable."
            why_chosen = [
                {"rule": "Adaptive Resiliency Rule", "justification": "Primary digital service outage detected; automatically redirected to statutory online/offline reissue portal."},
                {"rule": "Continuity Rule", "justification": "Ensures citizen recovery workflow is unblocked without waiting for service restoration."}
            ]
        elif not has_doc_number and doc_type in ["edu_cert", "driving_licence"]:
            # Missing roll / document number makes DigiLocker difficult
            recommended = route_2
            adaptive_switch_reason = "Roll/Registration number is missing. DigiLocker cannot search cloud records without a roll number; recommending Board / RTO duplicate application (Plan B)."
            decision_summary = f"Recommended: {route_2['name']} because previous document number/copy is unavailable for automated cloud pull."
            why_chosen = [
                {"rule": "Identifier Verification Rule", "justification": "Automated digital repositories require registration or roll numbers to query candidate records."},
                {"rule": "Plan B Reissue Rule", "justification": f"Statutory portal ({portal_name}) allows historical archive search using candidate name, school/college code, and year."}
            ]
        elif readiness_score >= 70 and has_police_report and (has_affidavit or not needs_affidavit):
            recommended = route_2
            decision_summary = (
                f"Recommended: {route_2['name']} for official physical replacement. "
                "The applicant possesses complete prerequisite documentation (Police DDR and identity proof), "
                "allowing direct official filing."
            )
            why_chosen = [
                {"rule": "Readiness Completeness Rule", "justification": f"Citizen has achieved {readiness_score}/100 readiness score; mandatory statutory prerequisites are fulfilled."},
                {"rule": "Official Source Rule", "justification": f"Verified portal ({portal_name}) is registered in authoritative registry with confirmed fee schedule."},
                {"rule": "Physical Document Requirement", "justification": "Citizen declared lost/stolen physical credential; official portal provides authentic re-embossed replacement."}
            ]
        elif digilocker_supported and r1_feasible:
            recommended = route_1
            decision_summary = (
                f"Recommended: {route_1['name']} as the immediate zero-cost primary path. "
                "Physical portal reissue is temporarily deferred until missing prerequisites (Police Report / Affidavit) are obtained."
            )
            why_chosen = [
                {"rule": "Zero-Cost Immediate Access Rule", "justification": "DigiLocker delivers an instant legally valid digital credential under Section 9A of IT Act 2000 at zero cost."},
                {"rule": "Prerequisite Optimization Rule", "justification": "Applicant lacks police loss report or affidavit for physical reissue; digital route unblocks citizen immediately while paperwork is assembled."}
            ]
        else:
            recommended = route_2
            decision_summary = f"Recommended: {route_2['name']} as primary statutory path."
            why_chosen = [
                {"rule": "Statutory Authority Rule", "justification": f"Direct submission via {portal_name} is the standard statutory mechanism."}
            ]

        # Alternative routes
        alternatives = [r for r in routes if recommended and r["route_id"] != recommended["route_id"] and r["status"] == "FEASIBLE"]
        if not alternatives and routes:
            alternatives = [r for r in routes if recommended and r["route_id"] != recommended["route_id"]]

        # Explicit Plan B and Plan C
        plan_b = alternatives[0] if len(alternatives) > 0 else None
        plan_c = alternatives[1] if len(alternatives) > 1 else (route_3 if recommended != route_3 else None)

        return {
            "recommended_route": recommended,
            "alternative_routes": alternatives,
            "plan_b": plan_b,
            "plan_c": plan_c,
            "adaptive_switch_reason": adaptive_switch_reason,
            "primary_route_available": primary_route_available,
            "all_routes": routes,
            "decision_summary": decision_summary,
            "why_chosen_matrix": why_chosen,
            "is_blocked_by_missing_authority": not bool(authority) or authority.lower() in ["unknown", "unknown autonomous college"],
            "statutory_evidence_basis": fee_info.get("source_title", "Central Source Registry")
        }
