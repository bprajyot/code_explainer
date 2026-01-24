
# ==========================================
# BACKEND - backend/app/main.py
# ==========================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api.routes import router
from .config import get_settings
from pathlib import Path

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Python code explanation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount output directory for file downloads
output_path = Path(settings.OUTPUT_DIR)
output_path.mkdir(exist_ok=True)
app.mount("/files", StaticFiles(directory=str(output_path)), name="files")

app.include_router(router, prefix="/api", tags=["analysis"])

@app.get("/")
async def root():
    return {"message": "Python Code Explainer API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}