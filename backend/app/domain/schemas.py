
from pydantic import BaseModel, Field
from typing import Optional


class LocationSchema(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class IssueCreateRequest(BaseModel):
    location: LocationSchema
    description: str = Field(..., min_length=3)
    image_url: Optional[str] = None


class IssueCreateResponse(BaseModel):
    issue_id: str
    status: str
