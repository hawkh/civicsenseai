import os
import json
from typing import Optional

LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"


class EventPublisher:
    """
    Publishes events to Pub/Sub in production.
    No-op in local development.
    """

    def __init__(
        self,
        project_id: str,
        topic_name: str,
        publisher: Optional[object] = None,
    ):
        self.project_id = project_id
        self.topic_name = topic_name

        if not LOCAL_DEV:
            from google.cloud import pubsub_v1
            self.publisher = publisher or pubsub_v1.PublisherClient()
            self.topic_path = self.publisher.topic_path(
                project_id, topic_name
            )
        else:
            self.publisher = None
            self.topic_path = None

    def publish(self, event_type: str, issue_id: str):
        """
        Publish event or no-op in LOCAL_DEV.
        """
        if LOCAL_DEV:
            print(
                f"[LOCAL_DEV] Event published: {event_type} "
                f"(issue_id={issue_id})"
            )
            return

        message = {
            "event_type": event_type,
            "issue_id": issue_id,
        }

        self.publisher.publish(
            self.topic_path,
            json.dumps(message).encode("utf-8"),
        )
