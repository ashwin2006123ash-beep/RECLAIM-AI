# RECLAIM AI 2.0 — Official Hackathon Submission Checklist
> **Hackathon:** Agentic AI Hackathon 2026 — Powered by Ziro.Digital  
> **Platform / Host:** Ziro.Digital Portal  
> **Submission Deadline:** Official Evaluation Period  

---

## 📋 Required Dashboard Fields & Prepared Data

| Field Name | Status | Prepared Value / Artifact Reference |
| :--- | :---: | :--- |
| **Project Title** | ✅ READY | `RECLAIM AI 2.0 — Autonomous Civic Document Recovery Intelligence Platform` |
| **Project Tagline** | ✅ READY | `"Lost a document? Reclaim your next step."` |
| **Problem Statement** | ✅ READY | `Lost Document Reissue Guide` |
| **Industry Track** | ✅ READY | `Social Impact & Sustainability AI` |
| **Primary Technology Stack** | ✅ READY | `Python 3.13, Flask REST API, SQLite, Google Gemini API (google-genai), Vanilla CSS3, ES6 JavaScript, Docker, Render` |
| **Repository URL** | ⏳ PENDING USER | To be filled after user pushes current workspace to GitHub |
| **Live Deployed Demo URL** | ⏳ PENDING USER | Ready for 1-click deploy to Render via included `render.yaml` or `Dockerfile` |
| **Demo Video URL** | ⏳ PENDING USER | 2.5-minute video recorded following [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) |
| **Pitch Presentation Slides** | ✅ READY | Full slide outline prepared in [`PRESENTATION_OUTLINE.md`](PRESENTATION_OUTLINE.md) |
| **Local Execution Instructions** | ✅ READY | Complete commands in [`README.md`](README.md) (`pip install -r requirements.txt && python app.py`) |
| **Automated Test Results** | ✅ READY | **29/29 unit & integration tests passing** (`python -m pytest -v`) |
| **Official Hackathon Test Cases** | ✅ READY | TC1 (PASS), TC2 (PASS), TC3 (PASS), TC4 (PASS) verified via `/api/tests/run` |
| **Five Core Innovations** | ✅ READY | 1. Recovery Twin, 2. Proof-of-Truth Vault, 3. Adaptive Planner, 4. Risk Radar, 5. Safe Sandbox |
| **Safety & Privacy Safeguards** | ✅ READY | Zero-PII storage, SSRF protection, domain allowlist, idempotency keys, Step 8 Human Approval Gate |

---

## 🛠️ Step-by-Step Guide for the User to Complete Final Submission

1. **Step 1: Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "feat: complete RECLAIM AI 2.0 autonomous civic recovery platform for Agentic AI Hackathon 2026"
   git branch -M main
   git remote add origin https://github.com/<your-username>/RECLAIM-AI.git
   git push -u origin main
   ```

2. **Step 2: Deploy to Render (Optional / Recommended)**
   - Go to [render.com](https://render.com) -> New -> Blueprint.
   - Select your GitHub repository; Render will automatically detect `render.yaml`.
   - Your live URL will be: `https://reclaim-ai.onrender.com`.

3. **Step 3: Record Demo Video**
   - Follow the exact 2.5-minute script in [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md).
   - Show the live UI at `http://127.0.0.1:5000`:
     - Load preset (Driving Licence Karnataka or CBSE Class 12).
     - Show Recovery Twin dependency graph and toggle evidence to demonstrate dynamic recalculation.
     - Show Proof-of-Truth Evidence Vault & Conflicting Claims resolution.
     - Show Adaptive Multi-Route Planner and "Why did the agent choose this?" panel.
     - Demonstrate Recovery Risk Radar Safe Domain Scanner.
     - Execute Safe Action Sandbox submission with idempotency and independent verification.
     - Run the 4 Official Test Cases in the Test Lab.
   - Upload video to YouTube (unlisted) or Loom.

4. **Step 4: Paste links into the Hackathon Dashboard**
   - Copy Project Title, Tagline, GitHub URL, Deployed URL, and Video link into the form.
   - Submit!
