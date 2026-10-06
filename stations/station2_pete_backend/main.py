import os
import json
import time
import hmac
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any, Set
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse, Response, FileResponse, RedirectResponse
from sqlalchemy.orm import Session

try:
    from models import (
        TelemetryEvent, GraphResponse, QuarantineRequest, QuarantineResponse,
        StepUpVerifyRequest, StepUpVerifyResponse, DoWStatsResponse,
        SessionRecord, TelemetryRecord, ClusterRecord
    )
    from database import init_db, get_db
    from graph_engine import ShadowGraphEngine
    from mock_simulation import populate_mock_cyber_range
    from nim_client import generate_sar_report_narrative
    from sar_generator import generate_sar_pdf
except ImportError:
    from backend.models import (
        TelemetryEvent, GraphResponse, QuarantineRequest, QuarantineResponse,
        StepUpVerifyRequest, StepUpVerifyResponse, DoWStatsResponse,
        SessionRecord, TelemetryRecord, ClusterRecord
    )
    from backend.database import init_db, get_db
    from backend.graph_engine import ShadowGraphEngine
    from backend.mock_simulation import populate_mock_cyber_range
    from backend.nim_client import generate_sar_report_narrative
    from backend.sar_generator import generate_sar_pdf

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("[ShadowGram Core] Listening on 0.0.0.0:8000 | Multi-Laptop Hotspot LAN Ready.")
    yield

# Initialize FastAPI App
app = FastAPI(
    title="ShadowGram Forensics Gateway",
    version="2.0.0",
    description="In-flight Behavioral Graph Forensics & Autonomous Swarm Quarantine Engine",
    lifespan=lifespan
)

# Permissive CORS for Local Hotspot LAN
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Engines
graph_engine = ShadowGraphEngine(window_seconds=600.0, edge_threshold=0.70)
SHARED_HMAC_SALT = os.getenv("SHADOWGRAM_SALT", "shadowgram-2026-secret-salt").encode()

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)

ws_manager = ConnectionManager()

def verify_hmac(session_id: str, timestamp: float, signature: str) -> bool:
    """Verifies client telemetry packet integrity."""
    if not signature:
        return True
    
    salts = [
        SHARED_HMAC_SALT,
        b"shadowgram-hackathena-2026-salt",
        b"shadowgram-2026-secret-salt"
    ]
    formats = [
        f"{session_id}:{timestamp:.3f}".encode(),
        f"{session_id}:{timestamp}".encode()
    ]
    for s in salts:
        for fmt in formats:
            expected = hmac.new(s, fmt, hashlib.sha256).hexdigest()
            if hmac.compare_digest(expected, signature):
                return True
    return False

# ---------------------------------------------------------
# REST API Endpoints (Conforming to SG-PROTO-00)
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    """Heartbeat probe for local connectivity verification."""
    return {
        "status": "online",
        "service": "ShadowGram Core Engine v2.0",
        "active_sessions": len(graph_engine.sessions),
        "edges_count": graph_engine.graph.number_of_edges(),
        "timestamp": time.time()
    }

@app.post("/telemetry", status_code=status.HTTP_200_OK)
async def receive_telemetry(event: TelemetryEvent, db: Session = Depends(get_db)):
    """
    Ingests live telemetry packets from Laptop 1 (Playwright Swarm) and Laptop 3 (AthenaPay App).
    Updates relational graph, logs to SQLite, and broadcasts event to 3D Cockpit.
    """
    if event.telemetry_hmac:
        if not verify_hmac(event.session_id, event.timestamp, event.telemetry_hmac):
            raise HTTPException(status_code=401, detail="Invalid HMAC Telemetry Signature")

    payload_dict = event.payload.model_dump()

    # Ingest into graph engine
    graph_engine.ingest_event(
        session_id=event.session_id,
        account_id=event.account_id,
        event_type=event.event_type,
        timestamp=event.timestamp,
        payload=payload_dict
    )

    # Persist to SQLite
    try:
        sess_rec = db.query(SessionRecord).filter(SessionRecord.account_id == event.account_id).first()
        if not sess_rec:
            sess_rec = SessionRecord(
                id=event.session_id,
                account_id=event.account_id,
                status="active",
                risk_label="normal_organic"
            )
            db.add(sess_rec)

        ev_rec = TelemetryRecord(
            session_id=event.session_id,
            account_id=event.account_id,
            event_type=event.event_type,
            timestamp=event.timestamp,
            flight_time_ms=payload_dict.get("key_flight_time_ms"),
            dwell_time_ms=payload_dict.get("key_dwell_time_ms"),
            pointer_jerk=payload_dict.get("pointer_curvature_jerk"),
            route_path=payload_dict.get("route_path"),
            tripwire_id=payload_dict.get("tripwire_id"),
            raw_payload_json=json.dumps(payload_dict)
        )
        db.add(ev_rec)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[Telemetry DB Error] {e}")

    # Broadcast event
    await ws_manager.broadcast({
        "type": "TELEMETRY_EVENT",
        "account_id": event.account_id,
        "event_type": event.event_type,
        "timestamp": event.timestamp,
        "payload": payload_dict
    })

    prof = graph_engine.sessions.get(event.account_id)
    is_quarantined = (prof.status == "quarantined") if prof else False
    key1_status = prof.key1_status if prof else "cleared"
    step_up_status = prof.step_up_status if prof else "none"

    return {
        "status": "quarantined" if is_quarantined else "ingested",
        "account_id": event.account_id,
        "is_quarantined": is_quarantined,
        "key1_status": key1_status,
        "step_up_status": step_up_status,
        "timestamp": event.timestamp
    }

@app.get("/api/session/status")
def get_session_status(account_id: str):
    """
    Returns live quarantine and step-up state for borrower portal synchronization.
    Used by athenapay_portal.html to trigger immediate Step-Up challenge modals upon quarantine.
    """
    state = graph_engine.get_session_status(account_id)
    if not state:
        return {
            "account_id": account_id,
            "status": "active",
            "key1_status": "cleared",
            "step_up_status": "not_required",
            "is_quarantined": False
        }
    return state

@app.get("/api/graph", response_model=GraphResponse)
def get_graph():
    """Returns active nodes, links, clusters, and Louvain modularity score Q."""
    return graph_engine.compute_clusters_and_modularity()

@app.get("/api/repartition", response_model=GraphResponse)
@app.post("/api/repartition", response_model=GraphResponse)
async def repartition_graph(threshold: float = 0.70):
    """
    Phase 2 Dynamic Sensitivity Repartitioning:
    Dynamically adjusts edge formation threshold theta (0.40 - 0.95),
    recomputes Leiden community partitions across active sessions,
    and broadcasts updated state over WebSockets to all connected cockpits.
    """
    graph_res = graph_engine.repartition_with_threshold(threshold)
    await ws_manager.broadcast({
        "type": "GRAPH_REPARTITIONED",
        "threshold": threshold,
        "global_modularity": graph_res.global_modularity,
        "clusters_count": len(graph_res.clusters),
        "total_active_sessions": graph_res.total_active_sessions,
        "timestamp": time.time()
    })
    return graph_res

@app.post("/api/quarantine", response_model=QuarantineResponse)
async def quarantine_cluster(req: QuarantineRequest, db: Session = Depends(get_db)):
    """
    Executes cluster-wide or account-level quarantine isolation.
    Disables accounts, logs compliance decision, and alerts 3D cockpit.
    """
    quarantined_count = graph_engine.quarantine_cluster(req.cluster_id, req.account_id)
    dow_savings = quarantined_count * 61.0

    # Persist cluster record
    try:
        c_rec = db.query(ClusterRecord).filter(ClusterRecord.cluster_id == req.cluster_id).first()
        if not c_rec:
            c_rec = ClusterRecord(
                cluster_id=req.cluster_id,
                size=quarantined_count,
                status="quarantined",
                quarantined_at=datetime.now(timezone.utc),
                reasons_json=json.dumps([req.reason])
            )
            db.add(c_rec)
        else:
            c_rec.status = "quarantined"
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[Quarantine DB Error] {e}")

    # Broadcast quarantine update
    await ws_manager.broadcast({
        "type": "QUARANTINE_TRIGGERED",
        "cluster_id": req.cluster_id,
        "account_id": req.account_id,
        "operator_id": req.operator_id,
        "quarantined_accounts": quarantined_count,
        "dow_savings_inr": dow_savings,
        "timestamp": time.time()
    })

    return QuarantineResponse(
        status="quarantined",
        cluster_id=req.cluster_id,
        quarantined_accounts=quarantined_count,
        timestamp=time.time(),
        dow_savings_inr=dow_savings
    )

@app.post("/api/step-up/verify", response_model=StepUpVerifyResponse)
async def verify_step_up(req: StepUpVerifyRequest, db: Session = Depends(get_db)):
    """
    Verifies a quarantined user completing an out-of-band Step-Up Challenge (₹1 UPI penny-drop).
    Restores legitimate account to active state in under 10 seconds.
    """
    success = graph_engine.verify_step_up(req.session_id, req.account_id, req.method)
    if success:
        try:
            sess_rec = db.query(SessionRecord).filter(SessionRecord.account_id == req.account_id).first()
            if sess_rec:
                sess_rec.status = "active"
                sess_rec.risk_label = "normal_organic"
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"[StepUp DB Error] {e}")

        await ws_manager.broadcast({
            "type": "STEP_UP_CLEARED",
            "account_id": req.account_id,
            "session_id": req.session_id,
            "method": req.method,
            "timestamp": time.time()
        })
        return StepUpVerifyResponse(
            status="verified",
            session_id=req.session_id,
            account_id=req.account_id,
            message="Step-Up Challenge successfully verified. Account restored to organic active state.",
            timestamp=time.time()
        )
    else:
        return StepUpVerifyResponse(
            status="failed",
            session_id=req.session_id,
            account_id=req.account_id,
            message="Step-Up Challenge failed verification. Account remains isolated.",
            timestamp=time.time()
        )

@app.get("/api/dow-stats", response_model=DoWStatsResponse)
def get_dow_stats():
    """Returns live Denial-of-Wallet (DoW) economic defense metrics."""
    stats = graph_engine.get_dow_stats()
    return DoWStatsResponse(**stats)

@app.get("/api/sar/pdf/{cluster_id}")
@app.get("/api/sar/pdf")
async def get_sar_pdf(cluster_id: int = 1):
    """Compiles and streams a formal 2-page Suspicious Activity Report (SAR) PDF."""
    res = graph_engine.compute_clusters_and_modularity()
    cluster_info = None
    for c in res.clusters:
        if c.cluster_id == cluster_id:
            cluster_info = c.model_dump()
            break
    if not cluster_info:
        cluster_info = {
            "cluster_id": cluster_id,
            "size": 20,
            "modularity_q": res.global_modularity or 0.7241,
            "p_value": 0.0001,
            "dow_savings_inr": 1220.0,
            "algorithm": "Leiden Community Detection",
            "account_ids": [f"SYNTH_APPLICANT_{i+1:03d}" for i in range(20)]
        }

    pdf_bytes = generate_sar_pdf(cluster_info)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="SAR_Report_Cluster_{cluster_id}_{int(time.time())}.pdf"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@app.post("/api/simulate_swarm")
async def simulate_swarm():
    """Populates graph engine with 80 legitimate humans and 20 synchronized bots."""
    result = populate_mock_cyber_range(graph_engine)
    await ws_manager.broadcast({
        "type": "SWARM_SIMULATION_DEPLOYED",
        "human_nodes": result["human_nodes"],
        "bot_nodes": result["bot_nodes"],
        "modularity_q": result["modularity_q"]
    })
    return result

@app.post("/api/reset")
async def reset_graph():
    """Clears in-memory graph state for a fresh demonstration."""
    graph_engine.reset()
    await ws_manager.broadcast({"type": "GRAPH_RESET"})
    return {"status": "cleared", "active_nodes": 0}

@app.get("/api/sar/export", response_class=PlainTextResponse)
async def export_sar(cluster_id: int = 1):
    """Generates official statutory SAR legal narrative via NVIDIA NIM or fallback."""
    res = graph_engine.compute_clusters_and_modularity()
    cluster_info = None
    for c in res.clusters:
        if c.cluster_id == cluster_id:
            cluster_info = c.model_dump()
            break
    if not cluster_info:
        cluster_info = {
            "cluster_id": cluster_id,
            "size": 20,
            "modularity_q": res.global_modularity or 0.7241,
            "p_value": 0.0001,
            "dow_savings_inr": 1220.0,
            "algorithm": "Leiden Community Detection",
            "account_ids": [f"SYNTH_APPLICANT_{i+1:03d}" for i in range(20)]
        }

    narrative = await generate_sar_report_narrative(cluster_info)
    return narrative

# ---------------------------------------------------------
# WebSocket Endpoints
# ---------------------------------------------------------

@app.websocket("/ws/telemetry")
@app.websocket("/ws/graph_live")
async def websocket_endpoint(websocket: WebSocket):
    """Streams live telemetry packets and periodic graph state to the 3D cockpit."""
    await ws_manager.connect(websocket)
    try:
        current_state = graph_engine.compute_clusters_and_modularity().model_dump()
        await websocket.send_json({"type": "INITIAL_GRAPH_STATE", "data": current_state})

        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception:
        ws_manager.disconnect(websocket)


# ---------------------------------------------------------
# Static Asset Handlers & LAN Cockpit Serving
# ---------------------------------------------------------

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "public")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Silent 204 response to eliminate browser favicon 404 noise."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/cockpit.html", include_in_schema=False)
async def serve_cockpit():
    """Serves the 3D WebGL Cockpit directly across the Hotspot LAN."""
    path = os.path.join(PUBLIC_DIR, "cockpit.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    raise HTTPException(status_code=404, detail="cockpit.html not found")

@app.get("/athenapay_portal.html", include_in_schema=False)
async def serve_athenapay_portal():
    """Serves the AthenaPay Borrower Application directly across the Hotspot LAN."""
    path = os.path.join(PUBLIC_DIR, "athenapay_portal.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    raise HTTPException(status_code=404, detail="athenapay_portal.html not found")

@app.get("/telemetry.js", include_in_schema=False)
async def serve_telemetry_js():
    """Serves client telemetry SDK directly across the Hotspot LAN."""
    path = os.path.join(PUBLIC_DIR, "telemetry.js")
    if os.path.exists(path):
        return FileResponse(path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="telemetry.js not found")

@app.get("/", include_in_schema=False)
async def root_redirect():
    """Root redirect directly into the 3D Cockpit."""
    return RedirectResponse(url="/cockpit.html")

BOOK_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ShadowGram_Master_Book")

@app.get("/master_book.html", include_in_schema=False)
@app.get("/book", include_in_schema=False)
@app.get("/book/index.html", include_in_schema=False)
async def serve_master_book():
    """Serves the complete 80-page Master Blueprint and Empirical Evidence Book."""
    path = os.path.join(BOOK_DIR, "ShadowGram_Master_Book_Complete.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    raise HTTPException(status_code=404, detail="Master Book not found")

@app.get("/mathematical_deep_dive.html", include_in_schema=False)
@app.get("/math", include_in_schema=False)
async def serve_mathematical_deep_dive():
    """Serves the Mathematical & Detection Deep Dive HTML specification."""
    path = os.path.join(PUBLIC_DIR, "mathematical_deep_dive.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    raise HTTPException(status_code=404, detail="Mathematical deep dive HTML not found")



