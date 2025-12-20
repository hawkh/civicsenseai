import pytest
from pydantic import BaseModel
from unittest.mock import MagicMock, patch

from app.services.gemini.client import GeminiClient


class DummySchema(BaseModel):
    result: str


@patch("app.services.gemini.client.genai")
def test_valid_structured_output(mock_genai):
    mock_model = MagicMock()
    # Mock response.text to return valid JSON
    mock_model.generate_content.return_value.text = '{"result": "ok"}'
    mock_genai.GenerativeModel.return_value = mock_model

    client = GeminiClient(project_id="test-project")
    output = client.generate_structured_output(
        prompt="test",
        output_schema=DummySchema
    )

    assert output.result == "ok"


@patch("app.services.gemini.client.genai")
def test_invalid_schema_raises(mock_genai):
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = '{"invalid": "data"}'
    mock_genai.GenerativeModel.return_value = mock_model

    client = GeminiClient(project_id="test-project")

    with pytest.raises(ValueError):
        client.generate_structured_output(
            prompt="test",
            output_schema=DummySchema
        )
