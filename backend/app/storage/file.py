import os
import uuid
from pathlib import Path
from ..config import get_settings

class FileStorage:
    def __init__(self):
        self.settings = get_settings()
        self.output_dir = Path(self.settings.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "markdown").mkdir(exist_ok=True)
        (self.output_dir / "pdf").mkdir(exist_ok=True)
    
    def save_markdown(self, content: str, filename: str) -> tuple[str, str]:
        """Save Markdown file and return (file_id, filepath)"""
        file_id = str(uuid.uuid4())
        filepath = self.output_dir / "markdown" / f"{file_id}_{filename}.md"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_id, str(filepath)
    
    def save_pdf(self, content: str, filename: str, file_id: str) -> str:
        """Save HTML file (can be saved as PDF) and return filepath"""
        filepath = self.output_dir / "pdf" / f"{file_id}_{filename}.html"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def get_markdown_path(self, file_id: str) -> str:
        """Get markdown file path by ID"""
        for file in (self.output_dir / "markdown").glob(f"{file_id}_*"):
            return str(file)
        return ""
    
    def get_pdf_path(self, file_id: str) -> str:
        """Get PDF/HTML file path by ID"""
        for file in (self.output_dir / "pdf").glob(f"{file_id}_*"):
            return str(file)
        return ""