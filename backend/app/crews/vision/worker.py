import os
import logging

from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import VisionClassification, IssueType
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher

logger = logging.getLogger(__name__)


class VisionWorker:
    """
    Vision agent responsible for classifying issues from images + text.
    """

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
            logger.warning("Issue %s not found, skipping vision", issue_id)
            return

        if issue.status != IssueStatus.SUBMITTED:
            logger.info(
                "Issue %s status=%s not eligible for vision",
                issue_id,
                issue.status,
            )
            return

        if os.getenv("LOCAL_DEV", "false").lower() == "true":
            classification = VisionClassification(
                issue_type=IssueType.GARBAGE,
                severity=2,
                hazardous=False,
                confidence=0.92,
                notes="Auto-classified in local development",
            )
        else:
            prompt = self._build_prompt(issue)
            classification = self.gemini.generate_structured_output(
                prompt=prompt,
                output_schema=VisionClassification,
            )

        self.repo.update_status(
            issue_id=issue_id,
            new_status=IssueStatus.CLASSIFIED,
            updates={"classification": classification.model_dump()},
        )

        if self.publisher:
            self.publisher.publish(
                event_type="ISSUE_CLASSIFIED",
                issue_id=issue_id,
            )

        logger.info("Issue %s classified successfully", issue_id)

    def _build_prompt(self, issue) -> str:
        return f"""
You are a civic vision analysis agent.

Analyze the following issue and return ONLY valid JSON
matching the VisionClassification schema.

Description:
{issue.description}

Image URL:
{issue.image_url}

Respond with JSON only. No explanations.
"""
