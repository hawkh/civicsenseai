from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Complaint, Evidence
from app.services.gemini.client import GeminiClient
import shutil
import os
import uuid
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])

UPLOAD_DIR = "uploaded_media"
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "civic-sense") # Fallback

def get_gemini():
    return GeminiClient(project_id=PROJECT_ID)

class AudioAnalysis(BaseModel):
    description: str
    contact_info: str | None = None

@router.post("")
async def create_report(
    background_tasks: BackgroundTasks,
    description: str = Form(None),
    contact_info: str = Form(None),
    source: str = Form("web"),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    # Determine media type
    media_type = "unknown"
    file_path = None

    if file:
        if file.content_type.startswith("image"):
            media_type = "image"
        elif file.content_type.startswith("audio"):
            media_type = "audio"
        elif file.content_type.startswith("video"):
            media_type = "video"

        # Save File
        file_extension = os.path.splitext(file.filename)[1]
        # If no extension (e.g. blob), guess based on mime
        if not file_extension:
            if media_type == "audio":
                file_extension = ".webm" # Common for web recording
            elif media_type == "image":
                file_extension = ".jpg"

        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # NLU Processing if Audio
    final_description = description
    final_contact_info = contact_info

    if media_type == "audio" and file_path:
        # Use Gemini to transcribe/analyze
        try:
            gemini = get_gemini()
            # Analyze audio to extract description and contact info
            # We do this synchronously for now to return the result,
            # or we could do it in background and update the DB.
            # Given the user wants "voice inputs also and convert them to nlu",
            # implied immediate feedback or at least correct data entry.

            analysis = gemini.analyze_audio_report(file_path, AudioAnalysis)

            if not final_description:
                final_description = analysis.description
            else:
                final_description += f" [Voice Transcript]: {analysis.description}"

            if not final_contact_info and analysis.contact_info:
                final_contact_info = analysis.contact_info

        except Exception as e:
            print(f"Gemini processing failed: {e}")
            if not final_description:
                final_description = "[Audio Processing Failed]"

    # Create Complaint
    db_complaint = Complaint(
        description=final_description,
        source=source,
        contact_info=final_contact_info,
        status="open"
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)

    # Save Evidence Record
    if file_path:
        db_evidence = Evidence(
            complaint_id=db_complaint.id,
            file_path=file_path,
            media_type=media_type
        )
        db.add(db_evidence)
        db.commit()

    return {
        "id": db_complaint.id,
        "message": "Report submitted successfully",
        "description": final_description,
        "contact_info": final_contact_info
    }
