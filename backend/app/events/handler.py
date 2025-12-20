from fastapi import Request
import base64
import json


async def handle_pubsub_message(request: Request, handler):
    try:
        envelope = await request.json()
    except Exception:
        return {"status": "ignored"}

    if not envelope or "message" not in envelope:
        return {"status": "ignored"}

    message = envelope.get("message", {})
    data = message.get("data")

    if not data:
        return {"status": "ignored"}

    try:
        payload = json.loads(
            base64.b64decode(data).decode("utf-8")
        )
    except Exception as e:
        print("[ERROR] Invalid base64 payload:", e)
        return {"status": "error", "reason": "invalid payload"}

    issue_id = payload.get("issue_id")
    if not issue_id:
        return {"status": "ignored"}

    # Call handler (sync or async)
    result = handler(issue_id)
    if hasattr(result, "__await__"):
        await result

    return {"status": "ok"}
