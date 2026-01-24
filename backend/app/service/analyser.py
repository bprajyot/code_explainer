# ==========================================
# BACKEND - backend/app/services/analyzer.py
# ==========================================
from .parser import CodeParser
from .error import ErrorDetector
from .diagram import DiagramGenerator
from .ai import AIService
from ..models.schemas import CodeAnalysisResponse

class CodeAnalyzer:
    def __init__(self):
        self.ai_service = AIService()
    
    async def analyze(self, code: str, filename: str) -> CodeAnalysisResponse:
        parser = CodeParser(code)
        tree = parser.parse()
        
        imports = parser.extract_imports()
        variables = parser.extract_variables()
        functions = parser.extract_functions()
        classes = parser.extract_classes()
        
        error_detector = ErrorDetector(code)
        errors = error_detector.detect_errors()
        
        diagrams = {}
        if tree:
            diagram_gen = DiagramGenerator(code, tree)
            diagrams = diagram_gen.generate_all_diagrams()
        
        structure_info = {
            "functions": functions,
            "classes": classes,
            "imports": imports
        }
        overview = await self.ai_service.generate_overview(code, structure_info)
        
        return CodeAnalysisResponse(
            overview=overview,
            variables=variables,
            functions=functions,
            classes=classes,
            imports=imports,
            errors=errors,
            diagrams=diagrams,
            markdown_content="",
            pdf_content=None,
            file_id=""
        )