from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum


class FlagType(str, Enum):
    BOOLEAN = "boolean"
    STRING = "string"
    NUMBER = "number"
    JSON = "json"


class FeatureFlag(BaseModel):
    key: str = Field(..., description="Unique identifier for the feature flag")
    name: str = Field(..., description="Display name of the feature flag")
    description: Optional[str] = Field(None, description="Description of the feature flag")
    type: FlagType = Field(..., description="Type of the feature flag value")
    value: Any = Field(..., description="Value of the feature flag")
    enabled: bool = Field(default=True, description="Whether the feature flag is enabled")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FeatureFlagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[FlagType] = None
    value: Optional[Any] = None
    enabled: Optional[bool] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class WebhookEvent(BaseModel):
    event_type: str
    flag_key: str
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
