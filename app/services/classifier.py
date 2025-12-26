import requests
from typing import Dict, Any
from app import config
from app.models.responseModels import ErrorResponse

class HuggingFaceClassifier:
    """
    Handles communication with Hugging Face Inference API.
    Encapsulates all API logic and error handling.
    """
    
    def __init__(self):
        """Initialize classifier with API credentials and headers."""
        self.api_url = config.HF_API_URL
        self.headers = {
            "Authorization": f"Bearer {config.HF_API_TOKEN}"
        }
        self.timeout = config.MODEL_TIMEOUT
    
    def classify(self, text: str) -> Dict[str, Any]:
        """
        Send text to Hugging Face API and get classification.
        
        Args:
            text: The text to classify
            
        Returns:
            Dict with API response or error information
        """
        payload = {
            "inputs": text
        }
        
        try:
            # Make HTTP POST request to Hugging Face Inference API
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            
            # Handle various HTTP error statuses
            if response.status_code == 503:
                # Model loading or temporarily unavailable
                return {
                    "error": "model_unavailable",
                    "message": "The model is temporarily unavailable. Please try again in a few moments.",
                    "status_code": 503
                }
            elif response.status_code == 500:
                # Server error at Hugging Face
                return {
                    "error": "server_error",
                    "message": "Hugging Face server encountered an error. Please try again later.",
                    "status_code": 500
                }
            elif response.status_code == 429:
                # Rate limited - too many requests
                return {
                    "error": "rate_limited",
                    "message": "Too many requests. Please wait a moment and try again.",
                    "status_code": 429
                }
            elif response.status_code == 401:
                # Invalid API token
                return {
                    "error": "authentication_failed",
                    "message": "Invalid or expired API token.",
                    "status_code": 401
                }
            elif response.status_code == 400:
                # Bad request - input validation error
                return {
                    "error": "bad_request",
                    "message": f"Invalid input: {response.text}",
                    "status_code": 400
                }
            elif not response.ok:
                # Any other HTTP error
                return {
                    "error": "http_error",
                    "message": f"Hugging Face API returned status {response.status_code}",
                    "status_code": response.status_code
                }
            
            # Successful response - parse and return JSON
            return response.json()
            
        except requests.exceptions.Timeout:
            # Request took too long
            return {
                "error": "timeout",
                "message": f"Request to Hugging Face API timed out after {self.timeout} seconds.",
                "status_code": 504
            }
        except requests.exceptions.ConnectionError:
            # Network error - can't connect to API
            return {
                "error": "connection_error",
                "message": "Failed to connect to Hugging Face API. Check your internet connection.",
                "status_code": 503
            }
        except Exception as e:
            # Unexpected error
            return {
                "error": "unexpected_error",
                "message": f"An unexpected error occurred: {str(e)}",
                "status_code": 500
            }
