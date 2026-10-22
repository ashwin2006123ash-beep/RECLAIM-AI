"""
RECLAIM AI 2.0 - Innovation 2: Counterfactual Recovery Simulator
Provides what-if side-by-side scenario modeling to contrast recovery plans,
readiness scores, prerequisite blockers, and safety warnings across critical civic dimensions.
Clearly distinguishes modeled counterfactual outcomes from verified government policy.
"""
from typing import Dict, Any, List, Optional
import copy
from agent.readiness import calculate_readiness_score
from agent.fee_verifier import verify_document_fee
from agent.adaptive_planner import AdaptiveRecoveryPlanner
from agent.recovery_twin import RecoveryTwinEngine

SIMULATOR_DISCLAIMER = (
    "COUNTERFACTUAL SIMULATION: Modeled what-if outcome generated for comparative analysis. "
    "Statutory requirements reflect applicable Indian legislation (CMVR 1989, IT Act 2000, Passports Act 1967)."
)

COUNTERFACTUAL_SCENARIOS = [
    {
        "id": "scenario_lost_vs_stolen",
        "title": "Lost vs. Stolen Document",
        "description": "Compares an accidental loss against criminal theft. Stolen status strictly mandates a Police First Information Report (FIR) and triggers immediate fraud warnings.",
        "dimension": "status_type",
        "baseline_label": "Accidental Loss (Misplaced)",
        "modeled_label": "Stolen / Theft Condition"
    },
    {
        "id": "scenario_copy_available_vs_missing",
        "title": "Document Number/Copy Available vs. Missing",
        "description": "Compares having a previous registration number or scan vs. possessing zero historical records. Determines whether DigiLocker instant digital retrieval is viable.",
        "dimension": "has_doc_number_or_copy",
        "baseline_label": "Previous Copy / Registration Number Known",
        "modeled_label": "Zero Copy / Number Completely Unknown"
    },
    {
        "id": "scenario_authority_known_vs_unknown",
        "title": "Issuing Authority Known vs. Unknown",
        "description": "Compares a known central board/RTO against an unlisted or autonomous entity. Demonstrates how the agent shifts into clarification mode without hallucinating.",
        "dimension": "issuing_authority",
        "baseline_label": "Verified Issuing Authority (e.g. CBSE / MoRTH)",
        "modeled_label": "Unknown / Unspecified Autonomous Institution"
    },
    {
        "id": "scenario_verified_fee_vs_unverified",
        "title": "Verified Statutory Fee vs. Unverified Fee",
        "description": "Compares gazetted statutory fees against unverified costs, proving that payment simulations are locked whenever fees cannot be independently verified.",
        "dimension": "fee_verification",
        "baseline_label": "Statutory Gazette-Verified Fee",
        "modeled_label": "Unverified Fee (Obscure Issuer)"
    },
    {
        "id": "scenario_complete_vs_incomplete_evidence",
        "title": "Complete vs. Incomplete Supporting Evidence",
        "description": "Compares a fully documented case (FIR + Affidavit + ID Proof + Copy) against a case with zero documentation, showing dynamic twin unblocking.",
        "dimension": "evidence_completeness",
        "baseline_label": "Full Documentation Prepared",
        "modeled_label": "Zero Documentation Prepared"
    }
]

class CounterfactualSimulator:
    """
    Simulates counterfactual civic recovery paths and computes deltas in
    readiness, required evidence, route viability, blocked twin nodes, and next actions.
    """

    @classmethod
    def get_supported_scenarios(cls) -> List[Dict[str, Any]]:
        return COUNTERFACTUAL_SCENARIOS

    @classmethod
    def run_simulation(cls, base_case: Dict[str, Any], scenario_id: str) -> Dict[str, Any]:
        """
        Runs a comparative simulation between the base case and the chosen counterfactual scenario.
        """
        scenario_meta = next((s for s in COUNTERFACTUAL_SCENARIOS if s["id"] == scenario_id), None)
        if not scenario_meta:
            scenario_meta = COUNTERFACTUAL_SCENARIOS[0]
            scenario_id = scenario_meta["id"]

        # Deep copies for baseline and modeled cases
        baseline = copy.deepcopy(base_case)
        modeled = copy.deepcopy(base_case)

        # Apply counterfactual mutations
        if scenario_id == "scenario_lost_vs_stolen":
            baseline["status_type"] = "lost"
            modeled["status_type"] = "stolen"
            modeled["has_police_report"] = False  # Stolen without report highlights the blocker!

        elif scenario_id == "scenario_copy_available_vs_missing":
            baseline["has_doc_number_or_copy"] = True
            modeled["has_doc_number_or_copy"] = False

        elif scenario_id == "scenario_authority_known_vs_unknown":
            if not baseline.get("issuing_authority") or baseline.get("issuing_authority").lower() in ["unknown", "unknown autonomous college"]:
                baseline["issuing_authority"] = "Central Board of Secondary Education (CBSE)"
                baseline["jurisdiction"] = "Central / All India"
            modeled["issuing_authority"] = "Unknown Autonomous College"
            modeled["jurisdiction"] = "Unknown State"

        elif scenario_id == "scenario_verified_fee_vs_unverified":
            baseline["document_type"] = "driving_licence"
            baseline["issuing_authority"] = "Ministry of Road Transport and Highways (MoRTH)"
            modeled["document_type"] = "other_cert"
            modeled["issuing_authority"] = "Private Autonomous Training Institute"

        elif scenario_id == "scenario_complete_vs_incomplete_evidence":
            baseline["has_police_report"] = True
            baseline["has_affidavit"] = True
            baseline["has_id_proof"] = True
            baseline["has_doc_number_or_copy"] = True

            modeled["has_police_report"] = False
            modeled["has_affidavit"] = False
            modeled["has_id_proof"] = False
            modeled["has_doc_number_or_copy"] = False

        # Evaluate both states
        baseline_eval = cls._evaluate_case_state(baseline)
        modeled_eval = cls._evaluate_case_state(modeled)

        # Calculate deltas
        score_delta = modeled_eval["readiness_score"] - baseline_eval["readiness_score"]
        blocker_diff = list(set(modeled_eval["blocked_nodes"]) - set(baseline_eval["blocked_nodes"]))
        new_requirements = list(set(modeled_eval["mandatory_requirements"]) - set(baseline_eval["mandatory_requirements"]))

        key_takeaway = cls._generate_takeaway(scenario_id, baseline_eval, modeled_eval)

        return {
            "status": "success",
            "scenario_id": scenario_id,
            "scenario_title": scenario_meta["title"],
            "scenario_description": scenario_meta["description"],
            "statutory_disclaimer": SIMULATOR_DISCLAIMER,
            "baseline": {
                "label": scenario_meta["baseline_label"],
                "data": baseline,
                "readiness_score": baseline_eval["readiness_score"],
                "readiness_band": baseline_eval["readiness_band"],
                "fee_status": baseline_eval["fee_status"],
                "fee_amount": baseline_eval["fee_amount"],
                "recommended_route": baseline_eval["recommended_route"],
                "digilocker_viable": baseline_eval["digilocker_viable"],
                "blocked_nodes": baseline_eval["blocked_nodes"],
                "mandatory_requirements": baseline_eval["mandatory_requirements"],
                "next_action": baseline_eval["next_action"]
            },
            "modeled": {
                "label": scenario_meta["modeled_label"],
                "data": modeled,
                "readiness_score": modeled_eval["readiness_score"],
                "readiness_band": modeled_eval["readiness_band"],
                "fee_status": modeled_eval["fee_status"],
                "fee_amount": modeled_eval["fee_amount"],
                "recommended_route": modeled_eval["recommended_route"],
                "digilocker_viable": modeled_eval["digilocker_viable"],
                "blocked_nodes": modeled_eval["blocked_nodes"],
                "mandatory_requirements": modeled_eval["mandatory_requirements"],
                "next_action": modeled_eval["next_action"]
            },
            "comparative_deltas": {
                "readiness_score_delta": score_delta,
                "readiness_trend": "IMPROVED" if score_delta > 0 else ("DECREASED" if score_delta < 0 else "UNCHANGED"),
                "new_blocked_nodes": blocker_diff,
                "new_mandatory_requirements": new_requirements,
                "route_shifted": baseline_eval["recommended_route"] != modeled_eval["recommended_route"],
                "key_takeaway": key_takeaway
            }
        }

    @classmethod
    def _evaluate_case_state(cls, case: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates readiness, route viability, fees, and twin graph for a given case payload."""
        readiness = calculate_readiness_score(case)
        doc_type = case.get("document_type", "edu_cert")
        authority = case.get("issuing_authority", "")
        status_type = case.get("status_type", "lost")
        has_doc_number = bool(case.get("has_doc_number_or_copy"))
        has_police = bool(case.get("has_police_report"))
        has_affidavit = bool(case.get("has_affidavit"))
        has_id = bool(case.get("has_id_proof"))

        fee_info = verify_document_fee(doc_type, authority)
        twin = RecoveryTwinEngine.build_or_update_twin("COUNTERFACTUAL_TEMP", case)
        nodes = twin["dependency_graph"]["nodes"]
        blocked_nodes = [nid for nid, n in nodes.items() if n["state"] in ["BLOCKED", "NEEDS_VERIFICATION"]]

        # Routes comparison
        routes = AdaptiveRecoveryPlanner.evaluate_and_compare_routes(case, readiness)
        rec_route = routes["recommended_route"]["name"] if routes.get("recommended_route") else "None (Pending Clarification)"
        all_routes = routes.get("all_routes", [])
        digilocker_route = next((r for r in all_routes if "DIGILOCKER" in r.get("route_id", "")), None)
        digilocker_viable = bool(digilocker_route and digilocker_route.get("status") == "FEASIBLE" and has_doc_number)

        # Mandatory requirements
        reqs = []
        if status_type == "stolen" or doc_type in ["driving_licence", "passport"]:
            reqs.append("Police FIR / Lost Document Entry (Mandatory)")
        if doc_type in ["edu_cert", "passport", "other_cert"]:
            reqs.append("Notarized Loss Affidavit on Stamp Paper")
        reqs.append("Valid Government Photo Identity Proof")
        if not has_doc_number:
            reqs.append("Previous Document Number or Archive Search")

        return {
            "readiness_score": readiness["score"],
            "readiness_band": readiness.get("readiness_level", "Moderate"),
            "fee_status": fee_info.get("status", "not_verified"),
            "fee_amount": fee_info.get("amount"),
            "recommended_route": rec_route,
            "digilocker_viable": digilocker_viable,
            "blocked_nodes": blocked_nodes,
            "mandatory_requirements": reqs,
            "next_action": twin.get("next_best_action", "Review recovery guidance")
        }

    @classmethod
    def _generate_takeaway(cls, scenario_id: str, b: Dict[str, Any], m: Dict[str, Any]) -> str:
        if scenario_id == "scenario_lost_vs_stolen":
            return (
                "When a document is stolen rather than misplaced, statutory rules strictly require a formal Police FIR/DDR. "
                "The recovery twin halts application progression at the evidence stage until the police report reference is declared, "
                "preventing identity fraud and unauthorized duplicate claims."
            )
        elif scenario_id == "scenario_copy_available_vs_missing":
            if b["digilocker_viable"] and not m["digilocker_viable"]:
                return (
                    "Losing your document number or copy eliminates the instant 0-minute DigiLocker pull. "
                    "The agent dynamically routes the user to the physical/statutory portal duplicate process, "
                    "which requires affidavit notarization and authority archive lookups."
                )
            return "Document copy presence enables instant digital recovery and increases citizen readiness."
        elif scenario_id == "scenario_authority_known_vs_unknown":
            return (
                "When the issuing authority is unknown, the agent never hallucinates forms or fees. "
                "Instead, it halts at Node 1 (IDENTIFY_AUTHORITY), locks fee calculations, and issues targeted "
                "follow-up questions to identify the statutory board or university."
            )
        elif scenario_id == "scenario_verified_fee_vs_unverified":
            return (
                "For gazetted statutory fees (e.g. CMVR Rule 81 ₹400 for DL), fee breakdowns are transparent and verified. "
                "For unverified issuers, payment simulations are strictly locked behind human review with zero fee fabrication."
            )
        elif scenario_id == "scenario_complete_vs_incomplete_evidence":
            return (
                f"Full documentation yields a readiness score of {b['readiness_score']}%, unblocking the entire dependency pipeline. "
                f"Without evidence, readiness drops to {m['readiness_score']}%, providing an ordered checklist of exactly what to obtain next."
            )
        return "Counterfactual analysis illustrates agent pipeline adaptability across legal circumstances."
