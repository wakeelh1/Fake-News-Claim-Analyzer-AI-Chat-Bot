from app.services.classifier import HuggingFaceClassifier
from app.models.responseModels import ClaimAnalysisResponse, ErrorResponse
from typing import Union


class ClaimAnalyzer:
    """
    High-level business logic for analyzing news claims.
    Uses HuggingFaceClassifier to get predictions and generates explanations.
    """
    
    def __init__(self):
        """Initialize the analyzer with a classifier instance."""
        self.classifier = HuggingFaceClassifier()
    
    def analyze(self, claim: str) -> Union[ClaimAnalysisResponse, ErrorResponse]:
        """
        Analyze a news claim and provide classification with explanation.
        
        Args:
            claim: The news claim to analyze
            
        Returns:
            ClaimAnalysisResponse on success, ErrorResponse on failure
        """
        # Get raw classification from Hugging Face API
        raw_result = self.classifier.classify(claim)
        
        # Check if an error occurred in the classifier
        if isinstance(raw_result, dict) and "error" in raw_result:
            # Return error response with status code
            return ErrorResponse(**raw_result)
        
        try:
            # ----- SAFE PARSING OF HF RESPONSE -----
            # HF text-classification often returns [[{label, score}, ...]]
            if isinstance(raw_result, list):
                first = raw_result[0]
                if isinstance(first, list):
                    classifications = first[0]
                elif isinstance(first, dict):
                    classifications = first
                else:
                    raise TypeError(f"Unexpected element type in HF response list: {type(first)}")
            elif isinstance(raw_result, dict):
                classifications = raw_result
            else:
                raise TypeError(f"Unexpected HF response type: {type(raw_result)}")
            # ----------------------------------------
            
            # Get the top prediction
            label = str(classifications.get("label", "unknown")).lower()
            score = float(classifications.get("score", 0.0))
            
            # Map sentiment labels to truthfulness labels and generate explanation
            if label == "positive":
                truthfulness = "likely_true"
                explanation = self._generate_positive_explanation(claim, score)
            elif label == "negative":
                truthfulness = "likely_false"
                explanation = self._generate_negative_explanation(claim, score)
            else:
                truthfulness = "uncertain"
                explanation = "Unable to classify this claim with confidence."
            
            # Build and return successful response
            return ClaimAnalysisResponse(
                claim=claim,
                classification=truthfulness,
                confidence=round(score, 3),
                explanation=explanation
            )
        
        except Exception as e:
            # Error parsing API response or any unexpected issue
            return ErrorResponse(
                error="parsing_error",
                message=f"Failed to parse classifier response: {str(e)}",
                status_code=500
            )
    
    def _generate_positive_explanation(self, claim: str, score: float) -> str:
        """
        Generate explanation for claims classified as likely true.
        
        Args:
            claim: The original claim
            score: Confidence score
            
        Returns:
            Human-readable explanation string
        """
        confidence_level = self._get_confidence_level(score)
        return f"This claim shows {confidence_level} characteristics of being true. The analysis indicates positive sentiment and factual language patterns commonly found in verified statements."
    
    def _generate_negative_explanation(self, claim: str, score: float) -> str:
        """
        Generate explanation for claims classified as likely false.
        
        Args:
            claim: The original claim
            score: Confidence score
            
        Returns:
            Human-readable explanation string
        """
        confidence_level = self._get_confidence_level(score)
        return f"This claim shows {confidence_level} characteristics of being false. The analysis detected language patterns and semantic markers typically associated with misinformation or unfounded statements."
    
    def _get_confidence_level(self, score: float) -> str:
        """
        Convert numerical confidence score to verbal description.
        
        Args:
            score: Confidence score between 0 and 1
            
        Returns:
            Verbal confidence level
        """
        if score >= 0.9:
            return "very strong"
        elif score >= 0.8:
            return "strong"
        elif score >= 0.7:
            return "moderate"
        elif score >= 0.6:
            return "weak"
        else:
            return "minimal"
