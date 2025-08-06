# Cline AI Service API Specification (Revised)

## 1. Introduction

This document defines the Application Programming Interface (API) for the Cline AI Service. The Cline AI Service is designed to provide core AI functionalities, including pattern recognition, context management, and prompt generation, to various components within the Recovery Compass ecosystem. This API will serve as the central interface for integrating Cline AI capabilities into frontend applications, automated agents (like Manus and Perplexity MCP), and developer tooling, ensuring adherence to Gold-Plated IPE standards and maximizing strategic force multiplication. This revision incorporates insights from recent strategic guidance, emphasizing the shift from isolated actions to systemic, environment-shaping solutions and the transformation of issues into opportunities for compounding value.

## 2. API Endpoints

This section details the various API endpoints, their functionalities, and their respective HTTP methods, now with an enhanced focus on systemic integration and force multiplication.

### 2.1 Pattern Recognition Endpoints

#### `POST /patterns/recognize`

*   **Description:** Analyzes input data (text, images, structured data) to identify predefined or emerging patterns relevant to Recovery Compass objectives and ERD principles. This endpoint is crucial for the "Insight Catalyst" and for feeding into Pattern Registry 2.0, now explicitly supporting the identification of systemic weaknesses and opportunities for strategic solutions (GuidanceInsightsAttach.md).
*   **Request Body:**
    ```json
    {
      "dataType": "string", // e.g., "text", "image", "structured", "code_repository_snapshot"
      "data": "any",        // The actual data to analyze. Can include codebases for identifying documentation sprawl or script duplication.
      "contextId": "string", // Optional: ID of a context to apply during recognition.
      "analysisType": "string" // Optional: e.g., "ERD_compliance", "systemic_weakness_identification", "workflow_optimization"
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
          "details": "object",   // Specific details about the recognized pattern, including identified systemic issues or opportunities.
          "strategicRecommendation": "string" // New: Recommended strategic action based on the pattern (e.g., "Implement Unified Automation Framework").
        }
      ],
      "analysisSummary": "string", // Human-readable summary of the recognition and strategic implications.
      "forceMultiplicationPotential": "number" // New: Quantifiable potential for force multiplication (e.g., estimated cost savings, efficiency gain).
    }
    ```

#### `GET /patterns/{patternId}`

*   **Description:** Retrieves detailed information about a specific recognized pattern, including its strategic implications and force multiplication potential.
*   **Parameters:**
    *   `patternId` (path): The unique identifier of the pattern.
*   **Response Body:** (Details of a `Pattern` object, now including `strategicRecommendation` and `forceMultiplicationPotential`)

### 2.2 Context Management Endpoints

#### `POST /context/create`

*   **Description:** Creates a new operational or user-specific context for Cline AI. This context can influence pattern recognition, prompt generation, and overall AI behavior, aligning with the "Actualization Map" concept and now supporting the definition of systemic environments for environment-shaping solutions (GuidanceInsightsAttach.md).
*   **Request Body:**
    ```json
    {
      "name": "string",
      "description": "string",
      "parameters": "object", // Key-value pairs defining the context (e.g., user preferences, B2B client profile, ERD-specific parameters, organizational structure, existing toolchains).
      "environmentDefinition": "object" // New: Structured definition of the environment for systemic analysis.
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

*   **Description:** Updates an existing context, allowing for dynamic adjustments to environmental definitions and strategic parameters.
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

*   **Description:** Retrieves the details of a specific context, including its environmental definition.
*   **Parameters:**
    *   `contextId` (path): The unique identifier of the context.
*   **Response Body:** (Details of a `Context` object, now including `environmentDefinition`)

### 2.3 Prompt Generation Endpoints

#### `POST /prompts/generate`

*   **Description:** Generates dynamic, context-aware prompts for various applications, including adaptive question flows, personalized insights, and funder narratives. This endpoint is central to the "Adaptive Question Engine" and "Story-Mode Snippet Generator," now capable of generating prompts for strategic solutions and systematic documentation (GuidanceInsightsAttach.md).
*   **Request Body:**
    ```json
    {
      "promptType": "string", // e.g., "question", "insight", "narrative", "strategic_action_plan", "documentation_guidance"
      "contextId": "string",  // Optional: Context to inform prompt generation.
      "parameters": "object",  // Specific parameters for prompt generation (e.g., user journey data, target audience, ERD principles, identified patterns, strategic recommendations).
      "targetOutcome": "string" // New: Desired outcome for the generated prompt (e.g., "user engagement", "system optimization", "funder narrative").
    }
    ```
*   **Response Body:**
    ```json
    {
      "generatedPrompt": "string",
      "promptId": "string", // Optional: ID for tracking/versioning generated prompts.
      "metadata": "object" // Additional metadata about the prompt (e.g., associated ERD principles, source data, strategic alignment).
    }
    ```

#### `POST /prompts/evaluate`

*   **Description:** Evaluates the effectiveness or relevance of a generated prompt based on user interaction or predefined criteria. This supports continuous optimization and feedback loops for strategic prompt generation.
*   **Request Body:**
    ```json
    {
      "promptId": "string",
      "evaluationMetric": "string", // e.g., "engagement", "relevance", "conversion", "strategic_impact"
      "value": "number"           // The measured value for the metric.
    }
    ```
*   **Response Body:**
    ```json
    {
      "message": "Prompt evaluation recorded."
    }
    ```

## 3. Data Models (Revised)

This section defines the data structures (request and response payloads) used across the API, updated to reflect the enhanced capabilities for systemic analysis and strategic output.

### 3.1 Request Models

#### `PatternRecognitionRequest` (Revised)

Used by `POST /patterns/recognize`.

```json
{
  "dataType": "string", // Required. Type of data: "text", "image", "structured", "code_repository_snapshot", etc.
  "data": "any",        // Required. The actual data payload. Format depends on `dataType`.
  "contextId": "string", // Optional. ID of a context to apply during recognition.
  "analysisType": "string" // Optional. New: e.g., "ERD_compliance", "systemic_weakness_identification", "workflow_optimization", "script_duplication_analysis"
}
```

#### `ContextCreationRequest` (Revised)

Used by `POST /context/create`.

```json
{
  "name": "string",        // Required. Human-readable name for the context.
  "description": "string",   // Optional. Description of the context.
  "parameters": "object",   // Required. Key-value pairs defining the context (e.g., user preferences, B2B client profile, ERD-specific parameters, organizational structure, existing toolchains).
  "environmentDefinition": "object" // New: Structured definition of the environment for systemic analysis (e.g., { "toolchains": ["git", "CI/CD"], "documentation_systems": ["Confluence", "Markdown_repos"] }).
}
```

#### `ContextUpdateRequest` (Revised)

Used by `PUT /context/{contextId}`.

```json
{
  "name": "string",        // Optional. Human-readable name for the context.
  "description": "string",   // Optional. Description of the context.
  "parameters": "object",   // Optional. Key-value pairs defining the context. Merges with existing parameters.
  "environmentDefinition": "object" // Optional. Structured definition of the environment for systemic analysis.
}
```

#### `PromptGenerationRequest` (Revised)

Used by `POST /prompts/generate`.

```json
{
  "promptType": "string", // Required. Type of prompt to generate: "question", "insight", "narrative", "strategic_action_plan", "documentation_guidance", etc.
  "contextId": "string",  // Optional. Context ID to inform prompt generation.
  "parameters": "object",  // Required. Specific parameters for prompt generation (e.g., user journey data, target audience, ERD principles, identified patterns, strategic recommendations).
  "targetOutcome": "string" // New: Desired outcome for the generated prompt (e.g., "user engagement", "system optimization", "funder narrative", "CI/CD cost reduction").
}
```

#### `PromptEvaluationRequest` (No Change)

Used by `POST /prompts/evaluate`.

```json
{
  "promptId": "string",         // Required. ID of the prompt being evaluated.
  "evaluationMetric": "string", // Required. Metric for evaluation: "engagement", "relevance", "conversion", "strategic_impact", etc.
  "value": "number"             // Required. The measured value for the metric.
}
```

### 3.2 Response Models (Revised)

#### `PatternRecognitionResponse` (Revised)

Returned by `POST /patterns/recognize`.

```json
{
  "patterns": [
    {
      "id": "string",           // Unique ID of the recognized pattern.
      "name": "string",         // Human-readable name of the pattern.
      "confidence": "number",   // Confidence score (0.0 - 1.0).
      "details": "object",       // Specific details about the recognized pattern, e.g., matched ERD principles, archetypes, identified systemic issues (e.g., "documentation_sprawl", "script_duplication").
      "strategicRecommendation": "string" // New: Recommended strategic action based on the pattern (e.g., "Implement Unified Automation Framework", "Create Living Knowledge System").
    }
  ],
  "analysisSummary": "string", // Human-readable summary of the recognition process and findings.
  "forceMultiplicationPotential": "number" // New: Quantifiable potential for force multiplication (e.g., estimated cost savings, efficiency gain, e.g., 0.70 for 70% reduction).
}
```

#### `ContextCreationResponse` (No Change)

Returned by `POST /context/create`.

```json
{
  "contextId": "string", // Unique ID of the newly created context.
  "message": "string"    // Confirmation message.
}
```

#### `ContextUpdateResponse` (No Change)

Returned by `PUT /context/{contextId}`.

```json
{
  "contextId": "string", // Unique ID of the updated context.
  "message": "string"    // Confirmation message.
}
```

#### `ContextDetailsResponse` (Revised)

Returned by `GET /context/{contextId}`.

```json
{
  "contextId": "string",
  "name": "string",
  "description": "string",
  "parameters": "object", // Key-value pairs defining the context.
  "environmentDefinition": "object", // New: Structured definition of the environment.
  "createdAt": "string",  // ISO 8601 timestamp.
  "updatedAt": "string"   // ISO 8601 timestamp.
}
```

#### `PromptGenerationResponse` (Revised)

Returned by `POST /prompts/generate`.

```json
{
  "generatedPrompt": "string", // The generated prompt text.
  "promptId": "string",        // Optional. Unique ID for tracking/versioning generated prompts.
  "metadata": "object",         // Optional. Additional metadata about the prompt (e.g., associated ERD principles, source data, strategic alignment, target outcome).
  "strategicAlignmentScore": "number" // New: Score indicating alignment with strategic objectives (0.0 - 1.0).
}
```

#### `PromptEvaluationResponse` (No Change)

Returned by `POST /prompts/evaluate`.

```json
{
  "message": "string" // Confirmation message.
}
```

## 4. Authentication and Authorization

(No Change from previous version)

## 5. Error Handling

(No Change from previous version)

## 6. Versioning

(No Change from previous version)

## 7. Rate Limiting

(No Change from previous version)

## 8. Examples

(No Change from previous version)



