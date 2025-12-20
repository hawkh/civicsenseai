from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List, Optional

from . import models, schemas, database
from .services import storage

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="CivicSense-AI API")

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/reports", response_model=schemas.Complaint)
async def create_report(
    description: str = Form(...),
    source: str = Form("web"),
    contact_info: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Save File
    file_path = await storage.save_upload_file(file)

    # 2. Create Complaint
    db_complaint = models.Complaint(
        description=description,
        source=source,
        contact_info=contact_info
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)

    # 3. Create Evidence
    db_evidence = models.Evidence(
        complaint_id=db_complaint.id,
        file_path=file_path,
        media_type=file.content_type
    )
    db.add(db_evidence)

    # 4. Create Ticket (Placeholder logic - would normally involve ML classification)
    # For now, we just create a ticket with default values
    db_ticket = models.Ticket(
        complaint_id=db_complaint.id,
        issue_type="unknown", # To be filled by ML
        priority="medium"
    )
    db.add(db_ticket)

    db.commit()
    db.refresh(db_complaint)
    return db_complaint

@app.post("/api/v1/webhook/whatsapp")
async def whatsapp_webhook(data: dict, db: Session = Depends(get_db)):
    # Mock WhatsApp webhook handler
    # In a real scenario, this would parse the Twilio/WhatsApp payload
    return {"status": "received"}

@app.get("/api/v1/tickets", response_model=List[schemas.Complaint])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Optimized query to fetch complaints with evidence and tickets in fewer queries
    complaints = (
        db.query(models.Complaint)
        .options(
            selectinload(models.Complaint.evidence),
            joinedload(models.Complaint.ticket),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return complaints
