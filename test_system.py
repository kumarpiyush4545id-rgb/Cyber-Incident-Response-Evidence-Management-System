"""
CIREMS Automated End-to-End Test Suite
Tests all 11 required project workflows:
1. Register and log in as an investigator
2. Create a new cyber incident
3. Add attack details
4. Upload digital evidence
5. Generate its SHA-256 hash
6. Verify evidence integrity
7. View the chain of custody
8. Upload a security log file
9. Analyze suspicious login attempts
10. View threat analysis results
11. Generate and download a PDF investigation report
"""
import sys
import os

# Add backend directory to path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    print("=" * 70)
    print("RUNNING CIREMS AUTOMATED FORENSIC WORKFLOW TEST SUITE")
    print("=" * 70)

    client = TestClient(app)
    with client:
        # Workflow 1: Register and login as investigator
        reg_resp = client.post("/api/auth/register", json={
            "username": "tester_inv",
            "email": "tester@cyberforensics.org",
            "password": "Password@1234",
            "full_name": "Test Examiner Vance",
            "role": "investigator",
            "department": "Forensics Lab",
            "badge_number": "TEST-DFIR-99"
        })
        if reg_resp.status_code == 201:
            print("[PASS] Workflow 1a: Registered new investigator account.")
        else:
            print(f"[INFO] Workflow 1a: User already registered or status {reg_resp.status_code}")

        login_resp = client.post("/api/auth/login", json={
            "username": "tester_inv",
            "password": "Password@1234"
        })
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("[PASS] Workflow 1b: Authenticated & received JWT bearer token.")

        # Workflow 2: Create a new cyber incident
        inc_resp = client.post("/api/incidents", json={
            "title": "Automated Test Incident: Unauthorized SMB Lateral Movement",
            "description": "Suspicious NTLM relay activity detected targeting internal file servers.",
            "category": "Unauthorized Access",
            "severity": "High",
            "status": "Open",
            "incident_datetime": "2026-11-16T10:00:00",
            "affected_system": "FileShare-Cluster-02",
            "source_ip": "192.168.1.189",
            "destination_ip": "192.168.1.10"
        }, headers=headers)
        assert inc_resp.status_code == 201, f"Create incident failed: {inc_resp.text}"
        incident = inc_resp.json()
        incident_id = incident["id"]
        print(f"[PASS] Workflow 2: Created new incident case {incident['case_id']} (ID: {incident_id}).")

        # Workflow 3: Add attack details
        atk_resp = client.post("/api/attack-details", json={
            "incident_id": incident_id,
            "attack_type": "NTLM Relay & Pass-the-Hash",
            "attack_source": "Compromised Internal Workstation (192.168.1.189)",
            "attack_vector": "SMB signing disabled on legacy workstation subnet",
            "target_system": "FileShare-Cluster-02",
            "source_ip": "192.168.1.189",
            "destination_ip": "192.168.1.10",
            "mitre_tactics": "Lateral Movement (T1557), Credential Access (T1558)",
            "indicators_of_compromise": ["192.168.1.189", "ntlm_relay_agent.exe"],
            "suspicious_activity_description": "Rapid succession of SMB connections using administrative token.",
            "investigator_observations": "Host isolated; SMB signing enforced via GPO."
        }, headers=headers)
        assert atk_resp.status_code == 200, f"Add attack detail failed: {atk_resp.text}"
        print("[PASS] Workflow 3: Documented attack vectors & MITRE tactics.")

        # Workflow 4: Upload digital evidence
        test_file_content = b"CRITICAL FORENSIC EVIDENCE: Captured NTLM hash dump from test incident.\n"
        files = {"file": ("ntlm_hashes_dump.log", test_file_content, "text/plain")}
        data = {"incident_id": str(incident_id), "description": "Memory artifact from compromised endpoint."}
        ev_resp = client.post("/api/evidence/upload", files=files, data=data, headers=headers)
        assert ev_resp.status_code == 200, f"Upload evidence failed: {ev_resp.text}"
        evidence = ev_resp.json()
        ev_id = evidence["id"]
        print(f"[PASS] Workflow 4: Uploaded evidence {evidence['evidence_id']} ({evidence['original_filename']}).")

        # Workflow 5: Generate its SHA-256 hash
        assert len(evidence["original_sha256"]) == 64, "Invalid SHA-256 length"
        print(f"[PASS] Workflow 5: SHA-256 hash computed immediately: {evidence['original_sha256']}")

        # Workflow 6: Verify evidence integrity
        verify_resp = client.post(f"/api/evidence/{ev_id}/verify-hash", headers=headers)
        assert verify_resp.status_code == 200, f"Verify hash failed: {verify_resp.text}"
        assert verify_resp.json()["integrity_status"] == "VERIFIED"
        print("[PASS] Workflow 6: Evidence integrity cryptographically verified (Status: VERIFIED).")

        # Workflow 7: View chain of custody
        coc_resp = client.get(f"/api/chain-of-custody?evidence_id={ev_id}", headers=headers)
        assert coc_resp.status_code == 200, f"Custody query failed: {coc_resp.text}"
        records = coc_resp.json()
        assert len(records) >= 2, "Expected at least 2 custody records (Upload & Verification)"
        print(f"[PASS] Workflow 7: Chronological chain of custody retrieved ({len(records)} entries).")

        # Workflow 8: Upload a security log file
        sample_log = (
            "Nov 16 04:12:01 server-01 sshd[901]: Failed password for root from 185.220.101.44 port 3821 ssh2\n"
            "Nov 16 04:12:03 server-01 sshd[902]: Failed password for root from 185.220.101.44 port 3824 ssh2\n"
            "Nov 16 04:12:06 server-01 sshd[903]: Failed password for admin from 185.220.101.44 port 3828 ssh2\n"
            "Nov 16 04:12:09 server-01 sshd[904]: Failed password for oracle from 185.220.101.44 port 3832 ssh2\n"
        )
        log_resp = client.post("/api/logs/upload-and-analyze", data={
            "log_name": "test_auth_audit.log",
            "log_type": "Authentication",
            "incident_id": str(incident_id),
            "raw_text": sample_log
        }, headers=headers)
        assert log_resp.status_code == 200, f"Log upload failed: {log_resp.text}"
        log_analysis = log_resp.json()
        print(f"[PASS] Workflow 8: Uploaded and ingested security log ({log_analysis['total_entries']} lines).")

        # Workflow 9: Analyze suspicious login attempts
        assert log_analysis["failed_logins"] == 4, "Expected 4 failed logins"
        assert len(log_analysis["suspicious_ips"]) > 0, "Expected at least 1 flagged IP"
        print(f"[PASS] Workflow 9: Pandas log analysis detected {log_analysis['failed_logins']} failed logins and flagged hostile IP {log_analysis['suspicious_ips'][0]['ip']}.")

        # Workflow 10: View threat analysis results
        threat_resp = client.post("/api/threat-intelligence/analyze", json={
            "incident_id": incident_id
        }, headers=headers)
        assert threat_resp.status_code == 200, f"Threat analysis failed: {threat_resp.text}"
        threat = threat_resp.json()
        assert threat["risk_score"] > 0, "Risk score should be > 0"
        print(f"[PASS] Workflow 10: AI Threat Analysis computed risk rating {threat['risk_score']}/100 with {len(threat['observations'])} threat observation(s).")

        # Workflow 11: Generate and download a PDF investigation report
        rep_resp = client.post(f"/api/reports/generate/{incident_id}", json={
            "incident_id": incident_id,
            "title": f"Forensic Dossier: Case {incident['case_id']}",
            "investigator_notes": "All indicators contained and evidence cryptographically preserved."
        }, headers=headers)
        assert rep_resp.status_code == 200, f"Generate report failed: {rep_resp.text}"
        report = rep_resp.json()
        rep_id = report["id"]
        print(f"[PASS] Workflow 11a: ReportLab compiled forensic PDF report {report['report_id']}.")

        dl_resp = client.get(f"/api/reports/{rep_id}/download", headers=headers)
        assert dl_resp.status_code == 200, f"Download report failed: {dl_resp.text}"
        assert dl_resp.headers["content-type"] == "application/pdf"
        assert len(dl_resp.content) > 1000, "PDF content is too small"
        print(f"[PASS] Workflow 11b: Downloaded official forensic PDF dossier ({len(dl_resp.content)} bytes).")

    print("=" * 70)
    print("ALL 11 FORENSIC WORKFLOWS TESTED SUCCESSFULLY! 100% OPERATIONAL.")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
