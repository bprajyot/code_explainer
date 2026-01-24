# ==========================================
# BACKEND - backend/app/services/parser.py
# ==========================================
import ast
from typing import List, Dict, Any, Optional
from ..models.schemas import Variable, Function, Class, Import
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class CodeParser:
    def __init__(self, code: str):
        logger.info("Initializing CodeParser")
        self.code = code
        self.tree = None
        
    def parse(self) -> Optional[ast.AST]:
        """Parse Python code into AST"""
        try:
            logger.debug(f"Parsing code of length {len(self.code)}")
            self.tree = ast.parse(self.code)
            logger.info("Code parsed successfully")
            return self.tree
        except SyntaxError as e:
            logger.error(f"Syntax error during parsing: {e.msg} at line {e.lineno}")
            return None
    
    def extract_imports(self) -> List[Import]:
        """Extract all imports from code"""
        if not self.tree:
            logger.warning("No AST available for import extraction")
            return []
        
        logger.info("Extracting imports")
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
        
        logger.info(f"Extracted {len(imports)} imports")
        return imports
    
    def extract_variables(self) -> List[Variable]:
        """Extract variables with their occurrences"""
        if not self.tree:
            logger.warning("No AST available for variable extraction")
            return []
        
        logger.info("Extracting variables")
        variables = []
        variable_occurrences = {}
        
        # Track all name usage
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name):
                if node.id not in variable_occurrences:
                    variable_occurrences[node.id] = []
                variable_occurrences[node.id].append(node.lineno)
        
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
                            line_number=node.lineno,
                            occurrences=variable_occurrences.get(target.id, [])
                        ))
        
        # Function variables
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
                                    line_number=stmt.lineno,
                                    occurrences=variable_occurrences.get(target.id, [])
                                ))
        
        logger.info(f"Extracted {len(variables)} variables")
        return variables
    
    def _infer_type(self, node) -> str:
        """Infer variable type from AST node"""
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
        """Extract functions with variables used"""
        if not self.tree:
            logger.warning("No AST available for function extraction")
            return []
        
        logger.info("Extracting functions")
        functions = []
        function_calls = {}
        
        # Track function calls
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name not in function_calls:
                        function_calls[func_name] = []
                    function_calls[func_name].append(node.lineno)
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not self._is_method(node):
                    params = [arg.arg for arg in node.args.args]
                    return_type = None
                    if node.returns:
                        return_type = ast.unparse(node.returns)
                    
                    # Extract variables used in function
                    variables_used = []
                    for inner_node in ast.walk(node):
                        if isinstance(inner_node, ast.Name):
                            if inner_node.id not in variables_used:
                                variables_used.append(inner_node.id)
                    
                    docstring = ast.get_docstring(node)
                    
                    functions.append(Function(
                        name=node.name,
                        parameters=params,
                        return_type=return_type,
                        docstring=docstring,
                        line_number=node.lineno,
                        variables_used=variables_used,
                        occurrences=function_calls.get(node.name, [])
                    ))
        
        logger.info(f"Extracted {len(functions)} functions")
        return functions
    
    def _is_method(self, node) -> bool:
        """Check if function is a class method"""
        for parent in ast.walk(self.tree):
            if isinstance(parent, ast.ClassDef):
                if node in parent.body:
                    return True
        return False
    
    def extract_classes(self) -> List[Class]:
        """Extract classes from code"""
        if not self.tree:
            logger.warning("No AST available for class extraction")
            return []
        
        logger.info("Extracting classes")
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
        
        logger.info(f"Extracted {len(classes)} classes")
        return classes