# ==========================================
# BACKEND - backend/app/storage/pdf_generator.py
# ==========================================
from markdown import markdown

class PDFGenerator:
    def generate(self, markdown_content: str) -> str:
        """Convert Markdown to styled HTML"""
        html_content = markdown(
            markdown_content, 
            extensions=['fenced_code', 'tables']
        )
        
        full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Code Analysis Report</title>
    <style>
        @media print {{ body {{ margin: 2cm; }} }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #1e1e1e;
            color: #d4d4d4;
            line-height: 1.6;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1, h2, h3 {{
            color: #569cd6;
            border-bottom: 2px solid #404040;
            padding-bottom: 0.3em;
            margin-top: 1.5em;
        }}
        code {{
            background-color: #2d2d2d;
            color: #ce9178;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #2d2d2d;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #569cd6;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        th, td {{
            border: 1px solid #404040;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #2d2d2d;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
        return full_html