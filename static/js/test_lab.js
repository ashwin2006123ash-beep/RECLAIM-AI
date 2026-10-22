/**
 * RECLAIM AI 2.0 - Test Laboratory & Adversarial Safety Lab Controller
 * Supports dual testing suites:
 * 1. Official Hackathon Scenarios (TC1, TC2, TC3, TC4)
 * 2. Adversarial Safety Test Lab (7 Synthetic Cybersecurity & Fraud Scenarios)
 */

import { API } from './api.js';
import { UI } from './ui.js';

export const TestLab = {
  scenarios: [],
  testResults: {},
  adversarialScenarios: [],
  adversarialResults: {},
  activeTab: 'official', // 'official' or 'adversarial'

  async init(containerEl) {
    if (!containerEl) return;
    this.container = containerEl;
    await this.loadOfficialScenarios();
    await this.loadAdversarialScenarios();
    this.render();
  },

  async loadOfficialScenarios() {
    try {
      const data = await API.getTests();
      if (data.status === 'success') {
        this.scenarios = data.scenarios || [];
        this.scenarios.forEach(sc => {
          if (sc.latest_run) {
            this.testResults[sc.scenario_id] = sc.latest_run;
          }
        });
      }
    } catch (e) {
      console.error('Failed to load official test scenarios:', e);
    }
  },

  async loadAdversarialScenarios() {
    try {
      const data = await API.getAdversarialScenarios();
      if (data.status === 'success') {
        this.adversarialScenarios = data.scenarios || [];
      }
    } catch (e) {
      console.error('Failed to load adversarial scenarios:', e);
    }
  },

  render() {
    this.container.innerHTML = `
      <div class="test-lab-header">
        <span class="panel-step-badge" style="background: rgba(59,130,246,0.15); color: #93c5fd; border-color: rgba(59,130,246,0.3); margin-bottom: 12px; display: inline-block;">
          TEST LABORATORY & CIVIC SAFETY EVALUATION
        </span>
        <h2 style="font-size: 2rem; margin-bottom: 8px;">Interactive Test Laboratory</h2>
        <p style="max-width: 740px; margin: 0 auto 20px;">
          Deterministic verification of the 4 official hackathon problem statements and 7 adversarial cybersecurity scenarios.
        </p>

        <!-- Suite Switcher Tabs -->
        <div style="display: flex; justify-content: center; gap: 8px; margin-bottom: 20px;">
          <button id="tab-btn-official" class="tab-btn ${this.activeTab === 'official' ? 'active' : ''}">
            📋 Official Hackathon Cases (TC1–TC4)
          </button>
          <button id="tab-btn-adversarial" class="tab-btn ${this.activeTab === 'adversarial' ? 'active' : ''}">
            🛡️ Adversarial Safety Test Lab (7 Scenarios)
          </button>
        </div>

        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
          <button id="btn-run-all-tests" class="btn btn-primary">
            ▶ Run Selected Suite (${this.activeTab === 'official' ? 'TC1–TC4' : '7 Adversarial Tests'})
          </button>
          <button id="btn-refresh-tests" class="btn btn-secondary">
            ↻ Refresh Suite
          </button>
        </div>
      </div>

      <div class="test-scenarios-grid" id="test-cards-grid">
        ${this.activeTab === 'official'
          ? this.scenarios.map(sc => this.renderOfficialCard(sc)).join('')
          : this.adversarialScenarios.map(adv => this.renderAdversarialCard(adv)).join('')
        }
      </div>

      <div id="inspector-container"></div>
    `;

    // Tab Switchers
    document.getElementById('tab-btn-official')?.addEventListener('click', () => {
      this.activeTab = 'official';
      this.render();
    });

    document.getElementById('tab-btn-adversarial')?.addEventListener('click', () => {
      this.activeTab = 'adversarial';
      this.render();
    });

    // Run All button
    document.getElementById('btn-run-all-tests')?.addEventListener('click', () => {
      if (this.activeTab === 'official') {
        this.runOfficialSuite('ALL');
      } else {
        this.runAdversarialSuite('ALL');
      }
    });

    // Refresh
    document.getElementById('btn-refresh-tests')?.addEventListener('click', async () => {
      await this.loadOfficialScenarios();
      await this.loadAdversarialScenarios();
      this.render();
      UI.showToast('Test results refreshed.', 'info');
    });

    // Attach card action listeners
    if (this.activeTab === 'official') {
      this.scenarios.forEach(sc => {
        document.getElementById(`btn-run-${sc.scenario_id}`)?.addEventListener('click', () => {
          this.runOfficialSuite(sc.scenario_id);
        });
        document.getElementById(`btn-inspect-${sc.scenario_id}`)?.addEventListener('click', () => {
          this.showInspector(sc.scenario_id, 'official');
        });
      });
    } else {
      this.adversarialScenarios.forEach(adv => {
        document.getElementById(`btn-run-${adv.id}`)?.addEventListener('click', () => {
          this.runAdversarialSuite(adv.id);
        });
        document.getElementById(`btn-inspect-${adv.id}`)?.addEventListener('click', () => {
          this.showInspector(adv.id, 'adversarial');
        });
      });
    }
  },

  renderOfficialCard(sc) {
    const res = this.testResults[sc.scenario_id];
    const status = res ? res.status : 'PENDING';
    const statusClass = status === 'PASS' ? 'pass' : (status === 'FAIL' ? 'fail' : 'pending');

    return `
      <div class="test-card">
        <div class="test-card-top">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <span class="test-card-tag">${sc.scenario_id}</span>
            <span class="test-status-pill ${statusClass}">${status}</span>
          </div>
          <h3>${sc.title.split('—')[1] || sc.title}</h3>
          <p>${sc.description}</p>
        </div>
        <div>
          <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 12px; background: rgba(0,0,0,0.2); padding: 8px 10px; border-radius: 6px;">
            <strong>Expected:</strong> ${sc.expected_summary}
          </div>
          <div style="display: flex; gap: 8px;">
            <button id="btn-run-${sc.scenario_id}" class="btn btn-secondary btn-sm" style="flex: 1;">
              ▶ Run Test
            </button>
            <button id="btn-inspect-${sc.scenario_id}" class="btn btn-secondary btn-sm" style="padding: 6px 10px;">
              🔍 Inspect
            </button>
          </div>
        </div>
      </div>
    `;
  },

  renderAdversarialCard(adv) {
    const res = this.adversarialResults[adv.id];
    const status = res ? res.status : 'PENDING';
    const statusClass = status === 'PASS' ? 'pass' : (status === 'FAIL' ? 'fail' : 'pending');

    return `
      <div class="test-card">
        <div class="test-card-top">
          <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <span class="test-card-tag" style="background: rgba(244,63,94,0.15); color: #fb7185;">${adv.id.replace('ADV_', 'SEC-')}</span>
            <span class="test-status-pill ${statusClass}">${status}</span>
          </div>
          <h3>${adv.title}</h3>
          <p style="font-size: 0.78rem; color: var(--text-muted);">${adv.description}</p>
        </div>
        <div>
          <div style="font-size: 0.76rem; color: var(--text-secondary); margin-bottom: 10px; background: rgba(0,0,0,0.25); padding: 6px 8px; border-radius: 4px; font-family: var(--font-mono);">
            Target: ${adv.test_target.slice(0, 36)}...
          </div>
          <div style="display: flex; gap: 8px;">
            <button id="btn-run-${adv.id}" class="btn btn-secondary btn-sm" style="flex: 1;">
              ▶ Test Defense
            </button>
            <button id="btn-inspect-${adv.id}" class="btn btn-secondary btn-sm" style="padding: 6px 10px;">
              🔍 Audit
            </button>
          </div>
        </div>
      </div>
    `;
  },

  async runOfficialSuite(targetId) {
    UI.showToast(`Executing official scenario: ${targetId}...`, 'info');
    try {
      const res = await API.runTests(targetId);
      if (res.status === 'success') {
        res.results.forEach(r => {
          this.testResults[r.scenario_id] = r;
        });
        this.render();
        UI.showToast(`Official verification complete: ${res.executed_count} scenarios executed.`, 'success');
      }
    } catch (e) {
      UI.showToast(`Test execution failed: ${e.message}`, 'error');
    }
  },

  async runAdversarialSuite(targetId) {
    UI.showToast(`Executing adversarial security test: ${targetId}...`, 'info');
    try {
      const res = await API.runAdversarialTests(targetId);
      if (res.status === 'success') {
        res.results.forEach(r => {
          this.adversarialResults[r.scenario_id] = r;
        });
        this.render();
        UI.showToast(`Security suite complete: ${res.passed_count}/${res.executed_count} passed.`, 'success');
      }
    } catch (e) {
      UI.showToast(`Adversarial test failed: ${e.message}`, 'error');
    }
  },

  showInspector(targetId, type = 'official') {
    const container = document.getElementById('inspector-container');
    if (!container) return;

    if (type === 'official') {
      const sc = this.scenarios.find(s => s.scenario_id === targetId);
      const res = this.testResults[targetId];
      if (!sc) return;

      container.innerHTML = `
        <div class="inspector-panel">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <h3 style="font-size: 1.1rem; color: var(--text-highlight);">
              Audit Inspector — ${sc.title}
            </h3>
            <button id="btn-close-inspector" class="btn btn-secondary btn-sm">✕ Close</button>
          </div>
          <table class="inspector-table">
            <tr><th style="width: 25%;">Scenario ID:</th><td><code>${sc.scenario_id}</code></td></tr>
            <tr><th>Status:</th><td><span class="test-status-pill ${(res?.status || '').toLowerCase()}">${res?.status || 'NOT RUN'}</span></td></tr>
            <tr><th>Expected Result:</th><td>${sc.expected_summary}</td></tr>
            <tr><th>Actual Agent Outcome:</th><td>${res?.actual || 'Test has not been executed yet in this session.'}</td></tr>
            <tr><th>Supporting Evidence:</th><td>${(res?.evidence || []).map(e => `<div>&bull; ${e}</div>`).join('') || 'None'}</td></tr>
          </table>
        </div>
      `;
    } else {
      const adv = this.adversarialScenarios.find(a => a.id === targetId);
      const res = this.adversarialResults[targetId];
      if (!adv) return;

      container.innerHTML = `
        <div class="inspector-panel">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <h3 style="font-size: 1.1rem; color: var(--text-highlight);">
              Cybersecurity Audit Inspector — ${adv.title}
            </h3>
            <button id="btn-close-inspector" class="btn btn-secondary btn-sm">✕ Close</button>
          </div>
          <table class="inspector-table">
            <tr><th style="width: 25%;">Threat Category:</th><td><code>${adv.category}</code></td></tr>
            <tr><th>Target Vector:</th><td><code>${adv.test_target}</code></td></tr>
            <tr><th>Defense Status:</th><td><span class="test-status-pill ${(res?.status || '').toLowerCase()}">${res?.status || 'NOT RUN'}</span></td></tr>
            <tr><th>Expected Defense:</th><td>${res?.expected || 'Interception by allowlist / SSRF / Idempotency boundary.'}</td></tr>
            <tr><th>Actual Audit Finding:</th><td>${res?.actual || 'Security test has not been executed yet in this session.'}</td></tr>
            <tr><th>Evidence Trail:</th><td>${(res?.evidence || []).map(e => `<div>&bull; ${e}</div>`).join('') || 'None'}</td></tr>
          </table>
        </div>
      `;
    }

    document.getElementById('btn-close-inspector')?.addEventListener('click', () => {
      container.innerHTML = '';
    });
    container.scrollIntoView({ behavior: 'smooth' });
  }
};
