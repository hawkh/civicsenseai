from fastapi import APIRouter, Depends
import uuid

from app.domain.models import Issue, IssueStatus
from app.domain.schemas import IssueCreateRequest, IssueCreateResponse
from app.datastore.firestore import IssueRepository
from app.events.publisher import EventPublisher

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


def get_repo():
    return IssueRepository()


def get_publisher():
    return EventPublisher(
        project_id="civicsense-481806",
        topic_name="civicsense",
    )


@router.post("", response_model=IssueCreateResponse)
def create_issue(
    payload: IssueCreateRequest,
    repo: IssueRepository = Depends(get_repo),
    publisher: EventPublisher = Depends(get_publisher),
):
    issue_id = f"ISSUE_{uuid.uuid4().hex[:8]}"

    issue = Issue(
        issue_id=issue_id,
        location=payload.location,
        description=payload.description,
        image_url=payload.image_url,
        status=IssueStatus.SUBMITTED,
    )

    repo.create(issue)

    publisher.publish(
        event_type="ISSUE_SUBMITTED",
        issue_id=issue_id,
    )

    return IssueCreateResponse(
        issue_id=issue_id,
        status=issue.status,
    )
