"""
Pydantic schemas for Cline AI Service
"""
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


# Environment Definition Schema
class EnvironmentDefinition(BaseModel):
    """Structured environment definition for systemic analysis"""
    toolchains: Optional[List[str]] = Field(
        None, description="Primary development and operational tools"
    )
    documentation_systems: Optional[List[str]] = Field(
        None, description="Knowledge management and documentation platforms"
    )
    communication_platforms: Optional[List[str]] = Field(
        None, description="Team communication tools"
    )
    data_storage_solutions: Optional[List[str]] = Field(
        None, description="Databases and storage services"
    )
    cloud_providers: Optional[List[str]] = Field(
        None, description="Cloud infrastructure providers"
    )
    custom_attributes: Optional[Dict[str, Any]] = Field(
        None, description="Flexible context-specific attributes"
    )


# Context Management Schemas
class ContextCreationRequest(BaseModel):
    """Request schema for creating a new context"""
    name: str = Field(..., description="Human-readable context name")
    description: Optional[str] = Field(None, description="Context description")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value pairs influencing AI behavior"
    )
    environment_definition: Optional[EnvironmentDefinition] = Field(
        None, description="Structured environment definition"
    )


class ContextCreationResponse(BaseModel):
    """Response schema for context creation"""
    context_id: str = Field(..., description="Unique context identifier")
    status: str = Field(..., description="Creation status")
    message: str = Field(..., description="Status message")


class ContextUpdateRequest(BaseModel):
    """Request schema for updating an existing context"""
    name: Optional[str] = Field(None, description="Updated context name")
    description: Optional[str] = Field(None, description="Updated description")
    parameters: Optional[Dict[str, Any]] = Field(
        None, description="Updated parameters"
    )
    environment_definition: Optional[EnvironmentDefinition] = Field(
        None, description="Updated environment definition"
    )


class ContextUpdateResponse(BaseModel):
    """Response schema for context update"""
    context_id: str = Field(..., description="Context identifier")
    status: str = Field(..., description="Update status")
    message: str = Field(..., description="Status message")


class ContextDetailsResponse(BaseModel):
    """Response schema for context details retrieval"""
    context_id: str = Field(..., description="Context identifier")
    name: str = Field(..., description="Context name")
    description: Optional[str] = Field(None, description="Context description")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Context parameters"
    )
    environment_definition: Optional[EnvironmentDefinition] = Field(
        None, description="Environment definition"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


# Pattern Analysis Schemas
class PatternAnalysisRequest(BaseModel):
    """Request schema for context-aware pattern analysis"""
    context_id: str = Field(
        ..., description="Context identifier for analysis"
    )
    text_input: Optional[str] = Field(
        None, description="Text content to analyze"
    )
    structured_data: Optional[str] = Field(
        None, description="Structured data"
    )
    structured_format: Optional[str] = Field(
        None, description="Data format"
    )


class ContextAnalysisMetrics(BaseModel):
    """Metrics showing context-specific analysis value"""
    applicability_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="How well patterns fit this context"
    )
    estimated_time_saved: int = Field(
        ..., ge=0,
        description="Minutes saved vs manual analysis"
    )
    automation_potential: float = Field(
        ..., ge=0.0, le=1.0,
        description="Percentage of recommendations automatable"
    )


class BaselineComparison(BaseModel):
    """Comparison metrics against baseline performance"""
    accuracy_improvement: float = Field(
        ..., ge=0.0,
        description="Accuracy improvement over baseline"
    )
    false_positive_reduction: float = Field(
        ..., ge=0.0,
        description="Reduction in false positives"
    )


class PatternAnalysisMetadata(BaseModel):
    """Enhanced metadata for pattern analysis"""
    input_types: List[str] = Field(..., description="Types of input processed")
    processing_time_ms: int = Field(
        ..., ge=0, description="Processing time in milliseconds"
    )
    ipe_compliance: bool = Field(
        ..., description="Gold-Plated IPE compliance status"
    )
    baseline_comparison: BaselineComparison = Field(
        ..., description="Performance vs baseline"
    )


class EnhancedPattern(BaseModel):
    """Pattern with context-aware enhancements"""
    id: str = Field(..., description="Pattern identifier")
    name: str = Field(..., description="Pattern name")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Base confidence score"
    )
    context_adjusted_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Context-adjusted confidence"
    )
    insights: str = Field(..., description="Pattern insights")
    recommendations: List[str] = Field(
        ..., description="Context-specific recommendations"
    )
    force_multiplication_score: int = Field(
        ..., ge=0, le=100, description="Force multiplication potential"
    )
    erd_alignment_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Alignment with ERD principles"
    )
    insurance_compliance_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Insurance documentation compliance"
    )
    implementation_time_estimate: int = Field(
        ..., ge=0,
        description="Estimated implementation time in hours"
    )

    @validator('id')
    def validate_id_format(cls, v):
        if not v.startswith('pat-'):
            raise ValueError('Pattern ID must start with "pat-"')
        return v


class PatternAnalysisResponse(BaseModel):
    """Response schema for context-aware pattern analysis"""
    patterns: List[EnhancedPattern] = Field(
        ..., description="Detected patterns with context enhancements"
    )
    context_analysis: ContextAnalysisMetrics = Field(
        ..., description="Context-specific analysis metrics"
    )
    meta: PatternAnalysisMetadata = Field(
        ..., description="Analysis metadata and performance metrics"
    )
    quantifiable_impact: Dict[str, Any] = Field(
        ..., description="Measurable impact on Recovery Compass operations"
    )
