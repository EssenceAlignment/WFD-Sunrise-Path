# Pattern Recognition API Examples

## HTTPie Example Request and Response

### Text Input Request
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

## Postman Collection

### Collection Info
```json
{
  "info": {
    "name": "Cline AI Pattern Recognition",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Recognize Patterns - Text",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "text_input",
              "value": "Implementing sustainable environmental practices for community recovery programs",
              "type": "text"
            }
          ]
        },
        "url": {
          "raw": "http://localhost:8000/patterns/recognize",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["patterns", "recognize"]
        }
      }
    },
    {
      "name": "Recognize Patterns - Multiple Inputs",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "text_input",
              "value": "Recovery-focused community initiative",
              "type": "text"
            },
            {
              "key": "structured_format",
              "value": "json",
              "type": "text"
            },
            {
              "key": "structured_data",
              "value": "{\"program\": \"peer_support\", \"impact\": \"high\"}",
              "type": "text"
            }
          ]
        },
        "url": {
          "raw": "http://localhost:8000/patterns/recognize",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["patterns", "recognize"]
        }
      }
    },
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/health",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["health"]
        }
      }
    }
  ]
}
```

## cURL Examples

### Text Input
```bash
curl -X POST "http://localhost:8000/patterns/recognize" \
  -F "text_input=Environmental sustainability and recovery programs"
```

### Image Upload
```bash
curl -X POST "http://localhost:8000/patterns/recognize" \
  -F "image_file=@sample_image.png"
```

### Structured Data (JSON)
```bash
curl -X POST "http://localhost:8000/patterns/recognize" \
  -F "structured_format=json" \
  -F 'structured_data={"recovery_metrics": {"participants": 150, "success_rate": 0.78}}'
```

### Repository Snapshot
```bash
curl -X POST "http://localhost:8000/patterns/recognize" \
  -F "repository_snapshot=@project.tar.gz"
```

### Multiple Inputs
```bash
curl -X POST "http://localhost:8000/patterns/recognize" \
  -F "text_input=Healing-centered approach to community development" \
  -F "structured_format=json" \
  -F 'structured_data={"type": "recovery_program", "participants": 200}'
