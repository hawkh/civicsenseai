from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import RoutingDecision
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher


class RoutingWorker:
    """
    Routing agent responsible for assigning authority.
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
        issue = self.repo.get(issue_id)

        # ✅ SAFE: never crash
        if not issue:
            print(f"[WARN] Issue {issue_id} not found, skipping routing")
            return

        # ✅ Correct state gate
        if issue.status != IssueStatus.CLASSIFIED:
            print(f"[INFO] Issue {issue_id} not ready for routing")
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
        return f"""
You are a civic routing agent.

Based on the issue classification and description,
decide which authority should handle it.

Issue Description:
{issue.description}

Classification:
{issue.classification}

Return ONLY valid JSON matching the RoutingDecision schema.
No explanations.
"""
