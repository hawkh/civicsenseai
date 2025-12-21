import os
import logging

from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import VerificationResult
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher


logger = logging.getLogger(__name__)


class VerificationWorker:
    """
    Verification agent responsible for confirming issue resolution.
    """

    def __init__(
        self,
        repo: IssueRepository,
        gemini: GeminiClient,
        publisher: EventPublisher,
    ):
        self.repo = repo
        self.gemini = gemini
        self.publisher = publisher

    def handle(self, issue_id: str):
        """
        Process verification after routing.
        """

        issue = self.repo.get(issue_id)

        if not issue:
            logger.warning("Issue %s not found, skipping verification", issue_id)
            return

        if issue.status != IssueStatus.ROUTED:
            logger.info(
                "Issue %s status=%s not ready for verification",
                issue_id,
                issue.status,
            )
            return

        if os.getenv("LOCAL_DEV", "false").lower() == "true":
            verification = VerificationResult(
                verified=True,
                confidence=0.95,
                notes="Auto-verified in local development",
            )
        else:
            prompt = self._build_prompt(issue)
            verification: VerificationResult = self.gemini.generate_structured_output(
                prompt=prompt,
                output_schema=VerificationResult,
            )

        self.repo.update_status(
            issue_id=issue_id,
            new_status=IssueStatus.VERIFIED,
            updates={"verification": verification.model_dump()},
        )

        self.publisher.publish(
            event_type="ISSUE_VERIFIED",
            issue_id=issue_id,
        )

        logger.info("Issue %s successfully verified", issue_id)

    def _build_prompt(self, issue) -> str:
        """
        Build a strict verification prompt for Gemini.
        """
        return f"""
You are a civic verification agent.

Based on the issue description, classification, and routing decision,
determine whether the issue can be marked as VERIFIED.

Issue Description:
{issue.description}

Classification:
{issue.classification}

Routing Decision:
{issue.routing}

Return ONLY valid JSON matching the VerificationResult schema.
No explanations.
"""
