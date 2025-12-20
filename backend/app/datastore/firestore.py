import os
from typing import Optional, Dict
from datetime import datetime
from app.domain.models import Issue, IssueStatus

LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"

_LOCAL_STORE: Dict[str, Issue] = {}


class IssueRepository:
    def __init__(self, client=None):
        if not LOCAL_DEV:
            from google.cloud import firestore
            self.client = client or firestore.Client()
            self.collection = self.client.collection("issues")

    def create(self, issue: Issue):
        issue.created_at = datetime.utcnow()

        if LOCAL_DEV:
            _LOCAL_STORE[issue.issue_id] = issue
            return issue

        self.collection.document(issue.issue_id).set(issue.model_dump())
        return issue


    def get(self, issue_id: str) -> Optional[Issue]:
        if LOCAL_DEV:
            return _LOCAL_STORE.get(issue_id)

        doc = self.collection.document(issue_id).get()
        if not doc.exists:
            return None

        return Issue(**doc.to_dict())


    def get_with_timeline(self, issue_id: str) -> Optional[dict]:
        issue = self.get(issue_id)
        if not issue:
            return None

        timeline = [
            {
                "status": IssueStatus.SUBMITTED,
                "at": issue.created_at,
            }
        ]

        if issue.classification:
            timeline.append({
                "status": IssueStatus.CLASSIFIED,
                "at": issue.classified_at,
                "details": issue.classification,
            })

        if issue.routing:
            timeline.append({
                "status": IssueStatus.ROUTED,
                "at": issue.routed_at,
                "details": issue.routing,
            })

        if issue.verification:
            timeline.append({
                "status": IssueStatus.VERIFIED,
                "at": issue.verified_at,
                "details": issue.verification,
            })

        return {
            "issue_id": issue.issue_id,
            "location": issue.location,
            "description": issue.description,
            "image_url": issue.image_url,
            "status": issue.status,
            "created_at": issue.created_at,
            "timeline": timeline,
        }


    def update_status(
        self,
        issue_id: str,
        new_status: IssueStatus,
        updates: Optional[dict] = None,
    ):
        issue = self.get(issue_id)
        if not issue:
            raise ValueError("Issue not found")

        issue.transition_to(new_status)

        # auto timestamping per stage
        now = datetime.utcnow()
        if new_status == IssueStatus.CLASSIFIED:
            issue.classified_at = now
        elif new_status == IssueStatus.ROUTED:
            issue.routed_at = now
        elif new_status == IssueStatus.VERIFIED:
            issue.verified_at = now

        if updates:
            for k, v in updates.items():
                setattr(issue, k, v)

        if LOCAL_DEV:
            _LOCAL_STORE[issue_id] = issue
            return issue

        self.collection.document(issue_id).set(issue.model_dump())
        return issue
