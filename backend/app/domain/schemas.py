from pydantic import BaseModel, Field
from typing import Dict


class IssueCreateRequest(BaseModel):
    """
    Payload sent by frontend when creating an issue.
    """
    location: Dict[str, float] = Field(
        ..., example={"lat": 17.44, "lng": 78.34}
    )
    description: str = Field(
        ..., example="Large pothole near the bus stop"
    )
    image_url: str = Field(
        ..., example="gs://civicsense-uploads/image.png"
    )


# -------------------------
# API RESPONSE SCHEMAS
# -------------------------

class IssueCreateResponse(BaseModel):
    """
    Response returned after issue creation.
    """
    issue_id: str
    status: str


class IssueStatusResponse(BaseModel):
    """
    Minimal status view for polling.
    """
    issue_id: str
    status: str
