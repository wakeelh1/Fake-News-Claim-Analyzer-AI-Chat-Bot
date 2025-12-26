from pydantic import BaseModel, Field
from typing import Optional

class ClaimAnalysisResponse(BaseModel):
    """
    Response schema for successful claim analysis.
    Returned when the analysis completes without errors.
    """
    claim: str = Field(
        ...,
        description="The original claim that was analyzed"
    )
    classification: str = Field(
        ...,
        description="The predicted classification",
        example="true"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )
    explanation: str = Field(
        ...,
        description="Human-readable explanation of the classification"
    )

class ErrorResponse(BaseModel):
    """
    Response schema for error cases.
    Returned when the analysis fails for any reason.
    """
    error: str = Field(
        ...,
        description="Error type or category"
    )
    message: str = Field(
        ...,
        description="Detailed error message"
    )
    status_code: int = Field(
        ...,
        description="HTTP status code"
    )
