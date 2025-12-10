from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EvidenceBase(BaseModel):
    media_type: str

class Evidence(EvidenceBase):
    id: int
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True

class TicketBase(BaseModel):
    issue_type: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "open"

class Ticket(TicketBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ComplaintBase(BaseModel):
    description: Optional[str] = None
    contact_info: Optional[str] = None
    source: str = "web"

class ComplaintCreate(ComplaintBase):
    pass

class Complaint(ComplaintBase):
    id: int
    status: str
    created_at: datetime
    evidence: List[Evidence] = []
    ticket: Optional[Ticket] = None

    class Config:
        from_attributes = True
