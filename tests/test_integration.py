import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestIntegration:
    
    def test_create_task_integration(self):
        payload = {
            "title": "Integration Test Task",
            "description": "Testing task creation via API",
            "priority": "medium"
        }
        
        response = client.post("/v1/tasks", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Integration Test Task"
        assert data["description"] == "Testing task creation via API"
        assert data["priority"] == "medium"
        assert "id" in data
        assert "created_at" in data