"""
RECLAIM AI 2.0 - Database Layer
SQLite connection management, initialization, and migrations
Supports Recovery Twins, Evidence Claims, Conflicting Claims, and Mock Portal State
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone
from config import Config

def get_db_connection():
    """Returns a connection to the SQLite database with row factory enabled."""
    db_path = Config.DATABASE_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes database schema with required tables and indexes."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Existing Sessions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        document_type TEXT NOT NULL,
        jurisdiction TEXT,
        issuing_authority TEXT,
        status_type TEXT DEFAULT 'lost',
        workflow_status TEXT DEFAULT 'intake',
        readiness_score INTEGER DEFAULT 0,
        fee_status TEXT DEFAULT 'not_verified',
        fee_amount REAL,
        fee_currency TEXT DEFAULT 'INR',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        payload_json TEXT
    );
    """)
    
    # 2. Existing Evidence Vault Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence_vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        source_id TEXT NOT NULL,
        source_title TEXT NOT NULL,
        source_url TEXT NOT NULL,
        verification_status TEXT NOT NULL,
        extracted_summary TEXT,
        decision_supported TEXT,
        retrieved_at TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE
    );
    """)
    
    # 3. Existing Agent Trace Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workflow_trace (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        step_number INTEGER NOT NULL,
        step_name TEXT NOT NULL,
        status TEXT NOT NULL,
        input_summary TEXT,
        decision TEXT,
        reason TEXT,
        evidence_ref TEXT,
        action_taken TEXT,
        outcome TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE
    );
    """)
    
    # 4. Existing Human-in-the-Loop Approvals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS approvals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        proposed_action TEXT NOT NULL,
        approval_status TEXT DEFAULT 'pending',
        user_decision TEXT,
        consequences TEXT,
        decision_timestamp TEXT,
        execution_result TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE
    );
    """)
    
    # 5. Existing Test Laboratory Results Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scenario_id TEXT NOT NULL,
        scenario_name TEXT NOT NULL,
        input_data TEXT NOT NULL,
        expected_result TEXT NOT NULL,
        actual_result TEXT NOT NULL,
        status TEXT NOT NULL,
        evidence TEXT,
        executed_at TEXT NOT NULL
    );
    """)
    
    # ==================== INNOVATION 1: RECOVERY TWINS ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recovery_twins (
        case_id TEXT PRIMARY KEY,
        document_type TEXT NOT NULL,
        jurisdiction TEXT,
        issuing_authority TEXT,
        status_type TEXT DEFAULT 'lost',
        facts_json TEXT,
        dependency_graph_json TEXT,
        readiness_score INTEGER DEFAULT 0,
        current_status TEXT DEFAULT 'INITIALIZED',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # ==================== INNOVATION 2: EVIDENCE CLAIMS & CONFLICTS ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence_claims (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        claim_text TEXT NOT NULL,
        source_id TEXT,
        source_url TEXT NOT NULL,
        excerpt TEXT,
        source_tag TEXT NOT NULL, -- LIVE_VERIFIED, CACHED, USER_PROVIDED, SYNTHETIC_DEMO, UNVERIFIED
        verification_status TEXT NOT NULL,
        confidence TEXT,
        retrieved_at TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conflicting_claims (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        topic TEXT NOT NULL,
        claim_a TEXT NOT NULL,
        source_a TEXT NOT NULL,
        date_a TEXT,
        claim_b TEXT NOT NULL,
        source_b TEXT NOT NULL,
        date_b TEXT,
        stronger_source TEXT,
        resolution_reason TEXT,
        is_resolved INTEGER DEFAULT 0,
        detected_at TEXT NOT NULL
    );
    """)

    # ==================== INNOVATION 5: MOCK PORTAL APPLICATIONS ====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mock_portal_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_ref TEXT UNIQUE NOT NULL,
        idempotency_key TEXT UNIQUE NOT NULL,
        case_id TEXT NOT NULL,
        applicant_data_json TEXT NOT NULL,
        portal_name TEXT NOT NULL,
        submission_status TEXT NOT NULL, -- DRAFT, SUBMITTED, CONFIRMED, FAILED
        submitted_at TEXT NOT NULL,
        receipt_json TEXT NOT NULL,
        audit_trail_json TEXT NOT NULL
    );
    """)
    
    # Create indexes for speed and integrity
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_trace_session ON workflow_trace(session_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_evidence_session ON evidence_vault(session_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_approvals_session ON approvals(session_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_test_scenario ON test_results(scenario_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_twins_case ON recovery_twins(case_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_case ON evidence_claims(case_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_conflicts_case ON conflicting_claims(case_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mock_idempotency ON mock_portal_applications(idempotency_key);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mock_ref ON mock_portal_applications(application_ref);")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("RECLAIM AI 2.0 Database initialized successfully at", Config.DATABASE_PATH)
