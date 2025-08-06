from pydantic import BaseModel, Field
from typing import Any, List, Optional, Dict
from typing_extensions import Annotated # For Python < 3.9, use typing_extensions

class Pattern(BaseModel):
    id: Annotated[str, Field(pattern="^pat-[0-9a-f]{8}$")]
    name: str
    confidence: float
    details: Any
    strategicRecommendation: Optional[str] = None

class PatternRecognitionResponse(BaseModel):
    patterns: List[Pattern]
    analysisSummary: str
    forceMultiplicationPotential: Optional[float] = None

class PatternRecognitionRequest(BaseModel):
    dataType: str
    data: Any
    contextId: Optional[str] = None
    analysisType: Optional[str] = None





class EnvironmentDefinition(BaseModel):
    toolchains: Optional[List[str]] = None
    documentation_systems: Optional[List[str]] = None
    communication_platforms: Optional[List[str]] = None
    data_storage_solutions: Optional[List[str]] = None
    cloud_providers: Optional[List[str]] = None
    custom_attributes: Optional[Any] = None

class ContextCreationRequest(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] # Changed from Any to Dict[str, Any]
    environmentDefinition: Optional[EnvironmentDefinition] = None

class ContextCreationResponse(BaseModel):
    contextId: str
    status: str
    message: str

class ContextUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None # Changed from Any to Optional[Dict[str, Any]]
    environmentDefinition: Optional[EnvironmentDefinition] = None

class ContextUpdateResponse(BaseModel):
    contextId: str
    status: str
    message: str

class ContextDetailsResponse(BaseModel):
    contextId: str
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] # Changed from Any to Dict[str, Any]
    environmentDefinition: Optional[EnvironmentDefinition] = None
    createdAt: str
    updatedAt: str


