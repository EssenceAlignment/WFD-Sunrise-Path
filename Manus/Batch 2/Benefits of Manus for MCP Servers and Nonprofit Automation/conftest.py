import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Fixture to provide a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def sample_text_data():
    """Fixture to provide sample text data for testing."""
    return "Environmental sustainability and recovery programs"

@pytest.fixture
def sample_structured_data():
    """Fixture to provide sample structured data for testing."""
    return {"key": "value", "another_key": "another_value"}

@pytest.fixture
def sample_csv_data():
    """Fixture to provide sample CSV data for testing."""
    return "header1,header2\nvalue1,value2"


