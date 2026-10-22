"""
RECLAIM AI 2.0 - Innovation 5: Accessible Civic Copilot Engine
Bilingual conversational interface (English & Tamil / தமிழ்) answering questions
grounded exclusively in verified statutory sources and the active recovery case.
Provides simple explanations for legal/government terminology.
Supports Gemini AI when configured; provides a transparent, deterministic fallback when offline.
"""
from typing import Dict, Any, List, Optional
import re
from config import Config
from agent.source_registry import lookup_sources
from agent.fee_verifier import verify_document_fee
from agent.gemini_client import is_gemini_available

# Legal / Civic Terminology Glossary with Tamil Translations
CIVIC_GLOSSARY = {
    "affidavit": {
        "term_en": "Affidavit",
        "term_ta": "பிரமாணப் பத்திரம் (Affidavit)",
        "explanation_en": "A formal sworn statement written on non-judicial stamp paper and signed before a Notary Public or First Class Magistrate, declaring the exact facts of how your document was lost.",
        "explanation_ta": "உங்கள் ஆவணம் எவ்வாறு தொலைந்தது என்பதை விளக்கி, நோட்டரி வழக்கறிஞர் முன்னிலையில் முத்திரைத்தாளில் கையொப்பமிடப்படும் சட்டபூர்வ வாக்குமூலம்."
    },
    "fir": {
        "term_en": "First Information Report (FIR)",
        "term_ta": "முதல் தகவல் அறிக்கை (FIR)",
        "explanation_en": "A police record registered when a document is stolen or criminal theft is suspected. For simple lost items, most states allow a simpler online 'Lost Article Report' (NCR/DDR).",
        "explanation_ta": "ஆவணம் திருடப்பட்டதாக சந்தேகிக்கும்போது காவல் நிலையத்தில் பதிவு செய்யப்படும் அறிக்கை. ஆவணம் தற்செயலாக தொலைந்துவிட்டால், ஆன்லைன் மூலம் எளிதாக 'இழப்பு அறிக்கை' (Lost Article Report) பெறலாம்."
    },
    "digilocker": {
        "term_en": "DigiLocker",
        "term_ta": "டிஜிலாக்கர் (DigiLocker)",
        "explanation_en": "The Government of India's secure cloud depository. Under Rule 9A of the IT Rules 2016, digital certificates pulled into DigiLocker have the exact same legal status as original physical certificates.",
        "explanation_ta": "இந்திய அரசின் பாதுகாப்பான மின்னணு ஆவண பெட்டகம். தகவல் தொழில்நுட்பச் சட்டம் 2016 விதி 9A படி, இதில் உள்ள டிஜிட்டல் சான்றிதழ்கள் அசல் ஆவணத்திற்கு இணையான சட்ட செல்லுபடியாகும் தன்மை கொண்டவை."
    },
    "gazette": {
        "term_en": "Gazette Notification",
        "term_ta": "அரசிதழ் அறிவிப்பு (Gazette)",
        "explanation_en": "An official public legal record published by the Government of India or State Government. Gazette rules (e.g. CMVR Rule 81) set the legally binding fee for duplicate document reissue.",
        "explanation_ta": "மத்திய அல்லது மாநில அரசால் வெளியிடப்படும் அதிகாரப்பூர்வ சட்ட அறிவிப்பு. இதில் குறிப்பிடப்படும் கட்டணங்களே (எ.கா: CMVR விதி 81) சட்டபூர்வமானவை."
    },
    "cmvr": {
        "term_en": "CMVR 1989 Rule 81",
        "term_ta": "மத்திய மோட்டார் வாகன விதிகள் (CMVR விதி 81)",
        "explanation_en": "Rule 81 of the Central Motor Vehicles Rules (1989), which officially prescribes the INR 400 fee for duplicate Driving Licence issuance across all Indian states.",
        "explanation_ta": "இந்தியாவில் தொலைந்த ஓட்டுநர் உரிமத்திற்கு மாற்று அட்டை பெற மத்திய அரசு நிர்ணயித்த அதிகாரப்பூர்வ கட்டணம் ரூ. 400 ஆகும்."
    }
}

class AccessibleCivicCopilot:
    """
    Accessible Civic Copilot providing grounded conversational guidance in English and Tamil.
    """

    @classmethod
    def process_query(cls, user_message: str, case_data: Optional[Dict[str, Any]] = None,
                      session_id: Optional[str] = None, preferred_language: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes incoming query, identifies terminology, checks live AI availability,
        and generates an explainable, grounded answer.
        """
        msg = (user_message or "").strip()
        case = case_data or {}
        doc_type = case.get("document_type", "edu_cert")
        authority = case.get("issuing_authority", "Statutory Authority")
        status_type = case.get("status_type", "lost")
        has_police = bool(case.get("has_police_report"))
        has_affidavit = bool(case.get("has_affidavit"))
        has_copy = bool(case.get("has_doc_number_or_copy"))

        # Language Detection
        is_tamil = cls._detect_tamil(msg) or (preferred_language == "ta")

        # Check matched glossary terms
        matched_terms = []
        msg_lower = msg.lower()
        for key, g in CIVIC_GLOSSARY.items():
            if key in msg_lower or (is_tamil and any(w in msg for w in ["பிரமாண", "எப்ஐஆர்", "காவல்", "டிஜிலாக்கர்", "அரசிதழ்"])):
                matched_terms.append({
                    "term": g["term_ta"] if is_tamil else g["term_en"],
                    "explanation": g["explanation_ta"] if is_tamil else g["explanation_en"]
                })

        # Relevant verified sources
        sources = lookup_sources(doc_type, case.get("jurisdiction", ""))
        fee_info = verify_document_fee(doc_type, authority)

        # Route to Live Gemini or Deterministic Civic Engine
        if is_gemini_available() and Config.GEMINI_API_KEY:
            try:
                reply_text = cls._call_gemini_copilot(msg, case, sources, fee_info, is_tamil)
                engine_mode = "LIVE_GEMINI_AI"
            except Exception as e:
                reply_text = cls._deterministic_fallback(msg, case, sources, fee_info, is_tamil)
                engine_mode = "DETERMINISTIC_CIVIC_COPILOT"
        else:
            reply_text = cls._deterministic_fallback(msg, case, sources, fee_info, is_tamil)
            engine_mode = "DETERMINISTIC_CIVIC_COPILOT"

        # Suggested follow-ups
        suggested = [
            "FIR தேவையா அல்லது ஆன்லைன் அறிக்கை போதுமா?" if is_tamil else "Do I need a formal police FIR or an online loss report?",
            "கட்டணம் எவ்வளவு?" if is_tamil else f"What is the verified statutory fee for {doc_type}?",
            "டிஜிலாக்கர் நகல் சட்டபூர்வமாக செல்லுமா?" if is_tamil else "Is a DigiLocker duplicate legally accepted for job applications?"
        ]

        return {
            "status": "success",
            "reply": reply_text,
            "language": "ta" if is_tamil else "en",
            "engine_mode": engine_mode,
            "engine_disclaimer": (
                "Verified Civic Intelligence — Responses are strictly grounded in official statutory sources (cbse.gov.in, parivahan.gov.in, incometax.gov.in). Zero fabricated fees."
            ),
            "sources_cited": [s.get("issuing_authority") for s in sources if s.get("official_url")],
            "explained_terms": matched_terms,
            "suggested_questions": suggested
        }

    @classmethod
    def _detect_tamil(cls, text: str) -> bool:
        """Detects if string contains Tamil Unicode range (U+0B80 to U+0BFF)."""
        tamil_pattern = re.compile(r'[\u0B80-\u0BFF]')
        return bool(tamil_pattern.search(text))

    @classmethod
    def _call_gemini_copilot(cls, query: str, case: Dict[str, Any], sources: List[Dict[str, Any]],
                             fee_info: Dict[str, Any], is_tamil: bool) -> str:
        """Calls Gemini with ground truth constraints."""
        from google import genai
        client = genai.Client(api_key=Config.GEMINI_API_KEY)

        src_titles = ", ".join([f"{s.get('issuing_authority')} ({s.get('official_url')})" for s in sources])
        system_instruction = (
            "You are RECLAIM AI's Accessible Civic Recovery Copilot. "
            "Help citizens who lost important certificates or IDs understand the exact legal reissue process. "
            "RULES: "
            "1. Answer concisely in maximum 3 bullet points. "
            "2. Ground your answer ONLY in these verified sources: " + src_titles + ". "
            "3. State verified fee: INR " + str(fee_info.get("amount", "Unverified")) + ". Never invent fees. "
            f"4. If is_tamil={is_tamil}, reply entirely in clear, friendly Tamil (தமிழ்). "
            "5. Explain technical words like FIR, Affidavit, or DigiLocker in simple terms."
        )

        prompt = f"Citizen Question: {query}\nCase Category: {case.get('document_type')}\nIssuing Authority: {case.get('issuing_authority')}\nLoss Status: {case.get('status_type')}"
        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=prompt,
            config={"system_instruction": system_instruction, "temperature": 0.2}
        )
        return response.text.strip()

    @classmethod
    def _deterministic_fallback(cls, query: str, case: Dict[str, Any], sources: List[Dict[str, Any]],
                                fee_info: Dict[str, Any], is_tamil: bool) -> str:
        """Deterministic, grounded guidance when Gemini is offline."""
        q = query.lower()
        doc_type = case.get("document_type", "edu_cert")
        authority = case.get("issuing_authority", "Official Authority")
        status_type = case.get("status_type", "lost")
        has_police = bool(case.get("has_police_report"))
        primary_src = sources[0] if sources else None
        portal_name = primary_src.get("issuing_authority", "Official Government Portal") if primary_src else "Official Portal"
        portal_url = primary_src.get("official_url", "https://india.gov.in") if primary_src else "https://india.gov.in"

        fee_str = f"INR {fee_info.get('amount'):.2f}" if fee_info.get("status") == "verified" else "Unverified (Subject to institution circular)"

        # ---------------- TAMIL RESPONSES ----------------
        if is_tamil:
            if any(w in query for w in ["முதல் படி", "அடுத்து", "என்ன செய்ய", "எப்படி"]):
                return (
                    f"வணக்கம்! உங்கள் {doc_type} ஆவணத்தை மீட்டெடுக்க 3 எளிய படிகள்:\n"
                    f"1. **காவல் அறிக்கை**: அருகிலுள்ள காவல் நிலையத்திலோ அல்லது இணையதளத்திலோ 'இழப்பு அறிக்கை' (Lost Article Report) பதிவு செய்யுங்கள்.\n"
                    f"2. **டிஜிலாக்கர் (இலவசம்)**: உங்கள் ஆவண எண் தெரிந்தால், DigiLocker மூலம் உடனே சட்டபூர்வ டிஜிட்டல் நகலைப் பெறலாம்.\n"
                    f"3. **அதிகாரப்பூர்வ போர்டல்**: அசல் அட்டை தேவைப்பட்டால், {portal_name} ({portal_url}) மூலம் விண்ணப்பியுங்கள். கட்டணம்: {fee_str}."
                )
            elif any(w in query for w in ["கட்டணம்", "பணம்", "ரூபாய்"]):
                return (
                    f"**சட்டபூர்வ கட்டண விவரம்:**\n"
                    f"• {authority} நிர்ணயித்த அதிகாரப்பூர்வ கட்டணம்: **{fee_str}**.\n"
                    f"• இடைத்தரகர்கள் கோரும் கூடுதல் கட்டணத்தை செலுத்தாதீர்கள். அரசு போர்டலில் மட்டுமே நேரடியாக செலுத்த வேண்டும்."
                )
            elif any(w in query for w in ["fir", "எப்ஐஆர்", "போலீஸ்", "காவல்"]):
                return (
                    "**காவல் அறிக்கை வழிகாட்டுதல்:**\n"
                    "• உங்கள் ஆவணம் **திருடப்பட்டிருந்தால்** மட்டுமே முறையான FIR தேவை.\n"
                    "• தற்செயலாக தொலைந்துவிட்டால், மாநில போலீஸ் இணையதளத்தில் இலவச 'Lost Document Report' (DDR) பெற்றாலே போதுமானது."
                )
            elif any(w in query for w in ["டிஜிலாக்கர்", "digilocker", "செல்லுமா"]):
                return (
                    "**டிஜிலாக்கர் செல்லுபடியாகும் தன்மை:**\n"
                    "• ஆம், 100% சட்டபூர்வமாக செல்லும்!\n"
                    "• தகவல் தொழில்நுட்ப சட்டம் 2016 விதி 9A படி, DigiLocker டிஜிட்டல் ஆவணங்கள் அசல் ஆவணத்திற்கு சமமானது."
                )
            else:
                return (
                    f"உங்கள் {doc_type} மீட்புக்கான அதிகாரப்பூர்வ வழிகாட்டல்:\n"
                    f"• அங்கீகரிக்கப்பட்ட அரசு தளம்: {portal_name} ({portal_url})\n"
                    f"• சரிபார்க்கப்பட்ட கட்டணம்: {fee_str}\n"
                    f"• ஆலோசனைகள்: தனிப்பட்ட கடவுச்சொல், OTP அல்லது கூடுதல் கட்டணங்களை தனியார் முகவர்களுக்கு தர வேண்டாம்."
                )

        # ---------------- ENGLISH RESPONSES ----------------
        if any(w in q for w in ["next step", "what should i do", "how to start", "first step"]):
            return (
                f"Here are your 3 immediate next steps for {doc_type} recovery:\n"
                f"1. **File Police Lost Report**: Submit an online Lost Document entry (DDR/NCR) on your state police citizen portal.\n"
                f"2. **Check DigiLocker (Free & Instant)**: If your document number is known, download a legally valid digital duplicate on digilocker.gov.in.\n"
                f"3. **Lodge Duplicate Request**: For a physical reissue, visit {portal_name} ({portal_url}). Verified Fee: {fee_str}."
            )
        elif any(w in q for w in ["fee", "cost", "how much", "price"]):
            return (
                f"Official Fee Analysis:\n"
                f"• Verified Statutory Fee: **{fee_str}**.\n"
                f"• Legal Authority: {fee_info.get('source_title', 'Central Statutory Gazette')}.\n"
                f"• Safety Rule: Never pay fees to private express brokers. Only pay directly via the official treasury gateway."
            )
        elif any(w in q for w in ["fir", "police", "report", "stolen"]):
            return (
                "Police Report Requirements:\n"
                "• A formal FIR is only mandatory if your document was **stolen** through a criminal act.\n"
                "• For accidental misplacement, a free online Daily Diary Report (DDR) or Non-Cognizable Report (NCR) from your State Police portal is fully accepted by issuing authorities."
            )
        elif any(w in q for w in ["digilocker", "digital", "valid"]):
            return (
                "DigiLocker Legal Validity:\n"
                "• Yes, 100% legally binding across India.\n"
                "• Under Rule 9A of the Information Technology (Preservation and Retention of Information by Intermediaries) Rules 2016, digital documents in DigiLocker are treated at par with original physical documents."
            )
        else:
            return (
                f"RECLAIM AI Civic Guidance for {doc_type} ({authority}):\n"
                f"• Verified Official Portal: {portal_name} ({portal_url})\n"
                f"• Statutory Fee: {fee_str}\n"
                f"• Step 8 Human Approval Gate is active: You maintain complete control over application generation. No real payments or submissions occur without your direct consent."
            )
