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
from ..utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

@router.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(file: UploadFile = File(...)):
    """Analyze Python code file"""
    logger.info(f"Received analysis request for file: {file.filename}")
    
    try:
        content = await file.read()
        code = content.decode('utf-8')
        filename = file.filename
        
        logger.info(f"File size: {len(code)} bytes")
        
        # Analyze
        analyzer = CodeAnalyzer()
        analysis = await analyzer.analyze(code, filename)
        
        # Generate documentation
        md_generator = MarkdownGenerator()
        markdown_content = md_generator.generate(analysis, filename, code)
        formal_report = md_generator.generate_formal_report(analysis, filename)
        
        pdf_generator = PDFGenerator()
        pdf_content = pdf_generator.generate(formal_report)
        
        # Save files
        storage = FileStorage()
        file_id, md_path = storage.save_markdown(markdown_content, filename)
        pdf_path = storage.save_pdf(pdf_content, filename, file_id)
        
        analysis.markdown_content = markdown_content
        analysis.pdf_content = pdf_content
        analysis.file_id = file_id
        
        logger.info(f"Analysis complete. File ID: {file_id}")
        return analysis
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/download/markdown/{file_id}")
async def download_markdown(file_id: str):
    """Download Markdown file"""
    logger.info(f"Download request for markdown: {file_id}")
    
    storage = FileStorage()
    filepath = storage.get_markdown_path(file_id)
    
    if not filepath:
        logger.warning(f"Markdown file not found: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")
    
    logger.info(f"Serving markdown file: {filepath}")
    return FileResponse(
        filepath,
        media_type="text/markdown",
        filename=f"analysis_{file_id}.md"
    )

@router.get("/download/pdf/{file_id}")
async def download_pdf(file_id: str):
    """Download HTML file"""
    logger.info(f"Download request for HTML: {file_id}")
    
    storage = FileStorage()
    filepath = storage.get_pdf_path(file_id)
    
    if not filepath:
        logger.warning(f"HTML file not found: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")
    
    logger.info(f"Serving HTML file: {filepath}")
    return FileResponse(
        filepath,
        media_type="text/html",
        filename=f"analysis_{file_id}.html"
    )