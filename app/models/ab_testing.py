from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ExperimentStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class VariantType(str, Enum):
    CONTROL = "control"
    TREATMENT = "treatment"

class Variant(BaseModel):
    name: str
    type: VariantType
    description: Optional[str] = None
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    configuration: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Experiment(BaseModel):
    name: str
    description: Optional[str] = None
    status: ExperimentStatus = ExperimentStatus.DRAFT
    variants: List[Variant]
    targeting_rules: List[str] = Field(default_factory=list)  # List of targeting rule names
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    sample_size: Optional[int] = None  # Total number of users to include
    metrics: List[str] = Field(default_factory=list)  # List of metrics to track
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ExperimentAssignment(BaseModel):
    experiment_id: str
    user_id: str
    variant_name: str
    assigned_at: datetime = Field(default_factory=datetime.utcnow)

class MetricValue(BaseModel):
    experiment_id: str
    variant_name: str
    metric_name: str
    value: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ExperimentResult(BaseModel):
    experiment_id: str
    variant_name: str
    total_users: int
    metrics: Dict[str, Dict[str, float]]  # metric_name -> {value, confidence_interval}
    start_time: datetime
    end_time: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 