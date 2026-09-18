# AI-Powered Network Anomaly Detection System (SOC Platform)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end, enterprise-grade Security Operations Center (SOC) platform for real-time network packet inspection, multi-tier anomaly detection, automated incident analysis with Generative AI (Google Gemini), and active threat mitigation.

Developed by **Ongkar Pal** (Galgotias University).

---

## Key Features

- **Live Packet Capture & Parsing**: Real-time traffic ingestion and parsing powered by `Scapy` across TCP, UDP, ICMP, DNS, HTTP, and TLS protocols.
- **Multi-Tier Detection Engine**:
  - **Rule-Based Engine**: Detects signature threats, dangerous/uncommon port communication, protocol anomalies, and malformed flags.
  - **Machine Learning Detector**: Isolation Forest and statistical anomaly scoring on packet metrics.
  - **UEBA (User & Entity Behavior Analytics)**: Detects deviations from baseline network activity and sudden exfiltration spikes.
  - **Rate Limiting & DDoS Defense**: Tracks per-IP velocity thresholds and triggers automated mitigations on flood attempts.
  - **Threat Intelligence Integration**: Real-time IP reputation and malicious score checks via AbuseIPDB API.
  - **Active IPS Mitigation**: Dynamic IP blocking, packet dropping, and firewall rule enforcement.
- **Interactive SOC Dashboard**:
  - Dark-mode glassmorphic interface with real-time charts (`Chart.js`).
  - Live anomaly alert feed with severity color coding (Critical, High, Medium, Low).
  - Geographic threat intelligence and source/destination IP flow visualization.
  - Network graph inspection of active nodes.
- **Generative AI Analyst (Sentinel)**:
  - Incident response plan generation with Google Gemini (`gemini-2.5-flash`).
  - Interactive AI SOC assistant for natural-language threat investigation and triage recommendations.
  - Graceful fallback mock engine if no API key is configured.
- **Automated Security Audit Reporting**:
  - Dynamic PDF report generation summarizing network traffic, threat distributions, and MITRE-aligned incident logs.
- **Built-in Attack Simulation**:
  - Automated attacker script (`simulate_attack.py`) simulating high-velocity UDP floods, data exfiltration, and malformed TCP payloads.

---

## Project Architecture

```
network-anomaly-detection/
├── backend/
│   ├── alerts/              # Alert dispatching and notification management
│   ├── api/                 # FastAPI routers (traffic, alerts, analytics, llm, reports)
│   ├── database/            # SQLAlchemy models, PostgreSQL connection, CRUD operations
│   ├── detection/           # Rule-based, ML detector, UEBA, IPS, threat intelligence
│   ├── logs/                # Sniffer packet logs (network_traffic.csv)
│   ├── packet_capture/      # Scapy live packet sniffer
│   ├── utils/               # DNS resolver and network helpers
│   ├── create_tables.py     # Database schema initializer
│   └── main.py              # FastAPI application entry point
├── frontend/
│   └── index.html           # Full SOC Dashboard UI (served directly at root)
├── reports/
│   ├── Project_Report.md    # Comprehensive academic and technical project report
│   ├── Project_Report.pdf   # Pre-compiled PDF report
│   └── generate_pdf.py      # Automated report generator
├── datasets/                # Sample PCAP / CSV datasets
├── ml_models/               # Serialized ML models
├── .env.example             # Environment variable template
├── requirements.txt         # Project dependencies
├── simulate_attack.py       # Attack simulation script for testing
└── start.bat                # Windows one-click startup script
```

---

## Prerequisites

1. **Python 3.10+** installed on your system.
2. **PostgreSQL** database (running on port 5432 or configured in `backend/database/connection.py`).
3. **Npcap** (Windows) or **libpcap** (Linux/macOS) installed for Scapy packet sniffing:
   - On Windows: Install [Npcap](https://npcap.com/) with "WinPcap API-compatible Mode" enabled.

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ongkar08/network-anomaly-detection.git
cd network-anomaly-detection
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the sample environment file:

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys (optional, system falls back to simulation mode if keys are not provided):

```env
GEMINI_API_KEY=your_gemini_api_key_here
ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here
```

### 5. Initialize the Database

Ensure PostgreSQL is running and initialize the tables:

```bash
python backend/create_tables.py
```

---

## Running the Application

### Option A: One-Click Startup (Windows)

Simply run:

```cmd
start.bat
```

This starts the FastAPI backend server and launches the packet capture sniffer in parallel.

### Option B: Manual Startup

**Terminal 1 — FastAPI Backend Server:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Live Packet Sniffer (Run with Administrator privileges):**
```bash
python backend/packet_capture/sniffer.py
```

Open your browser and navigate to:
```
http://localhost:8000
```

---

## Testing & Simulating Attacks

To test the anomaly detection pipeline, launch the attack simulation script in a separate terminal:

```bash
python simulate_attack.py
```

This will generate:
1. **High-Velocity UDP Flood** (Trips the rate limiter and DDoS detection).
2. **Data Exfiltration** (Trips UEBA and large packet payload detectors).
3. **Malformed TCP Anomalies** (Trips rule-based and ML detectors).

Watch the SOC dashboard at `http://localhost:8000` react in real time.

---

## Author

- **Ongkar Pal** ([@Ongkar08](https://github.com/Ongkar08))
- B. Tech CSE, Galgotias University
