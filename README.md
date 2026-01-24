# Python Code Explainer System

AI-powered tool for analyzing and explaining Python code.

## Installation

1. Install Ollama and pull the model:
   ```bash
   ollama pull deepseek-coder
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

## Running the Application

1. Start backend (in backend directory):
   ```bash
   uvicorn app.main:app --reload
   ```

2. Start frontend (in frontend directory):
   ```bash
   streamlit run app.py
   ```

3. Access the application at http://localhost:8501

## Features

- AI-powered code analysis using Ollama DeepSeek
- Visual Mermaid diagrams (flowchart, sequence, class)
- Error detection and best practice checking
- Markdown and HTML report generation
- Local file storage (no cloud dependencies)

## File Storage

Files are stored locally in the `output/` directory:
- `output/markdown/` - Markdown documentation
- `output/pdf/` - HTML reports (can be printed to PDF)

## Important
This project is currently under development, and some features are not yet complete.