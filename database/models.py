"""
RECLAIM AI 2.0 - Database Models & Repository Operations
Provides clean, parameterized CRUD operations with strict type handling
Includes Recovery Twins, Evidence Claims, Conflicts, and Mock Portal State
"""
import sqlite3
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from database.db import get_db_connection

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

# ==================== EXISTING SESSION REPOSITORY ====================

def create_or_update_session(session_id: str, document_type: str, jurisdiction: str,
                            issuing_authority: str, status_type: str = "lost",
                            workflow_status: str = "intake", readiness_score: int = 0,
                            fee_status: str = "not_verified", fee_amount: Optional[float] = None,
                            fee_currency: str = "INR", payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    payload_str = json.dumps(payload or {})
    
    cursor.execute("""
    INSERT INTO sessions (
        session_id, document_type, jurisdiction, issuing_authority,
        status_type, workflow_status, readiness_score, fee_status,
        fee_amount, fee_currency, created_at, updated_at, payload_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(session_id) DO UPDATE SET
        document_type=excluded.document_type,
        jurisdiction=excluded.jurisdiction,
        issuing_authority=excluded.issuing_authority,
        status_type=excluded.status_type,
        workflow_status=excluded.workflow_status,
        readiness_score=excluded.readiness_score,
        fee_status=excluded.fee_status,
        fee_amount=excluded.fee_amount,
        fee_currency=excluded.fee_currency,
        updated_at=excluded.updated_at,
        payload_json=excluded.payload_json
    """, (
        session_id, document_type, jurisdiction, issuing_authority,
        status_type, workflow_status, readiness_score, fee_status,
        fee_amount, fee_currency, now, now, payload_str
    ))
    conn.commit()
    conn.close()
    return get_session_by_id(session_id)

def get_session_by_id(session_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    if data.get("payload_json"):
        try:
            data["payload"] = json.loads(data["payload_json"])
        except Exception:
            data["payload"] = {}
    return data

def update_session_workflow(session_id: str, workflow_status: str,
                            readiness_score: Optional[int] = None,
                            fee_status: Optional[str] = None,
                            fee_amount: Optional[float] = None) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    
    updates = ["workflow_status = ?", "updated_at = ?"]
    params = [workflow_status, now]
    
    if readiness_score is not None:
        updates.append("readiness_score = ?")
        params.append(readiness_score)
    if fee_status is not None:
        updates.append("fee_status = ?")
        params.append(fee_status)
    if fee_amount is not None:
        updates.append("fee_amount = ?")
        params.append(fee_amount)
        
    params.append(session_id)
    query = f"UPDATE sessions SET {', '.join(updates)} WHERE session_id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# ==================== EXISTING EVIDENCE VAULT REPOSITORY ====================

def add_evidence(session_id: str, source_id: str, source_title: str,
                 source_url: str, verification_status: str,
                 extracted_summary: str, decision_supported: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    cursor.execute("""
    INSERT INTO evidence_vault (
        session_id, source_id, source_title, source_url,
        verification_status, extracted_summary, decision_supported, retrieved_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (session_id, source_id, source_title, source_url,
          verification_status, extracted_summary, decision_supported, now))
    rec_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return rec_id

def get_session_evidence(session_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evidence_vault WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ==================== EXISTING WORKFLOW TRACE REPOSITORY ====================

def add_trace_event(session_id: str, step_number: int, step_name: str,
                    status: str, input_summary: str, decision: str,
                    reason: str, evidence_ref: str, action_taken: str,
                    outcome: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    cursor.execute("""
    INSERT INTO workflow_trace (
        session_id, step_number, step_name, status,
        input_summary, decision, reason, evidence_ref,
        action_taken, outcome, timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (session_id, step_number, step_name, status,
          input_summary, decision, reason, evidence_ref,
          action_taken, outcome, now))
    trace_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return trace_id

def get_session_trace(session_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workflow_trace WHERE session_id = ? ORDER BY step_number ASC, id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ==================== EXISTING APPROVAL REPOSITORY ====================

def create_approval_request(session_id: str, proposed_action: str, consequences: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO approvals (
        session_id, proposed_action, approval_status, consequences
    ) VALUES (?, ?, 'pending', ?)
    """, (session_id, proposed_action, consequences))
    approval_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return approval_id

def resolve_approval_request(approval_id: int, user_decision: str,
                             approval_status: str, execution_result: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    cursor.execute("""
    UPDATE approvals
    SET user_decision = ?, approval_status = ?, execution_result = ?, decision_timestamp = ?
    WHERE id = ?
    """, (user_decision, approval_status, execution_result, now, approval_id))
    conn.commit()
    conn.close()

def get_session_approvals(session_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM approvals WHERE session_id = ? ORDER BY id DESC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ==================== EXISTING TEST RESULTS REPOSITORY ====================

def record_test_result(scenario_id: str, scenario_name: str, input_data: str,
                       expected_result: str, actual_result: str, status: str,
                       evidence: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    cursor.execute("""
    INSERT INTO test_results (
        scenario_id, scenario_name, input_data, expected_result,
        actual_result, status, evidence, executed_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (scenario_id, scenario_name, input_data, expected_result,
          actual_result, status, evidence, now))
    test_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return test_id

def get_latest_test_results() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT t1.* FROM test_results t1
    JOIN (
        SELECT scenario_id, MAX(id) as max_id
        FROM test_results
        GROUP BY scenario_id
    ) t2 ON t1.id = t2.max_id
    ORDER BY t1.scenario_id ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ==================== INNOVATION 1: RECOVERY TWINS REPOSITORY ====================

def save_recovery_twin(case_id: str, document_type: str, jurisdiction: str,
                       issuing_authority: str, status_type: str,
                       facts: Dict[str, Any], dependency_graph: Dict[str, Any],
                       readiness_score: int, current_status: str = "ACTIVE") -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    facts_str = json.dumps(facts)
    graph_str = json.dumps(dependency_graph)

    cursor.execute("""
    INSERT INTO recovery_twins (
        case_id, document_type, jurisdiction, issuing_authority,
        status_type, facts_json, dependency_graph_json, readiness_score,
        current_status, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(case_id) DO UPDATE SET
        document_type=excluded.document_type,
        jurisdiction=excluded.jurisdiction,
        issuing_authority=excluded.issuing_authority,
        status_type=excluded.status_type,
        facts_json=excluded.facts_json,
        dependency_graph_json=excluded.dependency_graph_json,
        readiness_score=excluded.readiness_score,
        current_status=excluded.current_status,
        updated_at=excluded.updated_at
    """, (
        case_id, document_type, jurisdiction, issuing_authority,
        status_type, facts_str, graph_str, readiness_score,
        current_status, now, now
    ))
    conn.commit()
    conn.close()
    return get_recovery_twin(case_id)

def get_recovery_twin(case_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recovery_twins WHERE case_id = ?", (case_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["facts"] = json.loads(data["facts_json"]) if data.get("facts_json") else {}
    data["dependency_graph"] = json.loads(data["dependency_graph_json"]) if data.get("dependency_graph_json") else {}
    return data

# ==================== INNOVATION 2: EVIDENCE CLAIMS & CONFLICTS ====================

def add_evidence_claim(case_id: str, claim_text: str, source_id: Optional[str],
                       source_url: str, excerpt: str, source_tag: str,
                       verification_status: str, confidence: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    cursor.execute("""
    INSERT INTO evidence_claims (
        case_id, claim_text, source_id, source_url, excerpt,
        source_tag, verification_status, confidence, retrieved_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id, claim_text, source_id, source_url, excerpt,
        source_tag, verification_status, confidence, now
    ))
    claim_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return claim_id

def get_case_claims(case_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evidence_claims WHERE case_id = ? ORDER BY id ASC", (case_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def record_conflicting_claims(case_id: str, topic: str, claim_a: str, source_a: str, date_a: Optional[str],
                              claim_b: str, source_b: str, date_b: Optional[str],
                              stronger_source: Optional[str], resolution_reason: str,
                              is_resolved: bool = False) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    cursor.execute("""
    INSERT INTO conflicting_claims (
        case_id, topic, claim_a, source_a, date_a,
        claim_b, source_b, date_b, stronger_source,
        resolution_reason, is_resolved, detected_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id, topic, claim_a, source_a, date_a,
        claim_b, source_b, date_b, stronger_source,
        resolution_reason, 1 if is_resolved else 0, now
    ))
    conflict_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return conflict_id

def get_case_conflicts(case_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conflicting_claims WHERE case_id = ? ORDER BY id ASC", (case_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ==================== INNOVATION 5: MOCK PORTAL APPLICATIONS ====================

def create_mock_portal_application(application_ref: str, idempotency_key: str,
                                   case_id: str, applicant_data: Dict[str, Any],
                                   portal_name: str, submission_status: str,
                                   receipt: Dict[str, Any], audit_trail: List[Dict[str, Any]]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    now = utc_now_iso()
    app_str = json.dumps(applicant_data)
    receipt_str = json.dumps(receipt)
    audit_str = json.dumps(audit_trail)

    cursor.execute("""
    INSERT INTO mock_portal_applications (
        application_ref, idempotency_key, case_id, applicant_data_json,
        portal_name, submission_status, submitted_at, receipt_json, audit_trail_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        application_ref, idempotency_key, case_id, app_str,
        portal_name, submission_status, now, receipt_str, audit_str
    ))
    conn.commit()
    conn.close()
    return get_mock_portal_application_by_ref(application_ref)

def get_mock_portal_application_by_idempotency(idempotency_key: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mock_portal_applications WHERE idempotency_key = ?", (idempotency_key,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["applicant_data"] = json.loads(data["applicant_data_json"])
    data["receipt"] = json.loads(data["receipt_json"])
    data["audit_trail"] = json.loads(data["audit_trail_json"])
    return data

def get_mock_portal_application_by_ref(application_ref: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mock_portal_applications WHERE application_ref = ?", (application_ref,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    data["applicant_data"] = json.loads(data["applicant_data_json"])
    data["receipt"] = json.loads(data["receipt_json"])
    data["audit_trail"] = json.loads(data["audit_trail_json"])
    return data
