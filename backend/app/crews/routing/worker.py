import os
import logging
from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import RoutingDecision
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher

logger = logging.getLogger(__name__)


class RoutingWorker:
    def __init__(
        self,
        repo: IssueRepository,
        gemini: GeminiClient | None,
        publisher: EventPublisher | None,
    ):
        self.repo = repo
        self.gemini = gemini
        self.publisher = publisher

    def handle(self, issue_id: str):
        issue = self.repo.get(issue_id)
        if not issue or issue.status != IssueStatus.CLASSIFIED:
            return

        if os.getenv("LOCAL_DEV", "false").lower() == "true":
            routing = RoutingDecision(
                department="Sanitation",
                priority=3,
                confidence=0.9,
                rationale="Garbage issue",
            )
        else:
            routing = self.gemini.generate_structured_output(
                prompt=self._build_prompt(issue),
                output_schema=RoutingDecision,
            )

        self.repo.update_status(
            issue_id,
            IssueStatus.ROUTED,
            {"routing": routing.model_dump()},
        )

        if self.publisher:
            self.publisher.publish("ISSUE_ROUTED", issue_id)

        logger.info("Issue %s routed", issue_id)

    def _build_prompt(self, issue):
        return f"Route issue: {issue.description}"
