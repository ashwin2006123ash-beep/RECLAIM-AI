/**
 * RECLAIM AI — Recovery Compass
 * Master Application Controller:
 * 3-Stage Citizen Workflow + Adaptive Recovery Compass + Collapsible Judge Mode
 */

import { API } from './api.js';
import { UI } from './ui.js';
import { TestLab } from './test_lab.js';

class ReclaimCompassApp {
  constructor() {
    this.currentSessionId = null;
    this.currentApprovalId = null;
    this.currentGuidance = null;
    this.currentTwin = null;
    this.currentDraft = null;
    this.currentReceipt = null;
    this.presets = [];
    this.categories = [];
    this.preferredRoute = null;
    this.isJudgeModeOpen = false;
  }

  async init() {
    console.log('Initializing RECLAIM AI — Recovery Compass...');
    await this.checkHealth();
    await this.loadDocumentTypes();
    await this.loadPresets();
    this.setupDocCardSelector();
    this.setupNavigation();
    this.setupIntakeForm();
    this.setupLiveEvidenceWatchers();
    this.setupJudgeModeTabs();
    await this.setupCounterfactualSimulator();
    this.setupCivicCopilot();
    await TestLab.init(document.getElementById('test-lab-view'));
  }

  async checkHealth() {
    try {
      const health = await API.getHealth();
      const badge = document.getElementById('engine-status-badge');
      if (badge && health.ai_engine_status) {
        badge.innerHTML = `
          <span class="status-dot"></span>
          <span>${health.ai_engine_status}</span>
        `;
      }
    } catch (e) {
      console.warn('Health check warning:', e);
    }
  }

  async loadDocumentTypes() {
    try {
      const res = await API.getDocumentTypes();
      if (res.status === 'success') {
        this.categories = res.categories || [];
      }
    } catch (e) {
      console.error('Failed to load document categories:', e);
    }
  }

  setupDocCardSelector() {
    const cards = document.querySelectorAll('.doc-card-option');
    const syncSelect = document.getElementById('input-doc-type');
    const jurisdictionInput = document.getElementById('input-jurisdiction');
    const authorityInput = document.getElementById('input-authority');

    cards.forEach(card => {
      card.addEventListener('click', () => {
        cards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        const docVal = card.dataset.value;
        if (syncSelect) syncSelect.value = docVal;

        // Contextual smart defaults
        if (docVal === 'edu_cert') {
          if (jurisdictionInput) jurisdictionInput.value = 'Central / All India';
          if (authorityInput) authorityInput.value = 'Central Board of Secondary Education (CBSE)';
        } else if (docVal === 'driving_licence') {
          if (jurisdictionInput) jurisdictionInput.value = 'Karnataka';
          if (authorityInput) authorityInput.value = 'Ministry of Road Transport and Highways (MoRTH)';
        } else if (docVal === 'pan_card') {
          if (jurisdictionInput) jurisdictionInput.value = 'National';
          if (authorityInput) authorityInput.value = 'Income Tax Department of India';
        } else if (docVal === 'voter_id') {
          if (jurisdictionInput) jurisdictionInput.value = 'National';
          if (authorityInput) authorityInput.value = 'Election Commission of India (ECI)';
        } else if (docVal === 'aadhaar') {
          if (jurisdictionInput) jurisdictionInput.value = 'National';
          if (authorityInput) authorityInput.value = 'Unique Identification Authority of India (UIDAI)';
        } else if (docVal === 'passport') {
          if (jurisdictionInput) jurisdictionInput.value = 'National';
          if (authorityInput) authorityInput.value = 'Consular, Passport & Visa (CPV) Division';
        }
      });
    });
  }

  async loadPresets() {
    try {
      const res = await API.getPresets();
      if (res.status === 'success') {
        this.presets = res.presets || [];
        const strip = document.getElementById('presets-chips-container');
        if (strip) {
          strip.innerHTML = this.presets.map((p, idx) => `
            <button type="button" class="preset-chip" data-idx="${idx}" title="${p.notes || ''}">
              ⚡ ${p.name}
            </button>
          `).join('');

          strip.querySelectorAll('.preset-chip').forEach(btn => {
            btn.addEventListener('click', async (e) => {
              const idx = parseInt(e.currentTarget.dataset.idx, 10);
              await this.applyPreset(this.presets[idx]);
            });
          });
        }
      }
    } catch (e) {
      console.error('Failed to load presets:', e);
    }
  }

  async applyPreset(preset) {
    if (!preset) return;
    
    // Select corresponding document card
    const docType = preset.document_type || 'edu_cert';
    document.querySelectorAll('.doc-card-option').forEach(c => {
      c.classList.toggle('selected', c.dataset.value === docType);
    });

    const syncSelect = document.getElementById('input-doc-type');
    if (syncSelect) syncSelect.value = docType;

    document.getElementById('input-jurisdiction').value = preset.jurisdiction || 'Central / All India';
    document.getElementById('input-authority').value = preset.issuing_authority || '';
    
    const statusRadio = document.querySelector(`input[name="status_type"][value="${preset.status_type || 'lost'}"]`);
    if (statusRadio) statusRadio.checked = true;

    document.getElementById('input-circumstances').value = preset.circumstances || '';
    document.getElementById('chk-police-report').checked = Boolean(preset.has_police_report);
    document.getElementById('chk-affidavit').checked = Boolean(preset.has_affidavit);
    document.getElementById('chk-id-proof').checked = Boolean(preset.has_id_proof);
    document.getElementById('chk-doc-number').checked = Boolean(preset.has_doc_number_or_copy);

    const outageChk = document.getElementById('chk-simulate-outage');
    if (outageChk) outageChk.checked = Boolean(preset.simulate_route_outage);

    const extUrlInput = document.getElementById('input-external-url');
    if (extUrlInput) extUrlInput.value = preset.external_url_to_test || '';

    this.preferredRoute = null;

    UI.showToast(`Loaded preset: ${preset.name}`, 'info');
    
    // Automatically execute form to provide instant judge demonstration!
    await this.handleFormSubmit();
  }

  setupNavigation() {
    // Top nav links
    document.getElementById('nav-home-btn')?.addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('stage-1-tell-us')?.scrollIntoView({ behavior: 'smooth' });
    });

    document.getElementById('nav-plan-btn')?.addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('stage-3-action-plan')?.scrollIntoView({ behavior: 'smooth' });
    });

    // Copilot Help Modal trigger
    document.getElementById('nav-help-btn')?.addEventListener('click', () => {
      document.getElementById('copilot-modal').style.display = 'flex';
    });

    document.getElementById('btn-close-copilot')?.addEventListener('click', () => {
      document.getElementById('copilot-modal').style.display = 'none';
    });

    document.getElementById('copilot-modal')?.addEventListener('click', (e) => {
      if (e.target.id === 'copilot-modal') {
        document.getElementById('copilot-modal').style.display = 'none';
      }
    });

    // Advanced / Judge Mode Toggle
    const judgeBtn = document.getElementById('btn-toggle-judge-mode');
    const judgeSection = document.getElementById('advanced-judge-section');
    const closeJudgeBtn = document.getElementById('btn-close-judge-mode');

    const toggleJudgeMode = (open = null) => {
      this.isJudgeModeOpen = open !== null ? open : !this.isJudgeModeOpen;
      if (judgeSection) {
        judgeSection.style.display = this.isJudgeModeOpen ? 'block' : 'none';
      }
      if (judgeBtn) {
        judgeBtn.classList.toggle('active', this.isJudgeModeOpen);
      }
      if (this.isJudgeModeOpen) {
        judgeSection.scrollIntoView({ behavior: 'smooth' });
      }
    };

    judgeBtn?.addEventListener('click', () => toggleJudgeMode());
    closeJudgeBtn?.addEventListener('click', () => toggleJudgeMode(false));
  }

  setupJudgeModeTabs() {
    const tabs = document.querySelectorAll('.judge-tab-pill');
    tabs.forEach(tab => {
      tab.addEventListener('click', (e) => {
        tabs.forEach(t => t.classList.remove('active'));
        e.currentTarget.classList.add('active');
        const targetTab = e.currentTarget.dataset.tab;

        document.querySelectorAll('.judge-tab-content').forEach(c => {
          c.style.display = 'none';
        });
        const activeContent = document.getElementById(targetTab);
        if (activeContent) activeContent.style.display = 'block';
      });
    });
  }

  setupIntakeForm() {
    const form = document.getElementById('intake-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      this.preferredRoute = null;
      await this.handleFormSubmit();
    });
  }

  setupLiveEvidenceWatchers() {
    const checkboxes = ['chk-police-report', 'chk-affidavit', 'chk-id-proof', 'chk-doc-number', 'chk-simulate-outage'];
    checkboxes.forEach(chkId => {
      document.getElementById(chkId)?.addEventListener('change', async () => {
        if (this.currentSessionId) {
          await this.recalculateLiveTwin();
        }
      });
    });
  }

  async recalculateLiveTwin() {
    const payload = this.getSerializedFormData();
    payload.session_id = this.currentSessionId;
    try {
      const res = await API.updateRecoveryTwin(this.currentSessionId, payload);
      if (res.status === 'success' && res.recovery_twin) {
        this.currentTwin = res.recovery_twin;
        UI.renderRecoveryTwinGraph(
          this.currentTwin,
          document.getElementById('recovery-twin-graph-container'),
          (node) => UI.renderNodeInspector(node, document.getElementById('node-inspector-drawer'))
        );
      }
    } catch (e) {
      console.warn('Failed to update twin on toggle:', e);
    }
  }

  getSerializedFormData() {
    const docSelect = document.getElementById('input-doc-type');
    const selectedDocCard = document.querySelector('.doc-card-option.selected');
    const docType = selectedDocCard ? selectedDocCard.dataset.value : (docSelect?.value || 'edu_cert');

    return {
      session_id: this.currentSessionId || undefined,
      document_type: docType,
      jurisdiction: document.getElementById('input-jurisdiction').value,
      issuing_authority: document.getElementById('input-authority').value,
      status_type: document.querySelector('input[name="status_type"]:checked')?.value || 'lost',
      circumstances: document.getElementById('input-circumstances').value,
      has_police_report: document.getElementById('chk-police-report').checked,
      has_affidavit: document.getElementById('chk-affidavit').checked,
      has_id_proof: document.getElementById('chk-id-proof').checked,
      has_doc_number_or_copy: document.getElementById('chk-doc-number').checked,
      simulate_route_outage: Boolean(document.getElementById('chk-simulate-outage')?.checked),
      preferred_route: this.preferredRoute,
      external_url_to_test: document.getElementById('input-external-url')?.value?.trim() || null
    };
  }

  updateStepper(stepNum) {
    const s1 = document.getElementById('stepper-step-1');
    const s2 = document.getElementById('stepper-step-2');
    const s3 = document.getElementById('stepper-step-3');

    if (stepNum === 1) {
      s1?.classList.add('active'); s1?.classList.remove('completed');
      s2?.classList.remove('active', 'completed');
      s3?.classList.remove('active', 'completed');
    } else if (stepNum === 2) {
      s1?.classList.add('completed'); s1?.classList.remove('active');
      s2?.classList.add('active'); s2?.classList.remove('completed');
      s3?.classList.remove('active', 'completed');
    } else if (stepNum === 3) {
      s1?.classList.add('completed'); s1?.classList.remove('active');
      s2?.classList.add('completed'); s2?.classList.remove('active');
      s3?.classList.add('active');
    }
  }

  async handleFormSubmit(preferredRoute = null) {
    if (preferredRoute) {
      this.preferredRoute = preferredRoute;
    }

    const submitBtn = document.getElementById('btn-submit-intake');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '⚙️ Calculating Adaptive Recovery Route...';
    submitBtn.disabled = true;

    this.updateStepper(2);

    const payload = this.getSerializedFormData();

    try {
      UI.showToast('Evaluating statutory routes against evidence...', 'info');
      const res = await API.submitIntake(payload);
      
      if (res.status === 'success' && res.data) {
        const data = res.data;
        this.currentSessionId = data.session_id;
        this.currentApprovalId = data.approval_id;
        this.currentGuidance = data.guidance;
        this.currentTwin = data.recovery_twin;
        this.currentDraft = data.guidance.sandbox_draft;
        this.currentReceipt = null;

        // Render 1-Page Integrated Recovery Compass
        const compassContainer = document.getElementById('recovery-compass-result');
        UI.renderRecoveryCompass(
          data.guidance,
          compassContainer,
          (targetRouteId) => this.handleSwitchRoute(targetRouteId),
          () => this.handleSandboxApprove(),
          (ref) => this.handleSandboxVerify(ref),
          this.currentReceipt
        );

        this.updateStepper(3);

        // Update Judge Mode Tabs in Background
        await this.refreshTraceFeed();

        // 1. Recovery Twin
        UI.renderRecoveryTwinGraph(
          this.currentTwin,
          document.getElementById('recovery-twin-graph-container'),
          (node) => UI.renderNodeInspector(node, document.getElementById('node-inspector-drawer'))
        );

        // 2. Provenance Graph
        try {
          const provGraph = await API.getProvenanceGraph(this.currentSessionId);
          UI.renderProvenanceGraph(provGraph, document.getElementById('provenance-graph-container'));
        } catch (e) {
          console.warn('Provenance graph load error:', e);
        }

        // 3. Counterfactual Simulator
        await this.runActiveCounterfactual();

        // 4. Evidence Vault
        UI.renderEvidenceVault(
          data.guidance.research_intelligence,
          document.getElementById('evidence-vault-container')
        );

        // 5. Risk Radar
        UI.renderRiskRadar(
          data.risk_radar || data.guidance.risk_radar,
          document.getElementById('risk-radar-container'),
          async (urlToScan) => this.handleScanUrl(urlToScan)
        );

        // 6. Safe Sandbox
        this.renderSandbox();

        UI.showToast('Recovery Compass Plan ready in under 60s.', 'success');
        document.getElementById('stage-3-action-plan')?.scrollIntoView({ behavior: 'smooth' });
      } else {
        UI.showToast(`Error: ${res.message || 'Failed to generate guidance'}`, 'error');
      }
    } catch (e) {
      UI.showToast(`Execution error: ${e.message}`, 'error');
    } finally {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  }

  async handleSwitchRoute(targetRouteId) {
    this.preferredRoute = targetRouteId;
    UI.showToast(`Switching active plan to: ${targetRouteId}...`, 'info');
    await this.handleFormSubmit(targetRouteId);
  }

  async handleScanUrl(url) {
    const outputEl = document.getElementById('radar-scan-result');
    if (!outputEl) return;
    outputEl.innerHTML = '<span style="font-size: 0.8rem; color: var(--text-muted);">Scanning domain heuristics...</span>';
    try {
      const res = await API.scanUrl(url);
      if (res.status === 'success' && res.scan_report) {
        const s = res.scan_report;
        const isOfficial = s.is_official_government;
        outputEl.innerHTML = `
          <div style="padding: 10px; border-radius: 6px; font-size: 0.82rem; background: ${isOfficial ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)'}; border: 1px solid ${isOfficial ? 'var(--emerald-success)' : 'var(--rose-danger)'};">
            <strong>Scan Result:</strong> ${s.risk_level} &bull; 
            <strong>Hostname:</strong> ${s.hostname}<br>
            <span style="color: var(--text-secondary);">${s.threat_explanation}</span><br>
            <span style="color: var(--teal-primary); font-weight: 600;">Action: ${s.recommended_action}</span>
          </div>
        `;
      }
    } catch (e) {
      outputEl.innerHTML = `<span style="color: #f87171; font-size: 0.8rem;">Scan failed: ${e.message}</span>`;
    }
  }

  renderSandbox() {
    UI.renderSafeActionSandbox(
      this.currentDraft,
      this.currentReceipt,
      document.getElementById('safe-sandbox-container'),
      () => this.handleSandboxApprove(),
      () => this.handleSandboxReject(),
      (ref) => this.handleSandboxVerify(ref)
    );
  }

  async handleSandboxApprove() {
    if (!this.currentSessionId || !this.currentApprovalId) return;
    UI.showToast('Executing simulation against Safe Action Sandbox...', 'info');
    try {
      const res = await API.submitApproval(this.currentSessionId, this.currentApprovalId, 'approved');
      if (res.status === 'success' && res.data) {
        const data = res.data;
        this.currentReceipt = data.receipt;
        this.currentTwin = data.recovery_twin;

        // Re-render Recovery Compass with confirmed receipt
        const compassContainer = document.getElementById('recovery-compass-result');
        UI.renderRecoveryCompass(
          this.currentGuidance,
          compassContainer,
          (targetRouteId) => this.handleSwitchRoute(targetRouteId),
          () => this.handleSandboxApprove(),
          (ref) => this.handleSandboxVerify(ref),
          this.currentReceipt
        );

        this.renderSandbox();

        // Update Recovery Twin graph
        UI.renderRecoveryTwinGraph(
          this.currentTwin,
          document.getElementById('recovery-twin-graph-container'),
          (node) => UI.renderNodeInspector(node, document.getElementById('node-inspector-drawer'))
        );

        await this.refreshTraceFeed();

        // Refresh Provenance Graph so Tier 7 shows confirmed receipt
        try {
          const provGraph = await API.getProvenanceGraph(this.currentSessionId);
          UI.renderProvenanceGraph(provGraph, document.getElementById('provenance-graph-container'));
        } catch (e) {}

        UI.showToast(`Simulation confirmed under ${data.receipt.application_reference}!`, 'success');
      } else {
        UI.showToast(`Error: ${res.message}`, 'error');
      }
    } catch (e) {
      UI.showToast(`Sandbox execution error: ${e.message}`, 'error');
    }
  }

  async handleSandboxReject() {
    if (!this.currentSessionId || !this.currentApprovalId) return;
    try {
      const res = await API.submitApproval(this.currentSessionId, this.currentApprovalId, 'rejected');
      if (res.status === 'success' && res.data) {
        UI.showToast('Citizen declined action. Workflow safely paused.', 'info');
        this.currentTwin = res.data.recovery_twin;
        UI.renderRecoveryTwinGraph(
          this.currentTwin,
          document.getElementById('recovery-twin-graph-container'),
          (node) => UI.renderNodeInspector(node, document.getElementById('node-inspector-drawer'))
        );
        await this.refreshTraceFeed();
      }
    } catch (e) {
      UI.showToast(`Error: ${e.message}`, 'error');
    }
  }

  async handleSandboxVerify(applicationRef) {
    const outputEl = document.getElementById('sandbox-verify-output') || document.getElementById('sandbox-verification-output');
    if (!outputEl) return;
    outputEl.innerHTML = '<span style="font-size: 0.8rem; color: var(--text-muted);">Querying SQLite database...</span>';
    try {
      const res = await API.verifyMockPortal(applicationRef);
      if (res.status === 'success' && res.report) {
        const rep = res.report;
        outputEl.innerHTML = `
          <div style="padding: 10px; border-radius: 6px; font-size: 0.82rem; background: rgba(16,185,129,0.12); border: 1px solid var(--emerald-success); color: var(--text-primary); margin-top: 8px;">
            <strong>✓ Independent SQLite Verification Confirmed</strong><br>
            Reference: <code>${rep.application_ref}</code> &bull; Status: <strong>${rep.submission_status}</strong><br>
            Portal: ${rep.portal_name} &bull; Timestamp: ${rep.submitted_at}<br>
            <span style="color: #fbbf24; font-size: 0.76rem;">${rep.disclaimer}</span>
          </div>
        `;
      } else {
        outputEl.innerHTML = `<span style="color: #f87171;">Verification Failed: ${res.message || 'Record not found'}</span>`;
      }
    } catch (e) {
      outputEl.innerHTML = `<span style="color: #f87171;">Query error: ${e.message}</span>`;
    }
  }

  async refreshTraceFeed() {
    if (!this.currentSessionId) return;
    try {
      const traceData = await API.getTrace(this.currentSessionId);
      if (traceData.status === 'success') {
        UI.renderTraceFeed(traceData.trace, document.getElementById('agent-activity-view'));
      }
    } catch (e) {
      console.error('Failed to load trace events:', e);
    }
  }

  // ==================== INNOVATION 2: COUNTERFACTUAL SIMULATOR ====================
  async setupCounterfactualSimulator() {
    try {
      const res = await API.getCounterfactualScenarios();
      if (res.status === 'success') {
        this.counterfactualScenarios = res.scenarios || [];
        this.activeScenarioId = this.counterfactualScenarios[0]?.id || 'scenario_lost_vs_stolen';

        const container = document.getElementById('counterfactual-scenario-pills');
        if (container) {
          this.renderCounterfactualPills(container);
        }
        await this.runActiveCounterfactual();
      }
    } catch (e) {
      console.error('Failed to load counterfactual scenarios:', e);
    }
  }

  renderCounterfactualPills(container) {
    container.innerHTML = this.counterfactualScenarios.map(s => `
      <button type="button" class="preset-chip ${s.id === this.activeScenarioId ? 'active' : ''}" data-sid="${s.id}" style="${s.id === this.activeScenarioId ? 'border-color: var(--teal-primary); background: rgba(0,242,254,0.15); color: var(--teal-primary);' : ''}">
        ⚖️ ${s.title}
      </button>
    `).join('');

    container.querySelectorAll('button[data-sid]').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        this.activeScenarioId = e.currentTarget.dataset.sid;
        this.renderCounterfactualPills(container);
        await this.runActiveCounterfactual();
      });
    });
  }

  async runActiveCounterfactual() {
    const container = document.getElementById('counterfactual-container');
    if (!container) return;
    const caseData = this.getSerializedFormData();
    try {
      const simRes = await API.simulateCounterfactual(caseData, this.activeScenarioId);
      if (simRes.status === 'success') {
        UI.renderCounterfactualSimulator(
          simRes,
          container,
          (sid) => { this.activeScenarioId = sid; this.runActiveCounterfactual(); },
          this.counterfactualScenarios,
          this.activeScenarioId
        );
      }
    } catch (e) {
      console.warn('Counterfactual simulation error:', e);
    }
  }

  // ==================== INNOVATION 5: ACCESSIBLE CIVIC COPILOT ====================
  setupCivicCopilot() {
    this.currentLanguage = 'en';
    const container = document.getElementById('copilot-chat-container');
    if (!container) return;

    UI.renderCivicCopilot(
      container,
      (msg) => this.handleCopilotSend(msg),
      (q) => this.handleCopilotSend(q)
    );

    document.getElementById('btn-toggle-lang')?.addEventListener('click', () => {
      this.currentLanguage = this.currentLanguage === 'en' ? 'ta' : 'en';
      UI.showToast(`Civic Copilot language: ${this.currentLanguage === 'ta' ? 'தமிழ் (Tamil)' : 'English'}`, 'info');
      const langBtn = document.getElementById('btn-toggle-lang');
      if (langBtn) {
        langBtn.innerHTML = this.currentLanguage === 'ta' ? '🌐 மொழி: தமிழ் (Tamil)' : '🌐 Switch: English / தமிழ்';
      }
    });
  }

  async handleCopilotSend(msg) {
    if (!msg) return;
    UI.appendCopilotMessage('user', msg);
    try {
      const caseData = this.getSerializedFormData();
      const res = await API.sendCopilotMessage(msg, caseData, this.currentSessionId, this.currentLanguage);
      if (res.status === 'success') {
        UI.appendCopilotMessage('bot', res.reply, res.explained_terms);
      } else {
        UI.appendCopilotMessage('bot', `Apologies, I encountered an issue: ${res.message || 'Unknown error'}`);
      }
    } catch (e) {
      UI.appendCopilotMessage('bot', `Network error while querying copilot: ${e.message}`);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const app = new ReclaimCompassApp();
  app.init();
});
