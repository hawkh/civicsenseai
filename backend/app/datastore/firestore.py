import os
from typing import Optional
from app.domain.models import Issue, IssueStatus

LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"

# shared in-memory store
_LOCAL_STORE: dict[str, Issue] = {}


class IssueRepository:
    def __init__(self, client=None):
        self.local = LOCAL_DEV

        if not self.local:
            from google.cloud import firestore
            self.client = client or firestore.Client()
            self.collection = self.client.collection("issues")

    def create(self, issue: Issue) -> Issue:
        if self.local:
            _LOCAL_STORE[issue.issue_id] = issue
            return issue

        self.collection.document(issue.issue_id).set(issue.model_dump())
        return issue

    def get(self, issue_id: str) -> Optional[Issue]:
        if self.local:
            return _LOCAL_STORE.get(issue_id)

        doc = self.collection.document(issue_id).get()
        if not doc.exists:
            return None
        return Issue(**doc.to_dict())

    def update_status(
        self,
        issue_id: str,
        new_status: IssueStatus,
        updates: Optional[dict] = None,
    ) -> Issue:
        issue = self.get(issue_id)
        if not issue:
            raise ValueError("Issue not found")

        issue.transition_to(new_status)

        if updates:
            for k, v in updates.items():
                setattr(issue, k, v)

        if self.local:
            _LOCAL_STORE[issue_id] = issue
            return issue

        self.collection.document(issue_id).set(issue.model_dump())
        return issue
