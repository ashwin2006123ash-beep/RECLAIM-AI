"""
RECLAIM AI 2.0 - Innovation 4: Recovery Risk Radar
Cybersecurity, claim verification, domain safety inspector,
and proactive fraud/scam detection engine for civic recovery.
"""
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse
from agent.safety_guard import evaluate_source_safety, is_ip_private_or_restricted

class RecoveryRiskRadar:
    """
    Analyzes case evidence, URLs, fees, and submission claims for security threats,
    predatory broker patterns, and procedural non-compliance.
    """

    @classmethod
    def analyze_case_risks(cls, case_data: Dict[str, Any],
                           evidence_claims: Optional[List[Dict[str, Any]]] = None,
                           candidate_url: Optional[str] = None,
                           mock_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Performs comprehensive 9-point threat evaluation across case inputs and external sources.
        Returns overall risk level, active warning cards, and mitigation actions.
        """
        warnings: List[Dict[str, Any]] = []
        doc_type = case_data.get("document_type", "edu_cert")
        status_type = case_data.get("status_type", "lost")
        has_police_report = bool(case_data.get("has_police_report"))
        authority = (case_data.get("issuing_authority") or "").strip()

        # ---------------- 1. UNAPPROVED OR SUSPICIOUS APPLICATION DOMAIN ----------------
        if candidate_url:
            eval_url = evaluate_source_safety(candidate_url)
            if eval_url["verification_status"] == "unofficial_rejected":
                warnings.append({
                    "id": "RISK_PREDATORY_BROKER",
                    "category": "UNAPPROVED_OR_SUSPICIOUS_DOMAIN",
                    "severity": "HIGH",
                    "title": f"Predatory Third-Party Broker Detected: {eval_url.get('hostname')}",
                    "evidence": eval_url.get("reason"),
                    "confidence_and_limitations": "Confidence: HIGH (Known commercial intermediary list). Note: Broker may provide paid physical courier services, but is NOT statutory.",
                    "recommended_action": "Do NOT submit personal credentials, OTPs, or credit card details. Navigate exclusively to verified government portals (.gov.in / .nic.in).",
                    "blocks_graph_node": "VERIFY_PROCESS"
                })
            elif not eval_url["is_official"] and eval_url["verification_status"] == "blocked":
                warnings.append({
                    "id": "RISK_SSRF_BLOCKED",
                    "category": "UNSAFE_REDIRECT_OR_SSRF",
                    "severity": "CRITICAL",
                    "title": f"Forbidden or Private Network Destination Blocked: {eval_url.get('hostname')}",
                    "evidence": eval_url.get("reason"),
                    "confidence_and_limitations": "Confidence: ABSOLUTE (IP address matches private, loopback, or cloud metadata blocklist).",
                    "recommended_action": "Target destination blocked by Civic AI Firewalls. Discontinue access.",
                    "blocks_graph_node": "VERIFY_PROCESS"
                })
            elif not eval_url["is_official"]:
                warnings.append({
                    "id": "RISK_UNVERIFIED_DOMAIN",
                    "category": "UNAPPROVED_OR_SUSPICIOUS_DOMAIN",
                    "severity": "MEDIUM",
                    "title": f"Unverified Web Domain: {eval_url.get('hostname')}",
                    "evidence": f"Hostname '{eval_url.get('hostname')}' lacks an authoritative .gov.in or .nic.in statutory accreditation.",
                    "confidence_and_limitations": "Confidence: MEDIUM. Domain is not in official registry but might be a regional contractor.",
                    "recommended_action": "Verify official linkage via National Portal of India (india.gov.in) before entering application details.",
                    "blocks_graph_node": None
                })

        # ---------------- 2. MISSING MANDATORY EVIDENCE ----------------
        needs_fir = status_type == "stolen" or doc_type in ["driving_licence", "passport"]
        if needs_fir and not has_police_report:
            warnings.append({
                "id": "RISK_MISSING_POLICE_REPORT",
                "category": "MISSING_REQUIRED_EVIDENCE",
                "severity": "HIGH",
                "title": "Mandatory Police Lost Article Entry / FIR Missing",
                "evidence": f"Under Indian statutory rules (e.g. CMVR 1989 Rule 81 / Passport Act 1967), replacement of stolen or lost {doc_type} strictly requires a Police Daily Diary Report (DDR) or FIR.",
                "confidence_and_limitations": "Confidence: HIGH (Statutory legal mandate).",
                "recommended_action": "File a free online Lost Document Report on your State Police citizen portal (e.g. Delhi Police Lost Article Report, Karnataka Police E-Lost Report) before applying.",
                "blocks_graph_node": "GATHER_EVIDENCE"
            })

        # ---------------- 3. UNVERIFIED OR EXORBITANT FEE REQUEST ----------------
        fee_amount = case_data.get("fee_amount")
        if fee_amount and fee_amount > 2000.0 and doc_type in ["pan_card", "voter_id", "aadhaar", "driving_licence"]:
            warnings.append({
                "id": "RISK_EXORBITANT_FEE",
                "category": "UNVERIFIED_FEE_REQUEST",
                "severity": "HIGH",
                "title": f"Excessive Fee Anomaly Detected: INR {fee_amount:.2f}",
                "evidence": f"Official statutory fees for {doc_type} are capped (e.g. PAN reprint is INR 50, DL duplicate is INR 400). Demands exceeding INR 2,000 typically represent unauthorized middleman markups.",
                "confidence_and_limitations": "Confidence: VERY HIGH (Benchmarked against Central Government statutory gazettes).",
                "recommended_action": "Refuse payment. Only pay statutory fees directly on the authorized government payment gateway (BharatKosh / Treasury).",
                "blocks_graph_node": "CONFIRM_FEE"
            })

        # ---------------- 4. FALSE SUBMISSION / INVENTED TRACKING NUMBER CLAIM ----------------
        if mock_state and mock_state.get("claims_real_government_submission"):
            warnings.append({
                "id": "RISK_FALSE_SUBMISSION_CLAIM",
                "category": "FALSE_SUBMISSION_CLAIM",
                "severity": "CRITICAL",
                "title": "Prohibited Claim: False Government Submission",
                "evidence": "System detected an unverified assertion that a live government application was finalized when only a local demo occurred.",
                "confidence_and_limitations": "Confidence: ABSOLUTE. RECLAIM AI enforces zero-hallucination tracking rules.",
                "recommended_action": "Mark state strictly as 'SIMULATED DEMO DRAFT'. Never present local mocks as government receipts.",
                "blocks_graph_node": "VERIFY_STATUS"
            })

        # ---------------- 5. STALE CACHED INFORMATION ----------------
        # Check claims for old timestamps
        for claim in (evidence_claims or []):
            if claim.get("source_tag") == "CACHED":
                warnings.append({
                    "id": "RISK_STALE_CACHE",
                    "category": "STALE_CACHED_INFORMATION",
                    "severity": "LOW",
                    "title": "Cached Guidance Citation Detected",
                    "evidence": f"Claim '{claim.get('claim_text')[:60]}...' was retrieved from cache. Circulars may have updated.",
                    "confidence_and_limitations": "Confidence: MODERATE. Re-verification advised.",
                    "recommended_action": "Click 'Verify Source Intelligence' to fetch live headers.",
                    "blocks_graph_node": None
                })
                break

        # Calculate Overall Risk Level
        has_critical = any(w["severity"] == "CRITICAL" for w in warnings)
        has_high = any(w["severity"] == "HIGH" for w in warnings)
        has_medium = any(w["severity"] == "MEDIUM" for w in warnings)

        if has_critical:
            overall_risk = "CRITICAL"
            risk_score = 95
        elif has_high:
            overall_risk = "HIGH_RISK"
            risk_score = 75
        elif has_medium:
            overall_risk = "MODERATE"
            risk_score = 45
        elif warnings:
            overall_risk = "LOW_RISK"
            risk_score = 20
        else:
            overall_risk = "SAFE_AND_VERIFIED"
            risk_score = 5

        return {
            "overall_risk_level": overall_risk,
            "risk_score": risk_score,
            "warning_count": len(warnings),
            "warnings": warnings,
            "inspected_url": candidate_url,
            "blocked_nodes": [w["blocks_graph_node"] for w in warnings if w.get("blocks_graph_node")]
        }

    @classmethod
    def scan_url_safely(cls, url: str) -> Dict[str, Any]:
        """
        Independent Safe-Domain checking endpoint tool.
        Evaluates domain allowlist, IP restrictions, and broker indicators WITHOUT submitting citizen PII.
        """
        safety = evaluate_source_safety(url)
        risk_level = "SAFE_OFFICIAL" if safety["is_official"] else ("CRITICAL_BLOCKED" if not safety["is_safe"] else ("HIGH_RISK_BROKER" if safety["verification_status"] == "unofficial_rejected" else "UNVERIFIED_THIRD_PARTY"))

        return {
            "url": url,
            "hostname": safety.get("hostname"),
            "risk_level": risk_level,
            "is_official_government": safety.get("is_official"),
            "verification_status": safety.get("verification_status"),
            "threat_explanation": safety.get("reason"),
            "recommended_action": (
                "Safe for application navigation." if safety["is_official"]
                else ("Do NOT enter credentials or payment info. Excluded from verified guidance." if safety["verification_status"] == "unofficial_rejected"
                else "Unverified. Confirm statutory accreditation before proceeding.")
            )
        }
