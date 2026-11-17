# Cyber Incident Response & Evidence Management System (CIREMS)

A centralized, enterprise-grade cybersecurity and digital forensics investigation platform designed to record, manage, investigate, and respond to cyber incidents while strictly enforcing evidentiary integrity, append-only chain of custody, automated cryptographic verification, and AI-assisted threat analytics.

---

## 1. Executive Summary & Capabilities

CIREMS serves as a defense-grade Security Operations Center (SOC) and Digital Forensics & Incident Response (DFIR) case dossier manager:
- **Incident Case Management**: Create, triage, search, filter, and track cyber incident cases with MITRE ATT&CK categorization.
- **Attack Detail Documentation**: Record technical attack vectors, targets, adversary IPs, timestamps, and observed Indicators of Compromise (IOCs).
- **Digital Evidence Vault**: Securely ingest, store, and inventory digital evidence files (`TXT`, `PDF`, `CSV`, `LOG`, `PNG`, `JPG`, `JSON`).
- **Cryptographic SHA-256 Hashing**: Real-time streaming hash calculation upon ingestion. Recalculate hash on demand to detect unauthorized file tampering or disk corruption without ever overwriting the baseline.
- **Append-Only Chain of Custody**: Chronological, immutable custody trail tracking every upload, verification, transfer, and export. Ordinary and administrative users cannot modify or delete historical custody entries.
- **Security Log Analysis**: Pandas & Regex powered ingestion of server, authentication (SSH/Auth.log), and firewall logs with failed login aggregation and hostile IP extraction.
- **AI-Assisted Threat Heuristics**: Anomaly detection engine that maps events to MITRE ATT&CK tactics, computes risk scores (0–100), explains *why* an event is suspicious, and provides step-by-step containment instructions.
- **Forensic PDF Dossier Generation**: High-resolution, multi-page PDF generation via ReportLab complete with evidence hash tables, custody matrices, and examiner sign-off blocks.

---

## 2. Technology Stack

### Backend
- **Framework**: Python 3.12 + FastAPI (High-performance Async REST APIs)
- **Database Engine**: SQLAlchemy ORM with PostgreSQL & SQLite auto-fallback
- **Cryptographic Library**: Python `hashlib` (SHA-256 streaming verification)
- **Log Processing**: `pandas` & standard Python regex
- **Security & Authentication**: `bcrypt` (password hashing) + `pyjwt` (HMAC-SHA256 JWT tokens)
- **PDF Generation**: `reportlab` (forensic document layout engine)
- **File Handling**: `python-multipart`

### Frontend
- **Framework**: React 18 (Vite build system)
- **Styling**: Tailwind CSS with custom SOC dark glassmorphism theme (`#070B14`, `#0B0F19`, `#06B6D4`, `#3B82F6`)
- **Data Visualizations**: Recharts (Interactive Area velocity charts, Pie/Donut severity ratio, Bar distributions)
- **Icons**: Lucide React

---

## 3. System Architecture & Directory Layout

```text
cyber-incident-response/
│
├── backend/
│   ├── app/
│   │   ├── models/             # SQLAlchemy ORM Models (Users, Incidents, Evidence, CoC, Logs, Alerts, etc.)
│   │   ├── schemas/            # Pydantic v2 Request/Response validation schemas
│   │   ├── routes/             # FastAPI REST endpoints
│   │   │   ├── auth.py         # Login, registration, token issuance
│   │   │   ├── dashboard.py    # Real-time SOC metrics & velocity aggregation
│   │   │   ├── incidents.py    # Case CRUD, filtering, audit logging
│   │   │   ├── attack_details.py# Attack vectors, adversary IPs, IOCs
│   │   │   ├── evidence.py     # Upload, SHA-256 recalculation, tamper simulation, download
│   │   │   ├── chain_of_custody.py # Append-only custody logs & handover
│   │   │   ├── logs.py         # Pandas log parser & statistical aggregation
│   │   │   ├── threat.py       # AI/rule-based threat heuristics engine
│   │   │   ├── reports.py      # ReportLab PDF dossier generation & download
│   │   │   ├── users.py        # Investigator & examiner directory
│   │   │   └── alerts.py       # Tamper and critical threat alerts
│   │   ├── services/           # Core forensic logic (hash_service, log_parser, threat_service, pdf_report)
│   │   ├── security/           # JWT token management & RBAC dependencies
│   │   ├── utils/              # Sample data seeders & validators
│   │   ├── config.py           # Application settings
│   │   ├── database.py         # Database engine & session provider
│   │   └── main.py             # FastAPI application entrypoint & lifespan
│   ├── uploads/                # Isolated digital evidence storage vault
│   ├── reports/                # Generated forensic PDF reports
│   ├── sample_data/            # Sample authentication & web logs for testing
│   ├── requirements.txt        # Python backend dependencies
│   ├── schema.sql              # Pure PostgreSQL initialization script
│   └── .env                    # Configuration variables
│
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable UI (Navbar, Sidebar, StatCards, Timeline, HashModal, Badges)
│   │   ├── pages/              # Module Views (Dashboard, Incidents, Evidence, CoC, Logs, Threat, Reports, etc.)
│   │   ├── services/           # Frontend API client (api.js)
│   │   ├── App.jsx             # Main router & application controller
│   │   ├── main.jsx            # React root mounting
│   │   └── index.css           # Tailwind & custom cyber styling
│   ├── index.html              # HTML5 entrypoint
│   ├── package.json            # NPM dependencies & scripts
│   ├── vite.config.js          # Vite config & API reverse proxy
│   └── tailwind.config.js      # Custom theme extensions
│
├── test_system.py              # Automated End-to-End Test Suite (Tests all 11 workflows)
├── run_backend.bat             # One-click Windows backend launcher
├── run_frontend.bat            # One-click Windows frontend launcher
└── README.md                   # Complete documentation
```

---

## 4. Default Demonstration Credentials

The application automatically seeds realistic enterprise demo data upon first launch:

| Role | Username | Password | Badge ID | Department |
| :--- | :--- | :--- | :--- | :--- |
| **SOC Director (Admin)** | `admin` | `Admin@1234` | `SOC-DIR-001` | Cyber Threat Operations |
| **Lead Forensics Investigator** | `investigator` | `Investigator@1234` | `DFIR-INV-042` | Digital Forensics Unit |

---

## 5. Quick Start & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### Step 1: Start Backend Server
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend Swagger API Documentation:* `http://127.0.0.1:8000/docs`

### Step 2: Start Frontend Development Server
```bash
cd frontend
npm install
npm run dev
```
*Frontend Application:* `http://localhost:5173`

*(On Windows, you can also double-click `run_backend.bat` and `run_frontend.bat`)*

---

## 6. Technical Evaluation & Jury Demonstration Guide

To demonstrate the full end-to-end functionality of the platform:

1. **Authentication & RBAC**:
   - Open `http://localhost:5173`.
   - Click the "SOC Director (Admin)" or "Lead Forensics" quick-login button to sign in.
2. **Dashboard Overview**:
   - Observe live metric cards, rolling 7-day ingestion velocity charts, severity ratios, and recent activities.
3. **Incident Case Management**:
   - Navigate to **Incident Cases**. Filter by severity (`Critical`), status, or search terms.
   - Click **Create New Case** to record a case.
4. **Attack Detail Profiling**:
   - Navigate to **Attack Details** to view mapped MITRE ATT&CK tactics, adversary IPs, and registered IOCs.
5. **Digital Evidence Vault & SHA-256 Ingestion**:
   - Navigate to **Evidence Vault**.
   - Ingest an artifact (e.g. `alphv_ransom_note.txt` or any local file).
   - Observe immediate calculation of the 64-character SHA-256 hash.
6. **Cryptographic Integrity Verification & Tamper Simulation**:
   - In Evidence Vault, click **Verify Hash** on any evidence item.
   - Review baseline hash vs. current disk hash (`VERIFIED`).
   - Click **Simulate Evidence Tampering (Jury Demo)**: The system modifies a byte on disk and immediately recalculates the hash. Notice how the status flashes **MODIFIED (TAMPER DETECTED)** and generates an immediate critical security alert in the top notification bell!
7. **Append-Only Chain of Custody**:
   - Navigate to **Chain of Custody**.
   - Notice the chronological timeline showing collection, upload, verification, and tamper events.
   - Click **Record Custody Handover** to log a formal transfer to a forensics lab with mandatory remarks.
8. **Security Log Analysis**:
   - Navigate to **Log Analysis**.
   - Click **Load Sample Auth Log** or **Load Sample SQLi Log**.
   - Click **Parse & Analyze Logs** to run the Pandas analysis.
   - Inspect failed logins, suspicious IPs, risk scores, and the parsed inspector table.
9. **AI-Assisted Threat Intelligence**:
   - Navigate to **Threat Intelligence**.
   - Select an incident case or paste raw command lines.
   - Inspect the calculated Threat Risk Rating (0–100), MITRE mapping, technical rationale, and recommended containment steps.
10. **Investigation Report Generation**:
    - Navigate to **Investigation Reports**.
    - Click **Generate Forensic PDF Dossier**. Select a case and enter examiner notes.
    - Download and open the generated multi-page PDF to review the official forensic dossier.

---

## 7. Legal & Forensic Notice
Application-level custody tracking and cryptographic hashing demonstrate digital evidence handling compliance. In formal judicial proceedings, application controls should be combined with hardware write-blockers and air-gapped forensic storage media.
