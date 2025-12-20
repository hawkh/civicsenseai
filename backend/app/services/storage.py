import os
import shutil
import uuid
from fastapi import UploadFile
from starlette.concurrency import run_in_threadpool

UPLOAD_DIR = "uploaded_media"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    # Use UUID to prevent path traversal and filename collisions
    extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    def _save():
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

    await run_in_threadpool(_save)
    return file_path
