/**
 * RECLAIM AI 2.0 - Master Application Controller
 * Connects the 5 Innovations into one coordinated agent loop:
 * Recovery Twin -> Proof-of-Truth Vault -> Adaptive Planner -> Risk Radar -> Safe Sandbox
 */

import { API } from './api.js';
import { UI } from './ui.js';
import { TestLab } from './test_lab.js';

class ReclaimApp {
  constructor() {
    this.currentSessionId = null;
    this.currentApprovalId = null;
    this.currentGuidance = null;
    this.currentTwin = null;
    this.currentDraft = null;
    this.currentReceipt = null;
    this.presets = [];
    this.categories = [];
  }

  async init() {
    console.log('Initializing RECLAIM AI 2.0 Autonomous Civic Recovery Platform...');
    await this.checkHealth();
    await this.loadDocumentTypes();
    await this.loadPresets();
    this.setupNavigation();
    this.setupIntakeForm();
    this.setupLiveEvidenceWatchers();
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
        const select = document.getElementById('input-doc-type');
        if (select) {
          select.innerHTML = '<option value="">-- Select Document Category --</option>' +
            this.categories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
        }
      }
    } catch (e) {
      console.error('Failed to load document categories:', e);
    }
  }

  async loadPresets() {
    try {
      const res = await API.getPresets();
      if (res.status === 'success') {
        this.presets = res.presets || [];
        const strip = document.getElementById('presets-chips-container');
        if (strip) {
          strip.innerHTML = this.presets.map((p, idx) => `
            <button class="preset-chip" data-idx="${idx}" title="${p.notes || ''}">
              ⚡ ${p.name}
            </button>
          `).join('');

          strip.querySelectorAll('.preset-chip').forEach(btn => {
            btn.addEventListener('click', (e) => {
              const idx = parseInt(e.target.dataset.idx, 10);
              this.applyPreset(this.presets[idx]);
            });
          });
        }
      }
    } catch (e) {
      console.error('Failed to load presets:', e);
    }
  }

  applyPreset(preset) {
    if (!preset) return;
    document.getElementById('input-doc-type').value = preset.document_type || '';
    document.getElementById('input-jurisdiction').value = preset.jurisdiction || '';
    document.getElementById('input-authority').value = preset.issuing_authority || '';
    
    const statusRadio = document.querySelector(`input[name="status_type"][value="${preset.status_type || 'lost'}"]`);
    if (statusRadio) statusRadio.checked = true;

    document.getElementById('input-circumstances').value = preset.circumstances || '';
    document.getElementById('chk-police-report').checked = Boolean(preset.has_police_report);
    document.getElementById('chk-affidavit').checked = Boolean(preset.has_affidavit);
    document.getElementById('chk-id-proof').checked = Boolean(preset.has_id_proof);
    document.getElementById('chk-doc-number').checked = Boolean(preset.has_doc_number_or_copy);
    document.getElementById('input-external-url').value = preset.external_url_to_test || '';

    UI.showToast(`Loaded preset scenario: ${preset.name}`, 'info');
    document.getElementById('recovery-workspace').scrollIntoView({ behavior: 'smooth' });
  }

  setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-link-btn[data-target]');
    navButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const targetId = e.currentTarget.dataset.target;
        this.switchSection(targetId);
      });
    });

    document.getElementById('btn-hero-start')?.addEventListener('click', () => {
      document.getElementById('recovery-workspace').scrollIntoView({ behavior: 'smooth' });
    });

    document.getElementById('btn-hero-explore')?.addEventListener('click', () => {
      document.getElementById('project-info-section').scrollIntoView({ behavior: 'smooth' });
    });
  }

  switchSection(sectionId) {
    document.querySelectorAll('.nav-link-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.nav-link-btn[data-target="${sectionId}"]`)?.classList.add('active');

    const targetEl = document.getElementById(sectionId);
    if (targetEl) {
      targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  setupIntakeForm() {
    const form = document.getElementById('intake-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await this.handleFormSubmit();
    });

    document.getElementById('btn-reset-form')?.addEventListener('click', () => {
      form.reset();
      this.currentSessionId = null;
      this.currentApprovalId = null;
      this.currentGuidance = null;
      this.currentTwin = null;
      this.currentReceipt = null;
      document.getElementById('results-view').style.display = 'none';
      document.getElementById('recovery-twin-view').style.display = 'none';
      document.getElementById('route-planner-view').style.display = 'none';
      document.getElementById('evidence-vault-view').style.display = 'none';
      document.getElementById('risk-radar-view').style.display = 'none';
      document.getElementById('safe-sandbox-view').style.display = 'none';
      document.getElementById('agent-activity-view').innerHTML = `<p class="text-muted" style="text-align: center; padding: 24px;">Workspace reset. Ready for new inquiry.</p>`;
      UI.showToast('Workspace reset.', 'info');
    });
  }

  setupLiveEvidenceWatchers() {
    // When user toggles evidence checkboxes in an active case, dynamically recalculate Recovery Twin!
    const checkboxes = ['chk-police-report', 'chk-affidavit', 'chk-id-proof', 'chk-doc-number'];
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
        UI.showToast('Recovery Twin recalculated from updated evidence.', 'info');
      }
    } catch (e) {
      console.warn('Failed to update twin on toggle:', e);
    }
  }

  getSerializedFormData() {
    return {
      session_id: this.currentSessionId || undefined,
      document_type: document.getElementById('input-doc-type').value,
      jurisdiction: document.getElementById('input-jurisdiction').value,
      issuing_authority: document.getElementById('input-authority').value,
      status_type: document.querySelector('input[name="status_type"]:checked')?.value || 'lost',
      circumstances: document.getElementById('input-circumstances').value,
      has_police_report: document.getElementById('chk-police-report').checked,
      has_affidavit: document.getElementById('chk-affidavit').checked,
      has_id_proof: document.getElementById('chk-id-proof').checked,
      has_doc_number_or_copy: document.getElementById('chk-doc-number').checked,
      external_url_to_test: document.getElementById('input-external-url').value.trim() || null
    };
  }

  async handleFormSubmit() {
    const submitBtn = document.getElementById('btn-submit-intake');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '⚙️ Coordinated Agent Loop in Progress...';
    submitBtn.disabled = true;

    const payload = this.getSerializedFormData();

    try {
      UI.showToast('Executing: Observe -> Twin -> Investigate -> Reason -> Risk -> Sandbox...', 'info');
      const res = await API.submitIntake(payload);
      
      if (res.status === 'success' && res.data) {
        const data = res.data;
        this.currentSessionId = data.session_id;
        this.currentApprovalId = data.approval_id;
        this.currentGuidance = data.guidance;
        this.currentTwin = data.recovery_twin;
        this.currentDraft = data.guidance.sandbox_draft;
        this.currentReceipt = null;

        // Render Live Trace Feed
        await this.refreshTraceFeed();

        // 1. Render Recovery Twin & Dependency Graph
        const twinView = document.getElementById('recovery-twin-view');
        twinView.style.display = 'block';
        UI.renderRecoveryTwinGraph(
          this.currentTwin,
          document.getElementById('recovery-twin-graph-container'),
          (node) => UI.renderNodeInspector(node, document.getElementById('node-inspector-drawer'))
        );

        // 2. Render Adaptive Route Comparison
        const routeView = document.getElementById('route-planner-view');
        routeView.style.display = 'block';
        UI.renderRouteComparison(
          data.route_planning || data.guidance.route_planning,
          document.getElementById('route-planner-container')
        );

        // 3. Render Proof-of-Truth Evidence Vault
        const vaultView = document.getElementById('evidence-vault-view');
        vaultView.style.display = 'block';
        UI.renderEvidenceVault(
          data.guidance.research_intelligence,
          document.getElementById('evidence-vault-container')
        );

        // 4. Render Recovery Risk Radar
        const riskView = document.getElementById('risk-radar-view');
        riskView.style.display = 'block';
        UI.renderRiskRadar(
          data.risk_radar || data.guidance.risk_radar,
          document.getElementById('risk-radar-container'),
          async (urlToScan) => this.handleScanUrl(urlToScan)
        );

        // 5. Render Safe Action Sandbox
        const sandboxView = document.getElementById('safe-sandbox-view');
        sandboxView.style.display = 'block';
        this.renderSandbox();

        // 6. Render Baseline Results Dashboard
        this.renderBaselineResults(data.guidance);

        UI.showToast('All 5 Innovations connected. Case active.', 'success');
        document.getElementById('recovery-twin-section').scrollIntoView({ behavior: 'smooth' });
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
        this.renderSandbox();

        // Update Recovery Twin graph
        UI.renderRecoveryTwinGraph(
          this.currentTwin,
          document.getElementById('recovery-twin-graph-container'),
          (node) => UI.renderNodeInspector(node, document.getElementById('node-inspector-drawer'))
        );

        // Update tracking status
        if (data.tracking) {
          UI.renderTrackingStatus(data.tracking, document.getElementById('tracking-status-container'));
        }

        await this.refreshTraceFeed();
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
    const outputEl = document.getElementById('sandbox-verification-output');
    if (!outputEl) return;
    outputEl.innerHTML = '<span style="font-size: 0.8rem; color: var(--text-muted);">Querying mock portal database...</span>';
    try {
      const res = await API.verifyMockPortal(applicationRef);
      if (res.status === 'success' && res.report) {
        const rep = res.report;
        outputEl.innerHTML = `
          <div style="padding: 10px; border-radius: 6px; font-size: 0.82rem; background: rgba(16,185,129,0.12); border: 1px solid var(--emerald-success); color: var(--text-primary);">
            <strong>✓ Independent Database Verification Confirmed</strong><br>
            Reference: <code>${rep.application_ref}</code> &bull; Status: <strong>${rep.submission_status}</strong><br>
            Portal Gateway: ${rep.portal_name} &bull; Timestamp: ${rep.submitted_at}<br>
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

  renderBaselineResults(guidance) {
    const resultsContainer = document.getElementById('results-view');
    resultsContainer.style.display = 'block';

    UI.renderReadinessCard(guidance.readiness || {}, document.getElementById('readiness-gauge-container'));
    UI.renderFeeCard(guidance.fees || {}, document.getElementById('fee-card-container'));
    UI.renderNextSteps(guidance.next_steps || [], document.getElementById('next-steps-container'));
    UI.renderSourcesList(
      guidance.sources || [],
      guidance.flagged_sources || [],
      document.getElementById('sources-list-container')
    );
    UI.renderTrackingStatus(guidance.tracking || {}, document.getElementById('tracking-status-container'));
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
}

document.addEventListener('DOMContentLoaded', () => {
  const app = new ReclaimApp();
  app.init();
});
