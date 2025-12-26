from pydantic import BaseModel, Field

class ClaimAnalysisRequest(BaseModel):
    """
    Request schema for claim analysis endpoint.
    Pydantic validates input automatically and generates Swagger docs.
    """
    claim: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="The news claim to analyze (5-500 characters)",
        example="The Earth is flat"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "claim": "Global temperatures have risen by 1.1 degrees Celsius since pre-industrial times."
            }
        }
