# ==========================================
# BACKEND - backend/app/services/error_detector.py
# ==========================================
import ast
from typing import List
from ..models.schemas import Error

class ErrorDetector:
    def __init__(self, code: str):
        self.code = code
        self.lines = code.split('\n')
    
    def detect_errors(self) -> List[Error]:
        errors = []
        
        # Syntax errors
        try:
            ast.parse(self.code)
        except SyntaxError as e:
            errors.append(Error(
                severity="Critical",
                message=f"Syntax Error: {e.msg}",
                line_number=e.lineno,
                category="Syntax"
            ))
            return errors
        
        errors.extend(self._check_unused_imports())
        errors.extend(self._check_bad_practices())
        
        return errors
    
    def _check_unused_imports(self) -> List[Error]:
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
            errors.append(Error(
                severity="Warning",
                message=f"Unused import: {name}",
                line_number=None,
                category="Code Quality"
            ))
        
        return errors
    
    def _check_bad_practices(self) -> List[Error]:
        errors = []
        tree = ast.parse(self.code)
        
        # Check for bare except
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    errors.append(Error(
                        severity="Warning",
                        message="Bare 'except:' clause - specify exception type",
                        line_number=node.lineno,
                        category="Best Practice"
                    ))
        
        # Check for mutable default arguments
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        errors.append(Error(
                            severity="Warning",
                            message=f"Mutable default argument in function '{node.name}'",
                            line_number=node.lineno,
                            category="Best Practice"
                        ))
        
        return errors