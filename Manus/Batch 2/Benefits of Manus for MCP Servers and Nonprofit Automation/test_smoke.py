
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.ci_gate
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.ci_gate
def test_recognize_text_input():
    response = client.post(
        "/patterns/recognize",
        json={
            "dataType": "text",
            "data": "Environmental sustainability and recovery programs"
        }
    )
    assert response.status_code == 200
    assert len(response.json()["patterns"]) > 0

@pytest.mark.ci_gate
def test_recognize_image_input():
    # This test assumes a base64 encoded image or a path to an image file
    # For a real implementation, you'd need to mock the image processing
    response = client.post(
        "/patterns/recognize",
        json={
            "dataType": "image",
            "data": "base64_encoded_image_data_here"
        }
    )
    assert response.status_code == 200
    assert len(response.json()["patterns"]) > 0

@pytest.mark.ci_gate
def test_recognize_structured_json_input():
    response = client.post(
        "/patterns/recognize",
        json={
            "dataType": "structured",
            "data": {"key": "value", "another_key": "another_value"}
        }
    )
    assert response.status_code == 200
    assert len(response.json()["patterns"]) > 0

@pytest.mark.ci_gate
def test_recognize_structured_csv_input():
    response = client.post(
        "/patterns/recognize",
        json={
            "dataType": "structured",
            "data": "header1,header2\nvalue1,value2"
        }
    )
    assert response.status_code == 200
    assert len(response.json()["patterns"]) > 0

@pytest.mark.ci_gate
def test_recognize_code_repository_snapshot_input():
    # This test assumes a base64 encoded tar/zip or a path to the file
    # For a real implementation, you'd need to mock the file processing
    response = client.post(
        "/patterns/recognize",
        json={
            "dataType": "code_repository_snapshot",
            "data": "base64_encoded_tar_zip_data_here"
        }
    )
    assert response.status_code == 200
    assert len(response.json()["patterns"]) > 0



