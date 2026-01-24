# ==========================================
# BACKEND - backend/app/services/diagram_generator.py
# ==========================================
import ast
from typing import Dict

class DiagramGenerator:
    def __init__(self, code: str, tree: ast.AST):
        self.code = code
        self.tree = tree
    
    def generate_all_diagrams(self) -> Dict[str, str]:
        diagrams = {
            "flowchart": self.generate_flowchart(),
            "sequence": self.generate_sequence_diagram(),
        }
        
        class_diagram = self.generate_class_diagram()
        if class_diagram:
            diagrams["class"] = class_diagram
        
        return diagrams
    
    def generate_flowchart(self) -> str:
        mermaid = ["flowchart TD"]
        mermaid.append("    Start([Start]) --> Init[Initialize Variables]")
        
        node_counter = [0]
        
        def get_node_id():
            node_counter[0] += 1
            return f"N{node_counter[0]}"
        
        prev_node = "Init"
        
        for node in self.tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_node = get_node_id()
                mermaid.append(f"    {prev_node} --> {func_node}[Function: {node.name}]")
                prev_node = func_node
            elif isinstance(node, ast.ClassDef):
                class_node = get_node_id()
                mermaid.append(f"    {prev_node} --> {class_node}[Class: {node.name}]")
                prev_node = class_node
            elif isinstance(node, ast.If):
                if_node = get_node_id()
                mermaid.append(f"    {prev_node} --> {if_node}{{Conditional Logic}}")
                prev_node = if_node
        
        mermaid.append(f"    {prev_node} --> End([End])")
        
        return "\n".join(mermaid)
    
    def generate_sequence_diagram(self) -> str:
        mermaid = ["sequenceDiagram"]
        mermaid.append("    participant Main")
        
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)
        
        for func in functions[:5]:
            mermaid.append(f"    participant {func}")
        
        mermaid.append("    Main->>Main: Initialize")
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    caller = "Main"
                    callee = node.func.id
                    if callee in functions:
                        mermaid.append(f"    {caller}->>{callee}: Call {callee}()")
                        mermaid.append(f"    {callee}-->>Main: Return")
        
        return "\n".join(mermaid)
    
    def generate_class_diagram(self) -> str:
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node)
        
        if not classes:
            return ""
        
        mermaid = ["classDiagram"]
        
        for cls in classes:
            methods = []
            attributes = []
            
            for item in cls.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append(item.name)
                elif isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            attributes.append(target.id)
            
            mermaid.append(f"    class {cls.name} {{")
            for attr in attributes:
                mermaid.append(f"        +{attr}")
            for method in methods:
                mermaid.append(f"        +{method}()")
            mermaid.append("    }")
            
            for base in cls.bases:
                if isinstance(base, ast.Name):
                    mermaid.append(f"    {base.id} <|-- {cls.name}")
        
        return "\n".join(mermaid)