# 🛡️ ShadowGram: Autonomous AI Swarm Fraud Defense Cyber-Range
**Event:** HackAthena 2026 | **Track:** Track 04 (Synthetic Identity & KYC) & Track 05 (Open Fraud)  
**Architecture:** 4-Laptop Live Multi-Station Cyber-Range over Local Mobile Hotspot (`ShadowGram-AP`)  
**Core Thesis:** Relational Graph Behavioral Forensics ($Q \ge 0.72$) — *Destroying the AI Syndicate Hive, Not Playing Whack-a-Mole*.

---

## 🗂️ 4-Station Live Cyber-Range Matrix

| Station | Lead | Hardware | Core Engine & Responsibility |
| :--- | :--- | :--- | :--- |
| **Station 1 (Red Team Swarm)** | **Alan Alexander** | Gaming Laptop #1 (Windows/NVIDIA) | 20-Context Playwright Bot Swarm, Flash & Hogan Neuromotor Trajectory Generator, NVIDIA NIM Identity Generator |
| **Station 2 (Lead Hub & 3D Cockpit)** | **ParadoxPete & Aiswarya** | Gaming Laptop #2 (Linux / Dedicated GPU) | **Pete:** FastAPI Backend Gateway, Louvain Graph Modularity Engine, Kinetic Jerk Classifier<br>**Aiswarya:** Three.js 3D Force-Directed Graph Cockpit, Laser Emissive Shaders, Web Audio SFX |
| **Station 3 (Target Portal)** | **Judge Interaction** | Laptop #3 (Windows/Mac) | AthenaPay Micro-Credit Portal, 6-Second Judge Testing Rule (95% pre-filled), Zero-PII Telemetry SDK |
| **Station 4 (Legal & Compliance)** | **Ashlin & Mohammed Nihad** | Laptop #4 (Windows) | NVIDIA NIM Llama-3.3-70B Legal Engine (15s), 2-Page Courtroom SAR PDF Exporter, KYC ELA/Diffusion Scanner |

---

## ⚡ Role 3: Red-Team Swarm Runner & Client Telemetry (Alan E Alexander)

### 1. Flash & Hogan Neuromotor Kinematics (`simulation/trajectory.py`)
* Implements biological 5th-degree minimum-jerk polynomial curves:
  $$s(\tau) = 10\tau^3 - 15\tau^4 + 6\tau^5$$
* Features dynamic overshoot correction when target distance exceeds 220px.
* Emulates realistic 8–12 Hz physiological micro-tremor with zero external dependencies.

### 2. High-Performance Swarm Runner (`simulation/swarm_runner.py`)
* **Strict Memory Limit:** Operates **1 single Chromium process** with 20 lightweight isolated `BrowserContext` instances.
* **Media Route Abort:** Intercepts and blocks images, fonts, and styles, keeping total RAM consumption **strictly < 600MB**.
* **Micro-Temporal Arrival Burst:** Synchronizes all 20 bot loan applications within a tight **1.4-second arrival window** ($Z > 4.5$).
* **Dual Operation Modes:** Supports full Playwright browser automation or high-speed direct synthetic telemetry dispatch.

### 3. Live NVIDIA NIM Persona Generator (`simulation/generate_personas.py`)
* Connects live to NVIDIA NIM (`meta/llama-3.2-11b-vision-instruct` / `meta/llama-3.3-70b-instruct`) via OpenAI-compatible endpoints.
* Generates 20 authentic Indian identities with varied occupations, cities, PANs, and convincing emergency loan reasons.
* Includes a local deterministic generator so the system works 100% offline if venue Wi-Fi drops.

### 4. Client Telemetry SDK (`public/telemetry.js`)
* **Zero-PII Mandate:** Captures no key characters, names, or values. Only records millisecond time deltas ($\Delta t$): Key Flight Time and Key Dwell Time.
* **50ms Cursor Throttle:** Samples cursor coordinates at most once per 50ms to guarantee zero UI lag when a visiting judge types.
* **Cryptographic HMAC Signing:** Signs every telemetry batch using `HMAC_SHA256(session_id + timestamp, session_salt)` to reject forged cURL requests.
* **Honey-DOM Tripwire:** Detects clicks on invisible DOM elements (`#honey-dom-profile-sync`) to flag crude automated scrapers instantly.

### 5. AthenaPay Target Portal (<6-Second Judge Testing Rule)
* Built in both React/Next.js ([`app/loan/page.tsx`](app/loan/page.tsx)) and standalone HTML ([`public/athenapay_portal.html`](public/athenapay_portal.html)).
* 95% pre-filled by default (Name: Rohan Verma, PAN: ABCDE1234F, Income: ₹45,000, Amount: ₹10,000).
* Exactly **1 editable field**: *"Loan Reason: [ Type 3 words ]"*.
* Allows a visiting hackathon judge to walk up, type 3 words, click apply, and complete an authentic human test in under 6 seconds.

---

## 🧪 Verification & Testing

### 1. Lead Architect Backend & Forensics (Role 1)
```bash
PYTHONPATH=. venv/bin/pytest -v
# Output: 11 passed in 3.8s (100% pass rate)
```

### 2. Red-Team Swarm & Telemetry (Role 3 - Alan)
```bash
python tests/test_role3_pipeline.py
# Output: 4 passed in 1.08s (100% pass rate)
```

---

## 🚀 Live Demonstration Execution

### Station 2: Launch Central Forensics Gateway (Laptop 2)
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Station 3: Launch AthenaPay Portal (Laptop 3)
```bash
python -m http.server 3000 --directory public
```
Open `http://localhost:3000/athenapay_portal.html` in browser.

### Station 1: Launch Swarm Attack (Laptop 1)
```bash
# Live Playwright browser attack:
python simulation/swarm_runner.py --target-url http://192.168.43.3:3000 --bots 20

# Direct high-speed synthetic mode (fallback):
python simulation/swarm_runner.py --direct --telemetry-url http://192.168.43.2:8000/telemetry --bots 20
```

### Station 4: Launch Compliance & SAR Terminal (Laptop 4)
```bash
set SHADOWGRAM_SERVER=http://192.168.43.2:8000
python compliance_terminal.py
```

---

---

## 📚 Master Documentation, Specifications & Deliverables

### 🏆 Presentation Decks & Interactive Live Pitch Matrix
* [**`public/presentation_roles_and_pitch_script.html`**](public/presentation_roles_and_pitch_script.html) — Interactive 10-Minute Judging Dashboard with countdown timer, slide-by-slide scripts, hardware triggers, and filterable 10-card Judge Q&A Defense Matrix.
* [**`Final ppt template.pptx`**](Final%20ppt%20template.pptx) — The official HackAthena'26 5-slide competition presentation deck (featuring transparent card containers, slate borders, and 24pt bold typography).
* [**`ShadowGram_Final_Demo_Presentation.pptx`**](ShadowGram_Final_Demo_Presentation.pptx) — Standalone presentation deck backup.

### 🔬 Technical Specifications & Mathematics
* [**`SHADOWGRAM_THE_COMPLETE_JOURNEY_STORY.md`**](SHADOWGRAM_THE_COMPLETE_JOURNEY_STORY.md) — Comprehensive narrative chronicle of the entire project, architecture pivot, real-world trials, and 28 Git commits.
* [**`SHADOWGRAM_PHASE2_STE100_TECHNICAL_SPECIFICATION.md`**](SHADOWGRAM_PHASE2_STE100_TECHNICAL_SPECIFICATION.md) — Complete Phase 2 Technical Specification written in ASD-STE100 (Simplified Technical English).
* [**`public/shadowgram_phase2_technical_specification_ste100.html`**](public/shadowgram_phase2_technical_specification_ste100.html) — ASD-STE100 interactive HTML specification with vector SVG diagrams.
* [**`SHADOWGRAM_MATHEMATICAL_AND_DETECTION_DEEP_DIVE.md`**](SHADOWGRAM_MATHEMATICAL_AND_DETECTION_DEEP_DIVE.md) — Mathematical proofs (Flash-Hogan minimum jerk, 5-layer multiplex tensor, Louvain modularity $Q$, Maslov-Sneppen null model).
* [**`PHASE_2_MASTER_DEMO_AND_MATHEMATICS_SPECIFICATION.md`**](PHASE_2_MASTER_DEMO_AND_MATHEMATICS_SPECIFICATION.md) — Master demonstration specifications and sensor thresholds.

### 📋 Protocols, Audits & Station Guides
* [`PROGRESS_CHECKPOINT_LEAD.md`](PROGRESS_CHECKPOINT_LEAD.md) — Lead Architect (Pete) M1 & M2 Milestone Certification.
* [`PROGRESS_CHECKPOINT_MEMBER3.md`](PROGRESS_CHECKPOINT_MEMBER3.md) — Red Team Lead (Alan) M1 & M4 Protocol Audit.
* [`00_CHECKPOINT_AND_INTEGRATION_PROTOCOL.md`](ShadowGram_Team_Execution_Pack/00_CHECKPOINT_AND_INTEGRATION_PROTOCOL.md) — Global Frozen Protocol and Cross-Platform Setup.
* [`SHADOWGRAM_EMPIRICAL_PROOFS_AND_AUDIT_DOSSIER.md`](SHADOWGRAM_EMPIRICAL_PROOFS_AND_AUDIT_DOSSIER.md) — Fact-checked legal & empirical research dossier.
* [`ShadowGram_Master_Book/`](ShadowGram_Master_Book/) — Complete 80-page forensic blueprint and empirical proof archive.
* [`stations/`](stations/) — Multi-station source packages for Alan (Station 1), Pete (Station 2), Aiswarya (Station 3), and Ashlin (Station 4).

---

## 🧪 Full Test Suite Execution (62/62 Tests Passing)
```bash
./venv/bin/python run_all_tests.py
# 62/62 verified across all 8 phases (100% success rate)
```

