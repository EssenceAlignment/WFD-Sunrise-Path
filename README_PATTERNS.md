# Pattern Recognition Service

## Overview

The Pattern Recognition Service provides a REST API endpoint for identifying patterns in various input types that advance Recovery Compass goals and Environmental Response Design (ERD) principles.

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r app/requirements.txt
```

## Running the Service

```bash
# Start the FastAPI server
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python main.py
```

## API Endpoints

### POST /patterns/recognize

Recognizes patterns in various input types.

**Supported Input Types:**
- Plain text
- Images (upload)
- Structured data (JSON/CSV)
- Code repository snapshots (TAR/ZIP)

**Response Schema:**
```json
{
  "patterns": [
    {
      "id": "pat-NNN",
      "name": "Human-readable label",
      "confidence": 0.00-1.00,
      "insights": "Detailed explanation",
      "recommendations": ["action1", "action2"],
      "force_multiplication_score": 0-100
    }
  ],
  "meta": {
    "input_types": ["text", "image", "structured", "code_repository_snapshot"],
    "processing_time_ms": 0,
    "ipe_compliance": true
  }
}
```

### GET /health

Health check endpoint.

## Testing Commands

### Using HTTPie

```bash
# Text input example
http --form POST localhost:8000/patterns/recognize \
  text_input="Implementing sustainable environmental practices for community recovery programs"

# Image upload example
http --form POST localhost:8000/patterns/recognize \
  image_file@"./sample_image.jpg"

# Structured data example (JSON)
http --form POST localhost:8000/patterns/recognize \
  structured_format="json" \
  structured_data='{"recovery_metrics": {"participants": 150, "success_rate": 0.78}}'

# Repository snapshot example
http --form POST localhost:8000/patterns/recognize \
  repository_snapshot@"./project.tar.gz"

# Multiple inputs
http --form POST localhost:8000/patterns/recognize \
  text_input="Recovery-focused community initiative" \
  structured_format="json" \
  structured_data='{"program": "peer_support", "impact": "high"}'
```

### Using cURL

```bash
# Text input example
curl -X POST "http://localhost:8000/patterns/recognize" \
  -F "text_input=Environmental sustainability and recovery programs"

# Image upload example
curl -X POST "http://localhost:8000/patterns/recognize" \
  -F "image_file=@sample_image.png"

# Multiple inputs example
curl -X POST "http://localhost:8000/patterns/recognize" \
  -F "text_input=Healing-centered approach to community development" \
  -F "structured_format=json" \
  -F 'structured_data={"type": "recovery_program", "participants": 200}'
```

### Using Python requests

```python
import requests

# Text input
response = requests.post(
    "http://localhost:8000/patterns/recognize",
    data={"text_input": "Sustainable recovery and environmental response"}
)
print(response.json())

# Image upload
with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/patterns/recognize",
        files={"image_file": f}
    )
print(response.json())
```

## Example Request and Response

### Request (HTTPie)
```bash
http --form POST localhost:8000/patterns/recognize \
  text_input="Our organization focuses on environmental sustainability and recovery-oriented community programs"
```

### Response
```json
{
  "patterns": [
    {
      "id": "pat-001",
      "name": "Environmental Response Design Alignment",
      "confidence": 0.85,
      "insights": "Content demonstrates alignment with ERD principles through emphasis on sustainable practices and environmental consciousness. This pattern indicates opportunities for force multiplication through community engagement and resource optimization.",
      "recommendations": [
        "Integrate ERD framework into operational workflows",
        "Establish metrics for environmental impact tracking",
        "Create community feedback loops for continuous improvement"
      ],
      "force_multiplication_score": 75
    },
    {
      "id": "pat-002",
      "name": "Recovery-Centered Approach",
      "confidence": 0.92,
      "insights": "Strong recovery-focused language detected, indicating alignment with Recovery Compass mission. This pattern suggests high potential for community impact and stakeholder engagement.",
      "recommendations": [
        "Develop peer support programs",
        "Create resource mapping for recovery services",
        "Implement outcome tracking systems"
      ],
      "force_multiplication_score": 88
    }
  ],
  "meta": {
    "input_types": ["text"],
    "processing_time_ms": 42,
    "ipe_compliance": true
  }
}
```

## Observability

The service emits structured logs with metrics:
- Pattern count
- Average confidence score
- Average force multiplication score
- Input types processed
- Processing time

Example log output:
```
2025-02-08 10:30:45 - cline_ai_service - INFO - Pattern recognition completed - patterns_count: 2, avg_confidence: 0.88, avg_fm_score: 81, input_types: [<InputType.TEXT: 'text'>], processing_time_ms: 42
```

## Security Features

- Automatic secret redaction (API keys, credit cards, emails)
- Content safety checks for malicious patterns
- Comprehensive error handling
- Request validation

## Development Notes

- This is a prototype implementation with stub pattern detectors
- All requests pass IPE compliance in the current version
- Pattern detection logic can be extended with ML models
- Supports concurrent requests via FastAPI async handlers
