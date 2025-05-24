from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class TimeRange(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    CUSTOM = "custom"


class MetricDefinition(BaseModel):
    name: str
    type: MetricType
    description: Optional[str] = None
    labels: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MetricValue(BaseModel):
    metric_name: str
    value: float
    labels: Dict[str, str] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MetricAggregation(BaseModel):
    metric_name: str
    time_range: TimeRange
    start_time: datetime
    end_time: datetime
    values: List[float]
    labels: Dict[str, str] = Field(default_factory=dict)
    count: int
    sum: float
    min: float
    max: float
    avg: float
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Dashboard(BaseModel):
    name: str
    description: Optional[str] = None
    widgets: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Widget(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    position: Dict[str, int] = Field(default_factory=dict)
    size: Dict[str, int] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Report(BaseModel):
    name: str
    description: Optional[str] = None
    metrics: List[str]
    time_range: TimeRange
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    filters: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ReportResult(BaseModel):
    report_id: str
    metrics: Dict[str, MetricAggregation]
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    execution_time: float
    status: str
    error: Optional[str] = None
