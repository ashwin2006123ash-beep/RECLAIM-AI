# RECLAIM AI 2.0 — Official Hackathon Submission Checklist
> **Hackathon:** Agentic AI Hackathon 2026 — Powered by Ziro.Digital  
> **Platform / Host:** Ziro.Digital Portal  
> **Assigned Problem Statement:** Lost Document Reissue Guide  
> **Track:** Social Impact & Sustainability AI  

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
| **Pitch Presentation Slides** | ✅ READY | Full 9-slide deck outline prepared in [`PRESENTATION_OUTLINE.md`](PRESENTATION_OUTLINE.md) |
| **Local Execution Instructions** | ✅ READY | Complete commands in [`README.md`](README.md) (`pip install -r requirements.txt && python app.py`) |
| **Automated Test Results** | ✅ READY | **45/45 unit, integration, and security tests passing (100%)** (`python -m pytest -v`) |
| **Official Hackathon Test Cases** | ✅ READY | TC1 (PASS), TC2 (PASS), TC3 (PASS), TC4 (PASS) verified via `/api/tests/run` |
| **Five Core Innovations** | ✅ READY | 1. Civic Recovery Twin, 2. Counterfactual Simulator, 3. Provenance Graph, 4. Adversarial Safety Lab, 5. Accessible Civic Copilot |
| **Demonstration Presets** | ✅ READY | 6 one-click demo presets matching Section 7 scenarios (`/api/presets`) |
| **Safety & Privacy Safeguards** | ✅ READY | Zero-PII storage, SSRF protection, domain allowlist, idempotency keys, Step 8 Human Approval Gate |

---

## 🧪 Verified Automated Test Suite Summary (45 Tests)

```text
tests/test_adversarial_lab.py::test_adversarial_scenarios_list PASSED    [  2%]
tests/test_adversarial_lab.py::test_run_all_adversarial_scenarios PASSED [  4%]
tests/test_approval_gate.py::test_approval_and_execution_lifecycle PASSED [  6%]
tests/test_approval_gate.py::test_rejection_lifecycle PASSED             [  8%]
tests/test_copilot.py::test_copilot_english_guidance PASSED              [ 11%]
tests/test_copilot.py::test_copilot_tamil_support PASSED                 [ 13%]
tests/test_copilot.py::test_copilot_glossary_explanation PASSED          [ 15%]
tests/test_counterfactual.py::test_counterfactual_scenarios_list PASSED  [ 17%]
tests/test_counterfactual.py::test_counterfactual_lost_vs_stolen PASSED  [ 20%]
tests/test_counterfactual.py::test_counterfactual_copy_available_vs_missing PASSED [ 22%]
tests/test_counterfactual.py::test_counterfactual_authority_known_vs_unknown PASSED [ 24%]
tests/test_fee_verifier.py::test_verified_driving_licence_fee PASSED     [ 26%]
tests/test_fee_verifier.py::test_verified_voter_id_fee_is_zero PASSED    [ 28%]
tests/test_fee_verifier.py::test_unverified_fee_for_unknown_authority PASSED [ 31%]
tests/test_hackathon_cases.py::test_api_run_all_hackathon_test_cases PASSED [ 33%]
tests/test_hackathon_cases.py::test_tc1_individual PASSED                [ 35%]
tests/test_hackathon_cases.py::test_tc2_individual PASSED                [ 37%]
tests/test_hackathon_cases.py::test_tc3_individual PASSED                [ 40%]
tests/test_hackathon_cases.py::test_tc4_individual PASSED                [ 42%]
tests/test_health.py::test_health_check PASSED                           [ 44%]
tests/test_health.py::test_document_types PASSED                         [ 46%]
tests/test_health.py::test_sources_endpoint PASSED                       [ 48%]
tests/test_innovations_2_0.py::test_recovery_twin_dynamic_recalculation PASSED [ 51%]
tests/test_innovations_2_0.py::test_missing_authority_blocks_graph_and_routes PASSED [ 53%]
tests/test_innovations_2_0.py::test_proof_of_truth_claims_and_conflicts PASSED [ 55%]
tests/test_innovations_2_0.py::test_adaptive_multi_route_comparison PASSED [ 57%]
tests/test_innovations_2_0.py::test_recovery_risk_radar_detection PASSED [ 60%]
tests/test_innovations_2_0.py::test_mock_portal_idempotency_and_verification PASSED [ 62%]
tests/test_innovations_2_0.py::test_mock_portal_simulated_failure PASSED [ 64%]
tests/test_provenance_graph.py::test_provenance_graph_structure PASSED   [ 66%]
tests/test_provenance_graph.py::test_provenance_graph_unsupported_claim_highlighting PASSED [ 68%]
tests/test_readiness.py::test_full_readiness_score PASSED                [ 71%]
tests/test_readiness.py::test_partial_readiness_score PASSED             [ 73%]
tests/test_readiness.py::test_zero_readiness_score PASSED                [ 75%]
tests/test_risk_radar_api.py::test_risk_radar_post_json PASSED           [ 77%]
tests/test_risk_radar_api.py::test_risk_radar_post_unofficial_broker PASSED [ 80%]
tests/test_risk_radar_api.py::test_risk_radar_get_query_param PASSED     [ 82%]
tests/test_risk_radar_api.py::test_risk_radar_options_preflight PASSED   [ 84%]
tests/test_risk_radar_api.py::test_risk_radar_trailing_slash_handling PASSED [ 86%]
tests/test_safety_guard.py::test_block_localhost_ssrf PASSED             [ 88%]
tests/test_safety_guard.py::test_block_cloud_metadata_endpoints PASSED   [ 91%]
tests/test_safety_guard.py::test_block_private_ips PASSED                [ 93%]
tests/test_safety_guard.py::test_flag_unofficial_agent_broker PASSED     [ 95%]
tests/test_safety_guard.py::test_verify_official_domains PASSED          [ 97%]
tests/test_workflow.py::test_workflow_execution_and_trace PASSED         [100%]

============================= 45 passed in 4.12s ==============================
```

---

## 🛠️ Step-by-Step Guide for the User to Complete Final Submission

1. **Step 1: Push to GitHub**
   ```bash
   git add .
   git commit -m "feat: complete RECLAIM AI 2.0 with all 5 innovations and 45 passing tests"
   git push origin main
   ```

2. **Step 2: Deploy to Render (1-Click Deployment)**
   - Log in to [render.com](https://render.com) &rarr; Click **New** &rarr; **Blueprint**.
   - Connect your GitHub repository. Render automatically reads `render.yaml`.
   - Your application will deploy to: `https://reclaim-ai.onrender.com`.

3. **Step 3: Record Demo Video (2.5 Minutes)**
   - Follow [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md).
   - Show:
     - Preset loading (e.g. Stolen DL with FIR blocker)
     - Recovery Twin & topological dependency graph
     - Provenance Graph (7-tier DAG)
     - Counterfactual Recovery Simulator (side-by-side what-if deltas)
     - Risk Radar Safe-Domain Scanner (`quick-pan-agent.com` flagged)
     - Safe Action Sandbox approval & independent SQLite verification
     - Accessible Civic Copilot in English & Tamil (தமிழ்)
     - Test Laboratory showing TC1–TC4 and Adversarial Tests passing.

4. **Step 4: Paste links into the Hackathon Dashboard**
   - Fill in Project Title, Tagline, GitHub URL, Live Render URL, and Demo Video link.
   - Click Submit!
