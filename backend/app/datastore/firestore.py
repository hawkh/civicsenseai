
import os
from functools import lru_cache
from google.cloud import firestore
from app.domain.models import Issue


class IssueRepository:
    def __init__(self):
        project_id = os.getenv("GCP_PROJECT_ID")
        if not project_id:
            raise RuntimeError("GCP_PROJECT_ID not set")

        self.client = firestore.Client(project=project_id)
        self.collection = self.client.collection("issues")

    def create(self, issue: Issue):
        self.collection.document(issue.issue_id).set(issue.model_dump())

    def get(self, issue_id: str):
        doc = self.collection.document(issue_id).get()
        return Issue(**doc.to_dict()) if doc.exists else None

    def list_all(self):
        return [
            Issue(**doc.to_dict())
            for doc in self.collection.stream()
        ]

@lru_cache
def get_issue_repo() -> IssueRepository:
    """Returns a cached instance of IssueRepository (Singleton)."""
    return IssueRepository()
