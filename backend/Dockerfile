
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV PORT=8080

# Command to run uvicorn with proxy headers enabled
# --proxy-headers is CRITICAL for Cloud Run to trust the ingress headers
# --forwarded-allow-ips "*" is CRITICAL to trust the load balancer/proxy IPs
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips "*"
