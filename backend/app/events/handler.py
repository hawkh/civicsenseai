import base64
import json
from fastapi import Request, HTTPException


async def handle_pubsub_message(
    request: Request,
    handler,
):
    """
    Generic handler for Pub/Sub push events.
    """

    envelope = await request.json()

    if not envelope or "message" not in envelope:
        raise HTTPException(status_code=400, detail="Invalid Pub/Sub envelope")

    message = envelope["message"]

    if "data" not in message:
        raise HTTPException(status_code=400, detail="Missing message.data")

    try:
        payload = base64.b64decode(message["data"]).decode("utf-8")
        data = json.loads(payload)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 payload")

    issue_id = data.get("issue_id")
    if not issue_id:
        raise HTTPException(status_code=400, detail="Missing issue_id")

    # Call the worker handler
    await handler(issue_id)

    return {"status": "ok"}
