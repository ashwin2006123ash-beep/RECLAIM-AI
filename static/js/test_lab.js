/**
 * RECLAIM AI - Test Laboratory Controller
 * Manages automated execution of TC1, TC2, TC3, TC4 with inspector views
 */

import { API } from './api.js';
import { UI } from './ui.js';

export const TestLab = {
  scenarios: [],
  testResults: {},

  async init(containerEl) {
    if (!containerEl) return;
    this.container = containerEl;
    await this.loadScenarios();
    this.render();
  },

  async loadScenarios() {
    try {
      const data = await API.getTests();
      if (data.status === 'success') {
        this.scenarios = data.scenarios || [];
        // Map any latest runs
        this.scenarios.forEach(sc => {
          if (sc.latest_run) {
            this.testResults[sc.scenario_id] = sc.latest_run;
          }
        });
      }
    } catch (e) {
      console.error('Failed to load test scenarios:', e);
    }
  },

  render() {
    this.container.innerHTML = `
      <div class="test-lab-header">
        <span class="panel-step-badge" style="background: rgba(59,130,246,0.15); color: #93c5fd; border-color: rgba(59,130,246,0.3); margin-bottom: 12px; display: inline-block;">
          OFFICIAL HACKATHON VERIFICATION SUITE
        </span>
        <h2 style="font-size: 2rem; margin-bottom: 8px;">Interactive Test Laboratory</h2>
        <p style="max-width: 700px; margin: 0 auto 24px;">
          Deterministic verification of the 4 official hackathon problem scenarios. 
          Run individual tests or execute the full test suite with genuine agent state verification.
        </p>
        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
          <button id="btn-run-all-tests" class="btn btn-primary">
            ▶ Run Complete Test Suite (TC1–TC4)
          </button>
          <button id="btn-refresh-tests" class="btn btn-secondary">
            ↻ Refresh Results
          </button>
        </div>
      </div>

      <div class="test-scenarios-grid" id="test-cards-grid">
        ${this.scenarios.map(sc => this.renderTestCard(sc)).join('')}
      </div>

      <div id="inspector-container"></div>
    `;

    document.getElementById('btn-run-all-tests')?.addEventListener('click', () => this.runSuite('ALL'));
    document.getElementById('btn-refresh-tests')?.addEventListener('click', async () => {
      await this.loadScenarios();
      this.render();
      UI.showToast('Test results refreshed.', 'info');
    });

    // Attach individual scenario run listeners
    this.scenarios.forEach(sc => {
      document.getElementById(`btn-run-${sc.scenario_id}`)?.addEventListener('click', () => {
        this.runSuite(sc.scenario_id);
      });
      document.getElementById(`btn-inspect-${sc.scenario_id}`)?.addEventListener('click', () => {
        this.showInspector(sc.scenario_id);
      });
    });
  },

  renderTestCard(sc) {
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

  async runSuite(targetId) {
    UI.showToast(`Executing test scenario: ${targetId}...`, 'info');
    try {
      const res = await API.runTests(targetId);
      if (res.status === 'success') {
        res.results.forEach(r => {
          this.testResults[r.scenario_id] = r;
        });
        this.render();
        UI.showToast(`Completed test execution: ${targetId} (${res.executed_count} scenarios verified).`, 'success');
        if (targetId !== 'ALL') {
          this.showInspector(targetId);
        }
      } else {
        UI.showToast(`Test execution failed: ${res.message}`, 'error');
      }
    } catch (e) {
      UI.showToast(`Network or server error running tests: ${e.message}`, 'error');
    }
  },

  showInspector(scenarioId) {
    const inspectorEl = document.getElementById('inspector-container');
    if (!inspectorEl) return;
    const sc = this.scenarios.find(s => s.scenario_id === scenarioId);
    const res = this.testResults[scenarioId];
    if (!sc) return;

    inspectorEl.innerHTML = `
      <div class="inspector-panel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 12px;">
          <div>
            <h3 style="font-size: 1.2rem;">🔬 Test Inspector: ${sc.scenario_id} — ${sc.title}</h3>
            <span class="test-status-pill ${res?.status === 'PASS' ? 'pass' : (res?.status === 'FAIL' ? 'fail' : 'pending')}">
              STATUS: ${res?.status || 'AWAITING RUN'}
            </span>
          </div>
          <button id="btn-close-inspector" class="btn btn-secondary btn-sm">✕ Close Inspector</button>
        </div>

        <table class="inspector-table">
          <tr>
            <th style="width: 20%;">Dimension</th>
            <th>Details & Verified Evidence</th>
          </tr>
          <tr>
            <td><strong>Description</strong></td>
            <td>${sc.description}</td>
          </tr>
          <tr>
            <td><strong>Expected Result</strong></td>
            <td style="color: #93c5fd;">${sc.expected_summary}</td>
          </tr>
          <tr>
            <td><strong>Actual Agent Output</strong></td>
            <td style="color: ${res?.status === 'PASS' ? '#34d399' : '#f87171'}; font-weight: 500;">
              ${res ? res.actual : 'Test has not been executed in this session yet.'}
            </td>
          </tr>
          <tr>
            <td><strong>Audit Evidence</strong></td>
            <td>
              ${res && res.evidence ? (Array.isArray(res.evidence) ? res.evidence.map(e => `<div>&bull; ${e}</div>`).join('') : res.evidence) : 'N/A'}
            </td>
          </tr>
        </table>
      </div>
    `;

    document.getElementById('btn-close-inspector')?.addEventListener('click', () => {
      inspectorEl.innerHTML = '';
    });
  }
};
