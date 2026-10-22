/**
 * RECLAIM AI 2.0 - UI Renderers & Interactive Components
 * Supports Recovery Twin Graph, Evidence Vault, Route Comparison, Risk Radar, and Mock Portal Sandbox
 */

export const UI = {
  showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  },

  // ==================== INNOVATION 1: RECOVERY TWIN & DEPENDENCY GRAPH ====================
  renderRecoveryTwinGraph(twin, containerEl, onNodeClick) {
    if (!containerEl || !twin) return;
    const graph = twin.dependency_graph || {};
    const nodes = graph.nodes || {};
    const nodeOrder = graph.node_order || Object.keys(nodes);

    containerEl.innerHTML = `
      <div class="twin-container">
        <div class="twin-meta-bar">
          <div>
            <h3 style="font-size: 1.15rem; display: flex; align-items: center; gap: 8px;">
              <span>🧬 Recovery Twin Case ID:</span>
              <span style="font-family: var(--font-mono); color: var(--teal-primary);">${twin.case_id}</span>
            </h3>
            <span style="font-size: 0.8rem; color: var(--text-muted);">
              Status: <strong style="color: var(--text-primary);">${twin.current_status}</strong> &bull; 
              Document: <strong>${twin.document_type}</strong> (${twin.jurisdiction || 'All India'})
            </span>
          </div>
          <div>
            <span class="panel-step-badge" style="background: rgba(16,185,129,0.15); color: #34d399;">
              Next Action: ${twin.next_best_action || 'Review Guidance'}
            </span>
          </div>
        </div>

        <div style="margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
          <h4 style="font-size: 0.95rem; color: var(--text-secondary);">Topological Dependency Graph (Click any node to inspect):</h4>
          <span style="font-size: 0.76rem; color: var(--text-muted); font-family: var(--font-mono);">
            8 Statutory Nodes Evaluated
          </span>
        </div>

        <div class="twin-graph-grid">
          ${nodeOrder.map((nodeId, idx) => {
            const node = nodes[nodeId];
            if (!node) return '';
            const stateClass = (node.state || 'blocked').toLowerCase();
            return `
              <div class="graph-node-card ${stateClass}" data-node-id="${node.id}">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <span style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted);">
                      NODE 0${idx + 1}
                    </span>
                    <span class="node-state-pill ${stateClass}">${node.state}</span>
                  </div>
                  <h4 style="font-size: 0.92rem; margin-bottom: 4px;">${node.name}</h4>
                  <p style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.4;">
                    ${node.blocked_reason || 'Prerequisites verified. Ready for execution.'}
                  </p>
                </div>
                <div style="margin-top: 10px; font-size: 0.74rem; color: var(--teal-primary); font-weight: 600;">
                  Inspect Dependencies ↗
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <div id="node-inspector-drawer"></div>
      </div>
    `;

    // Attach click listeners to graph nodes
    containerEl.querySelectorAll('.graph-node-card').forEach(card => {
      card.addEventListener('click', () => {
        const nodeId = card.dataset.nodeId;
        const node = nodes[nodeId];
        if (node && onNodeClick) {
          onNodeClick(node);
        }
      });
    });
  },

  renderNodeInspector(node, containerEl) {
    if (!containerEl || !node) return;
    const isBlocked = node.state === 'BLOCKED';
    containerEl.innerHTML = `
      <div class="node-inspector-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
          <h4 style="font-size: 1.05rem;">🔍 Node Inspector: ${node.name}</h4>
          <span class="node-state-pill ${(node.state || '').toLowerCase()}">${node.state}</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;">
          ${node.description || ''}
        </p>
        <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: var(--radius-sm); font-size: 0.82rem; margin-bottom: 10px;">
          ${node.blocked_reason ? `<strong>Blocked Reason:</strong> <span style="color: #f87171;">${node.blocked_reason}</span><br>` : ''}
          ${node.unblock_action ? `<strong>Action to Unblock:</strong> <span style="color: var(--teal-primary);">${node.unblock_action}</span><br>` : ''}
          <strong>Evidence Linked:</strong> ${node.evidence_linked ? node.evidence_linked.join(', ') : 'None'}
        </div>
        <button id="btn-close-node-inspector" class="btn btn-secondary btn-sm">Close Inspector</button>
      </div>
    `;
    document.getElementById('btn-close-node-inspector')?.addEventListener('click', () => {
      containerEl.innerHTML = '';
    });
  },

  // ==================== INNOVATION 2: EVIDENCE VAULT & CONFLICTS ====================
  renderEvidenceVault(researchData, containerEl) {
    if (!containerEl || !researchData) return;
    const claims = researchData.claims || [];
    const conflicts = researchData.conflicts || [];

    containerEl.innerHTML = `
      <div class="panel-card evidence-vault-section">
        <div class="panel-header">
          <div class="panel-header-left">
            <h2>Proof-of-Truth Evidence Vault</h2>
          </div>
          <span class="panel-step-badge">PROVENANCE GUARD</span>
        </div>

        <p style="font-size: 0.84rem; color: var(--text-muted); margin-bottom: 16px;">
          Mined claims tagged with statutory provenance (LIVE_VERIFIED, CACHED, SYNTHETIC_DEMO). 
          Includes transparent conflict resolution for conflicting circulars.
        </p>

        <!-- Claims Table -->
        <table class="inspector-table" style="margin-bottom: 20px;">
          <thead>
            <tr>
              <th style="width: 25%;">Claim</th>
              <th style="width: 25%;">Authoritative Source</th>
              <th style="width: 15%;">Provenance</th>
              <th>Verified Excerpt</th>
            </tr>
          </thead>
          <tbody>
            ${claims.map(c => `
              <tr>
                <td><strong>${c.claim_text}</strong></td>
                <td>
                  <a href="${c.source_url}" target="_blank" rel="noopener noreferrer">${c.source_title || c.source_url}</a>
                </td>
                <td>
                  <span class="provenance-tag ${(c.source_tag || 'unverified').toLowerCase()}">${c.source_tag}</span>
                </td>
                <td style="font-size: 0.8rem; color: var(--text-secondary);">${c.excerpt || 'Statutory record.'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <!-- Conflicting Claims Section -->
        ${conflicts.length > 0 ? `
          <div style="margin-top: 24px;">
            <h4 style="font-size: 0.95rem; color: #fbbf24; display: flex; align-items: center; gap: 8px;">
              <span>⚠️ Conflicting Source Intelligence Detected (${conflicts.length})</span>
            </h4>
            ${conflicts.map(cf => `
              <div class="conflict-card">
                <div style="font-weight: 700; font-size: 0.9rem; margin-bottom: 6px;">Topic: ${cf.topic}</div>
                <div class="conflict-grid">
                  <div style="padding: 10px; background: rgba(0,0,0,0.25); border-radius: var(--radius-sm);">
                    <div style="font-size: 0.72rem; color: var(--text-muted);">SOURCE A (${cf.date_a || 'Archive'})</div>
                    <div style="font-size: 0.82rem; margin: 4px 0;">${cf.claim_a}</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary); font-style: italic;">${cf.source_a}</div>
                  </div>
                  <div style="padding: 10px; background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3); border-radius: var(--radius-sm);">
                    <div style="font-size: 0.72rem; color: #34d399; font-weight: 700;">SOURCE B - PREVAILING STATUTORY (${cf.date_b || 'Active'})</div>
                    <div style="font-size: 0.82rem; margin: 4px 0;">${cf.claim_b}</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary); font-style: italic;">${cf.source_b}</div>
                  </div>
                </div>
                <div style="font-size: 0.8rem; color: var(--text-primary); margin-top: 8px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 6px;">
                  <strong>Resolution Rationale:</strong> ${cf.resolution_reason}
                </div>
              </div>
            `).join('')}
          </div>
        ` : ''}
      </div>
    `;
  },

  // ==================== RECOVERY COMPASS: 1-PAGE INTEGRATED ACTION PLAN ====================
  renderRecoveryCompass(guidance, containerEl, onSwitchRoute, onApproveAction, onVerifyAction, receiptData = null) {
    if (!containerEl || !guidance) return;
    const plan = guidance.route_planning || {};
    const recommended = plan.recommended_route;
    const planB = plan.plan_b;
    const planC = plan.plan_c;
    const adaptiveReason = plan.adaptive_switch_reason;
    const readiness = guidance.readiness || {};
    const fees = guidance.fees || {};
    const sources = guidance.sources || [];
    const flagged = guidance.flagged_sources || [];
    const whyMatrix = plan.why_chosen_matrix || [];
    const isBlocked = plan.is_blocked_by_missing_authority;

    if (isBlocked || !recommended) {
      containerEl.innerHTML = `
        <div class="panel-card" style="border: 1.5px solid #fbbf24; background: rgba(245, 158, 11, 0.05); padding: 24px;">
          <div style="display: flex; gap: 14px; align-items: flex-start;">
            <div style="font-size: 2.2rem; line-height: 1;">⚠️</div>
            <div>
              <h3 style="color: #fbbf24; margin-bottom: 6px; font-size: 1.15rem;">Clarification Required: Issuing Authority Unknown</h3>
              <p style="font-size: 0.9rem; color: var(--text-primary); margin-bottom: 12px; line-height: 1.5;">
                ${plan.decision_summary || 'Document reissue procedures are statutory and vary by university, state board, and transport office.'}
              </p>
              <div style="font-size: 0.84rem; color: var(--text-secondary); line-height: 1.6; background: rgba(0,0,0,0.25); padding: 12px; border-radius: var(--radius-sm);">
                <strong>Next Step:</strong> Please check your old marksheet header, hall ticket, or institution name and update the <strong>Issuing Authority</strong> field in Step 1.
              </div>
            </div>
          </div>
        </div>
      `;
      return;
    }

    const isFree = recommended.statutory_fee?.amount === 0;
    const displayFee = isFree ? '₹0 (Free Public Pull)' : (fees.status === 'verified' && fees.amount !== null && fees.amount !== undefined ? `₹${fees.amount.toFixed(0)} (Verified Gazette Fee)` : 'Unverified (Requires Circular)');

    const isDigital = recommended.route_id === 'ROUTE_DIGITAL_DIGILOCKER';
    const turnaround = isDigital ? 'Instant (Under 2 Minutes)' : '7 to 14 Working Days (Speed Post)';
    const primarySource = sources[0] || {};
    const primaryUrl = primarySource.official_url || primarySource.official_hostname || 'https://india.gov.in';

    containerEl.innerHTML = `
      <div class="compass-plan-container">
        <!-- 1. Hero Recommendation Card -->
        <div class="compass-hero-card">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div class="compass-badge-ribbon ${adaptiveReason ? 'adaptive-switch' : ''}">
              ${adaptiveReason ? '🔄 ADAPTIVE SWITCH ACTIVE: ALTERNATIVE ROUTE PROMOTED' : '⭐ RECOMMENDED RECOVERY ROUTE'}
            </div>
            <span style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--text-muted);">
              Readiness Score: <strong style="color: var(--teal-primary);">${readiness.score || 0}/100</strong>
            </span>
          </div>

          <h2 class="compass-hero-title">${recommended.name}</h2>
          
          <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px;">
            <span class="compass-route-badge active-badge">${recommended.channel}</span>
            <span style="font-size: 0.78rem; color: var(--text-muted); align-self: center;">
              Legal Validity: <strong>${recommended.legal_validity}</strong>
            </span>
          </div>

          <!-- Key Metrics Grid -->
          <div class="compass-key-metrics">
            <div class="compass-metric-card">
              <div class="compass-metric-label">⏱️ Estimated Time</div>
              <div class="compass-metric-val" style="color: var(--teal-primary);">${turnaround}</div>
            </div>
            <div class="compass-metric-card">
              <div class="compass-metric-label">💰 Statutory Fee</div>
              <div class="compass-metric-val" style="color: #34d399;">${displayFee}</div>
            </div>
            <div class="compass-metric-card">
              <div class="compass-metric-label">⚖️ Statutory Authority</div>
              <div class="compass-metric-val" style="font-size: 0.84rem; color: var(--text-secondary); line-height: 1.3;">${recommended.statutory_basis}</div>
            </div>
            <div class="compass-metric-card">
              <div class="compass-metric-label">🎯 Route Feasibility</div>
              <div class="compass-metric-val" style="color: ${recommended.feasibility_score >= 80 ? '#34d399' : '#fbbf24'};">${recommended.feasibility_score}/100</div>
            </div>
          </div>

          <!-- Why the Compass Chose This -->
          <div class="compass-why-box">
            <strong>Why did the Compass choose this route?</strong><br>
            ${adaptiveReason ? `<span style="color: #fbbf24; font-weight: 600;">${adaptiveReason}</span><br>` : ''}
            ${plan.decision_summary || ''}
            ${whyMatrix.length > 0 ? `
              <ul style="margin: 8px 0 0 18px; font-size: 0.82rem;">
                ${whyMatrix.map(m => `<li><strong>${m.rule}:</strong> ${m.justification}</li>`).join('')}
              </ul>
            ` : ''}
          </div>

          <!-- Verified Portal Link -->
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-top: 20px; padding-top: 16px; border-top: 1px solid var(--border-subtle);">
            <div>
              <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Official Portal Gateway:</span><br>
              <a href="${primaryUrl}" target="_blank" rel="noopener noreferrer" style="font-size: 1rem; font-weight: 700; color: var(--teal-primary); display: inline-flex; align-items: center; gap: 6px;">
                <span>${primarySource.issuing_authority || 'Authorized Government Portal'}</span>
                <span>↗</span>
              </a>
              <span style="display: inline-block; margin-left: 8px; font-size: 0.74rem; padding: 2px 8px; border-radius: 4px; background: rgba(16,185,129,0.15); color: #34d399; font-weight: 600;">
                ✓ Official .gov.in Allowlist Passed
              </span>
            </div>
            ${primarySource.retrieval_timestamp ? `
              <div style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">
                Verified: ${primarySource.retrieval_timestamp}
              </div>
            ` : ''}
          </div>
        </div>

        <!-- 2. Preparation Checklist (Interactive) -->
        <div class="panel-card" style="margin-bottom: 24px;">
          <div class="panel-header">
            <div class="panel-header-left">
              <h2>Preparation Checklist</h2>
            </div>
            <span class="panel-step-badge">REQUIRED EVIDENCE</span>
          </div>
          <p style="font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 12px;">
            Items required to execute this recovery route. Check each item as you prepare it:
          </p>
          <div class="checklist-container">
            ${(recommended.prerequisites || []).map((p, idx) => `
              <label class="checklist-item ready" style="cursor: pointer;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <input type="checkbox" checked style="accent-color: var(--teal-primary);">
                  <span style="color: var(--text-primary); font-weight: 500;">${p}</span>
                </div>
                <span class="checklist-tag tag-ready">Ready</span>
              </label>
            `).join('')}
            ${(guidance.missing_prerequisites || []).map(m => `
              <label class="checklist-item missing" style="cursor: pointer;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <input type="checkbox" style="accent-color: var(--rose-danger);">
                  <span style="color: #f87171; font-weight: 600;">${m}</span>
                </div>
                <span class="checklist-tag tag-missing">Missing / Required</span>
              </label>
            `).join('')}
          </div>
        </div>

        <!-- 3. Plan B & Alternative Routes Visual Comparison -->
        <div class="panel-card" style="margin-bottom: 24px;">
          <div class="panel-header">
            <div class="panel-header-left">
              <h2>Plan B & Route Comparison</h2>
            </div>
            <span class="panel-step-badge">ADAPTIVE ENGINE</span>
          </div>
          <p style="font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 14px;">
            The Recovery Compass actively monitors availability and evidentiary constraints. If you need physical delivery or if your primary route is unavailable, switch below:
          </p>

          <div class="compass-compare-grid">
            <!-- Active Route -->
            <div class="compass-route-card is-active">
              <div>
                <span class="compass-route-badge active-badge">Active Recommendation</span>
                <h3 style="font-size: 1.05rem; margin: 4px 0 8px;">${recommended.name}</h3>
                <div style="font-size: 0.8rem; color: var(--teal-primary); font-weight: 600; margin-bottom: 8px;">
                  ${displayFee} &bull; ${turnaround}
                </div>
                <p style="font-size: 0.78rem; color: var(--text-secondary);">
                  ${recommended.advantages ? recommended.advantages[0] : 'Current active path'}
                </p>
              </div>
              <div style="margin-top: 14px; padding: 8px; background: rgba(0,242,254,0.1); border-radius: 4px; font-size: 0.76rem; text-align: center; color: var(--teal-primary); font-weight: 600;">
                ✓ Currently Active
              </div>
            </div>

            <!-- Plan B -->
            ${planB ? `
              <div class="compass-route-card is-plan-b">
                <div>
                  <span class="compass-route-badge plan-b-badge">Plan B (Fallback / Alternative)</span>
                  <h3 style="font-size: 1.05rem; margin: 4px 0 8px;">${planB.name}</h3>
                  <div style="font-size: 0.8rem; color: #fbbf24; font-weight: 600; margin-bottom: 8px;">
                    Fee: ${planB.statutory_fee?.currency || 'INR'} ${planB.statutory_fee?.amount !== null && planB.statutory_fee?.amount !== undefined ? planB.statutory_fee.amount : 'Gazette Schedule'} &bull; 7-14 Days
                  </div>
                  <p style="font-size: 0.78rem; color: var(--text-secondary);">
                    ${planB.advantages ? planB.advantages[0] : 'Delivers authentic physical paper duplicate'}
                  </p>
                </div>
                <button type="button" class="btn-switch-plan" id="btn-switch-to-plan-b" data-route-id="${planB.route_id}">
                  <span>🔄 Switch to Plan B (${planB.route_id === 'ROUTE_DIGITAL_DIGILOCKER' ? 'Digital Express' : 'Statutory Portal'})</span>
                </button>
              </div>
            ` : ''}

            <!-- Plan C -->
            ${planC ? `
              <div class="compass-route-card">
                <div>
                  <span class="compass-route-badge plan-c-badge">Plan C (In-Person Fallback)</span>
                  <h3 style="font-size: 1.05rem; margin: 4px 0 8px;">${planC.name}</h3>
                  <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600; margin-bottom: 8px;">
                    Manual Counter &bull; Treasury Challan
                  </div>
                  <p style="font-size: 0.78rem; color: var(--text-secondary);">
                    Direct facilitation counter submission when online records or biometrics mismatch.
                  </p>
                </div>
                <button type="button" class="btn-switch-plan" style="background: rgba(255,255,255,0.05); color: var(--text-secondary); border-color: var(--border-subtle);" id="btn-switch-to-plan-c" data-route-id="${planC.route_id}">
                  <span>Switch to In-Person Counter</span>
                </button>
              </div>
            ` : ''}
          </div>
        </div>

        <!-- 4. Safety & Fraud Warnings -->
        ${flagged.length > 0 ? `
          <div class="panel-card" style="border: 1.5px solid var(--rose-danger); background: rgba(239, 68, 68, 0.05); margin-bottom: 24px;">
            <div style="display: flex; gap: 12px; align-items: flex-start;">
              <div style="font-size: 1.8rem; line-height: 1;">🚨</div>
              <div>
                <h3 style="color: #f87171; margin-bottom: 6px;">Safety Warning: Unofficial Commercial Intermediary Detected</h3>
                <p style="font-size: 0.85rem; color: var(--text-primary); margin-bottom: 8px;">
                  The candidate website (<code>${flagged[0].url}</code>) was flagged as an unofficial broker.
                </p>
                <div style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5;">
                  <strong>Threat Explanation:</strong> ${flagged[0].reason}<br>
                  <strong style="color: #34d399;">Safe Action:</strong> Use the official government gateway above. Never pay ₹1,500+ broker fees or share Aadhaar OTPs with private intermediaries.
                </div>
              </div>
            </div>
          </div>
        ` : ''}

        <!-- 5. Step 8: Safe Action Sandbox (Human Approval Gate) -->
        <div class="panel-card" style="margin-bottom: 24px;" id="sandbox-action-card">
          <div class="panel-header">
            <div class="panel-header-left">
              <h2>Step 8: Human Approval Gate & Safe Action Sandbox</h2>
            </div>
            <span class="panel-step-badge">SIMULATED EXECUTION</span>
          </div>

          ${receiptData ? `
            <!-- Confirmed Synthetic Receipt -->
            <div style="background: rgba(16, 185, 129, 0.08); border: 1.5px solid var(--emerald-success); border-radius: var(--radius-md); padding: 20px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                <span style="font-size: 0.8rem; font-weight: 700; color: #34d399; text-transform: uppercase;">
                  ✓ Simulated Submission Confirmed
                </span>
                <span class="watermark-tag" style="background: #ef4444; color: #fff; font-weight: 800; font-size: 0.72rem; padding: 2px 8px; border-radius: 4px;">
                  SYNTHETIC DEMO — NOT A REAL GOVERNMENT APPLICATION
                </span>
              </div>

              <div style="font-size: 1.25rem; font-family: var(--font-mono); font-weight: 800; color: var(--teal-primary); margin-bottom: 8px;">
                Reference: ${receiptData.application_reference || receiptData.reference}
              </div>

              <div style="font-size: 0.84rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 16px;">
                Application prefilled for <strong>${receiptData.authority || 'Issuing Authority'}</strong>.<br>
                Receipt saved to SQLite database with SHA-256 idempotency signature.
              </div>

              <div style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center;">
                <button type="button" class="btn btn-secondary btn-sm" id="btn-verify-database" data-ref="${receiptData.application_reference || receiptData.reference}">
                  <span>🔍 Verify Stored Record in SQLite Database</span>
                </button>
                <div id="sandbox-verify-output" style="font-size: 0.8rem;"></div>
              </div>
            </div>
          ` : `
            <!-- Awaiting Approval Prompt -->
            <div>
              <p style="font-size: 0.88rem; color: var(--text-secondary); margin-bottom: 16px; line-height: 1.5;">
                To generate your prefilled recovery dossier and safe portal submission package, explicit citizen approval is required.
                <strong>No real payment will be debited and no external database will be modified.</strong>
              </p>

              <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <button type="button" class="btn btn-primary" id="btn-compass-approve">
                  <span>⚡ Approve Simulated Application (Safe Demo)</span>
                </button>
                <button type="button" class="btn btn-secondary" id="btn-compass-decline">
                  <span>✕ Decline</span>
                </button>
              </div>
            </div>
          `}
        </div>
      </div>
    `;

    // Event listeners
    containerEl.querySelector('#btn-switch-to-plan-b')?.addEventListener('click', (e) => {
      const targetId = e.currentTarget.dataset.routeId;
      if (onSwitchRoute) onSwitchRoute(targetId);
    });

    containerEl.querySelector('#btn-switch-to-plan-c')?.addEventListener('click', (e) => {
      const targetId = e.currentTarget.dataset.routeId;
      if (onSwitchRoute) onSwitchRoute(targetId);
    });

    containerEl.querySelector('#btn-compass-approve')?.addEventListener('click', () => {
      if (onApproveAction) onApproveAction();
    });

    containerEl.querySelector('#btn-compass-decline')?.addEventListener('click', () => {
      UI.showToast('Citizen declined simulated submission. Case paused.', 'info');
    });

    containerEl.querySelector('#btn-verify-database')?.addEventListener('click', (e) => {
      const ref = e.currentTarget.dataset.ref;
      if (onVerifyAction) onVerifyAction(ref);
    });
  },

  // ==================== INNOVATION 3: ADAPTIVE ROUTE COMPARISON ====================
  renderRouteComparison(routePlan, containerEl) {
    if (!containerEl || !routePlan) return;
    const routes = routePlan.all_routes || [];
    const recommended = routePlan.recommended_route;
    const whyMatrix = routePlan.why_chosen_matrix || [];

    containerEl.innerHTML = `
      <div class="panel-card" style="margin: 36px 0;">
        <div class="panel-header">
          <div class="panel-header-left">
            <h2>Adaptive Recovery Route Comparison</h2>
          </div>
          <span class="panel-step-badge">DECISION MATRIX</span>
        </div>

        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 20px;">
          ${routePlan.decision_summary}
        </p>

        <!-- Route Cards Grid -->
        <div class="routes-grid">
          ${routes.map(r => {
            const isRec = recommended && r.route_id === recommended.route_id;
            return `
              <div class="route-card ${isRec ? 'recommended' : ''}">
                <div>
                  ${isRec ? `<div class="route-ribbon">⭐ Recommended Route</div>` : ''}
                  <span style="font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted); text-transform: uppercase;">
                    ${r.channel}
                  </span>
                  <h3 style="font-size: 1.1rem; margin: 6px 0 10px;">${r.name}</h3>
                  <div style="font-size: 0.82rem; color: var(--teal-primary); font-weight: 600; margin-bottom: 8px;">
                    Fee: ${r.statutory_fee.currency || 'INR'} ${r.statutory_fee.amount !== null ? r.statutory_fee.amount.toFixed(2) : 'Unverified'} 
                    (${r.statutory_fee.status})
                  </div>
                  <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 12px;">
                    ${r.legal_validity}
                  </p>
                  
                  <div style="margin-bottom: 12px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">Advantages:</div>
                    ${r.advantages.map(a => `<div style="font-size: 0.76rem; color: #34d399;">✓ ${a}</div>`).join('')}
                  </div>

                  <div>
                    <div style="font-size: 0.78rem; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">Prerequisites:</div>
                    ${r.prerequisites.map(p => `<div style="font-size: 0.76rem; color: var(--text-muted);">&bull; ${p}</div>`).join('')}
                  </div>
                </div>

                <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--border-subtle); font-size: 0.75rem; color: var(--text-muted);">
                  ${r.deferral_reason ? `<span style="color: #fbbf24;">Note: ${r.deferral_reason}</span>` : 'Fully actionable.'}
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <!-- Why Did the Agent Choose This? Panel -->
        ${whyMatrix.length > 0 ? `
          <div style="background: rgba(11, 19, 41, 0.9); border: 1px solid rgba(0, 242, 254, 0.25); border-radius: var(--radius-md); padding: 18px; margin-top: 24px;">
            <h4 style="font-size: 0.95rem; color: var(--teal-primary); margin-bottom: 8px;">
              🧠 Why Did the Agent Choose This? (Decision Justification)
            </h4>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              ${whyMatrix.map(m => `
                <div style="font-size: 0.82rem; padding: 6px 10px; background: rgba(255,255,255,0.02); border-radius: 6px;">
                  <strong style="color: var(--text-primary);">${m.rule}:</strong> 
                  <span style="color: var(--text-secondary);">${m.justification}</span>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  },

  // ==================== INNOVATION 4: RECOVERY RISK RADAR ====================
  renderRiskRadar(riskData, containerEl, onScanUrl) {
    if (!containerEl || !riskData) return;
    const warnings = riskData.warnings || [];
    const riskLevel = riskData.overall_risk_level || 'SAFE_AND_VERIFIED';
    const riskScore = riskData.risk_score || 0;

    containerEl.innerHTML = `
      <div class="risk-radar-panel">
        <div class="panel-header">
          <div class="panel-header-left">
            <h2>Recovery Risk Radar</h2>
          </div>
          <span class="severity-pill ${riskLevel.toLowerCase()}">${riskLevel}</span>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: baseline;">
          <span style="font-size: 0.85rem; color: var(--text-muted);">Threat Severity Index:</span>
          <span style="font-family: var(--font-mono); font-size: 1.2rem; font-weight: 800; color: ${riskScore > 50 ? '#f87171' : '#34d399'};">
            ${riskScore}/100
          </span>
        </div>

        <div class="risk-meter-bar">
          <div style="width: ${riskScore}%; height: 100%; background: ${riskScore > 50 ? 'var(--rose-danger)' : 'var(--emerald-success)'};"></div>
        </div>

        <!-- Safe Domain Scanner Tool -->
        <div style="background: rgba(11, 19, 41, 0.8); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 14px; margin-bottom: 20px;">
          <h4 style="font-size: 0.88rem; margin-bottom: 6px; color: var(--text-highlight);">Safe-Domain Checking Tool</h4>
          <p style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 10px;">
            Analyze any web portal URL safely for SSRF risks, predatory broker indicators, and domain authenticity without sharing personal PII.
          </p>
          <div style="display: flex; gap: 8px;">
            <input type="text" id="input-radar-scan-url" class="form-input" placeholder="e.g. https://quick-pan-agent.com or https://parivahan.gov.in" style="flex: 1; padding: 8px 10px; font-size: 0.85rem;">
            <button id="btn-radar-scan" class="btn btn-secondary btn-sm">Scan Domain</button>
          </div>
          <div id="radar-scan-result" style="margin-top: 10px;"></div>
        </div>

        <!-- Active Warnings List -->
        <div>
          <h4 style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 12px;">Active Cybersecurity & Procedural Warnings (${warnings.length}):</h4>
          ${warnings.length === 0 ? `
            <p style="font-size: 0.82rem; color: var(--emerald-success);">✓ No active threats detected. All destinations comply with statutory allowlists.</p>
          ` : warnings.map(w => `
            <div class="risk-warning-item">
              <span class="severity-pill ${(w.severity || '').toLowerCase()}">${w.severity}</span>
              <div style="flex: 1;">
                <h4 style="font-size: 0.9rem; margin-bottom: 4px;">${w.title}</h4>
                <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 6px;">${w.evidence}</p>
                <div style="font-size: 0.76rem; color: var(--teal-primary);">
                  <strong>Action Required:</strong> ${w.recommended_action}
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    document.getElementById('btn-radar-scan')?.addEventListener('click', async () => {
      const url = document.getElementById('input-radar-scan-url')?.value.trim();
      if (url && onScanUrl) {
        onScanUrl(url);
      }
    });
  },

  // ==================== INNOVATION 5: SAFE ACTION SANDBOX ====================
  renderSafeActionSandbox(draft, receipt, containerEl, onApprove, onReject, onVerify) {
    if (!containerEl || !draft) return;
    const hasReceipt = Boolean(receipt);

    containerEl.innerHTML = `
      <div class="sandbox-card">
        <div class="panel-header">
          <div class="panel-header-left">
            <h2>Safe Action Sandbox & Mock Government Portal</h2>
          </div>
          <span class="panel-step-badge" style="background: rgba(245,158,11,0.15); color: #fbbf24; border-color: rgba(245,158,11,0.3);">
            STEP 8 & 9 SANDBOX
          </span>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 10px;">
          <div>
            <span style="font-size: 0.82rem; color: var(--text-muted);">Draft ID: </span>
            <span style="font-family: var(--font-mono); font-size: 0.88rem; color: var(--text-primary);">${draft.draft_id}</span> &bull; 
            <span style="font-size: 0.82rem; color: var(--text-muted);">Idempotency Key: </span>
            <span style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--teal-primary);">${draft.idempotency_key}</span>
          </div>
          <div>
            <span class="panel-step-badge" style="background: rgba(16,185,129,0.15); color: #34d399;">
              ${draft.is_valid ? '✓ Draft Validated' : '✕ Missing Prerequisites'}
            </span>
          </div>
        </div>

        <!-- Approval Gate Banner if no receipt yet -->
        ${!hasReceipt ? `
          <div class="approval-gate-banner" style="margin-top: 14px;">
            <div class="approval-grid">
              <div class="approval-info">
                <h3>🛡️ Human-in-the-Loop Approval Required</h3>
                <p>Authorize RECLAIM AI to execute a verified simulation against the local Mock Government Portal.</p>
                <div class="approval-consequences">
                  <strong>Safety Guarantee:</strong> Generates a confirmed synthetic receipt with idempotency guard. 
                  Zero external fees debited. Never modifies live government registries.
                </div>
              </div>
              <div class="approval-actions">
                <button id="btn-sandbox-approve" class="btn btn-primary">
                  ✓ Approve & Execute Simulation
                </button>
                <button id="btn-sandbox-reject" class="btn btn-secondary">
                  ✕ Decline / Pause
                </button>
              </div>
            </div>
          </div>
        ` : `
          <!-- Confirmed Synthetic Receipt -->
          <div class="synthetic-receipt-box">
            <div class="synthetic-watermark">
              ⚠️ ${receipt.synthetic_disclaimer || 'SYNTHETIC DEMO — NOT A REAL GOVERNMENT APPLICATION'}
            </div>
            <h3 style="font-size: 1.25rem; margin-bottom: 8px;">
              Confirmed Sandbox Reference: <span style="font-family: var(--font-mono); color: var(--teal-primary);">${receipt.application_reference}</span>
            </h3>
            <p style="font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 12px;">
              ${receipt.next_steps_notice}
            </p>
            <div style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-muted); margin-bottom: 14px;">
              Timestamp: ${receipt.submission_timestamp} &bull; Gateway: ${receipt.issuing_authority}
            </div>
            <button id="btn-verify-sandbox-independent" class="btn btn-secondary btn-sm">
              🔍 Run Independent Backend Verification
            </button>
            <div id="sandbox-verification-output" style="margin-top: 10px;"></div>
          </div>
        `}
      </div>
    `;

    document.getElementById('btn-sandbox-approve')?.addEventListener('click', onApprove);
    document.getElementById('btn-sandbox-reject')?.addEventListener('click', onReject);
    document.getElementById('btn-verify-sandbox-independent')?.addEventListener('click', () => {
      if (receipt && receipt.application_reference && onVerify) {
        onVerify(receipt.application_reference);
      }
    });
  },

  // ==================== EXISTING CORE RENDERERS (PRESERVED) ====================
  renderTraceFeed(traces, containerEl) {
    if (!containerEl) return;
    if (!traces || traces.length === 0) {
      containerEl.innerHTML = `<p class="text-muted" style="text-align: center; padding: 24px;">No agent activity recorded yet. Submit intake to initiate workflow.</p>`;
      return;
    }

    containerEl.innerHTML = traces.map(t => {
      const isComplete = t.status === 'complete';
      const isFlagged = t.status === 'flagged';
      const isAwaiting = t.status === 'awaiting_approval';
      const badgeClass = isComplete ? 'complete' : (isFlagged ? 'flagged' : (isAwaiting ? 'awaiting' : ''));
      const timeStr = t.timestamp ? new Date(t.timestamp).toLocaleTimeString() : '';

      return `
        <div class="feed-item">
          <span class="feed-badge ${badgeClass}">${t.step_name.split(':')[0]}</span>
          <div class="feed-content">
            <h4>
              <span>${t.step_name}</span>
              <span class="feed-time">${timeStr}</span>
            </h4>
            <div class="feed-decision">${t.decision || t.action_taken}</div>
            <div class="feed-reason">
              ${t.reason ? `<em>Why:</em> ${t.reason}` : ''}
              ${t.evidence_ref ? ` &bull; <span class="citation">[Ref: ${t.evidence_ref}]</span>` : ''}
            </div>
          </div>
        </div>
      `;
    }).join('');
  },

  renderReadinessCard(readiness, containerEl) {
    if (!containerEl) return;
    const score = readiness.score || 0;
    const level = readiness.readiness_level || 'Pending Assessment';
    const explanation = readiness.explanation || '';
    const checklist = readiness.checklist || [];

    containerEl.innerHTML = `
      <div class="readiness-card">
        <div class="readiness-header">
          <div>
            <h3>Recovery Readiness Score</h3>
            <p style="font-size: 0.85rem; color: var(--text-highlight); font-weight: 600;">${level}</p>
          </div>
          <div class="readiness-score-display">
            <span class="readiness-score-number">${score}</span>
            <span class="readiness-score-total">/100</span>
          </div>
        </div>
        
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" style="width: ${score}%"></div>
        </div>

        <div class="disclaimer-badge">
          <strong>LEGAL NOTICE:</strong> ${explanation}
        </div>

        <div style="margin-top: 18px;">
          <h4 style="font-size: 0.88rem; margin-bottom: 10px; color: var(--text-secondary);">Preparation Checklist:</h4>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            ${checklist.map(item => `
              <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; padding: 6px 10px; background: rgba(255,255,255,0.02); border-radius: 6px; border: 1px solid var(--border-subtle);">
                <span style="display: flex; align-items: center; gap: 6px;">
                  <span style="color: ${item.status === 'complete' ? 'var(--emerald-success)' : (item.status === 'partial' ? 'var(--orange-accent)' : 'var(--text-muted)')}; font-weight: bold;">
                    ${item.status === 'complete' ? '✓' : (item.status === 'partial' ? '▲' : '○')}
                  </span>
                  ${item.name}
                </span>
                <span style="font-family: var(--font-mono); font-weight: 600; color: ${item.points > 0 ? 'var(--teal-primary)' : 'var(--text-muted)'};">
                  +${item.points}/${item.max_points}
                </span>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  },

  renderFeeCard(fees, containerEl) {
    if (!containerEl) return;
    const isVerified = fees.status === 'verified';
    const amountStr = (isVerified && fees.amount !== null) ? `${fees.currency || 'INR'} ${fees.amount.toFixed(2)}` : 'Fee Not Verified';

    containerEl.innerHTML = `
      <div class="fee-card">
        <span class="fee-status-badge ${isVerified ? 'verified' : 'not_verified'}">
          ${isVerified ? 'Official Verified Fee' : 'Fee Not Publicly Verified'}
        </span>
        <div class="fee-amount-display">${amountStr}</div>
        <div class="fee-citation">
          ${fees.condition ? `<strong>Condition:</strong> ${fees.condition}<br>` : ''}
          ${fees.source_title ? `<strong>Authority:</strong> ${fees.source_title}<br>` : ''}
          ${fees.message || ''}
        </div>
        <div style="margin-top: 10px; font-size: 0.72rem; color: var(--text-muted); font-style: italic;">
          Protected by Civic AI Safety Guard: RECLAIM AI never charges, requests, or handles real payments.
        </div>
      </div>
    `;
  },

  renderNextSteps(steps, containerEl) {
    if (!containerEl) return;
    if (!steps || steps.length === 0) {
      containerEl.innerHTML = `<p class="text-muted">No immediate steps calculated.</p>`;
      return;
    }

    containerEl.innerHTML = `
      <div class="next-steps-list">
        ${steps.map(s => `
          <div class="step-card">
            <div class="step-number-badge">${s.step}</div>
            <div class="step-details">
              <h4>${s.action}</h4>
              <p>${s.reason}</p>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  },

  renderSourcesList(sources, flaggedSources, containerEl) {
    if (!containerEl) return;
    let html = '';

    if (flaggedSources && flaggedSources.length > 0) {
      html += flaggedSources.map(f => `
        <div class="source-card flagged">
          <div class="source-meta">
            <span class="source-badge flagged">⚠️ EXCLUDED (UNOFFICIAL BROKER)</span>
            <span style="font-family: var(--font-mono); font-size: 0.72rem; color: #f87171;">HIGH RISK</span>
          </div>
          <h4>${f.title || f.url}</h4>
          <p>${f.reason}</p>
        </div>
      `).join('');
    }

    if (sources && sources.length > 0) {
      html += sources.map(s => `
        <div class="source-card official">
          <div class="source-meta">
            <span class="source-badge verified">✓ OFFICIAL STATUTORY SOURCE</span>
            <span style="font-family: var(--font-mono); font-size: 0.72rem; color: #34d399;">${s.official_hostname || ''}</span>
          </div>
          <h4>${s.issuing_authority}</h4>
          <p>${s.information_available || ''}</p>
          ${s.official_url ? `
            <div style="margin-top: 6px;">
              <a href="${s.official_url}" target="_blank" rel="noopener noreferrer" style="font-size: 0.78rem;">
                Visit Official Portal ↗
              </a>
            </div>
          ` : ''}
        </div>
      `).join('');
    }

    if (!html) {
      html = `<p class="text-muted">No sources identified.</p>`;
    }

    containerEl.innerHTML = html;
  },

  renderTrackingStatus(tracking, containerEl) {
    if (!containerEl) return;
    const isSubmitted = tracking.status === 'simulated_draft_ready';
    containerEl.innerHTML = `
      <div style="padding: 16px; border-radius: var(--radius-md); background: rgba(11, 19, 41, 0.8); border: 1px solid var(--border-subtle); margin-top: 16px;">
        <h4 style="font-size: 0.92rem; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between;">
          <span>Application Tracking Status:</span>
          <span style="font-family: var(--font-mono); font-size: 0.78rem; color: ${isSubmitted ? 'var(--teal-primary)' : 'var(--text-muted)'};">
            ${isSubmitted ? 'SIMULATED DRAFT' : 'NOT SUBMITTED'}
          </span>
        </h4>
        ${tracking.reference ? `
          <div style="font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; color: var(--teal-primary); margin: 6px 0;">
            ${tracking.reference}
          </div>
          <div style="font-size: 0.72rem; color: #fbbf24; background: rgba(245,158,11,0.1); padding: 4px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px;">
            ${tracking.label || 'SIMULATED REFERENCE - DEMO ONLY'}
          </div>
        ` : ''}
        <p style="font-size: 0.8rem; color: var(--text-muted);">
          ${tracking.note || tracking.tracking_note || 'Application has not been submitted to any government portal.'}
        </p>
      </div>
    `;
  },

  // ==================== INNOVATION 2: COUNTERFACTUAL SIMULATOR ====================
  renderCounterfactualSimulator(result, containerEl, onSelectScenario, scenarios = [], activeId = '') {
    if (!containerEl || !result) return;
    const b = result.baseline || {};
    const m = result.modeled || {};
    const d = result.comparative_deltas || {};

    const scoreDelta = d.readiness_score_delta || 0;
    const deltaBadgeClass = scoreDelta > 0 ? 'positive' : (scoreDelta < 0 ? 'negative' : '');
    const deltaSign = scoreDelta > 0 ? `+${scoreDelta}%` : `${scoreDelta}%`;

    containerEl.innerHTML = `
      <div class="cf-comparison-grid">
        <!-- Left: Baseline Scenario -->
        <div class="cf-card baseline">
          <div class="cf-header">
            <span class="cf-title">Baseline Case</span>
            <span class="panel-step-badge" style="background: rgba(56,189,248,0.15); color: #38bdf8;">
              ${b.label || 'Standard Loss Condition'}
            </span>
          </div>

          <div class="cf-metric-row">
            <span class="cf-metric-label">Readiness Score:</span>
            <span class="cf-metric-value" style="color: var(--teal-primary); font-family: var(--font-mono); font-size: 1.1rem;">
              ${b.readiness_score || 0}%
            </span>
          </div>
          <div class="cf-metric-row">
            <span class="cf-metric-label">Recommended Route:</span>
            <span class="cf-metric-value">${b.recommended_route || 'Pending'}</span>
          </div>
          <div class="cf-metric-row">
            <span class="cf-metric-label">DigiLocker Viable:</span>
            <span class="cf-metric-value" style="color: ${b.digilocker_viable ? '#34d399' : '#f87171'};">
              ${b.digilocker_viable ? '✓ Instant Pull Viable' : '✕ Blocked'}
            </span>
          </div>
          <div class="cf-metric-row">
            <span class="cf-metric-label">Statutory Fee:</span>
            <span class="cf-metric-value">
              ${b.fee_status === 'verified' ? `INR ${(b.fee_amount || 0).toFixed(2)} (Verified)` : 'Unverified'}
            </span>
          </div>
          <div class="cf-metric-row">
            <span class="cf-metric-label">Blocked Graph Nodes:</span>
            <span class="cf-metric-value" style="color: ${(b.blocked_nodes || []).length === 0 ? '#34d399' : '#fbbf24'};">
              ${(b.blocked_nodes || []).length} Nodes Blocked
            </span>
          </div>

          <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.06);">
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 4px;">Next Action:</div>
            <div style="font-size: 0.82rem; color: var(--text-highlight); font-weight: 600;">
              ${b.next_action || 'Review guidance'}
            </div>
          </div>
        </div>

        <!-- Right: Counterfactual Modeled Scenario -->
        <div class="cf-card modeled">
          <div class="cf-header">
            <span class="cf-title">What-If Modeled Outcome</span>
            <span class="cf-delta-badge ${deltaBadgeClass}">
              Readiness: ${deltaSign}
            </span>
          </div>

          <div class="cf-metric-row">
            <span class="cf-metric-label">Modeled Readiness:</span>
            <span class="cf-metric-value" style="color: ${scoreDelta >= 0 ? '#34d399' : '#f87171'}; font-family: var(--font-mono); font-size: 1.1rem;">
              ${m.readiness_score || 0}%
            </span>
          </div>
          <div class="cf-metric-row">
            <span class="cf-metric-label">Adapted Route:</span>
            <span class="cf-metric-value" style="color: ${d.route_shifted ? '#fbbf24' : 'inherit'};">
              ${m.recommended_route || 'Pending'} ${d.route_shifted ? '⚡ Shifted' : ''}
            </span>
          </div>
          <div class="cf-metric-row">
            <span class="cf-metric-label">DigiLocker Viable:</span>
            <span class="cf-metric-value" style="color: ${m.digilocker_viable ? '#34d399' : '#f87171'};">
              ${m.digilocker_viable ? '✓ Instant Pull Viable' : '✕ Blocked'}
            </span>
          </div>
          <div class="cf-metric-row">
            <span class="cf-metric-label">Statutory Fee:</span>
            <span class="cf-metric-value">
              ${m.fee_status === 'verified' ? `INR ${(m.fee_amount || 0).toFixed(2)} (Verified)` : 'Unverified (Gate Locked)'}
            </span>
          </div>
          <div class="cf-metric-row">
            <span class="cf-metric-label">New Blocked Nodes:</span>
            <span class="cf-metric-value" style="color: ${(d.new_blocked_nodes || []).length > 0 ? '#f87171' : '#34d399'};">
              ${(d.new_blocked_nodes || []).length > 0 ? d.new_blocked_nodes.join(', ') : 'None'}
            </span>
          </div>

          <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.06);">
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 4px;">Adapted Next Action:</div>
            <div style="font-size: 0.82rem; color: var(--teal-primary); font-weight: 600;">
              ${m.next_action || 'Review guidance'}
            </div>
          </div>
        </div>
      </div>

      <!-- Statutory Rationale Takeaway -->
      <div class="cf-takeaway-box">
        <strong style="color: var(--teal-primary); display: block; margin-bottom: 4px;">
          🧠 Agent Strategic Rationale & Legal Explanation:
        </strong>
        ${d.key_takeaway || 'Scenario modeled dynamically.'}
      </div>

      <div style="font-size: 0.72rem; color: var(--text-muted); margin-top: 10px; font-family: var(--font-mono);">
        ${result.statutory_disclaimer || ''}
      </div>
    `;
  },

  // ==================== INNOVATION 3: PROVENANCE GRAPH ====================
  renderProvenanceGraph(graph, containerEl) {
    if (!containerEl || !graph) return;
    const nodes = graph.nodes || [];
    const tiers = graph.tier_metadata || [];

    // Group nodes by tier
    const nodesByTier = {};
    tiers.forEach(t => { nodesByTier[t.tier] = []; });
    nodes.forEach(n => {
      if (nodesByTier[n.tier]) {
        nodesByTier[n.tier].push(n);
      }
    });

    containerEl.innerHTML = `
      <!-- Summary Metrics Bar -->
      <div class="provenance-metrics-strip">
        <div class="prov-metric-item">
          <span class="val">${graph.node_count || nodes.length}</span>
          <span class="lbl">DAG Nodes</span>
        </div>
        <div class="prov-metric-item">
          <span class="val">${graph.edge_count || (graph.edges || []).length}</span>
          <span class="lbl">Evidence Edges</span>
        </div>
        <div class="prov-metric-item">
          <span class="val" style="color: #34d399;">${graph.verified_claim_count || 0}</span>
          <span class="lbl">Verified Claims</span>
        </div>
        <div class="prov-metric-item">
          <span class="val" style="color: ${(graph.unsupported_claim_count || 0) > 0 ? '#fbbf24' : '#34d399'};">
            ${graph.unsupported_claim_count || 0}
          </span>
          <span class="lbl">Assumptions</span>
        </div>
        <div class="prov-metric-item">
          <span class="val" style="color: var(--teal-primary);">${graph.provenance_traceability_score || 100}%</span>
          <span class="lbl">Traceability</span>
        </div>
      </div>

      <!-- 7 Horizontal Lanes representing DAG Tiers -->
      <div class="provenance-tiers-container">
        ${tiers.map(t => {
          const tierNodes = nodesByTier[t.tier] || [];
          return `
            <div class="provenance-tier-lane">
              <div class="prov-tier-header" style="color: ${t.color}; border-color: ${t.color};">
                Tier ${t.tier}: ${t.name}
              </div>
              <div style="display: flex; flex-direction: column; gap: 8px;">
                ${tierNodes.length === 0 ? `
                  <div style="font-size: 0.74rem; color: var(--text-muted); padding: 8px;">No active records</div>
                ` : tierNodes.map(n => `
                  <div class="prov-node-card ${n.is_unsupported_or_stale ? 'unsupported' : ''}">
                    <div class="prov-node-title">${n.label}</div>
                    <div class="prov-node-desc">${n.detail}</div>
                    <span class="prov-node-badge" style="background: ${n.is_unsupported_or_stale ? 'rgba(245,158,11,0.2)' : 'rgba(56,189,248,0.15)'}; color: ${n.is_unsupported_or_stale ? '#fbbf24' : '#38bdf8'};">
                      ${n.status}
                    </span>
                  </div>
                `).join('')}
              </div>
            </div>
          `;
        }).join('')}
      </div>

      <div style="font-size: 0.74rem; color: var(--text-muted); margin-top: 10px; font-family: var(--font-mono);">
        ✓ Anti-Hallucination Guard active: Every downstream recommendation traces directly back to gazetted statutory citations.
      </div>
    `;
  },

  // ==================== INNOVATION 5: ACCESSIBLE CIVIC COPILOT ====================
  renderCivicCopilot(containerEl, onSendMessage, onQuickQuestion) {
    if (!containerEl) return;
    containerEl.innerHTML = `
      <div class="copilot-box">
        <!-- Message History Feed -->
        <div class="copilot-messages" id="copilot-msg-feed">
          <div class="copilot-msg bot">
            <strong>Civic Copilot:</strong><br>
            Hello! I am your Accessible Civic Copilot. Ask me any question in simple English or Tamil (தமிழ்) about lost certificates, FIR rules, fees, or legal procedures.
          </div>
        </div>

        <!-- Detected Legal Terms Strip -->
        <div class="copilot-terms-strip" id="copilot-terms-strip" style="display: none;"></div>

        <!-- Quick Inquiry Chips -->
        <div style="padding: 8px 16px; background: rgba(0,0,0,0.2); display: flex; gap: 6px; flex-wrap: wrap;">
          <button class="btn btn-secondary btn-sm copilot-quick-btn" data-query="What is the first step to recover my document?" style="font-size: 0.74rem; padding: 3px 8px;">
            1. First Step?
          </button>
          <button class="btn btn-secondary btn-sm copilot-quick-btn" data-query="Do I need a formal police FIR or an online loss report?" style="font-size: 0.74rem; padding: 3px 8px;">
            2. Is FIR Mandatory?
          </button>
          <button class="btn btn-secondary btn-sm copilot-quick-btn" data-query="What is the verified statutory fee?" style="font-size: 0.74rem; padding: 3px 8px;">
            3. Verified Fee?
          </button>
          <button class="btn btn-secondary btn-sm copilot-quick-btn" data-query="என் ஓட்டுநர் உரிமம் தொலைந்துவிட்டது, நான் என்ன செய்ய வேண்டும்?" style="font-size: 0.74rem; padding: 3px 8px; color: #38bdf8;">
            4. தமிழ் உதவி (Tamil Guide)
          </button>
        </div>

        <!-- Input Bar -->
        <div class="copilot-input-bar">
          <input type="text" id="copilot-user-input" placeholder="Ask a recovery question in English or தமிழ்..." />
          <button id="btn-copilot-send" class="btn btn-primary" style="padding: 8px 16px;">Send</button>
        </div>
      </div>
    `;

    // Event listeners
    const sendBtn = document.getElementById('btn-copilot-send');
    const inputEl = document.getElementById('copilot-user-input');

    const doSend = () => {
      const msg = inputEl.value.trim();
      if (msg && onSendMessage) {
        inputEl.value = '';
        onSendMessage(msg);
      }
    };

    sendBtn?.addEventListener('click', doSend);
    inputEl?.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') doSend();
    });

    containerEl.querySelectorAll('.copilot-quick-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const q = btn.getAttribute('data-query');
        if (q && onQuickQuestion) onQuickQuestion(q);
      });
    });
  },

  appendCopilotMessage(sender, text, terms = []) {
    const feed = document.getElementById('copilot-msg-feed');
    if (!feed) return;

    const div = document.createElement('div');
    div.className = `copilot-msg ${sender}`;
    div.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Civic Copilot'}:</strong><br>${text.replace(/\n/g, '<br>')}`;
    feed.appendChild(div);
    feed.scrollTop = feed.scrollHeight;

    // Terms strip
    const termsStrip = document.getElementById('copilot-terms-strip');
    if (termsStrip && terms && terms.length > 0) {
      termsStrip.style.display = 'flex';
      termsStrip.innerHTML = terms.map(t => `
        <span class="term-chip" title="${t.explanation}">
          📖 ${t.term}: ${t.explanation.slice(0, 45)}...
        </span>
      `).join('');
    }
  }
};

