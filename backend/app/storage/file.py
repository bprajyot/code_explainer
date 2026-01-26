import os
import uuid
from pathlib import Path
from ..config import get_settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class FileStorage:
    def __init__(self):
        logger.info("Initializing FileStorage")
        self.settings = get_settings()
        self.output_dir = Path(self.settings.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)
        logger.debug(f"Output directory: {self.output_dir}")
    
    def save_pdf(self, content: str, filename: str) -> tuple[str, str]:
        """Save PDF report and return (file_id, filepath)"""
        file_id = str(uuid.uuid4())
        filepath = self.output_dir / "reports" / f"report_{file_id}_{filename}.html"
        
        logger.info(f"Saving PDF report: {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.debug(f"PDF saved successfully. Size: {len(content)} bytes")
        return file_id, str(filepath)
    
    def get_pdf_path(self, file_id: str) -> str:
        """Get PDF file path by ID"""
        logger.debug(f"Looking for PDF with ID: {file_id}")
        for file in (self.output_dir / "reports").glob(f"report_{file_id}_*"):
            logger.debug(f"Found: {file}")
            return str(file)
        logger.warning(f"PDF not found for ID: {file_id}")
        return ""