from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, conint, confloat




class IssueType(str, Enum):
    POTHOLE = "pothole"
    GARBAGE = "garbage"
    WATER_LOGGING = "water_logging"
    STREET_LIGHT = "street_light"
    OTHER = "other"




class VisionClassification(BaseModel):
    issue_type: IssueType
    severity: conint(ge=1, le=10)
    hazardous: bool
    confidence: confloat(ge=0.0, le=1.0)
    model_version: Optional[str] = None




class RoutingDecision(BaseModel):
    department: str
    priority: conint(ge=1, le=5)
    confidence: confloat(ge=0.0, le=1.0)
    rationale: Optional[str] = None




class VerificationResult(BaseModel):
    resolved: bool
    confidence: confloat(ge=0.0, le=1.0)
    notes: Optional[str] = None
