
import os
from google.cloud import firestore
from app.domain.models import Issue

# Module-level singleton to prevent expensive re-initialization of Firestore client
# on every request. This is critical for performance as Client init involves
# auth and connection setup.
_client_instance = None

class IssueRepository:
    def __init__(self):
        project_id = os.getenv("GCP_PROJECT_ID")
        if not project_id:
            raise RuntimeError("GCP_PROJECT_ID not set")

        global _client_instance
        if _client_instance is None:
            _client_instance = firestore.Client(project=project_id)

        self.client = _client_instance
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
