from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import config
from app.api import api_routes

# Create FastAPI application instance
app = FastAPI(
    title=config.API_TITLE,
    version=config.API_VERSION,
    description=config.API_DESCRIPTION,
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc"  # ReDoc at /redoc
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_routes.router)

@app.get("/")
async def root():
    """
    Root endpoint - provides API information.
    """
    return {
        "message": "Fake News Claim Analyzer API",
        "version": config.API_VERSION,
        "docs": "Visit /docs for interactive API documentation"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": config.API_TITLE
    }

if __name__ == "__main__":
    import uvicorn
    
    # Run the server with hot-reload disabled for production
    uvicorn.run(
        "app.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True  # Set to False in production
    )
