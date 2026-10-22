# RECLAIM AI 2.0 — Presentation & Pitch Deck Outline
> **Assigned Problem Statement:** Lost Document Reissue Guide  
> **Hackathon:** Agentic AI Hackathon 2026 — Powered by Ziro.Digital  
> **Industry Track:** Social Impact & Sustainability AI  

---

## 📊 Mapping to Published Judging Criteria (Total: 100 Points)

| Criteria | Points | How RECLAIM AI 2.0 Delivers Competition-Winning Evidence |
| :--- | :---: | :--- |
| **1. Problem Fit & Usefulness** | **20 pts** | 100% faithful to the assigned "Lost Document Reissue Guide" problem. Eliminates predatory middleman scams, demystifies statutory fees, and guides Indian citizens through legitimate recovery channels. |
| **2. Agentic Capability** | **25 pts** | Coordinated 8-stage loop (Observe -> Twin -> Investigate -> Reason -> Risk -> Sandbox -> Verify -> Learn). Dynamic topological graph with 8 nodes and unblock triggers. |
| **3. Technical Implementation** | **20 pts** | Python 3.13, Flask REST API, SQLite parameterized database, official Google Gemini API + offline deterministic fallback, idempotency keys, 29/29 automated tests. |
| **4. Innovation** | **15 pts** | 5 Core Innovations: Recovery Twin, Proof-of-Truth Vault, Adaptive Multi-Route Planner, Recovery Risk Radar, and Safe Action Sandbox with persistent Mock Portal. |
| **5. User Experience** | **10 pts** | Civic Tech dark navy design system, interactive dependency graph, clickable node inspector, real-time agent trace, clear disclaimers, and Safe Domain scanner. |
| **6. Presentation** | **10 pts** | Structured 2.5-minute timed demo script, interactive Test Lab (TC1–TC4), and complete submission checklist. |

---

## 📽️ Slide-by-Slide Pitch Deck

### Slide 1: Title & The Civic Challenge
- **Headline:** RECLAIM AI 2.0 — Autonomous Civic Document Recovery Intelligence Platform
- **Tagline:** *"Lost a document? Reclaim your next step."*
- **The Citizen Crisis:** Over 15 million identity and educational documents lost annually in India. Citizens fall prey to fake agent websites, exorbitant commissions (up to ₹3,000), and contradictory circulars.

### Slide 2: The Coordinated Agentic Loop
- Diagram illustrating the unified 8-stage loop:
  - `OBSERVE` -> `BUILD RECOVERY TWIN` -> `INVESTIGATE` -> `REASON` -> `ASSESS RISK` -> `ACT SAFELY` -> `VERIFY` -> `LEARN`
- Zero hardcoded sequences; each stage consumes the exact output of the preceding stage.

### Slide 3: Innovation 1 & 2 — Recovery Twin & Proof-of-Truth Vault
- **Recovery Twin:** Structured case representation with an 8-node dependency graph. Nodes dynamically transition between `BLOCKED`, `READY`, and `COMPLETED` when evidence changes.
- **Proof-of-Truth Vault:** Mined statutory claims with provenance tags (`LIVE_VERIFIED`, `CACHED`). Conflicting circulars resolved using statutory hierarchy rules.

### Slide 4: Innovation 3 — Adaptive Multi-Route Planner
- Generates and compares 3 recovery channels:
  1. *Route 1 (DigiLocker):* Instant, zero cost, IT Act Sec 9A legal equivalence.
  2. *Route 2 (Statutory Portal):* Direct government postal reissue of physical embossed card.
  3. *Route 3 (Physical Counter):* Manual administrative fallback.
- **Explainable Decision Matrix:** *"Why did the agent choose this?"* panel with exact legal justifications.

### Slide 5: Innovation 4 — Recovery Risk Radar
- 9-category cybersecurity and procedural threat detector.
- Catches predatory commercial brokers, SSRF attacks, fee anomalies, and missing police reports.
- **Safe-Domain Checking Tool:** Real-time domain verification without submitting citizen PII.

### Slide 6: Innovation 5 — Safe Action Sandbox & Mock Government Portal
- Persistent mock portal backend simulating statutory application filing.
- **Civic AI Safeguards:**
  - Idempotency key protection (`IDEMP-...`) preventing duplicate transactions.
  - Step 8 Human Approval Gate before submission.
  - Independent database verification (`GET /api/mock-portal/verify/<ref>`).
  - Mandatory prominent watermark: `"SYNTHETIC DEMO — NOT A REAL GOVERNMENT APPLICATION"`.

### Slide 7: Verification & Test Laboratory
- **Official Hackathon Cases:**
  - *TC1 (Lost Certificate):* Authority established, `cbse.gov.in` duplicate portal retrieved, INR 250 fee verified — **PASS**.
  - *TC2 (Unofficial Agent Website):* `quick-pan-agent.com` flagged as `HIGH_RISK` and excluded — **PASS**.
  - *TC3 (Reissue Fee):* Exact statutory fee of INR 400 verified under CMVR Rule 81; simulated payment gated — **PASS**.
  - *TC4 (Request Number Received):* Honest `not_submitted` status; simulated demo reference clearly labelled — **PASS**.
- **Automated Test Results:** **29/29 tests passing (100% coverage)**.

### Slide 8: Technical Architecture & Social Impact
- **Architecture:** Python 3.13, Flask REST API, SQLite parameterized database, Google Gemini Interactions API (`google-genai`), Vanilla CSS3, Docker, Render.
- **Social Impact:** Democratizes civic knowledge, protects vulnerable citizens from fraud, and reduces bureaucratic friction.
