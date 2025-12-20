import os
from typing import Type, TypeVar

from pydantic import BaseModel

LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"

T = TypeVar("T", bound=BaseModel)


class GeminiClient:
    """
    Gemini client wrapper.
    Uses mock outputs in LOCAL_DEV.
    """

    def __init__(self, project_id: str, model_name: str = "gemini-1.5-pro"):
        self.project_id = project_id
        self.model_name = model_name

        if not LOCAL_DEV:
            import google.generativeai as genai
            genai.configure()
            self.model = genai.GenerativeModel(model_name)
        else:
            self.model = None

    def generate_structured_output(
        self,
        prompt: str,
        output_schema: Type[T],
    ) -> T:
        """
        Generate structured output.
        Mocked in LOCAL_DEV.
        """

        if LOCAL_DEV:
            # 🔹 Deterministic mock outputs for local dev
            if output_schema.__name__ == "VisionClassification":
                return output_schema(
                    issue_type="pothole",
                    severity=7,
                    hazardous=False,
                    confidence=0.92,
                )

            if output_schema.__name__ == "RoutingDecision":
                return output_schema(
                    department="Municipal Roads",
                    priority=2,
                    confidence=0.89,
                )

            if output_schema.__name__ == "VerificationResult":
                return output_schema(
                    resolved=True,
                    confidence=0.95,
                    notes="Issue appears resolved",
                )

            raise ValueError("Unknown schema")

        response = self.model.generate_content(prompt)
        return output_schema.model_validate_json(response.text)
