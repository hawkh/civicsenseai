from dotenv import load_dotenv
load_dotenv()

import os
import logging
from functools import lru_cache
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

if LOCAL_DEV:
    logger.info("Running in LOCAL_DEV mode")
else:
    if not PROJECT_ID:
        raise RuntimeError("GCP_PROJECT_ID env var not set")
    if not PUBSUB_TOPIC:
        raise RuntimeError("PUBSUB_TOPIC env var not set")

app = FastAPI(title="CivicSense AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://civicsenseai.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def force_cors_on_errors(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "https://civicsenseai.vercel.app"
            },
        )

app.include_router(issues_router)

@app.middleware("http")
async def force_cors_on_errors(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "https://civicsenseai.vercel.app"
            },
        )

# -------------------------
# Factories
# -------------------------

@lru_cache()
def get_repo() -> IssueRepository:
    # ⚡ Optimization: Singleton pattern for repository to pool Firestore connections
    return IssueRepository()

def get_gemini() -> GeminiClient | None:
    if LOCAL_DEV:
        return None
    return GeminiClient(project_id=PROJECT_ID)

def get_publisher() -> EventPublisher | None:
    if LOCAL_DEV:
        return None
    return EventPublisher(
        project_id=PROJECT_ID,
        topic_name=PUBSUB_TOPIC,
    )


# -------------------------
# Event endpoints
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


@app.get("/health")
def health():
    return {"status": "ok"}
