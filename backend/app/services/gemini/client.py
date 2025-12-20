import os
from typing import Type, TypeVar
import google.generativeai as genai
from pydantic import BaseModel

# We ignore LOCAL_DEV for intelligence as per user mandate
# LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"

T = TypeVar("T", bound=BaseModel)


class GeminiClient:
    """
    Gemini client wrapper.
    Enforces real AI implementation.
    """

    def __init__(self, project_id: str, model_name: str = "gemini-1.5-flash"):
        self.project_id = project_id
        self.model_name = model_name

        # Configure Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            # Fallback or error if key is missing, but assuming it's there
            print("Warning: GOOGLE_API_KEY not found in environment")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_structured_output(
        self,
        prompt: str,
        output_schema: Type[T],
    ) -> T:
        """
        Generate structured output using Gemini.
        """
        # Create a prompt that asks for JSON
        full_prompt = f"{prompt}\n\nRespond with a valid JSON object matching this schema: {output_schema.model_json_schema()}"

        response = self.model.generate_content(full_prompt, generation_config={"response_mime_type": "application/json"})

        # Parse the JSON response
        try:
            return output_schema.model_validate_json(response.text)
        except Exception as e:
            # Fallback if strict JSON mode fails (retry logic could go here)
            print(f"Error parsing JSON from Gemini: {e}")
            raise

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribes audio file using Gemini.
        """
        try:
            # Upload the file to Gemini
            audio_file = genai.upload_file(path=audio_file_path)

            # Generate content using the audio file
            response = self.model.generate_content(
                ["Please transcribe this audio file verbatim.", audio_file]
            )

            return response.text
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return ""

    def analyze_audio_report(self, audio_file_path: str, output_schema: Type[T]) -> T:
        """
        Analyzes audio to extract structured report data.
        """
        try:
            audio_file = genai.upload_file(path=audio_file_path)

            prompt = "Listen to this audio report and extract the following details: description of the issue, and any contact information if mentioned. If location is mentioned, include it in the description."
            full_prompt = [prompt, audio_file]

            response = self.model.generate_content(
                full_prompt,
                generation_config={"response_mime_type": "application/json", "response_schema": output_schema}
            )

            return output_schema.model_validate_json(response.text)
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            raise
