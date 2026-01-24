# ==========================================
# BACKEND - backend/app/main.py
# ==========================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api.routes import router
from .config import get_settings
from .utils.logger import setup_logger
from pathlib import Path

settings = get_settings()
logger = setup_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Python code explanation system with comprehensive analysis",
    version="2.0.0"
)

logger.info("Starting Python Code Explainer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount output directory
output_path = Path(settings.OUTPUT_DIR)
output_path.mkdir(exist_ok=True)
app.mount("/files", StaticFiles(directory=str(output_path)), name="files")

app.include_router(router, prefix="/api", tags=["analysis"])

@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {
        "message": "Python Code Explainer API", 
        "status": "running",
        "version": "2.0.0"
    }

@app.get("/health")
async def health():
    logger.debug("Health check endpoint accessed")
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete")
    logger.info(f"Output directory: {settings.OUTPUT_DIR}")
    logger.info(f"Ollama URL: {settings.OLLAMA_BASE_URL}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")