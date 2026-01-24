# ==========================================
# FRONTEND - frontend/components/sidebar.py
# ==========================================
import streamlit as st

def render_sidebar():
    """Render sidebar with upload and information"""
    with st.sidebar:
        st.markdown("## 📁 Upload Code")
        uploaded_file = st.file_uploader(
            "Choose a Python file",
            type=['py'],
            help="Upload a .py file to analyze"
        )
        
        st.markdown("---")
        st.markdown("## ℹ️ About")
        st.info("""
        **Python Code Explainer** provides:
        - AI-powered code analysis
        - Detailed function explanations
        - Visual architecture diagrams
        - Code quality suggestions
        - Comprehensive reports
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 Features")
        st.markdown("""
        - 📋 Detailed Overview
        - 📦 Import Explanations
        - 📊 Variable Tracking
        - ⚙️ Function Analysis
        - 🏗️ Class Documentation
        - 📈 Visual Diagrams
        - 💡 AI Suggestions
        - 📄 PDF Reports
        """)
        
        st.markdown("---")
        st.markdown("### 💻 Tech Stack")
        st.markdown("""
        - **Backend:** FastAPI
        - **AI:** Ollama DeepSeek
        - **Frontend:** Streamlit
        - **Storage:** Local Files
        """)
    
    return uploaded_file