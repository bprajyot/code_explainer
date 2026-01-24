# ==========================================
# BACKEND - backend/app/services/parser.py
# ==========================================
import ast
from typing import List, Dict, Any, Optional
from ..models.schemas import Variable, Function, Class, Import

class CodeParser:
    def __init__(self, code: str):
        self.code = code
        self.tree = None
        
    def parse(self) -> Optional[ast.AST]:
        try:
            self.tree = ast.parse(self.code)
            return self.tree
        except SyntaxError as e:
            return None
    
    def extract_imports(self) -> List[Import]:
        if not self.tree:
            return []
        
        imports = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(Import(
                        module=alias.name,
                        names=[alias.asname or alias.name],
                        line_number=node.lineno
                    ))
            elif isinstance(node, ast.ImportFrom):
                names = [alias.name for alias in node.names]
                imports.append(Import(
                    module=node.module or "",
                    names=names,
                    line_number=node.lineno
                ))
        return imports
    
    def extract_variables(self) -> List[Variable]:
        if not self.tree:
            return []
        
        variables = []
        
        # Global variables
        for node in self.tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_type = self._infer_type(node.value)
                        variables.append(Variable(
                            name=target.id,
                            type=var_type,
                            scope="global",
                            line_number=node.lineno
                        ))
        
        # Function variables (significant ones)
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Name):
                                var_type = self._infer_type(stmt.value)
                                variables.append(Variable(
                                    name=target.id,
                                    type=var_type,
                                    scope=f"function:{node.name}",
                                    line_number=stmt.lineno
                                ))
        
        return variables
    
    def _infer_type(self, node) -> str:
        if isinstance(node, ast.Constant):
            return type(node.value).__name__
        elif isinstance(node, ast.List):
            return "list"
        elif isinstance(node, ast.Dict):
            return "dict"
        elif isinstance(node, ast.Set):
            return "set"
        elif isinstance(node, ast.Tuple):
            return "tuple"
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id
        return "unknown"
    
    def extract_functions(self) -> List[Function]:
        if not self.tree:
            return []
        
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not self._is_method(node):
                    params = [arg.arg for arg in node.args.args]
                    return_type = None
                    if node.returns:
                        return_type = ast.unparse(node.returns)
                    
                    docstring = ast.get_docstring(node)
                    
                    functions.append(Function(
                        name=node.name,
                        parameters=params,
                        return_type=return_type,
                        docstring=docstring,
                        line_number=node.lineno
                    ))
        
        return functions
    
    def _is_method(self, node) -> bool:
        for parent in ast.walk(self.tree):
            if isinstance(parent, ast.ClassDef):
                if node in parent.body:
                    return True
        return False
    
    def extract_classes(self) -> List[Class]:
        if not self.tree:
            return []
        
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                attributes = []
                
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(item.name)
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                attributes.append(target.id)
                
                base_classes = [ast.unparse(base) for base in node.bases]
                docstring = ast.get_docstring(node)
                
                classes.append(Class(
                    name=node.name,
                    methods=methods,
                    attributes=attributes,
                    base_classes=base_classes,
                    docstring=docstring,
                    line_number=node.lineno
                ))
        
        return classes