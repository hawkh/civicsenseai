import os
from typing import Optional
from app.domain.models import Issue, IssueStatus
from typing import Optional, List
LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"

# In-memory store for LOCAL_DEV
_LOCAL_STORE: dict[str, Issue] = {}

# app/datastore/firestore.py
from google.cloud import firestore
from app.domain.models import Issue


class IssueRepository:
    def __init__(self):
        self.client = firestore.Client()
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

    def update_status(self, issue_id: str, new_status, updates=None):
        data = {"status": new_status}
        if updates:
            data.update(updates)
        self.collection.document(issue_id).update(data)
