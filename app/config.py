
# from logging import config
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Hugging Face Configuration
HF_MODEL_ID = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
# HF_MODEL_ID = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL_ID}"

# HF_MODEL_ID = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
# HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"

# API Configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))
API_TITLE = "Fake News Claim Analyzer"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Analyzes news claims and classifies them as likely true, false, or uncertain"

# Model Configuration
MODEL_TIMEOUT = 30  # seconds for API calls
MAX_CLAIM_LENGTH = 500  # maximum characters for a claim
