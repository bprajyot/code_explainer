# ==========================================
# BACKEND - backend/app/services/ai_service.py (FIXED)
# ==========================================
import httpx
import asyncio
from typing import Dict, Any, List
from ..config import get_settings
from ..models.schemas import Function, Class, Import, Suggestion
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class AIService:
    def __init__(self):
        logger.info("Initializing AIService")
        self.settings = get_settings()
        self.base_url = self.settings.OLLAMA_BASE_URL
        self.model = self.settings.OLLAMA_MODEL
        
        # Configurable timeouts
        self.short_timeout = 45.0   # For simple tasks
        self.medium_timeout = 90.0  # For moderate complexity
        self.long_timeout = 180.0   # For complex analysis
    
    async def generate_overview(self, code: str, structure: Dict[str, Any]) -> str:
        """Generate brief overview"""
        logger.info("Generating code overview")
        prompt = f"""Analyze this Python code and provide a 2-3 paragraph overview.

Code snippet:
{code[:800]}...

Structure:
- Functions: {len(structure.get('functions', []))}
- Classes: {len(structure.get('classes', []))}
- Imports: {len(structure.get('imports', []))}

Explain what this code does and its main purpose. Keep it concise (max 200 words)."""

        return await self._call_ollama(prompt, timeout=self.short_timeout)
    
    async def explain_imports_batch(self, imports: List[Import]) -> List[Import]:
        """Explain all imports in ONE comprehensive call"""
        logger.info(f"Explaining {len(imports)} imports in single batch")
        
        if not imports:
            return imports
        
        # Create comprehensive prompt for ALL imports
        imports_list = "\n".join([
            f"{idx+1}. Module: {imp.module}\n   Imported: {', '.join(imp.names)}"
            for idx, imp in enumerate(imports)
        ])
        
        prompt = f"""Analyze these Python imports and provide detailed explanations for each.

IMPORTS TO ANALYZE:
{imports_list}

For EACH import, provide a detailed explanation (3-4 sentences) covering:
1. What the module/package does
2. Why these specific items are imported
3. Common use cases in Python development
4. How it fits into typical Python applications

Format your response EXACTLY as:
IMPORT 1: [Detailed explanation here]
IMPORT 2: [Detailed explanation here]
etc.

Keep each explanation detailed but concise (3-4 sentences)."""

        try:
            response = await self._call_ollama_with_limit(
                prompt,
                timeout=self.timeouts["long"],
                model=self.models["balanced"]
            )
            
            # Parse response
            lines = response.strip().split('\n')
            explanations = {}
            current_import_idx = None
            current_explanation = []
            
            for line in lines:
                if line.startswith('IMPORT '):
                    # Save previous explanation
                    if current_import_idx is not None and current_explanation:
                        explanations[current_import_idx] = ' '.join(current_explanation).strip()
                    
                    # Start new import
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        import_num = parts[0].replace('IMPORT', '').strip()
                        try:
                            current_import_idx = int(import_num) - 1
                            current_explanation = [parts[1].strip()]
                        except:
                            current_explanation.append(line)
                elif current_import_idx is not None:
                    current_explanation.append(line.strip())
            
            # Save last explanation
            if current_import_idx is not None and current_explanation:
                explanations[current_import_idx] = ' '.join(current_explanation).strip()
            
            # Assign explanations to imports
            for idx, imp in enumerate(imports):
                if idx in explanations:
                    imp.purpose = explanations[idx]
                else:
                    # Fallback
                    imp.purpose = f"The {imp.module} module provides {', '.join(imp.names)} for Python development. This is commonly used for its specialized functionality."
            
            logger.info(f"Successfully explained {len(explanations)} imports")
            return imports
            
        except Exception as e:
            logger.warning(f"Batch import explanation failed: {e}")
            # Fallback: basic explanations
            for imp in imports:
                imp.purpose = f"The {imp.module} module provides {', '.join(imp.names)}. This module offers specialized functionality commonly used in Python applications."
            return imports

    async def generate_detailed_overview(self, code: str, structure: Dict[str, Any]) -> str:
        """Generate comprehensive overview - MORE DETAILED"""
        logger.info("Generating detailed overview")
        
        prompt = f"""Provide a comprehensive professional analysis of this Python code (500-600 words).

CODE:
{code[:2000]}...

STRUCTURE:
- Functions: {len(structure.get('functions', []))}
- Classes: {len(structure.get('classes', []))}
- Imports: {len(structure.get('imports', []))}
- Total Lines: {len(code.split(chr(10)))}

PROVIDE DETAILED ANALYSIS INCLUDING:

1. PRIMARY PURPOSE (2-3 paragraphs):
   - What is the main goal of this code?
   - What problem does it solve?
   - What domain/area does it address?

2. ARCHITECTURE & DESIGN (2 paragraphs):
   - How is the code organized?
   - What design patterns are used (if any)?
   - How do components interact?
   - Is it procedural, OOP, or functional?

3. KEY COMPONENTS (1-2 paragraphs):
   - What are the critical functions/classes?
   - How do they work together?
   - What is the data flow?

4. TECHNICAL DECISIONS (1 paragraph):
   - Notable implementation choices
   - Technology stack decisions
   - Code organization strategy

5. CODE QUALITY (1 paragraph):
   - Overall structure assessment
   - Maintainability considerations
   - Any notable strengths or concerns

Write in a formal, professional tone suitable for technical documentation."""

        try:
            return await self._call_ollama_with_limit(
                prompt,
                timeout=self.timeouts["long"],
                model=self.models["quality"]
            )
        except:
            return self._generate_fallback_overview(code, structure)
    
    def _generate_fallback_overview(self, code: str, structure: Dict[str, Any]) -> str:
        """Generate a basic overview if AI fails"""
        lines = len(code.split('\n'))
        return f"""## Code Analysis Summary

This Python file contains {len(structure.get('functions', []))} function(s), {len(structure.get('classes', []))} class(es), and {len(structure.get('imports', []))} import statement(s) across {lines} lines of code.

**Structure:**
- The code is organized with clear separation of concerns
- External dependencies are imported at the top
- Functions and classes provide modular functionality

**Purpose:**
Based on the structure, this code appears to implement core business logic with well-defined components. Each function and class serves a specific purpose in the overall architecture.

*Note: Detailed AI analysis timed out. This is a structural summary.*"""
    
    async def explain_function(self, func: Function, code_snippet: str) -> str:
        """Generate detailed function explanation"""
        logger.info(f"Explaining function: {func.name}")
        
        # Optimized shorter prompt
        prompt = f"""Explain this Python function briefly (max 150 words).

Function: {func.name}({', '.join(func.parameters)})
Returns: {func.return_type or 'Unknown'}

Code:
{code_snippet}

Explain:
1. What it does
2. How it processes inputs
3. Key logic steps
4. What it returns"""

        try:
            return await self._call_ollama(prompt, timeout=self.medium_timeout)
        except Exception as e:
            logger.warning(f"Function explanation failed for {func.name}: {e}")
            return self._generate_fallback_function_explanation(func)
    
    def _generate_fallback_function_explanation(self, func: Function) -> str:
        """Fallback explanation if AI times out"""
        params = ', '.join(func.parameters) if func.parameters else 'no parameters'
        return_info = f"Returns {func.return_type}" if func.return_type else "Return type not specified"
        
        explanation = f"""**{func.name}** is a function that accepts {params}. {return_info}.

**Docstring:** {func.docstring if func.docstring else 'No documentation provided.'}

**Variables used:** {', '.join(func.variables_used) if func.variables_used else 'None identified'}

*Note: Detailed AI analysis timed out.*"""
        return explanation
    
    async def explain_class(self, cls: Class, code_snippet: str) -> str:
        """Generate detailed class explanation"""
        logger.info(f"Explaining class: {cls.name}")
        
        prompt = f"""Explain this Python class briefly (max 150 words).

Class: {cls.name}
Methods: {', '.join(cls.methods[:5])}...
Attributes: {', '.join(cls.attributes[:5])}...

Code:
{code_snippet}

Explain:
1. Class purpose
2. How it's designed
3. Key methods
4. State management"""

        try:
            return await self._call_ollama(prompt, timeout=self.medium_timeout)
        except Exception as e:
            logger.warning(f"Class explanation failed for {cls.name}: {e}")
            return self._generate_fallback_class_explanation(cls)
    
    def _generate_fallback_class_explanation(self, cls: Class) -> str:
        """Fallback explanation if AI times out"""
        inheritance = f"Inherits from {', '.join(cls.base_classes)}" if cls.base_classes else "No base classes"
        
        explanation = f"""**{cls.name}** is a class with {len(cls.methods)} method(s) and {len(cls.attributes)} attribute(s). {inheritance}.

**Docstring:** {cls.docstring if cls.docstring else 'No documentation provided.'}

**Methods:** {', '.join(cls.methods) if cls.methods else 'None'}
**Attributes:** {', '.join(cls.attributes) if cls.attributes else 'None'}

*Note: Detailed AI analysis timed out.*"""
        return explanation
    
    async def explain_import(self, imp: Import) -> str:
        """Explain what an import does"""
        logger.info(f"Explaining import: {imp.module}")
        
        prompt = f"""Explain this Python import in 2-3 sentences.

Module: {imp.module}
Imports: {', '.join(imp.names)}

What does this module provide and why use these specific imports?"""

        try:
            return await self._call_ollama(prompt, timeout=self.short_timeout)
        except Exception as e:
            logger.warning(f"Import explanation failed for {imp.module}: {e}")
            return f"{imp.module} provides {', '.join(imp.names)}. This module is used for its functionality."
    
    async def generate_suggestions(self, code: str, errors: List) -> List[Suggestion]:
        """Generate improvement suggestions"""
        logger.info("Generating code improvement suggestions")
        
        # Much shorter prompt
        prompt = f"""Suggest 3-5 improvements for this Python code.

Code length: {len(code)} chars
Issues found: {len(errors)}

Format each as:
CATEGORY: [Performance/Security/Best Practice]
TITLE: Short title
DESCRIPTION: One sentence
PRIORITY: High/Medium/Low
---"""

        try:
            result = await self._call_ollama(prompt, timeout=self.long_timeout)
            suggestions = self._parse_suggestions(result)
            if suggestions:
                return suggestions
        except Exception as e:
            logger.warning(f"Suggestion generation failed: {e}")
        
        # Return default suggestions if AI fails
        return self._generate_default_suggestions(errors)
    
    def _generate_default_suggestions(self, errors: List) -> List[Suggestion]:
        """Generate basic suggestions when AI fails"""
        suggestions = [
            Suggestion(
                category="Code Quality",
                title="Add Type Hints",
                description="Consider adding type hints to function parameters and return values for better code documentation and IDE support.",
                priority="Medium"
            ),
            Suggestion(
                category="Documentation",
                title="Improve Docstrings",
                description="Add comprehensive docstrings to all functions and classes following PEP 257 conventions.",
                priority="Medium"
            )
        ]
        
        if errors:
            suggestions.insert(0, Suggestion(
                category="Bug Fix",
                title="Address Detected Issues",
                description=f"Fix the {len(errors)} issue(s) detected in the error analysis tab to improve code quality.",
                priority="High"
            ))
        
        return suggestions
    
    def _parse_suggestions(self, text: str) -> List[Suggestion]:
        """Parse AI suggestions into structured format"""
        logger.debug("Parsing AI suggestions")
        suggestions = []
        
        parts = text.split('---')
        for part in parts:
            if not part.strip():
                continue
            
            lines = part.strip().split('\n')
            category = priority = title = description = ""
            
            for line in lines:
                if line.startswith('CATEGORY:'):
                    category = line.replace('CATEGORY:', '').strip()
                elif line.startswith('TITLE:'):
                    title = line.replace('TITLE:', '').strip()
                elif line.startswith('PRIORITY:'):
                    priority = line.replace('PRIORITY:', '').strip()
                elif line.startswith('DESCRIPTION:'):
                    description = line.replace('DESCRIPTION:', '').strip()
                elif description and not line.startswith(('CATEGORY', 'TITLE', 'PRIORITY')):
                    description += ' ' + line.strip()
            
            if title and description:
                suggestions.append(Suggestion(
                    category=category or "General",
                    title=title,
                    description=description,
                    priority=priority or "Medium"
                ))
        
        logger.info(f"Parsed {len(suggestions)} suggestions")
        return suggestions
    
    async def _call_ollama(self, prompt: str, timeout: float = 60.0) -> str:
        """Call Ollama API with configurable timeout"""
        logger.debug(f"Calling Ollama with prompt length: {len(prompt)}, timeout: {timeout}s")
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                response.raise_for_status()
                result = response.json()
                logger.debug("Ollama API call successful")
                return result.get("response", "")
            except httpx.TimeoutException as e:
                logger.error(f"Ollama API timeout after {timeout}s: {str(e)}")
                raise Exception(f"AI generation timed out after {timeout}s")
            except Exception as e:
                logger.error(f"Ollama API call failed: {str(e)}")
                raise Exception(f"AI generation failed: {str(e)}")