-- ====================================================================
-- Cyber Incident Response & Evidence Management System (CIREMS)
-- Database Initialization & Schema Definition (PostgreSQL 14+)
-- ====================================================================

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'investigator', -- 'admin', 'investigator'
    department VARCHAR(100) DEFAULT 'SOC Operations',
    badge_number VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- 2. INCIDENTS TABLE
CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    case_id VARCHAR(50) UNIQUE NOT NULL, -- e.g. CIR-2026-001
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL, -- Phishing, Malware, Ransomware, Unauthorized Access, Brute Force, Denial of Service, Data Breach
    severity VARCHAR(20) NOT NULL, -- Low, Medium, High, Critical
    status VARCHAR(30) NOT NULL DEFAULT 'Open', -- Open, Under Investigation, Resolved, Closed
    incident_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    affected_system VARCHAR(255) NOT NULL,
    source_ip VARCHAR(64),
    destination_ip VARCHAR(64),
    assigned_investigator_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_incidents_case_id ON incidents(case_id);
CREATE INDEX IF NOT EXISTS idx_incidents_severity ON incidents(severity);
CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);
CREATE INDEX IF NOT EXISTS idx_incidents_category ON incidents(category);

-- 3. ATTACK DETAILS TABLE
CREATE TABLE IF NOT EXISTS attack_details (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    attack_type VARCHAR(100) NOT NULL,
    attack_source VARCHAR(150),
    attack_vector VARCHAR(150),
    target_system VARCHAR(255),
    source_ip VARCHAR(64),
    destination_ip VARCHAR(64),
    attack_timestamp TIMESTAMP WITH TIME ZONE,
    indicators_of_compromise JSONB DEFAULT '[]'::jsonb, -- Hashes, C2 domains, malicious IPs
    mitre_tactics VARCHAR(255),
    suspicious_activity_description TEXT,
    investigator_observations TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_attack_details_incident_id ON attack_details(incident_id);

-- 4. EVIDENCE TABLE
CREATE TABLE IF NOT EXISTS evidence (
    id SERIAL PRIMARY KEY,
    evidence_id VARCHAR(50) UNIQUE NOT NULL, -- e.g. EVD-2026-001
    incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(20) NOT NULL, -- TXT, PDF, CSV, LOG, PNG, JPG, JSON
    file_size BIGINT NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    original_sha256 VARCHAR(64) NOT NULL,
    current_sha256 VARCHAR(64) NOT NULL,
    integrity_status VARCHAR(20) NOT NULL DEFAULT 'VERIFIED', -- 'VERIFIED', 'MODIFIED', 'UNVERIFIED'
    last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    uploaded_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evidence_incident_id ON evidence(incident_id);
CREATE INDEX IF NOT EXISTS idx_evidence_evidence_id ON evidence(evidence_id);
CREATE INDEX IF NOT EXISTS idx_evidence_integrity ON evidence(integrity_status);

-- 5. CHAIN OF CUSTODY TABLE (Append-Only)
CREATE TABLE IF NOT EXISTS chain_of_custody (
    id SERIAL PRIMARY KEY,
    record_id VARCHAR(50) UNIQUE NOT NULL, -- e.g. COC-2026-001
    evidence_id INTEGER NOT NULL REFERENCES evidence(id) ON DELETE CASCADE,
    incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL, -- Collected, Uploaded, Accessed, Transferred, Verified, Downloaded
    previous_custodian VARCHAR(150),
    new_custodian VARCHAR(150),
    performed_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    remarks TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_coc_evidence_id ON chain_of_custody(evidence_id);
CREATE INDEX IF NOT EXISTS idx_coc_incident_id ON chain_of_custody(incident_id);
CREATE INDEX IF NOT EXISTS idx_coc_timestamp ON chain_of_custody(timestamp);

-- 6. LOG ANALYSIS TABLE
CREATE TABLE IF NOT EXISTS log_analysis (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER REFERENCES incidents(id) ON DELETE SET NULL,
    log_name VARCHAR(255) NOT NULL,
    log_type VARCHAR(50) NOT NULL, -- Server, Authentication, Firewall, Network, Application
    total_entries INTEGER NOT NULL DEFAULT 0,
    failed_logins INTEGER NOT NULL DEFAULT 0,
    suspicious_ips JSONB DEFAULT '[]'::jsonb,
    detected_patterns JSONB DEFAULT '[]'::jsonb,
    summary_stats JSONB DEFAULT '{}'::jsonb,
    analysis_findings TEXT,
    analyzed_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_log_analysis_incident ON log_analysis(incident_id);

-- 7. SECURITY ALERTS TABLE
CREATE TABLE IF NOT EXISTS security_alerts (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER REFERENCES incidents(id) ON DELETE CASCADE,
    evidence_id INTEGER REFERENCES evidence(id) ON DELETE SET NULL,
    alert_type VARCHAR(100) NOT NULL, -- Integrity Tampering, Brute Force Attack, Critical Threat IOC
    severity VARCHAR(20) NOT NULL, -- Low, Medium, High, Critical
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_alerts_severity ON security_alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON security_alerts(is_resolved);

-- 8. INVESTIGATION REPORTS TABLE
CREATE TABLE IF NOT EXISTS investigation_reports (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(50) UNIQUE NOT NULL, -- e.g. RPT-2026-001
    incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    generated_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reports_incident ON investigation_reports(incident_id);

-- 9. AUDIT LOGS TABLE (Append-Only)
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    username VARCHAR(100),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(50),
    ip_address VARCHAR(64),
    details JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
