# Cline AI Service API: Context Management Endpoints

This document provides detailed information about the Context Management Endpoints of the Cline AI Service API, including their functionality, request/response structures, and examples for various tools.

## 1. Endpoints Overview

The Context Management Endpoints allow for the creation, retrieval, and updating of operational or user-specific contexts within the Cline AI system. These contexts are crucial for providing relevant environmental and behavioral parameters to AI models, enhancing their performance and adherence to Gold-Plated IPE standards.

### `POST /context/create`
*   **Description:** Creates a new context.
*   **Method:** `POST`
*   **URL:** `/context/create`

### `GET /context/{contextId}`
*   **Description:** Retrieves the details of a specific context.
*   **Method:** `GET`
*   **URL:** `/context/{contextId}`

### `PUT /context/{contextId}`
*   **Description:** Updates an existing context.
*   **Method:** `PUT`
*   **URL:** `/context/{contextId}`

## 2. Request and Response Structures

### `EnvironmentDefinition` Model

This model defines the structured representation of an operational environment. It is a flexible object that can include various attributes relevant to the system's context.

```python
class EnvironmentDefinition(BaseModel):
    toolchains: Optional[List[str]] = None
    documentation_systems: Optional[List[str]] = None
    communication_platforms: Optional[List[str]] = None
    data_storage_solutions: Optional[List[str]] = None
    cloud_providers: Optional[List[str]] = None
    custom_attributes: Optional[Any] = None
```

**Example `environmentDefinition` JSON:**
```json
{
  "toolchains": [
    "git",
    "CI/CD",
    "monitoring_stack"
  ],
  "documentation_systems": [
    "Confluence",
    "Markdown_repos"
  ],
  "custom_attributes": {
    "project_phase": "development",
    "team_size": 15
  }
}
```

### `ContextCreationRequest`

Used to create a new context.

```python
class ContextCreationRequest(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any]
    environmentDefinition: Optional[EnvironmentDefinition] = None
```

### `ContextCreationResponse`

Response after a successful context creation.

```python
class ContextCreationResponse(BaseModel):
    contextId: str
    status: str
    message: str
```

### `ContextUpdateRequest`

Used to update an existing context.

```python
class ContextUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    environmentDefinition: Optional[EnvironmentDefinition] = None
```

### `ContextUpdateResponse`

Response after a successful context update.

```python
class ContextUpdateResponse(BaseModel):
    contextId: str
    status: str
    message: str
```

### `ContextDetailsResponse`

Response containing the details of a retrieved context.

```python
class ContextDetailsResponse(BaseModel):
    contextId: str
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any]
    environmentDefinition: Optional[EnvironmentDefinition] = None
    createdAt: str
    updatedAt: str
```

## 3. Examples

### `POST /context/create`

**HTTPie Example:**
```bash
http POST http://localhost:8000/context/create \
  name="MyDevelopmentContext" \
  description="Context for ongoing development work" \
  parameters:='{"user_id": "dev-001", "project_id": "RC-PROJ-005"}' \
  environmentDefinition:='{"toolchains": ["git", "vscode"], "custom_attributes": {"ide": "vscode"}}'
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/context/create \
  -H "Content-Type: application/json" \
  -d 
```

```json
{
    "name": "MyDevelopmentContext",
    "description": "Context for ongoing development work",
    "parameters": {"user_id": "dev-001", "project_id": "RC-PROJ-005"},
    "environmentDefinition": {
        "toolchains": ["git", "vscode"],
        "custom_attributes": {"ide": "vscode"}
    }
}
```

**Postman Example:**

*   **Method:** `POST`
*   **URL:** `http://localhost:8000/context/create`
*   **Headers:**
    *   `Content-Type: application/json`
*   **Body (raw JSON):**
```json
{
    "name": "MyDevelopmentContext",
    "description": "Context for ongoing development work",
    "parameters": {"user_id": "dev-001", "project_id": "RC-PROJ-005"},
    "environmentDefinition": {
        "toolchains": ["git", "vscode"],
        "custom_attributes": {"ide": "vscode"}
    }
}
```

### `GET /context/{contextId}`

**HTTPie Example:**
```bash
http GET http://localhost:8000/context/a1b2c3d4-e5f6-7890-1234-567890abcdef
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/context/a1b2c3d4-e5f6-7890-1234-567890abcdef
```

**Postman Example:**

*   **Method:** `GET`
*   **URL:** `http://localhost:8000/context/a1b2c3d4-e5f6-7890-1234-567890abcdef`

### `PUT /context/{contextId}`

**HTTPie Example:**
```bash
http PUT http://localhost:8000/context/a1b2c3d4-e5f6-7890-1234-567890abcdef \
  description="Updated description for the context" \
  parameters:='{"status": "active", "version": "2.0"}' \
  environmentDefinition:='{"cloud_providers": ["AWS"], "custom_attributes": {"deployment_region": "us-east-1"}}'
```

**cURL Example:**
```bash
curl -X PUT http://localhost:8000/context/a1b2c3d4-e5f6-7890-1234-567890abcdef \
  -H "Content-Type: application/json" \
  -d 
```

```json
{
    "description": "Updated description for the context",
    "parameters": {"status": "active", "version": "2.0"},
    "environmentDefinition": {
        "cloud_providers": ["AWS"],
        "custom_attributes": {"deployment_region": "us-east-1"}
    }
}
```

**Postman Example:**

*   **Method:** `PUT`
*   **URL:** `http://localhost:8000/context/a1b2c3d4-e5f6-7890-1234-567890abcdef`
*   **Headers:**
    *   `Content-Type: application/json`
*   **Body (raw JSON):**
```json
{
    "description": "Updated description for the context",
    "parameters": {"status": "active", "version": "2.0"},
    "environmentDefinition": {
        "cloud_providers": ["AWS"],
        "custom_attributes": {"deployment_region": "us-east-1"}
    }
}
```

This documentation provides a comprehensive guide for interacting with the Cline AI Context Management Endpoints, ensuring clarity and ease of use for developers and integrators.

