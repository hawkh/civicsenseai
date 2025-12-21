import os
import logging
from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import VerificationResult
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher

logger = logging.getLogger(__name__)


class VerificationWorker:
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
        if not issue or issue.status != IssueStatus.ROUTED:
            return

        if os.getenv("LOCAL_DEV", "false").lower() == "true":
            verification = VerificationResult(
                resolved=True,
                confidence=0.95,
                notes="Auto-verified in local dev",
            )
        else:
            verification = self.gemini.generate_structured_output(
                prompt=self._build_prompt(issue),
                output_schema=VerificationResult,
            )

        self.repo.update_status(
            issue_id,
            IssueStatus.VERIFIED,
            {"verification": verification.model_dump()},
        )

        if self.publisher:
            self.publisher.publish("ISSUE_VERIFIED", issue_id)

        logger.info("Issue %s verified", issue_id)

    def _build_prompt(self, issue):
        return f"Verify issue: {issue.description}"
