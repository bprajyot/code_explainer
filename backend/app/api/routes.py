from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse, Response
from ..models.schemas import CodeAnalysisResponse
from ..service.analyser import CodeAnalyzer
from ..storage.pdf import PDFGenerator
from ..storage.file import FileStorage
from ..utils.logger import setup_logger
import json

router = APIRouter()
logger = setup_logger(__name__)

@router.post("/analyze")
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
        
        # Generate PDF report
        pdf_generator = PDFGenerator()
        pdf_html = pdf_generator.generate_formal_report(analysis, filename, code)
        
        # Save PDF
        storage = FileStorage()
        file_id, pdf_path = storage.save_pdf(pdf_html, filename)
        
        # Build response
        response_dict = {
            "overview": analysis.overview,
            "detailed_overview": analysis.detailed_overview,
            "variables": [
                {
                    "name": v.name,
                    "type": v.type,
                    "scope": v.scope,
                    "line_number": v.line_number,
                    "occurrences": v.occurrences
                }
                for v in analysis.variables
            ],
            "functions": [
                {
                    "name": f.name,
                    "parameters": f.parameters,
                    "return_type": f.return_type,
                    "docstring": f.docstring,
                    "line_number": f.line_number,
                    "logic_explanation": f.logic_explanation,
                    "variables_used": f.variables_used,
                    "occurrences": f.occurrences
                }
                for f in analysis.functions
            ],
            "classes": [
                {
                    "name": c.name,
                    "methods": c.methods,
                    "attributes": c.attributes,
                    "base_classes": c.base_classes,
                    "docstring": c.docstring,
                    "line_number": c.line_number,
                    "detailed_explanation": c.detailed_explanation,
                    "method_explanations": c.method_explanations
                }
                for c in analysis.classes
            ],
            "imports": [
                {
                    "module": i.module,
                    "names": i.names,
                    "line_number": i.line_number,
                    "purpose": i.purpose
                }
                for i in analysis.imports
            ],
            "errors": [
                {
                    "severity": e.severity,
                    "message": e.message,
                    "line_number": e.line_number,
                    "category": e.category
                }
                for e in analysis.errors
            ],
            "suggestions": [
                {
                    "category": s.category,
                    "title": s.title,
                    "description": s.description,
                    "code_example": s.code_example,
                    "priority": s.priority
                }
                for s in analysis.suggestions
            ],
            "file_id": file_id,
            "pdf_ready": True
        }
        
        logger.info(f"Analysis complete. File ID: {file_id}")
        return JSONResponse(content=response_dict)
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/download/pdf/{file_id}")
async def download_pdf(file_id: str):
    """Download professional PDF report"""
    logger.info(f"PDF download request for: {file_id}")
    
    storage = FileStorage()
    filepath = storage.get_pdf_path(file_id)
    
    if not filepath:
        logger.warning(f"PDF not found: {file_id}")
        raise HTTPException(status_code=404, detail="Report not found")
    
    logger.info(f"Serving PDF: {filepath}")
    return FileResponse(
        filepath,
        media_type="text/html",
        filename=f"code_analysis_report_{file_id}.html",
        headers={
            "Content-Disposition": f"attachment; filename=code_analysis_report_{file_id}.html"
        }
    )