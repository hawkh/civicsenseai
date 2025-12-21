from pydantic import BaseModel, Field
from typing import Dict, Optional


class IssueCreateRequest(BaseModel):
    location: Dict[str, float] = Field(
        ..., example={"lat": 17.44, "lng": 78.34}
    )
    description: str = Field(
        ..., example="Large pothole near the bus stop"
    )
    image_url: Optional[str] = Field(
        None, example="gs://civicsense-uploads/image.png"
    )


class IssueCreateResponse(BaseModel):
    issue_id: str
    status: str
