/**
 * RECLAIM AI 2.0 - API Client Module
 * Handles REST communication with Flask backend across all 5 core innovations
 */

const API_BASE = '/api';

export const API = {
  async getHealth() {
    const res = await fetch('/health');
    return res.json();
  },

  async getDocumentTypes() {
    const res = await fetch(`${API_BASE}/document-types`);
    return res.json();
  },

  async getSources(category = null) {
    const url = category ? `${API_BASE}/sources?category=${encodeURIComponent(category)}` : `${API_BASE}/sources`;
    const res = await fetch(url);
    return res.json();
  },

  async getPresets() {
    const res = await fetch(`${API_BASE}/presets`);
    return res.json();
  },

  async submitIntake(payload) {
    const res = await fetch(`${API_BASE}/recovery/intake`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async submitApproval(sessionId, approvalId, decision, notes = '', simulateFailure = false) {
    const res = await fetch(`${API_BASE}/recovery/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        approval_id: approvalId,
        decision: decision,
        notes: notes,
        simulate_failure: simulateFailure
      })
    });
    return res.json();
  },

  // ================= INNOVATION 1: RECOVERY TWIN =================
  async getRecoveryTwin(caseId) {
    const res = await fetch(`${API_BASE}/recovery/${encodeURIComponent(caseId)}/twin`);
    return res.json();
  },

  async updateRecoveryTwin(caseId, payload) {
    const res = await fetch(`${API_BASE}/recovery/${encodeURIComponent(caseId)}/twin/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  // ================= INNOVATION 2: EVIDENCE VAULT =================
  async getEvidenceVault(caseId) {
    const res = await fetch(`${API_BASE}/recovery/${encodeURIComponent(caseId)}/evidence-vault`);
    return res.json();
  },

  // ================= INNOVATION 3: ROUTE COMPARISON =================
  async compareRoutes(payload) {
    const res = await fetch(`${API_BASE}/recovery/compare-routes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  // ================= INNOVATION 4: RISK RADAR =================
  async scanUrl(url) {
    const res = await fetch(`${API_BASE}/risk-radar/scan-url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url })
    });
    return res.json();
  },

  // ================= INNOVATION 5: MOCK PORTAL =================
  async verifyMockPortal(applicationRef) {
    const res = await fetch(`${API_BASE}/mock-portal/verify/${encodeURIComponent(applicationRef)}`);
    return res.json();
  },

  async submitMockPortal(draftPackage, citizenSignature = 'Demo Citizen', simulateFailure = false) {
    const res = await fetch(`${API_BASE}/mock-portal/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        draft_package: draftPackage,
        citizen_signature: citizenSignature,
        simulate_failure: simulateFailure
      })
    });
    return res.json();
  },

  // ================= TRACE & TESTS =================
  async getSession(sessionId) {
    const res = await fetch(`${API_BASE}/recovery/${encodeURIComponent(sessionId)}`);
    return res.json();
  },

  async getTrace(sessionId) {
    const res = await fetch(`${API_BASE}/recovery/${encodeURIComponent(sessionId)}/trace`);
    return res.json();
  },

  async getTests() {
    const res = await fetch(`${API_BASE}/tests`);
    return res.json();
  },

  async runTests(scenarioId = 'ALL') {
    const res = await fetch(`${API_BASE}/tests/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_id: scenarioId })
    });
    return res.json();
  },

  // ================= INNOVATION 2: COUNTERFACTUAL SIMULATOR =================
  async getCounterfactualScenarios() {
    const res = await fetch(`${API_BASE}/recovery/counterfactual-scenarios`);
    return res.json();
  },

  async simulateCounterfactual(caseData, scenarioId) {
    const res = await fetch(`${API_BASE}/recovery/counterfactual-simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case_data: caseData, scenario_id: scenarioId })
    });
    return res.json();
  },

  // ================= INNOVATION 3: PROVENANCE GRAPH =================
  async getProvenanceGraph(caseId) {
    const res = await fetch(`${API_BASE}/recovery/${encodeURIComponent(caseId)}/provenance-graph`);
    return res.json();
  },

  // ================= INNOVATION 4: ADVERSARIAL TEST LAB =================
  async getAdversarialScenarios() {
    const res = await fetch(`${API_BASE}/tests/adversarial-scenarios`);
    return res.json();
  },

  async runAdversarialTests(scenarioId = 'ALL') {
    const res = await fetch(`${API_BASE}/tests/run-adversarial`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_id: scenarioId })
    });
    return res.json();
  },

  // ================= INNOVATION 5: ACCESSIBLE CIVIC COPILOT =================
  async sendCopilotMessage(message, caseData = {}, sessionId = null, language = null) {
    const res = await fetch(`${API_BASE}/copilot/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: message,
        case_data: caseData,
        session_id: sessionId,
        language: language
      })
    });
    return res.json();
  }
};

