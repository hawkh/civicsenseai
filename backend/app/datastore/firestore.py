
import os
from google.cloud import firestore
from app.domain.models import Issue

# Global variable to cache the Firestore client
_firestore_client = None

def get_firestore_client():
    """
    Returns a cached Firestore client instance.
    Initializes it if it hasn't been created yet.
    """
    global _firestore_client
    if _firestore_client is None:
        project_id = os.getenv("GCP_PROJECT_ID")
        if not project_id:
            raise RuntimeError("GCP_PROJECT_ID not set")

        _firestore_client = firestore.Client(project=project_id)

    return _firestore_client

class IssueRepository:
    def __init__(self):
        self.client = get_firestore_client()
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
