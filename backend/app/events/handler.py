import base64
import json
from fastapi import Request


async def handle_pubsub_message(request: Request, handler):
    envelope = await request.json()

    if not envelope or "message" not in envelope:
        return {"status": "ignored"}

    message = envelope["message"]
    data = message.get("data")

    if not data:
        return {"status": "ignored"}

    payload = json.loads(base64.b64decode(data).decode("utf-8"))
    issue_id = payload.get("issue_id")

    if not issue_id:
        return {"status": "ignored"}

    # 🔥 FIX: call sync handler directly
    handler(issue_id)

    return {"status": "ok"}
