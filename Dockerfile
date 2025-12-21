FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# requirements.txt IS in backend/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# app/ is in backend/
COPY app ./app

EXPOSE 8080

CMD exec uvicorn app.main:app \
  --host 0.0.0.0 \
  --port $PORT \
  --proxy-headers \
  --forwarded-allow-ips "*"
