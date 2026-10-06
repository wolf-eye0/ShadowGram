from typing import List, Optional, Any, Dict
import time
from datetime import datetime, timezone

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, default_factory=None):
        if default_factory is not None:
            return default_factory()
        return default

try:
    from sqlalchemy import Column, String, Float, Integer, Text, DateTime
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()
except ImportError:
    class Base:
        pass
    def Column(*args, **kwargs):
        return None
    String = Float = Integer = Text = DateTime = lambda *args, **kwargs: None

# ---------------------------------------------------------
# SQLAlchemy Database Models (shadowgram.db)
# ---------------------------------------------------------

class SessionRecord(Base):
    __tablename__ = "sessions"

    id = Column(String(64), primary_key=True)
    account_id = Column(String(64), index=True, nullable=False)
    ip_hash = Column(String(64), nullable=True)
    status = Column(String(32), default="active")  # active | quarantined
    risk_label = Column(String(32), default="normal_organic")  # normal_organic | suspicious_syndicate | anomaly_outlier
    kinetic_jerk_score = Column(Float, default=0.5)
    cluster_id = Column(Integer, nullable=True)
    key1_status = Column(String(32), default="cleared")  # cleared | flagged_automation
    step_up_status = Column(String(32), default="not_required")  # not_required | pending | cleared | abandoned
    dow_saved = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class TelemetryRecord(Base):
    __tablename__ = "telemetry_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), index=True, nullable=False)
    account_id = Column(String(64), index=True, nullable=False)
    event_type = Column(String(32), nullable=False)
    timestamp = Column(Float, nullable=False)
    flight_time_ms = Column(Float, nullable=True)
    dwell_time_ms = Column(Float, nullable=True)
    pointer_jerk = Column(Float, nullable=True)
    route_path = Column(String(128), nullable=True)
    tripwire_id = Column(String(128), nullable=True)
    raw_payload_json = Column(Text, nullable=True)


class ClusterRecord(Base):
    __tablename__ = "clusters"

    cluster_id = Column(Integer, primary_key=True)
    size = Column(Integer, default=0)
    modularity_q = Column(Float, default=0.0)
    p_value = Column(Float, default=0.0001)
    dow_savings_inr = Column(Float, default=0.0)
    algorithm = Column(String(32), default="Leiden")
    status = Column(String(32), default="active")  # active | quarantined
    quarantined_at = Column(DateTime, nullable=True)
    reasons_json = Column(Text, nullable=True)


# ---------------------------------------------------------
# Pydantic Ingress & API Schemas (Frozen Contract SG-PROTO-00)
# ---------------------------------------------------------

class TelemetryPayload(BaseModel):
    key_flight_time_ms: Optional[float] = None
    key_dwell_time_ms: Optional[float] = None
    pointer_curvature_jerk: Optional[float] = None
    pointer_coordinates: Optional[List[List[float]]] = None  # [[x, y, t], ...]
    route_path: Optional[str] = None
    tripwire_id: Optional[str] = None
    client_canvas_hash: Optional[str] = None
    narrative_text: Optional[str] = None  # For semantic intent embedding
    client_id_artifact_score: Optional[float] = None
    click_dwell_duration_ms: Optional[float] = None
    mousemove_pre_click_count: Optional[int] = None
    touch_swipe_velocity: Optional[float] = None
    touch_contact_area: Optional[float] = None


class TelemetryEvent(BaseModel):
    session_id: str
    account_id: str
    timestamp: float = Field(default_factory=lambda: time.time())
    event_type: str  # keydown | pointerdown | route_change | honey_dom_trip | loan_submit | step_up
    telemetry_hmac: Optional[str] = None
    payload: TelemetryPayload = Field(default_factory=TelemetryPayload)


class GraphNode(BaseModel):
    id: str  # account_id
    session_id: str
    cluster_id: Optional[int] = None
    risk_label: str  # normal_organic | suspicious_syndicate | anomaly_outlier
    kinetic_jerk_score: float
    semantic_intent_vector: Optional[List[float]] = None
    status: str = "active"  # active | quarantined
    key1_status: str = "cleared"  # cleared | flagged_automation
    step_up_status: str = "not_required"  # not_required | pending | cleared | abandoned


class GraphLink(BaseModel):
    source: str
    target: str
    weight: float
    converged_layers: List[str]  # timing, navigation, semantic, kinetics, environment
    delta_t_seconds: float
    evidence: Optional[Dict[str, float]] = None
    common_cause_discount: float = 0.0


class GraphCluster(BaseModel):
    cluster_id: int
    size: int
    modularity_q: float
    p_value: float = Field(default=0.0001)
    dow_savings_inr: float = Field(default=0.0)
    algorithm: str = Field(default="Leiden")
    status: str  # active | quarantined
    factual_reasons: List[str]
    account_ids: List[str] = Field(default_factory=list)


class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]
    clusters: List[GraphCluster]
    global_modularity: float
    total_active_sessions: int
    total_dow_savings_inr: float = 0.0


class QuarantineRequest(BaseModel):
    cluster_id: int = 1
    account_id: Optional[str] = None
    action: str = "isolate"  # isolate | step_up_challenge | release
    reason: str = "Coordinated multi-agent swarm detected via Leiden community clustering"
    operator_id: str = "OFFICER-LEAD"



class QuarantineResponse(BaseModel):
    status: str
    cluster_id: int
    quarantined_accounts: int
    timestamp: float
    dow_savings_inr: float = 0.0


class StepUpVerifyRequest(BaseModel):
    session_id: str
    account_id: str
    method: str = "upi_penny_drop"  # upi_penny_drop | account_aggregator
    auth_token: Optional[str] = "DEMO-UPI-SUCCESS"


class StepUpVerifyResponse(BaseModel):
    status: str  # verified | failed
    session_id: str
    account_id: str
    message: str
    timestamp: float


class DoWStatsResponse(BaseModel):
    total_bots_intercepted: int
    total_inr_saved: float
    prevented_aadhaar_cost: float
    prevented_pan_cost: float
    prevented_liveness_cost: float
    prevented_bureau_cost: float
