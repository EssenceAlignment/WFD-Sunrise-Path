from fastapi import FastAPI, Request, HTTPException
from typing import Any, List, Optional, Dict
from app.schemas import (
    PatternRecognitionRequest,
    PatternRecognitionResponse,
    Pattern,
    ContextCreationRequest,
    ContextCreationResponse,
    ContextUpdateRequest,
    ContextUpdateResponse,
    ContextDetailsResponse,
    EnvironmentDefinition
)
from prometheus_client import generate_latest, Counter, Histogram
from starlette.responses import PlainTextResponse
import os
import time
import uuid
from datetime import datetime

app = FastAPI()

# Attach APP_VERSION label (env var) for release comparison.
APP_VERSION = os.environ.get("APP_VERSION", "unknown")

# Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "app_version"],
)

PATTERN_RECOGNITION_DURATION = Histogram(
    "pattern_recognition_duration_seconds",
    "Histogram of pattern recognition duration",
    ["pattern_type", "app_version"],
)

PATTERN_TYPE_COUNTER = Counter(
    "pattern_type_total",
    "Total count of each pattern type detected",
    ["pattern_type", "app_version"],
)

# In-memory storage for contexts (for prototype)
contexts_db: Dict[str, ContextDetailsResponse] = {}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    return PlainTextResponse(generate_latest())

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        app_version=APP_VERSION,
    ).inc()
    response = await call_next(request)
    return response

@app.post("/patterns/recognize", response_model=PatternRecognitionResponse)
async def recognize_patterns(request: PatternRecognitionRequest):
    start_time = time.time()
    
    # Simulate pattern detection and increment counter
    detected_patterns = [
        Pattern(
            id="pat-a1b2c3d4", # Updated to conform to regex
            name="Dummy Pattern",
            confidence=0.8,
            details={
                "source": "placeholder"
            }
        )
    ]
    
    for pattern in detected_patterns:
        PATTERN_TYPE_COUNTER.labels(
            pattern_type=pattern.name,
            app_version=APP_VERSION,
        ).inc()

    response_data = PatternRecognitionResponse(
        patterns=detected_patterns,
        analysisSummary="Dummy analysis summary."
    )
    end_time = time.time()
    PATTERN_RECOGNITION_DURATION.labels(
        pattern_type=request.dataType,
        app_version=APP_VERSION,
    ).observe(end_time - start_time)
    return response_data

# Context Management Endpoints

@app.post("/context/create", response_model=ContextCreationResponse)
async def create_context(request: ContextCreationRequest):
    context_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    new_context = ContextDetailsResponse(
        contextId=context_id,
        name=request.name,
        description=request.description,
        parameters=request.parameters,
        environmentDefinition=request.environmentDefinition,
        createdAt=now,
        updatedAt=now,
    )
    contexts_db[context_id] = new_context
    return ContextCreationResponse(
        contextId=context_id,
        status="success",
        message="Context created successfully."
    )

@app.put("/context/{contextId}", response_model=ContextUpdateResponse)
async def update_context(contextId: str, request: ContextUpdateRequest):
    if contextId not in contexts_db:
        raise HTTPException(status_code=404, detail="Context not found")

    existing_context = contexts_db[contextId]
    now = datetime.now().isoformat()

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "parameters" and isinstance(value, dict) and isinstance(existing_context.parameters, dict):
            existing_context.parameters.update(value)
        elif key == "environmentDefinition" and isinstance(value, dict) and isinstance(existing_context.environmentDefinition, dict):
            # Assuming environmentDefinition can be partially updated if it's a dict
            existing_context.environmentDefinition.custom_attributes.update(value.get("custom_attributes", {}))
            # For other fields in environmentDefinition, a full replacement might be simpler for now
            # or more granular updates would be needed based on specific requirements.
            if value.get("toolchains") is not None: existing_context.environmentDefinition.toolchains = value["toolchains"]
            if value.get("documentation_systems") is not None: existing_context.environmentDefinition.documentation_systems = value["documentation_systems"]
            if value.get("communication_platforms") is not None: existing_context.environmentDefinition.communication_platforms = value["communication_platforms"]
            if value.get("data_storage_solutions") is not None: existing_context.environmentDefinition.data_storage_solutions = value["data_storage_solutions"]
            if value.get("cloud_providers") is not None: existing_context.environmentDefinition.cloud_providers = value["cloud_providers"]
        else:
            setattr(existing_context, key, value)
    
    existing_context.updatedAt = now
    contexts_db[contextId] = existing_context # Update in DB

    return ContextUpdateResponse(
        contextId=contextId,
        status="success",
        message="Context updated successfully."
    )

@app.get("/context/{contextId}", response_model=ContextDetailsResponse)
async def get_context(contextId: str):
    if contextId not in contexts_db:
        raise HTTPException(status_code=404, detail="Context not found")
    return contexts_db[contextId]


