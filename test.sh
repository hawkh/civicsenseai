#!/usr/bin/env bash
set -e

# ===============================
# CONFIG
# ===============================
BASE_URL=${BASE_URL:-"http://127.0.0.1:8000"}
# For Cloud Run:
# BASE_URL="https://backend-1005385950490.us-central1.run.app"

echo "🚀 Testing CivicSense backend at: $BASE_URL"
echo

# ===============================
# 1. CREATE ISSUE
# ===============================
echo "1️⃣ Creating issue..."

CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/issues" \
  -H "Content-Type: application/json" \
  -d '{
    "location": { "lat": 17.44, "lng": 78.34 },
    "description": "Overflowing garbage near main road",
    "image_url": "gs://civicsense-images/test.jpg"
  }')

echo "Response: $CREATE_RESPONSE"

ISSUE_ID=$(echo "$CREATE_RESPONSE" | jq -r '.issue_id')

if [[ "$ISSUE_ID" == "null" || -z "$ISSUE_ID" ]]; then
  echo "❌ Failed to create issue"
  exit 1
fi

echo "✅ Issue created: $ISSUE_ID"
echo

# ===============================
# Helper: Pub/Sub payload
# ===============================
PAYLOAD=$(echo -n "{\"issue_id\":\"$ISSUE_ID\"}" | base64)

# ===============================
# 2. VISION EVENT
# ===============================
echo "2️⃣ Running vision worker..."

curl -s -X POST "$BASE_URL/events/vision" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": {
      \"data\": \"$PAYLOAD\"
    }
  }" | jq

echo "✅ Vision processing done"
echo

# ===============================
# 3. ROUTING EVENT
# ===============================
echo "3️⃣ Running routing worker..."

curl -s -X POST "$BASE_URL/events/routing" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": {
      \"data\": \"$PAYLOAD\"
    }
  }" | jq

echo "✅ Routing done"
echo

# ===============================
# 4. VERIFICATION EVENT
# ===============================
echo "4️⃣ Running verification worker..."

curl -s -X POST "$BASE_URL/events/verification" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": {
      \"data\": \"$PAYLOAD\"
    }
  }" | jq

echo "✅ Verification done"
echo

# ===============================
# 5. FETCH FINAL ISSUE
# ===============================
echo "5️⃣ Fetching final issue state..."

FINAL_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/issues/$ISSUE_ID")

echo "$FINAL_RESPONSE" | jq

STATUS=$(echo "$FINAL_RESPONSE" | jq -r '.status')

echo
echo "🎉 FINAL STATUS: $STATUS"

if [[ "$STATUS" != "verified" ]]; then
  echo "⚠️ Warning: Issue not fully verified"
else
  echo "✅ END-TO-END FLOW SUCCESSFUL"
fi
