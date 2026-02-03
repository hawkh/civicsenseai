from fastapi import APIRouter, Depends, HTTPException
import uuid
import os
from typing import List

from app.domain.models import Issue, IssueStatus
from app.domain.schemas import IssueCreateRequest, IssueCreateResponse
from app.datastore.firestore import IssueRepository, get_issue_repo
from app.events.publisher import EventPublisher

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"

@router.post("", response_model=IssueCreateResponse)
def create_issue(
    payload: IssueCreateRequest,
    repo: IssueRepository = Depends(get_issue_repo),
):
    try:
        issue_id = f"ISSUE_{uuid.uuid4().hex[:8]}"

        issue = Issue(
            issue_id=issue_id,
            location={
                "lat": payload.location.lat,
                "lng": payload.location.lng,
            },
            description=payload.description,
            image_url=payload.image_url,
            status=IssueStatus.SUBMITTED,
        )

        repo.create(issue)

        return IssueCreateResponse(
            issue_id=issue_id,
            status=issue.status,
        )

    except Exception as e:
        # 🔥 This prevents fake CORS errors
        raise HTTPException(status_code=500, detail=str(e))
