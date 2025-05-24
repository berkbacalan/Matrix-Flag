from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TargetingOperator(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    IN = "in"
    NOT_IN = "not_in"
    BETWEEN = "between"
    NOT_BETWEEN = "not_between"


class TargetingCondition(BaseModel):
    attribute: str
    operator: TargetingOperator
    value: Any
    description: Optional[str] = None


class TargetingRule(BaseModel):
    name: str
    description: Optional[str] = None
    conditions: List[TargetingCondition]
    percentage: Optional[float] = Field(None, ge=0, le=100)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TargetingRuleGroup(BaseModel):
    name: str
    description: Optional[str] = None
    rules: List[TargetingRule]
    operator: str = "AND"  # AND or OR
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserSegment(BaseModel):
    name: str
    description: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TargetingEvaluation(BaseModel):
    rule_id: str
    result: bool
    matched_conditions: List[str]
    unmatched_conditions: List[str]
    evaluation_time: datetime = Field(default_factory=datetime.utcnow)
