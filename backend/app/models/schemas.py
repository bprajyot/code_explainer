# ==========================================
# BACKEND - backend/app/api/schemas.py
# ==========================================
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CodeAnalysisRequest(BaseModel):
    code: str
    filename: str

class Variable(BaseModel):
    name: str
    type: Optional[str]
    scope: str
    line_number: int

class Function(BaseModel):
    name: str
    parameters: List[str]
    return_type: Optional[str]
    docstring: Optional[str]
    line_number: int

class Class(BaseModel):
    name: str
    methods: List[str]
    attributes: List[str]
    base_classes: List[str]
    docstring: Optional[str]
    line_number: int

class Import(BaseModel):
    module: str
    names: List[str]
    line_number: int

class Error(BaseModel):
    severity: str  # Critical, Warning, Info
    message: str
    line_number: Optional[int]
    category: str

class CodeAnalysisResponse(BaseModel):
    overview: str
    variables: List[Variable]
    functions: List[Function]
    classes: List[Class]
    imports: List[Import]
    errors: List[Error]
    diagrams: Dict[str, str]
    markdown_content: str
    pdf_content: Optional[str]
    file_id: str