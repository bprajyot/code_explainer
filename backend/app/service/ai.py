# ==========================================
# BACKEND - backend/app/services/ai_service.py
# ==========================================
import httpx
from typing import Dict, Any
from ..config import get_settings

class AIService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.OLLAMA_BASE_URL
        self.model = self.settings.OLLAMA_MODEL
    
    async def generate_overview(self, code: str, structure: Dict[str, Any]) -> str:
        prompt = f"""Analyze this Python code and provide a clear, beginner-friendly overview.

Code:
{code[:1000]}...

Structure:
- Functions: {len(structure.get('functions', []))}
- Classes: {len(structure.get('classes', []))}
- Imports: {len(structure.get('imports', []))}

Provide a 2-3 paragraph overview explaining:
1. What this code does (its purpose)
2. The main components and how they work together
3. Any notable patterns or design choices

Keep it simple and clear for junior developers."""

        return await self._call_ollama(prompt)
    
    async def _call_ollama(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
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
                return result.get("response", "")
            except Exception as e:
                return f"AI generation failed: {str(e)}"