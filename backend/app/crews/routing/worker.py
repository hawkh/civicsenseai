from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import RoutingDecision
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher


class RoutingWorker:
    """
    Routing agent responsible for assigning issues to departments.
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
        Process ISSUE_CLASSIFIED event.
        """

        issue = self.repo.get(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")

        # Idempotency guard
        if issue.status != IssueStatus.CLASSIFIED:
            return

        prompt = self._build_prompt(issue)

        routing: RoutingDecision = self.gemini.generate_structured_output(
            prompt=prompt,
            output_schema=RoutingDecision,
        )

        self.repo.update_status(
            issue_id=issue_id,
            new_status=IssueStatus.ROUTED,
            updates={
                "routing": routing.model_dump(),
            },
        )

        self.publisher.publish(
            event_type="ISSUE_ROUTED",
            issue_id=issue_id,
        )

    def _build_prompt(self, issue) -> str:
        """
        Build a strict routing prompt for Gemini.
        """
        classification = issue.classification or {}

        return f"""
You are a civic routing agent.

Based on the issue details below, decide which department
should handle this issue.

Issue Type: {classification.get("issue_type")}
Severity: {classification.get("severity")}
Hazardous: {classification.get("hazardous")}

Return ONLY valid JSON matching the RoutingDecision schema.
No explanations.
"""
