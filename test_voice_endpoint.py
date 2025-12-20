from fastapi.testclient import TestClient
from backend.app.main import app
import os

client = TestClient(app)

def test_create_report_endpoint():
    # Test basic report creation without file
    response = client.post(
        "/api/v1/reports",
        data={"description": "Test report", "contact_info": "test@example.com"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert "id" in response.json()

if __name__ == "__main__":
    test_create_report_endpoint()
