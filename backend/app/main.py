from dotenv import load_dotenv
load_dotenv()

import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.issues import router as issues_router
from app.events.handler import handle_pubsub_message

from app.crews.vision.worker import VisionWorker
from app.crews.routing.worker import RoutingWorker
from app.crews.verification.worker import VerificationWorker

from app.datastore.firestore import IssueRepository
from app.services.gemini.client import GeminiClient
from app.events.publisher import EventPublisher

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s",
)

logger = logging.getLogger(__name__)

LOCAL_DEV = os.getenv("LOCAL_DEV", "false").lower() == "true"
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC")

if not LOCAL_DEV:
    if not PROJECT_ID:
        raise RuntimeError("GCP_PROJECT_ID env var not set")
    if not PUBSUB_TOPIC:
        raise RuntimeError("PUBSUB_TOPIC env var not set")
else:
    logger.info("Running in LOCAL_DEV mode")

app = FastAPI(title="CivicSense AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(issues_router)


@app.get("/version")
def version():
    return {"version": "1.0.0", "local_dev": LOCAL_DEV}


def get_repo():
    return IssueRepository()


def get_gemini():
    if LOCAL_DEV:
        return None
    return GeminiClient(project_id=PROJECT_ID)


def get_publisher():
    if LOCAL_DEV:
        return None
    return EventPublisher(
        project_id=PROJECT_ID,
        topic_name=PUBSUB_TOPIC,
    )


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
