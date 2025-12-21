import os
import logging

from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import RoutingDecision
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher

logger = logging.getLogger(__name__)


class RoutingWorker:
    """
    Routing agent responsible for assigning issues to departments.
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
            logger.warning("Issue %s not found, skipping routing", issue_id)
            return

        if issue.status != IssueStatus.CLASSIFIED:
            logger.info(
                "Issue %s status=%s not eligible for routing",
                issue_id,
                issue.status,
            )
            return

        # ✅ LOCAL_DEV shortcut
        if os.getenv("LOCAL_DEV", "false").lower() == "true":
            routing = RoutingDecision(
                department="Municipal Sanitation",
                priority=3,
                confidence=0.90,
                rationale="Auto-routed in local development",
            )
        else:
            prompt = self._build_prompt(issue)
            routing: RoutingDecision = self.gemini.generate_structured_output(
                prompt=prompt,
                output_schema=RoutingDecision,
            )

        self.repo.update_status(
            issue_id=issue_id,
            new_status=IssueStatus.ROUTED,
            updates={"routing": routing.model_dump()},
        )

        if self.publisher:
            self.publisher.publish(
                event_type="ISSUE_ROUTED",
                issue_id=issue_id,
            )

        logger.info("Issue %s routed successfully", issue_id)

    def _build_prompt(self, issue) -> str:
        return f"""
You are a civic routing agent.

Based on the issue classification, decide which department
should handle it and its priority.

Issue Description:
{issue.description}

Classification:
{issue.classification}

Return ONLY valid JSON matching the RoutingDecision schema.
No explanations.
"""
