# ==========================================
# BACKEND - backend/app/api/routes.py
# ==========================================
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from ..models.schemas import CodeAnalysisResponse
from ..service.analyser import CodeAnalyzer
from ..storage.markdown import MarkdownGenerator
from ..storage.pdf import PDFGenerator
from ..storage.file import FileStorage

router = APIRouter()

@router.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(file: UploadFile = File(...)):
    """Analyze Python code file"""
    content = await file.read()
    code = content.decode('utf-8')
    filename = file.filename
    
    analyzer = CodeAnalyzer()
    analysis = await analyzer.analyze(code, filename)
    
    md_generator = MarkdownGenerator()
    markdown_content = md_generator.generate(analysis, filename, code)
    
    pdf_generator = PDFGenerator()
    pdf_content = pdf_generator.generate(markdown_content)
    
    storage = FileStorage()
    file_id, md_path = storage.save_markdown(markdown_content, filename)
    pdf_path = storage.save_pdf(pdf_content, filename, file_id)
    
    analysis.markdown_content = markdown_content
    analysis.pdf_content = pdf_content
    analysis.file_id = file_id
    
    return analysis

@router.get("/download/markdown/{file_id}")
async def download_markdown(file_id: str):
    """Download Markdown file"""
    storage = FileStorage()
    filepath = storage.get_markdown_path(file_id)
    
    if not filepath:
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        filepath,
        media_type="text/markdown",
        filename=f"analysis_{file_id}.md"
    )

@router.get("/download/pdf/{file_id}")
async def download_pdf(file_id: str):
    """Download HTML file (can be saved as PDF)"""
    storage = FileStorage()
    filepath = storage.get_pdf_path(file_id)
    
    if not filepath:
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        filepath,
        media_type="text/html",
        filename=f"analysis_{file_id}.html"
    )