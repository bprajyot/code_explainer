from supabase import create_client, Client
from ..config import config
import uuid

class SupabaseStorage:
    def __init__(self):
        settings = config()
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_BUCKET
    
    async def upload_markdown(self, content: str, filename: str) -> str:
        """Upload Markdown file to Supabase storage"""
        file_id = str(uuid.uuid4())
        file_path = f"markdown/{file_id}_{filename}.md"
        
        self.client.storage.from_(self.bucket).upload(
            file_path,
            content.encode('utf-8'),
            file_options={"content-type": "text/markdown"}
        )
        
        # Get public URL
        url = self.client.storage.from_(self.bucket).get_public_url(file_path)
        return url
    
    async def upload_pdf(self, content: bytes, filename: str) -> str:
        """Upload PDF file to Supabase storage"""
        file_id = str(uuid.uuid4())
        file_path = f"pdf/{file_id}_{filename}.pdf"
        
        self.client.storage.from_(self.bucket).upload(
            file_path,
            content,
            file_options={"content-type": "application/pdf"}
        )
        
        # Get public URL
        url = self.client.storage.from_(self.bucket).get_public_url(file_path)
        return url