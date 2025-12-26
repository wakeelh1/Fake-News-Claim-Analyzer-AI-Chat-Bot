from typing import Union
from fastapi import APIRouter
from app.models.requestModels import ClaimAnalysisRequest
from app.models.responseModels import ClaimAnalysisResponse, ErrorResponse
from app.services.analyzer import ClaimAnalyzer


# Create router for API endpoints
router = APIRouter(prefix="/api/v1", tags=["claims"])


# Initialize analyzer once when module loads
analyzer = ClaimAnalyzer()


@router.post(
    "/analyze-claim",
    response_model=Union[ClaimAnalysisResponse, ErrorResponse],
    summary="Analyze a news claim",
    description="Takes a news claim as input and returns classification (likely true/false/uncertain) with confidence and explanation."
)
async def analyze_claim(request: ClaimAnalysisRequest) -> Union[ClaimAnalysisResponse, ErrorResponse]:
    """
    POST endpoint to analyze a news claim.
    
    - **claim**: The news claim to analyze (5-500 characters)
    """
    # Analyze the claim using the analyzer service
    result = analyzer.analyze(request.claim)
    
    # Return either ClaimAnalysisResponse or ErrorResponse; FastAPI
    # will validate against the Union response_model.
    return result
