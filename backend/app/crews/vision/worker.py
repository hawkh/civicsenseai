from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import VisionClassification
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher


class VisionWorker:
    """
    Vision agent responsible for classifying issues from images + text.
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

    async def handle(self, issue_id: str):
        """
        Process ISSUE_SUBMITTED event.
        """

        issue = self.repo.get(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")

        if issue.status != IssueStatus.SUBMITTED:
            # Idempotency: ignore if already processed
            return

        prompt = self._build_prompt(issue)

        classification: VisionClassification = (
            self.gemini.generate_structured_output(
                prompt=prompt,
                output_schema=VisionClassification,
            )
        )

        self.repo.update_status(
            issue_id=issue_id,
            new_status=IssueStatus.CLASSIFIED,
            updates={
                "classification": classification.model_dump(),
            },
        )

        self.publisher.publish(
            event_type="ISSUE_CLASSIFIED",
            issue_id=issue_id,
        )

    def _build_prompt(self, issue) -> str:
        """
        Build a strict prompt for Gemini.
        """
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
