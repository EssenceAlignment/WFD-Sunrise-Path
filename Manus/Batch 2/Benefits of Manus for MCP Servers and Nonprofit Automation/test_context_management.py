import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

client = TestClient(app)

@pytest.mark.ci_gate
def test_create_context_success():
    response = client.post(
        "/context/create",
        json={
            "name": "Test Context 1",
            "description": "A context for testing purposes.",
            "parameters": {"user_id": "123", "session_id": "abc"},
            "environmentDefinition": {
                "toolchains": ["git", "docker"],
                "custom_attributes": {"project": "recovery_compass"}
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "contextId" in response.json()

@pytest.mark.ci_gate
def test_get_context_success():
    # First, create a context
    create_response = client.post(
        "/context/create",
        json={
            "name": "Context to Retrieve",
            "parameters": {"data_type": "financial"}
        }
    )
    context_id = create_response.json()["contextId"]

    # Then, retrieve it
    get_response = client.get(f"/context/{context_id}")
    assert get_response.status_code == 200
    assert get_response.json()["contextId"] == context_id
    assert get_response.json()["name"] == "Context to Retrieve"

@pytest.mark.ci_gate
def test_get_context_not_found():
    response = client.get("/context/non-existent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Context not found"

@pytest.mark.ci_gate
def test_update_context_success():
    # First, create a context
    create_response = client.post(
        "/context/create",
        json={
            "name": "Context to Update",
            "parameters": {"version": "1.0"}
        }
    )
    context_id = create_response.json()["contextId"]

    # Then, update it
    update_response = client.put(
        f"/context/{context_id}",
        json={
            "description": "Updated description.",
            "parameters": {"version": "2.0", "new_param": "value"},
            "environmentDefinition": {
                "toolchains": ["git", "kubernetes"],
                "custom_attributes": {"status": "active"}
            }
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "success"

    # Verify update
    get_response = client.get(f"/context/{context_id}")
    assert get_response.status_code == 200
    assert get_response.json()["description"] == "Updated description."
    assert get_response.json()["parameters"]["version"] == "2.0"
    assert get_response.json()["parameters"]["new_param"] == "value"
    assert "kubernetes" in get_response.json()["environmentDefinition"]["toolchains"]
    assert get_response.json()["environmentDefinition"]["custom_attributes"]["status"] == "active"

@pytest.mark.ci_gate
def test_update_context_not_found():
    response = client.put(
        "/context/non-existent-id",
        json={
            "name": "Should Not Update"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Context not found"

@pytest.mark.ci_gate
def test_create_context_invalid_data():
    response = client.post(
        "/context/create",
        json={
            "name": 123, # Invalid type for name
            "parameters": "not_a_dict" # Invalid type for parameters
        }
    )
    assert response.status_code == 422 # Unprocessable Entity for validation errors

@pytest.mark.ci_gate
def test_update_context_invalid_data():
    # First, create a context
    create_response = client.post(
        "/context/create",
        json={
            "name": "Context for Invalid Update",
            "parameters": {}
        }
    )
    context_id = create_response.json()["contextId"]

    response = client.put(
        f"/context/{context_id}",
        json={
            "parameters": "not_a_dict" # Invalid type for parameters
        }
    )
    assert response.status_code == 422


