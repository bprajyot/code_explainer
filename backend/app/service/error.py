# ==========================================
# BACKEND - backend/app/services/error_detector.py
# ==========================================
import ast
from typing import List
from ..models.schemas import Error
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ErrorDetector:
    def __init__(self, code: str):
        logger.info("Initializing ErrorDetector")
        self.code = code
        self.lines = code.split('\n')
    
    def detect_errors(self) -> List[Error]:
        """Detect all errors and warnings in code"""
        logger.info("Starting error detection")
        errors = []
        
        try:
            ast.parse(self.code)
            logger.info("No syntax errors found")
        except SyntaxError as e:
            logger.error(f"Syntax error detected: {e.msg} at line {e.lineno}")
            errors.append(Error(
                severity="Critical",
                message=f"Syntax Error: {e.msg}",
                line_number=e.lineno,
                category="Syntax"
            ))
            return errors
        
        errors.extend(self._check_unused_imports())
        errors.extend(self._check_bad_practices())
        
        logger.info(f"Error detection complete. Found {len(errors)} issues")
        return errors
    
    def _check_unused_imports(self) -> List[Error]:
        """Check for unused imports"""
        logger.debug("Checking for unused imports")
        errors = []
        tree = ast.parse(self.code)
        
        imported_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_names.add(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_names.add(alias.asname or alias.name)
        
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
        
        unused = imported_names - used_names
        for name in unused:
            logger.debug(f"Unused import detected: {name}")
            errors.append(Error(
                severity="Warning",
                message=f"Unused import: {name}",
                line_number=None,
                category="Code Quality"
            ))
        
        return errors
    
    def _check_bad_practices(self) -> List[Error]:
        """Check for bad coding practices"""
        logger.debug("Checking for bad practices")
        errors = []
        tree = ast.parse(self.code)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    logger.debug(f"Bare except clause found at line {node.lineno}")
                    errors.append(Error(
                        severity="Warning",
                        message="Bare 'except:' clause - specify exception type",
                        line_number=node.lineno,
                        category="Best Practice"
                    ))
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        logger.debug(f"Mutable default argument in {node.name}")
                        errors.append(Error(
                            severity="Warning",
                            message=f"Mutable default argument in function '{node.name}'",
                            line_number=node.lineno,
                            category="Best Practice"
                        ))
        
        return errors