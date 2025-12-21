from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field



class IssueStatus(str, Enum):
    SUBMITTED = "submitted"
    CLASSIFIED = "classified"
    ROUTED = "routed"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    VERIFIED = "verified"


# Allowed forward-only transitions
ALLOWED_TRANSITIONS = {
    IssueStatus.SUBMITTED: IssueStatus.CLASSIFIED,
    IssueStatus.CLASSIFIED: IssueStatus.ROUTED,
    IssueStatus.ROUTED: IssueStatus.IN_PROGRESS,
    IssueStatus.IN_PROGRESS: IssueStatus.RESOLVED,
    IssueStatus.RESOLVED: IssueStatus.VERIFIED,
}


def can_transition(from_status: IssueStatus, to_status: IssueStatus) -> bool:
    """
    Enforces strict, forward-only state transitions.
    """
    return ALLOWED_TRANSITIONS.get(from_status) == to_status



from typing import Optional

class Issue(BaseModel):
    """
    Core domain model.
    This is the single source of truth for system behavior.
    """

    issue_id: str
    status: IssueStatus = IssueStatus.SUBMITTED

    location: Dict[str, float]
    description: str
    image_url: Optional[str] = None  # ✅ FIX

    classification: Optional[Dict[str, Any]] = None
    routing: Optional[Dict[str, Any]] = None
    verification: Optional[Dict[str, Any]] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)



    def transition_to(self, new_status: IssueStatus):
        """
        Attempt to move the issue to a new state.
        Raises if the transition is invalid.
        """
        if not can_transition(self.status, new_status):
            raise ValueError(
                f"Invalid state transition: {self.status} → {new_status}"
            )

        self.status = new_status
        self.updated_at = datetime.utcnow()
