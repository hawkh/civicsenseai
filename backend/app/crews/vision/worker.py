import os
import logging
from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import VisionClassification
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher

logger = logging.getLogger(__name__)


class VisionWorker:
    def __init__(
        self,
        repo: IssueRepository,
        gemini: GeminiClient | None,
        publisher: EventPublisher | None,
    ):
        self.repo = repo
        self.gemini = gemini
        self.publisher = publisher

    async def handle(self, issue_id: str):
        issue = self.repo.get(issue_id)

        if not issue:
            logger.warning("Issue %s not found", issue_id)
            return

        if issue.status != IssueStatus.SUBMITTED:
            return

        if os.getenv("LOCAL_DEV", "false").lower() == "true":
            classification = VisionClassification(
                issue_type="garbage",
                severity=2,
                hazardous=False,
                confidence=0.92,
                notes="Auto-classified in local dev",
            )
        else:
            classification = self.gemini.generate_structured_output(
                prompt=self._build_prompt(issue),
                output_schema=VisionClassification,
            )

        self.repo.update_status(
            issue_id,
            IssueStatus.CLASSIFIED,
            {"classification": classification.model_dump()},
        )

        if self.publisher:
            self.publisher.publish("ISSUE_CLASSIFIED", issue_id)

        logger.info("Issue %s classified", issue_id)

    def _build_prompt(self, issue):
        return f"""
Analyze this civic issue and return ONLY JSON.

Description:
{issue.description}

Image:
{issue.image_url}
"""
