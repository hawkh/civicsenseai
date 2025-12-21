from fastapi import APIRouter, Depends, HTTPException, Response
import uuid
import os
from typing import List

from app.domain.models import Issue, IssueStatus
from app.domain.schemas import IssueCreateRequest, IssueCreateResponse
from app.datastore.firestore import IssueRepository
from app.events.publisher import EventPublisher

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"


# ✅ REQUIRED FOR BROWSER PREFLIGHT
@router.options("")
def options_issues():
    return Response(status_code=200)


def get_repo():
    return IssueRepository()


def get_publisher():
    if LOCAL_DEV:
        return None
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

    if publisher:
        publisher.publish(
            event_type="ISSUE_SUBMITTED",
            issue_id=issue_id,
        )

    return IssueCreateResponse(
        issue_id=issue_id,
        status=issue.status,
    )


@router.get("/{issue_id}", response_model=Issue)
def get_issue(issue_id: str, repo: IssueRepository = Depends(get_repo)):
    issue = repo.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.get("", response_model=List[Issue])
def list_issues(repo: IssueRepository = Depends(get_repo)):
    return repo.list_all()
