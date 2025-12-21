import os
from typing import Optional
from app.domain.models import Issue, IssueStatus
from typing import Optional, List
LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"

# In-memory store for LOCAL_DEV
_LOCAL_STORE: dict[str, Issue] = {}


class IssueRepository:
    def __init__(self, client=None):
        if not LOCAL_DEV:
            from google.cloud import firestore
            self.client = client or firestore.Client()
            self.collection = self.client.collection("issues")

    # -------------------------
    # CREATE
    # -------------------------
    def create(self, issue: Issue) -> Issue:
        if LOCAL_DEV:
            _LOCAL_STORE[issue.issue_id] = issue
            return issue

        self.collection.document(issue.issue_id).set(issue.model_dump())
        return issue

    # -------------------------
    # READ ONE
    # -------------------------
    def get(self, issue_id: str) -> Optional[Issue]:
        if LOCAL_DEV:
            return _LOCAL_STORE.get(issue_id)

        doc = self.collection.document(issue_id).get()
        if not doc.exists:
            return None
        return Issue(**doc.to_dict())

    def list_all(self) -> List[Issue]:
        if LOCAL_DEV:
            return list(_LOCAL_STORE.values())

        docs = self.collection.stream()
        return [Issue(**doc.to_dict()) for doc in docs]

    # -------------------------
    # UPDATE STATUS
    # -------------------------
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

        if LOCAL_DEV:
            _LOCAL_STORE[issue_id] = issue
            return issue

        self.collection.document(issue_id).set(issue.model_dump())
        return issue
