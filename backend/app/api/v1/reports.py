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
def create_report(
    background_tasks: BackgroundTasks,
    description: str = Form(None),
    contact_info: str = Form(None),
    source: str = Form("web"),
    # Updated to accept separate image and audio files
    image: UploadFile = File(None),
    audio: UploadFile = File(None),
    # Maintain backward compatibility with 'file' just in case, or deprecate it.
    # For this refactor, let's assume 'file' is mapped to 'image' or 'audio' by the caller if needed,
    # but strictly we are changing the contract to support both.
    # To avoid breaking existing clients (if any), we can keep 'file' as a fallback,
    # but the plan is to change the frontend too.
    # Let's support 'file' as a generic catch-all if image/audio aren't used, but prioritize explicit fields.
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    # Consolidate inputs
    files_to_process = []

    if image:
        files_to_process.append({"file": image, "type": "image"})
    if audio:
        files_to_process.append({"file": audio, "type": "audio"})
    if file and not image and not audio:
         # Fallback logic
        content_type = file.content_type
        t = "unknown"
        if content_type.startswith("image"): t = "image"
        elif content_type.startswith("audio"): t = "audio"
        elif content_type.startswith("video"): t = "video"
        files_to_process.append({"file": file, "type": t})

    saved_evidence = []
    final_description = description
    final_contact_info = contact_info

    # 1. Process files and save to disk
    for item in files_to_process:
        f = item["file"]
        t = item["type"]

        file_extension = os.path.splitext(f.filename)[1]
        if not file_extension:
            if t == "audio": file_extension = ".webm"
            elif t == "image": file_extension = ".jpg"

        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)

        saved_evidence.append({
            "path": file_path,
            "type": t
        })

    # 2. Perform NLU on Audio if present
    # Find the audio file in saved evidence
    audio_evidence = next((e for e in saved_evidence if e["type"] == "audio"), None)

    if audio_evidence:
        try:
            gemini = get_gemini()
            analysis = gemini.analyze_audio_report(audio_evidence["path"], AudioAnalysis)

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

    # 3. Create Complaint
    db_complaint = Complaint(
        description=final_description,
        source=source,
        contact_info=final_contact_info,
        status="open"
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)

    # 4. Save Evidence Records
    for evidence in saved_evidence:
        db_evidence = Evidence(
            complaint_id=db_complaint.id,
            file_path=evidence["path"],
            media_type=evidence["type"]
        )
        db.add(db_evidence)

    db.commit()

    return {
        "id": db_complaint.id,
        "message": "Report submitted successfully",
        "description": final_description,
        "contact_info": final_contact_info
    }
