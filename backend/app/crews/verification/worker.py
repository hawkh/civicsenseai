from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.services.gemini.schemas import VerificationResult
from app.domain.models import IssueStatus
from app.events.publisher import EventPublisher


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

        # ✅ SAFE: no crashes in event systems
        if not issue:
            print(f"[WARN] Issue {issue_id} not found, skipping verification")
            return

        # ✅ Correct state gate
        if issue.status != IssueStatus.ROUTED:
            print(f"[INFO] Issue {issue_id} not ready for verification")
            return

        prompt = self._build_prompt(issue)

        verification: VerificationResult = self.gemini.generate_structured_output(
            prompt=prompt,
            output_schema=VerificationResult,
        )

        self.repo.update_status(
            issue_id=issue_id,
            new_status=IssueStatus.VERIFIED,
            updates={
                "verification": verification.model_dump(),
            },
        )

        self.publisher.publish(
            event_type="ISSUE_VERIFIED",
            issue_id=issue_id,
        )

    def _build_prompt(self, issue) -> str:
        """
        Build a strict verification prompt for Gemini.
        """
        return f"""
You are a civic verification agent.

Based on the issue description, classification, and routing decision,
determine whether the issue is suitable to be marked as VERIFIED.

Issue Description:
{issue.description}

Classification:
{issue.classification}

Routing Decision:
{issue.routing}

Return ONLY valid JSON matching the VerificationResult schema.
No explanations.
"""
