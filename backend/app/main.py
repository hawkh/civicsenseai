import os
from fastapi import FastAPI, Request

from app.api.v1.issues import router as issues_router
from app.api.v1.reports import router as reports_router
from app.events.handler import handle_pubsub_message

from app.crews.vision.worker import VisionWorker
from app.crews.routing.worker import RoutingWorker
from app.crews.verification.worker import VerificationWorker

from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.events.publisher import EventPublisher


PROJECT_ID = os.getenv("GCP_PROJECT_ID")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC")

# -------------------------
# App
# -------------------------

app = FastAPI(title="CivicSense AI Backend")
app.include_router(issues_router)
app.include_router(reports_router)

# Create tables on startup (for SQLite)
from app.database import engine, Base
Base.metadata.create_all(bind=engine)

# -------------------------
# Factories
# -------------------------

def get_repo():
    return IssueRepository()

def get_gemini():
    return GeminiClient(project_id=PROJECT_ID)

def get_publisher():
    return EventPublisher(
        project_id=PROJECT_ID,
        topic_name=PUBSUB_TOPIC,
    )

# -------------------------
# Agent Event Endpoints
# -------------------------

@app.post("/events/vision")
async def vision_event(request: Request):
    worker = VisionWorker(
        repo=get_repo(),
        gemini=get_gemini(),
        publisher=get_publisher(),
    )
    return await handle_pubsub_message(request, worker.handle)


@app.post("/events/routing")
async def routing_event(request: Request):
    worker = RoutingWorker(
        repo=get_repo(),
        gemini=get_gemini(),
        publisher=get_publisher(),
    )
    return await handle_pubsub_message(request, worker.handle)


@app.post("/events/verification")
async def verification_event(request: Request):
    worker = VerificationWorker(
        repo=get_repo(),
        gemini=get_gemini(),
        publisher=get_publisher(),
    )
    return await handle_pubsub_message(request, worker.handle)
