from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_read_main():
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_report_no_file():
    response = client.post("/api/v1/reports", data={"description": "test"})
    # Should fail because file is required
    assert response.status_code == 422
