# ==========================================
# BACKEND - backend/app/api/schemas.py
# ==========================================
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Variable(BaseModel):
    name: str
    type: Optional[str]
    scope: str
    line_number: int
    occurrences: List[int] = []  # Line numbers where variable is used

class Function(BaseModel):
    name: str
    parameters: List[str]
    return_type: Optional[str]
    docstring: Optional[str]
    line_number: int
    logic_explanation: str = ""  # Detailed explanation
    variables_used: List[str] = []  # Variables used in function
    occurrences: List[int] = []  # Where function is called

class Class(BaseModel):
    name: str
    methods: List[str]
    attributes: List[str]
    base_classes: List[str]
    docstring: Optional[str]
    line_number: int
    detailed_explanation: str = ""
    method_explanations: str=""

class Import(BaseModel):
    module: str
    names: List[str]
    line_number: int
    purpose: str = ""  # What this import does

class Error(BaseModel):
    severity: str
    message: str
    line_number: Optional[int]
    category: str

class Suggestion(BaseModel):
    category: str  # Performance, Security, Best Practice, etc.
    title: str
    description: str
    code_example: Optional[str] = None
    priority: str  # High, Medium, Low

class CodeAnalysisResponse(BaseModel):
    overview: str
    detailed_overview: str
    variables: List[Variable]
    functions: List[Function]
    classes: List[Class]
    imports: List[Import]
    errors: List[Error]
    suggestions: List[Suggestion]
    diagrams: Dict[str, str]
    markdown_content: str
    pdf_content: Optional[str]
    file_id: str