
import os
from typing import Optional
from google.cloud import firestore
from app.domain.models import Issue

# Singleton instance
_client: Optional[firestore.Client] = None

def _get_client() -> firestore.Client:
    global _client
    if _client is None:
        project_id = os.getenv("GCP_PROJECT_ID")
        if not project_id:
            raise RuntimeError("GCP_PROJECT_ID not set")
        _client = firestore.Client(project=project_id)
    return _client

class IssueRepository:
    def __init__(self):
        self.client = _get_client()
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
