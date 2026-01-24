import requests
from typing import Dict, Any, Optional

class APIClient:
    """Client for backend API communication"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def analyze_code(self, file_content: bytes, filename: str) -> Optional[Dict[str, Any]]:
        """
        Send file to backend for analysis.
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            
        Returns:
            Analysis response dict or None on error
        """
        try:
            files = {"file": (filename, file_content, "text/x-python")}
            response = requests.post(
                f"{self.base_url}/api/analyze",
                files=files,
                timeout=600
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_health(self) -> Dict[str, Any]:
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json()
        except:
            return {"status": "unhealthy"}
