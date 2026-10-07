# SHADOWGRAM: THE COMPLETE JOURNEY, ARCHITECTURAL EVOLUTION & CHRONICLE
**Document ID:** `SG-NARRATIVE-JOURNEY-2026`  
**Classification:** Master Project Narrative, Development Chronicle & Technical History  
**Authors:** ParadoxPete (Station 2), Aiswarya Kallayil (Station 3), Alan Alexander (Station 1), Mohammed Nihad & Ashlin Theres (Station 4)  
**Active Working Branch:** `feature/quarantine-popup-experiment`  
**Network State:** Multi-Laptop Local Hotspot LAN (`0.0.0.0:8000`)  

---

## PROLOGUE: THE HACKATHON DILEMMA

In early October 2026, the team assembled for **HackAthena '26** with a singular, high-stakes objective: solve the existential threat confronting global digital lending platforms—**coordinated autonomous AI agent swarms executing synthetic micro-lending fraud**.

Digital micro-lending platforms (e.g., KreditBee, Kissht, RupeeRedee, slice, and BNPL providers) disburse micro-loans within 3 to 5 minutes through automated credit evaluation pipelines. This instant liquidity creates an irresistible target for organized criminal syndicates. Instead of human fraudsters manually submitting applications, adversaries deploy swarms of hundreds or thousands of headless AI agents. These agents harvest real or synthetic Aadhaar/PAN identities, simulate human browsing, and trigger simultaneous micro-loan disbursements.

Every existing anti-fraud and bot defense tool on the market collapses under this attack model.

---

## ACT I: THE GENESIS & DECONSTRUCTION OF COMPETITOR FAILURES

Before writing a single line of backend code, our team conducted a deep forensic audit of existing commercial solutions:

```
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                           THE FOUR FATAL COMPETITOR FAILURE MODES                         │
├──────────────────────────┬─────────────────────────────┬──────────────────────────────────┤
│ Solution Category        │ Leading Vendors             │ Fatal Vulnerability / Blindspot  │
├──────────────────────────┼─────────────────────────────┼──────────────────────────────────┤
│ Single-User Behavioral   │ BioCatch, Neuro-ID,         │ Requires historical baselines.   │
│ Biometrics               │ BehavioSec                  │ Blind to new, synthetic users.   │
├──────────────────────────┼─────────────────────────────┼──────────────────────────────────┤
│ Consortium Device &      │ LexisNexis ThreatMetrix,    │ Bypassed by rotating 4G/5G mobile│
│ IP Intelligence          │ Sift Science, TransUnion    │ residential proxies & clean UDIDs│
├──────────────────────────┼─────────────────────────────┼──────────────────────────────────┤
│ Interactive Puzzles      │ Arkose Labs, Cloudflare     │ Vision-LLMs solve CAPTCHAs >70%; │
│ & CAPTCHAs               │ Turnstile, reCAPTCHA v3     │ destructive to human UX & dropoff│
├──────────────────────────┼─────────────────────────────┼──────────────────────────────────┤
│ Downstream KYC & Credit  │ Aadhaar e-KYC, PAN APIs,    │ Denial-of-Wallet (DoW) bleeding: │
│ Bureau Scoring           │ CIBIL, Experian             │ ₹61.00 fee per bot before denial │
└──────────────────────────┴─────────────────────────────┴──────────────────────────────────┘
```

### 1.1 The Behavioral Biometrics Trap (BioCatch & Neuro-ID)
Vendors like BioCatch evaluate whether a user's typing and mouse movements match *their historical profile*. In synthetic new-account fraud, **there is no historical baseline**. The synthetic identity is being created for the very first time. Furthermore, single-user models analyze each session in a vacuum. If a bot moves with reasonable smoothness, the single-user model scores it as a clean applicant.

### 1.2 The Consortium IP & Device Fingerprint Illusion (ThreatMetrix & Sift)
Legacy fraud consortiums flag shared IP addresses and known device fingerprints. Attackers bypass this effortlessly by routing each bot instance through unique 4G/5G mobile residential proxy pools (e.g., BrightData, Oxylabs) and spoofing Canvas/WebGL hashes. Even worse, when legitimate university students or office workers apply for loans on a **shared campus Wi-Fi**, consortiums suffer massive false-positive spikes because innocent people share the same public IP subnet.

### 1.3 The Denial-of-Wallet (DoW) Capital Drain
When a bot passes through the initial loan application form to Step 2, the lending platform triggers external identity verification APIs:
- **Aadhaar e-KYC:** ₹3.00 per check (UIDAI Gazette Notification, Oct 14, 2021).
- **PAN Database Match:** ₹2.00 per lookup.
- **Biometric Face Liveness:** ₹6.00 per video challenge.
- **Credit Bureau Pull:** ₹50.00 (CIBIL/Experian).

**Total Downstream Cost:** **₹61.00 per applicant**.  
If a bot swarm of 10,000 synthetic identities floods a lender, the platform loses **₹610,000 in unrecoverable API fees** within minutes—even if not a single fraudulent loan is ultimately approved.

### 1.4 The Breakthrough Hypothesis
Our core realization was clear:  
> **"Do not attempt to catch an AI bot by looking at it in isolation. A sophisticated bot looks indistinguishable from a human. But an AI bot swarm cannot hide its relational physics. Across time, route topologies, semantic narratives, and microsecond kinetics, a swarm always leaves an unalterable relational shadow."**

This insight birthed **ShadowGram**.

---

## ACT II: THE ARCHITECTURAL PIVOT: THE TWO-KEY DEFENSE

To defeat both naive automation and sophisticated stealth swarms without compromising human user experience, we designed the **Two-Key Defense Architecture**:

```
                       INCOMING APPLICANT SESSION
                                   │
                                   ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ KEY 1: Fast Biomechanical Tripwire (<0.02ms Decision)        │
    │ Inspects Physical DOM Invariants:                           │
    │ • Zero pre-click mousemove events (Playwright artifact)     │
    │ • Zero click dwell time (<5ms script injection)             │
    │ • Robotic key flight time (<12ms)                           │
    └─────────────────────────────────────────────────────────────┘
                  │                                 │
         [Flagged Naive Bot]               [Passed Key 1 / Stealth]
                  │                                 │
                  ▼                                 ▼
      Immediate RED Flagging           ┌────────────────────────────┐
      Locked before Form Step 2        │ KEY 2: 5-Layer Relational  │
      Saves ₹61.00 DoW Bleed           │ Hypergraph Physics Engine  │
                                       └────────────────────────────┘
                                                     │
                                                     ▼
                                       ┌────────────────────────────┐
                                       │ 3-Layer Sparsification     │
                                       │ Common-Cause Wi-Fi Disc.   │
                                       │ Leiden Community Detection │
                                       │ Maslov-Sneppen Null Model  │
                                       └────────────────────────────┘
                                                     │
                                                     ▼
                                       ┌────────────────────────────┐
                                       │ 3D Cockpit Operator Alert  │
                                       │ 1-Click Cluster Quarantine │
                                       │ Reversible 1-Rupee UPI     │
                                       │ Courtroom SAR PDF Dossier  │
                                       └────────────────────────────┘
```

### 2.1 Key 1: The Fast Biomechanical Tripwire ($<0.02\text{ms}$)
Operates statelessly per request. When a naive script (Selenium, Playwright, Puppeteer) clicks a button, it dispatches an instantaneous DOM `click` or `pointerdown` event without preceding mouse trajectories. A human hand cannot click a button without moving the cursor toward it and resting on the key for at least 30–120ms. If `mousemove_pre_click_count == 0` or `click_dwell_duration_ms < 5.0ms`, Key 1 flags the session immediately in under 20 microseconds.

### 2.2 Key 2: The Relational 5-Layer Hypergraph Engine
Stealth bots bypass Key 1 by adding artificial delay and synthetic Bézier curves. Key 2 catches them not by their individual properties, but by their **pairwise correlation across 5 orthogonal layers**:
1. **Layer 1 (Micro-Timing Dynamics):** Exponential decay arrival kernel ($s_{\text{time}} = \max(0, e^{-\Delta t / 10.0})$) detecting coordinated burst arrivals.
2. **Layer 2 (FSM Route Navigation):** Jaccard set overlap and Longest Common Subsequence (LCS) tracking identical finite-state paths.
3. **Layer 3 (Semantic Intent Geometry):** Dense 384-dimensional cosine similarity over applicant narrative text using `all-MiniLM-L6-v2`.
4. **Layer 4 (Motor Kinetics & Jerk Variance):** Third-derivative jerk analysis ($J = d^3x/dt^3$) and jerk coefficient of variation ($\text{CV}_J = \sigma(J) / \mu(|J|)$). Distinguishes continuous 8–12 Hz biological tremor from constant-jerk polynomial Bézier curves.
5. **Layer 5 (Client Environment Entropy):** Cryptographic WebGL/Canvas rendering hash match.

### 2.3 The 3-Layer Orthogonal Sparsification Filter
To prevent random false-positive connections, an edge is created between two accounts if and only if:
$$\tilde{W}_{ij} \ge 0.78 \quad \mathbf{AND} \quad \text{At least 3 orthogonal layers converge!}$$

---

## ACT III: MULTI-STATION DIVISION OF LABOR & HARDWARE TOPOLOGY

To prove real-world viability, the team divided into four specialized stations operating across a live mobile Wi-Fi Hotspot LAN (`10.215.30.0/24`):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        SHADOWGRAM MULTI-LAPTOP CYBER RANGE TOPOLOGY                    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   [STATION 1: ALAN]                  [STATION 2: PETE - CENTRAL HOST]                  │
│   IP: 10.215.30.174                  IP: 10.215.30.162 (Port 8000)                     │
│   Role: Red-Team Swarm Runner        Role: Forensics Gateway & Core Graph Engine       │
│   • Playwright Bot Swarm             • FastAPI Ingestion Gateway (`main.py`)           │
│   • Flash-Hogan Min-Jerk Trajectory  • 5-Layer Relational Tensor (`graph_engine.py`)   │
│   • Poisson-Jitter Burst Dispatches  • SQLite Database & WebSockets (`shadowgram.db`)   │
│   • Telemetry HMAC Generator         • 3D WebGL Operations Cockpit (`cockpit.html`)    │
│            │                                      ▲              ▲                     │
│            │ POST /telemetry                      │              │                     │
│            └──────────────────────────────────────┤              │                     │
│                                                   │              │                     │
│   [STATION 3: AISWARYA]                           │              │                     │
│   IP: 10.215.30.204                               │              │                     │
│   Role: Borrower Portal & Frontend Lead           │              │                     │
│   • AthenaPay Borrower Web App (`athenapay_portal.html`)         │                     │
│   • Zero-PII Client Telemetry SDK (`telemetry.js`)               │                     │
│   • Honey-DOM Tripwire Trap                       │              │                     │
│   • Automatic 1-Rupee UPI Step-Up Modal Interceptor              │                     │
│   • Setu / OneMoney Account Aggregator Sandbox    │              │                     │
│                                                   │              │                     │
│   [STATION 4: NIHAD & ASHLIN]                     │              │                     │
│   Role: Compliance Officer & Legal SAR Generator  │              │                     │
│   • Courtroom SAR PDF Vector Engine (`sar_generator.py`)─────────┘                     │
│   • Maslov-Sneppen Permutation Null Model ($p < 0.001$)                                │
│   • Tamper-Evident HMAC-SHA256 Audit Trail Seal                                        │
│   • Statutory Grounding: ECOA Reg B, RBI 2025, EU AI Act                               │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ACT IV: THE COMMIT-BY-COMMIT EVOLUTION CHRONICLE (ALL 28 COMMITS)

Every major milestone, architectural decision, and bug fix in the Git repository is documented below:

| # | Commit SHA | Author | Date & Time | Commit Message & Technical Rationale |
|:---|:---|:---|:---|:---|
| 1 | `ed36c26` | wolf-eye0 | Oct 6 01:15 UTC | **Initial commit: ShadowGram Autonomous AI Swarm Defense architecture, team execution pack, and forensic engine.** Established project structure, initial architecture notes, and multi-role team execution manuals. |
| 2 | `2103576` | wolf-eye0 | Oct 6 01:42 UTC | **Implement core FastAPI backend, graph engine, kinetic classifier, and tests.** Scaffolded FastAPI gateway, initial NetworkX graph class, and basic kinetic trajectory evaluator. |
| 3 | `27bd9cb` | wolf-eye0 | Oct 6 01:55 UTC | **Add Principal Architect M1 & M2 milestone report.** Outlined system benchmarks, delivery deadlines, and multi-laptop hardware verification requirements. |
| 4 | `7a70a1c` | wolf-eye0 | Oct 6 02:10 UTC | **Support Alan's telemetry HMAC salt and formatting.** Synchronized cryptographic signature routines between frontend SDK and backend ingestion gateway to reject cURL tampering. |
| 5 | `283b93c` | Alan Alexander | Oct 6 02:25 UTC | **feat(role-3): ShadowGram Red-Team Swarm Runner & Client Telemetry Engine.** Alan implemented Station 1 Playwright runner with headless browser contexts and client telemetry collection. |
| 6 | `55d9ee5` | wolf-eye0 | Oct 6 02:35 UTC | **Merge Alan's Role 3 Red-Team Swarm Runner & Client Telemetry Engine.** Merged Station 1 codebase into the master integration tree. |
| 7 | `09ad1bb` | wolf-eye0 | Oct 6 03:05 UTC | **feat(core): Multi-station build v2, stress-test defenses, and role manuals.** Established individual station subfolders (`stations/station1_alan_swarm`, `stations/station2_pete_backend`, etc.) allowing parallel offline development. |
| 8 | `b70bcef` | wolf-eye0 | Oct 6 03:30 UTC | **feat(core): Evidence-Carrying Edges, Common-Cause Discount & Benchmark Suite v2.1.** Added evidence metadata to NetworkX edges, implemented Common-Cause subnet discount (-0.35 weight) for campus Wi-Fi, and built the initial benchmark suite. |
| 9 | `dd09315` | wolf-eye0 | Oct 6 04:02 UTC | **feat(core): calibrated relational multi-layer physics, 100% benchmark lift & 61/61 test pass.** Calibrated layer weights (`w = [0.25, 0.25, 0.25, 0.15, 0.10]`), achieving 100% recall on synthetic bot swarms and passing all 61 tests. |
| 10 | `fbc8487` | wolf-eye0 | Oct 6 04:52 UTC | **feat(core): calibrated relational multi-layer physics, 100% benchmark lift & 61/61 test pass.** Pushed backend-core verification tag to origin. |
| 11 | `9d37d18` | wolf-eye0 | Oct 6 06:12 UTC | **feat(book): embedded 13-point empirical audit table, live master book serving at /master_book.html and calibrated dynamic cockpit.** Embedded 80-page ASD-STE100 Master Book into FastAPI web server and connected Cockpit to dynamic backend polling. |
| 12 | `42f389c` | wolf-eye0 | Oct 6 07:20 UTC | **checkpoint(phase-1): mathematical deep-dive, what we innovated, Phase 1 status audit and Phase 2 roadmap.** Formalized Phase 1 checkpoint completion report and outlined the 6 Phase 2 innovation tracks. |
| 13 | `5daafa8` | wolf-eye0 | Oct 6 08:18 UTC | **docs(phase-1): finalize mathematical deep dive HTML specs and navigation routes.** Added mathematical deep dive HTML document and wired `/mathematical_deep_dive.html` route in FastAPI. |
| 14 | `57afad0` | wolf-eye0 | Oct 6 08:29 UTC | **docs(phase-2): add deep research audit dossier and team station execution guide.** Documented competitor analysis, Indian KYC pricing regulations, and ECOA adverse action requirements. |
| 15 | `6b8bf08` | Alan Alexander | Oct 6 09:19 UTC | **feat(station1): add dynamic Poisson jitter attack mode & digraph telemetry.** Alan added non-stationary Poisson burst delays to simulate sophisticated human typing speeds and financial digraph intervals. |
| 16 | `9950e3d` | wolf-eye0 | Oct 6 09:20 UTC | **feat(phase-2): implement Track 4 dynamic sensitivity slider & Track 6 tactical audio alerts.** Added real-time sensitivity slider ($\theta \in [0.40, 0.95]$) and Web Audio API synthesized tactical audio pings to Cockpit. |
| 17 | `0f161b1` | Alan Alexander | Oct 6 09:44 UTC | **feat(station1): add dual-mode persona loader with live NVIDIA NIM GenAI and cached options.** Added integration with NVIDIA NIM Llama-3.2 to generate synthetic Indian loan narratives on the fly, with local offline cache fallback. |
| 18 | `3fef270` | Ashlin Theres | Oct 6 10:27 UTC | **feat(compliance): embed Maslov-Sneppen p-value null model, RBI 2025 clauses & HMAC seal in SAR PDF.** Ashlin integrated degree-preserving permutation null test results and HMAC-SHA256 evidence seals into ReportLab SAR generator. |
| 19 | `6c2acc6` | Alan Alexander | Oct 6 10:52 UTC | **feat(station1): add comprehensive Station 1 & Phase 2 verification suite with live NVIDIA NIM and Two-Key defense checks.** Station 1 verification suite verifying both naive and stealth bot evasion patterns. |
| 20 | `588c683` | wolf-eye0 | Oct 6 11:16 UTC | **merge(alan): integrate Station 1 Phase 2 dynamic Poisson jitter swarm, digraph telemetry, and verification suite.** Merged Station 1 innovations into central branch. |
| 21 | `5e55e87` | wolf-eye0 | Oct 6 11:16 UTC | **docs(research): add Phase 2 Deep Research audit and offline test resilience.** Hardened test suite to guarantee 100% offline execution without active internet or HuggingFace model downloads. |
| 22 | `f3a1008` | wolf-eye0 | Oct 6 11:22 UTC | **merge(ashlin): integrate Station 4 Phase 2 SAR generator with Maslov-Sneppen p-value null model, RBI 2025 clauses & HMAC seal.** Merged Station 4 compliance deliverables into central branch. |
| 23 | `06e0577` | wolf-eye0 | Oct 6 11:24 UTC | **feat(aiswarya): integrate Track 5 Account Aggregator (Setu/OneMoney) sandbox in borrower portal and research notes.** Aiswarya integrated RBI Account Aggregator consent simulation in `athenapay_portal.html`. |
| 24 | `fe00b55` | wolf-eye0 | Oct 6 11:34 UTC | **fix(integration): make generate_sar_pdf polymorphic, sync stations, and ensure reliable packet delivery in direct swarm.** Updated `generate_sar_pdf` to accept both raw dicts and cluster IDs, returning bytes or saving to disk polymorphically. |
| 25 | `fd9380c` | Ashlin Theres | Oct 6 12:59 UTC | **fix(compliance): add CFPB Circular 2023-03 statutory citation to SAR regulatory headers.** Embedded CFPB Circular 2023-03 citations prohibiting black-box AI credit underwriting into SAR headers. |
| 26 | `c84c24c` | wolf-eye0 | Oct 6 14:16 UTC | **sync(station4): align station4 fallback_sar and nim_client with CFPB Circular 2023-03 compliance headers.** Synchronized Station 4 fallback templates with the central backend. |
| 27 | `91ab476` / `aa02d1e` | wolf-eye0 | Oct 6 15:31 UTC | **The Dark Screen Emergency & Resolution:** During Wi-Fi testing on Aiswarya's laptop, `athenapay_portal.html` rendered a dark blank screen due to an unclosed `<style>` block before `</head>`. Commit `91ab476` fixed it, was briefly reverted in `aa02d1e`, and permanently restored. |
| 28 | `a2c557b` | wolf-eye0 | Oct 6 17:34 UTC | **feat(quarantine): auto-popup 1-rupee UPI step-up modal upon operator quarantine with real-time sync.** Implemented real-time polling in `athenapay_portal.html` listening for quarantine events to auto-popup the Step-Up modal. |

---

## ACT V: CRITICAL BUGS, TRIALS & LIVE BREAKTHROUGHS

Building a live, cross-laptop cyber range in a live hackathon environment produced several real-world technical crises that required immediate forensic debugging.

### 5.1 Trial 1: The "Dark Screen / Blank Page" Incident
* **The Symptom:** When Aiswarya navigated to `http://10.215.30.162:8000/athenapay_portal.html` on her laptop, the screen rendered completely black/blank, with no UI inputs visible.
* **The Root Cause:** In merging styling updates for the glassmorphism theme, a closing `</style>` tag had been accidentally omitted before the `</head>` tag. As a result, the browser's HTML parser treated the entire `<body>` section as inline CSS, preventing DOM construction.
* **The Fix:** Restored the `</style>` tag across both `public/athenapay_portal.html` and `stations/station3_aiswarya_frontend/athenapay_portal.html`. The page immediately rendered crisp and responsive across the Wi-Fi LAN.

### 5.2 Trial 2: The Premature "Loan Approved" Disbursal Bug
* **The Symptom:** When Pete quarantined Aiswarya's session from the 3D Cockpit (turning her node RED/AMBER), Aiswarya filled out the loan form and clicked "APPLY NOW". To our dismay, the portal immediately displayed: *"Loan Approved! Disbursal Initiated"*. The quarantine was ignored!
* **The Root Cause Analysis:** Examination of `athenapay_portal.html#L305-L346` revealed that the client-side `form.addEventListener('submit')` simply pushed a telemetry event and immediately flipped the display state:
  ```javascript
  // The Buggy Code:
  form.style.display = 'none';
  successBox.style.display = 'block'; // Premature approval without checking status!
  ```
  The form never queried the server to verify whether the session was flagged or quarantined!
* **The Architectural Solution:** We rewrote the form submission handler to execute a synchronous in-flight check against `GET /api/session/status` (<15ms latency):
  ```javascript
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    // 1. Push and flush final submission telemetry
    window.ShadowGramTelemetry.pushEvent('loan_submit', ...);
    window.ShadowGramTelemetry.flush();

    // 2. Query live session state from backend
    const statusData = await window.ShadowGramTelemetry.checkStatus();

    // 3. If session is flagged RED (Key 1) or quarantined AMBER (Key 2):
    const requiresStepUp = isQuarantined || isFlagged || (statusData && statusData.requires_stepup);
    if (requiresStepUp) {
      // INTERCEPT DISBURSAL IMMEDIATELY!
      triggerQuarantineStepUp('Verification required before loan disbursal');
      return;
    }

    // 4. Honest Human: Disburse loan
    form.style.display = 'none';
    successBox.style.display = 'block';
  });
  ```
* **The Backend Sync:** Updated `backend/graph_engine.py` and `backend/main.py`:
  - `quarantine_cluster` was updated to support individual `account_id` quarantine in addition to cluster-wide isolation.
  - Added `GET /api/session/status?account_id=...` returning `{ is_flagged, is_quarantined, requires_stepup }`.
  - Added custom DOM event `shadowgram:quarantined` dispatched by `telemetry.js` when the server flags a packet.

---

## ACT VI: CURRENT OPERATIONAL STATE & PHASE 3 HORIZON

### 6.1 What Is Functioning Right Now?
1. **Live Wi-Fi Server:** FastAPI gateway running on `0.0.0.0:8000` (`task-3453`).
2. **Borrower Experience:** Aiswarya's laptop (`10.215.30.204`) interacts with `athenapay_portal.html` with Zero-PII keystroke dynamics, Honey-DOM tripwires, and live Step-Up interception.
3. **Forensics Cockpit:** Pete's laptop (`10.215.30.162`) renders the Three.js 3D force-directed graph with 60 FPS orbit controls, live Louvain modularity ticker ($Q = 0.8118$), tactical audio pings, and 1-click quarantine.
4. **Red-Team Swarm:** Alan's Playwright runner dispatches naive and stealth bot swarms with Flash-Hogan minimum-jerk kinematics.
5. **Courtroom SAR Generator:** Nihad's ReportLab vector engine compiles 2-Page legal SAR PDFs with Maslov-Sneppen permutation test charts ($p = 0.0002$) and HMAC-SHA256 evidence seals in $<20\text{ms}$.
6. **Full Test Health:** 62 out of 62 unit, integration, and regression tests pass with 0 failures (`run_all_tests.py`).

### 6.2 Empirical Benchmark Proofs (Phase 3 Stage Evaluation)
Testing across 120 heterogeneous sessions (`benchmark_evaluation.py`) establishes:
- **Net Graph Lift:** **+33.3% F1 score** over single-user baselines ($1.0000$ vs $0.6667$).
- **Stealth Bot Catch Rate:** **100.0% (20/20)** vs **0.0% (0/20)** for legacy filters.
- **Campus Wi-Fi False Positives:** **0 out of 30** (100% precision preserved by Common-Cause Subnet Discount).
- **Pre-KYC Capital Saved:** **₹2,440.00 INR** across 40 blocked attackers.

ShadowGram stands ready for the final judging round: mathematically rigorous, legally sound, and battle-tested live across the local Wi-Fi LAN.
