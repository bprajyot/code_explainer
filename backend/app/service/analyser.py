# ==========================================
# BACKEND - backend/app/services/analyzer.py
# ==========================================
import ast
from .parser import CodeParser
from .error import ErrorDetector
from .diagram import DiagramGenerator
from .ai import AIService
from ..models.schemas import CodeAnalysisResponse
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class CodeAnalyzer:
    def __init__(self):
        logger.info("Initializing CodeAnalyzer")
        self.ai_service = AIService()
    
    async def analyze(self, code: str, filename: str) -> CodeAnalysisResponse:
        """Main analysis pipeline"""
        logger.info(f"Starting analysis for file: {filename}")
        
        # Parse code
        parser = CodeParser(code)
        tree = parser.parse()
        
        # Extract structure
        imports = parser.extract_imports()
        variables = parser.extract_variables()
        functions = parser.extract_functions()
        classes = parser.extract_classes()
        
        # Detect errors
        error_detector = ErrorDetector(code)
        errors = error_detector.detect_errors()
        
        # Generate diagrams
        diagrams = {}
        if tree:
            diagram_gen = DiagramGenerator(code, tree)
            diagrams = diagram_gen.generate_all_diagrams()
        
        # AI explanations
        structure_info = {
            "functions": functions,
            "classes": classes,
            "imports": imports
        }
        
        logger.info("Generating AI explanations")
        overview = await self.ai_service.generate_overview(code, structure_info)
        detailed_overview = await self.ai_service.generate_detailed_overview(code, structure_info)
        
        # Explain functions
        for func in functions:
            func_code = self._extract_function_code(code, func.line_number)
            func.logic_explanation = await self.ai_service.explain_function(func, func_code)
        
        # Explain classes
        for cls in classes:
            class_code = self._extract_class_code(code, cls.line_number)
            cls.detailed_explanation = await self.ai_service.explain_class(cls, class_code)
        
        # Explain imports
        for imp in imports:
            imp.purpose = await self.ai_service.explain_import(imp)
        
        # Generate suggestions
        suggestions = await self.ai_service.generate_suggestions(code, errors)
        
        logger.info("Analysis complete")
        
        return CodeAnalysisResponse(
            overview=overview,
            detailed_overview=detailed_overview,
            variables=variables,
            functions=functions,
            classes=classes,
            imports=imports,
            errors=errors,
            suggestions=suggestions,
            diagrams=diagrams,
            markdown_content="",
            pdf_content=None,
            file_id=""
        )
    
    def _extract_function_code(self, code: str, start_line: int) -> str:
        """Extract function code snippet"""
        lines = code.split('\n')
        # Get 10 lines starting from function definition
        end_line = min(start_line + 9, len(lines))
        return '\n'.join(lines[start_line-1:end_line])
    
    def _extract_class_code(self, code: str, start_line: int) -> str:
        """Extract class code snippet"""
        lines = code.split('\n')
        # Get 15 lines starting from class definition
        end_line = min(start_line + 14, len(lines))
        return '\n'.join(lines[start_line-1:end_line])