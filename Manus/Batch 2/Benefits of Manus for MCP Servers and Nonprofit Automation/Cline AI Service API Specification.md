# Cline AI Service API Specification

## 1. Introduction

This document defines the Application Programming Interface (API) for the Cline AI Service. The Cline AI Service is designed to provide core AI functionalities, including pattern recognition, context management, and prompt generation, to various components within the Recovery Compass ecosystem. This API will serve as the central interface for integrating Cline AI capabilities into frontend applications, automated agents (like Manus and Perplexity MCP), and developer tooling, ensuring adherence to Gold-Plated IPE standards and maximizing strategic force multiplication.

## 2. API Endpoints

This section will detail the various API endpoints, their functionalities, and their respective HTTP methods.

### 2.1 Pattern Recognition Endpoints

### 2.2 Context Management Endpoints

### 2.3 Prompt Generation Endpoints

## 3. Data Models

This section will define the data structures (request and response payloads) used across the API.

### 3.1 Request Models

### 3.2 Response Models

## 4. Authentication and Authorization

## 5. Error Handling

## 6. Versioning

## 7. Rate Limiting

## 8. Examples





### 2.1 Pattern Recognition Endpoints

#### `POST /patterns/recognize`

*   **Description:** Analyzes input data (text, images, structured data) to identify predefined or emerging patterns relevant to Recovery Compass objectives and ERD principles. This endpoint is crucial for the "Insight Catalyst" and for feeding into Pattern Registry 2.0.
*   **Request Body:**
    ```json
    {
      "dataType": "string", // e.g., "text", "image", "structured"
      "data": "any",        // The actual data to analyze
      "contextId": "string" // Optional: ID of a context to apply during recognition
    }
    ```
*   **Response Body:**
    ```json
    {
      "patterns": [
        {
          "id": "string",
          "name": "string",
          "confidence": "number", // 0.0 - 1.0
          "details": "object"   // Specific details about the recognized pattern
        }
      ],
      "analysisSummary": "string" // Human-readable summary of the recognition
    }
    ```

#### `GET /patterns/{patternId}`

*   **Description:** Retrieves detailed information about a specific recognized pattern.
*   **Parameters:**
    *   `patternId` (path): The unique identifier of the pattern.
*   **Response Body:** (Details of a `Pattern` object)

### 2.2 Context Management Endpoints

#### `POST /context/create`

*   **Description:** Creates a new operational or user-specific context for Cline AI. This context can influence pattern recognition, prompt generation, and overall AI behavior, aligning with the "Actualization Map" concept.
*   **Request Body:**
    ```json
    {
      "name": "string",
      "description": "string",
      "parameters": "object" // Key-value pairs defining the context (e.g., user preferences, B2B client profile)
    }
    ```
*   **Response Body:**
    ```json
    {
      "contextId": "string",
      "message": "Context created successfully."
    }
    ```

#### `PUT /context/{contextId}`

*   **Description:** Updates an existing context.
*   **Parameters:**
    *   `contextId` (path): The unique identifier of the context.
*   **Request Body:** (Partial `Context` object for update)
*   **Response Body:**
    ```json
    {
      "contextId": "string",
      "message": "Context updated successfully."
    }
    ```

#### `GET /context/{contextId}`

*   **Description:** Retrieves the details of a specific context.
*   **Parameters:**
    *   `contextId` (path): The unique identifier of the context.
*   **Response Body:** (Details of a `Context` object)

### 2.3 Prompt Generation Endpoints

#### `POST /prompts/generate`

*   **Description:** Generates dynamic, context-aware prompts for various applications, including adaptive question flows, personalized insights, and funder narratives. This endpoint is central to the "Adaptive Question Engine" and "Story-Mode Snippet Generator."
*   **Request Body:**
    ```json
    {
      "promptType": "string", // e.g., "question", "insight", "narrative"
      "contextId": "string",  // Optional: Context to inform prompt generation
      "parameters": "object"  // Specific parameters for prompt generation (e.g., user journey data, target audience)
    }
    ```
*   **Response Body:**
    ```json
    {
      "generatedPrompt": "string",
      "promptId": "string" // Optional: ID for tracking/versioning generated prompts
    }
    ```

#### `POST /prompts/evaluate`

*   **Description:** Evaluates the effectiveness or relevance of a generated prompt based on user interaction or predefined criteria. This supports continuous optimization.
*   **Request Body:**
    ```json
    {
      "promptId": "string",
      "evaluationMetric": "string", // e.g., "engagement", "relevance", "conversion"
      "value": "number"           // The measured value for the metric
    }
    ```
*   **Response Body:**
    ```json
    {
      "message": "Prompt evaluation recorded."
    }
    ```





### 3.1 Request Models

#### `PatternRecognitionRequest`

Used by `POST /patterns/recognize`.

```json
{
  "dataType": "string", // Required. Type of data: "text", "image", "structured", etc.
  "data": "any",        // Required. The actual data payload. Format depends on `dataType`.
  "contextId": "string" // Optional. ID of a context to apply during recognition.
}
```

#### `ContextCreationRequest`

Used by `POST /context/create`.

```json
{
  "name": "string",        // Required. Human-readable name for the context.
  "description": "string",   // Optional. Description of the context.
  "parameters": "object"   // Required. Key-value pairs defining the context (e.g., user preferences, B2B client profile, ERD-specific parameters).
}
```

#### `ContextUpdateRequest`

Used by `PUT /context/{contextId}`.

```json
{
  "name": "string",        // Optional. Human-readable name for the context.
  "description": "string",   // Optional. Description of the context.
  "parameters": "object"   // Optional. Key-value pairs defining the context. Merges with existing parameters.
}
```

#### `PromptGenerationRequest`

Used by `POST /prompts/generate`.

```json
{
  "promptType": "string", // Required. Type of prompt to generate: "question", "insight", "narrative", etc.
  "contextId": "string",  // Optional. Context ID to inform prompt generation.
  "parameters": "object"  // Required. Specific parameters for prompt generation (e.g., user journey data, target audience, ERD principles).
}
```

#### `PromptEvaluationRequest`

Used by `POST /prompts/evaluate`.

```json
{
  "promptId": "string",         // Required. ID of the prompt being evaluated.
  "evaluationMetric": "string", // Required. Metric for evaluation: "engagement", "relevance", "conversion", etc.
  "value": "number"             // Required. The measured value for the metric.
}
```

### 3.2 Response Models

#### `PatternRecognitionResponse`

Returned by `POST /patterns/recognize`.

```json
{
  "patterns": [
    {
      "id": "string",           // Unique ID of the recognized pattern.
      "name": "string",         // Human-readable name of the pattern.
      "confidence": "number",   // Confidence score (0.0 - 1.0).
      "details": "object"       // Specific details about the recognized pattern, e.g., matched ERD principles, archetypes.
    }
  ],
  "analysisSummary": "string" // Human-readable summary of the recognition process and findings.
}
```

#### `ContextCreationResponse`

Returned by `POST /context/create`.

```json
{
  "contextId": "string", // Unique ID of the newly created context.
  "message": "string"    // Confirmation message.
}
```

#### `ContextUpdateResponse`

Returned by `PUT /context/{contextId}`.

```json
{
  "contextId": "string", // Unique ID of the updated context.
  "message": "string"    // Confirmation message.
}
```

#### `ContextDetailsResponse`

Returned by `GET /context/{contextId}`.

```json
{
  "contextId": "string",
  "name": "string",
  "description": "string",
  "parameters": "object", // Key-value pairs defining the context.
  "createdAt": "string",  // ISO 8601 timestamp.
  "updatedAt": "string"   // ISO 8601 timestamp.
}
```

#### `PromptGenerationResponse`

Returned by `POST /prompts/generate`.

```json
{
  "generatedPrompt": "string", // The generated prompt text.
  "promptId": "string",        // Optional. Unique ID for tracking/versioning generated prompts.
  "metadata": "object"         // Optional. Additional metadata about the prompt (e.g., associated ERD principles, source data).
}
```

#### `PromptEvaluationResponse`

Returned by `POST /prompts/evaluate`.

```json
{
  "message": "string" // Confirmation message.
}
```



