from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_tickets_empty():
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200
    assert response.json() == []

def test_create_report_and_verify():
    # 1. Create Report
    with open("backend/tests/test_image.png", "wb") as f:
        f.write(b"fake image data")

    with open("backend/tests/test_image.png", "rb") as f:
        response = client.post(
            "/api/v1/reports",
            data={"description": "Test pothole", "source": "web"},
            files={"file": ("test_image.png", f, "image/png")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test pothole"
    assert data["source"] == "web"
    assert "id" in data

    # 2. Verify it appears in tickets
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200
    tickets = response.json()
    assert len(tickets) > 0
    assert tickets[-1]["description"] == "Test pothole"
