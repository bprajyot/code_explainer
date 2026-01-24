import streamlit as st
import requests
from typing import Dict, Any
import base64

st.set_page_config(
    page_title="Python Code Explainer",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .error-critical {
        background-color: #ffebee;
        padding: 10px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
    }
    .error-warning {
        background-color: #fff3e0;
        padding: 10px;
        border-left: 4px solid #ff9800;
        margin: 10px 0;
    }
    .error-info {
        background-color: #e3f2fd;
        padding: 10px;
        border-left: 4px solid #2196f3;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

API_BASE_URL = "http://localhost:8000"

def analyze_code(file_content: bytes, filename: str) -> Dict[str, Any]:
    """Call backend API to analyze code"""
    try:
        files = {"file": (filename, file_content, "text/x-python")}
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            files=files,
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def download_button(label: str, data: str, filename: str, mime: str):
    """Create download button"""
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:{mime};base64,{b64}" download="{filename}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

def render_overview_tab(analysis: Dict[str, Any]):
    """Render Overview tab"""
    st.markdown("### 📋 Code Overview")
    st.markdown(analysis['overview'])
    
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Variables", len(analysis['variables']))
    with col2:
        st.metric("Functions", len(analysis['functions']))
    with col3:
        st.metric("Classes", len(analysis['classes']))
    with col4:
        st.metric("Imports", len(analysis['imports']))

def render_variables_tab(variables: list):
    """Render Variables tab"""
    if not variables:
        st.info("No significant variables found in the code.")
        return
    
    st.markdown("### 📊 Variables")
    
    for var in variables:
        with st.expander(f"**{var['name']}** ({var['type']})", expanded=False):
            st.markdown(f"**Scope:** `{var['scope']}`")
            st.markdown(f"**Line Number:** {var['line_number']}")

def render_functions_tab(functions: list):
    """Render Functions tab"""
    if not functions:
        st.info("No functions found in the code.")
        return
    
    st.markdown("### ⚙️ Functions")
    
    for func in functions:
        params = ", ".join(func['parameters'])
        with st.expander(f"**{func['name']}**({params})", expanded=False):
            if func['return_type']:
                st.markdown(f"**Returns:** `{func['return_type']}`")
            if func['docstring']:
                st.markdown("**Documentation:**")
                st.info(func['docstring'])
            st.markdown(f"**Defined at line:** {func['line_number']}")

def render_classes_tab(classes: list):
    """Render Classes tab"""
    if not classes:
        st.info("No classes found in the code.")
        return
    
    st.markdown("### 🏗️ Classes")
    
    for cls in classes:
        with st.expander(f"**{cls['name']}**", expanded=False):
            if cls['base_classes']:
                st.markdown(f"**Inherits from:** {', '.join(cls['base_classes'])}")
            
            if cls['docstring']:
                st.markdown("**Documentation:**")
                st.info(cls['docstring'])
            
            st.markdown(f"**Methods:** {', '.join(cls['methods']) if cls['methods'] else 'None'}")
            st.markdown(f"**Attributes:** {', '.join(cls['attributes']) if cls['attributes'] else 'None'}")
            st.markdown(f"**Defined at line:** {cls['line_number']}")

def render_diagrams_tab(diagrams: Dict[str, str]):
    """Render Diagrams tab"""
    if not diagrams:
        st.info("No diagrams available.")
        return
    
    st.markdown("### 📈 Code Diagrams")
    
    for diagram_type, diagram_code in diagrams.items():
        st.markdown(f"#### {diagram_type.title()} Diagram")
        st.code(diagram_code, language="mermaid")
        st.markdown("---")

def render_errors_tab(errors: list):
    """Render Errors tab"""
    if not errors:
        st.success("✅ No errors or warnings detected!")
        return
    
    st.markdown("### ⚠️ Errors and Warnings")
    
    critical = [e for e in errors if e['severity'] == 'Critical']
    warnings = [e for e in errors if e['severity'] == 'Warning']
    info = [e for e in errors if e['severity'] == 'Info']
    
    if critical:
        st.markdown("#### 🔴 Critical Issues")
        for error in critical:
            st.markdown(f"""
            <div class="error-critical">
                <strong>{error['category']}</strong>: {error['message']}<br>
                {'<em>Line ' + str(error['line_number']) + '</em>' if error['line_number'] else ''}
            </div>
            """, unsafe_allow_html=True)
    
    if warnings:
        st.markdown("#### 🟡 Warnings")
        for error in warnings:
            st.markdown(f"""
            <div class="error-warning">
                <strong>{error['category']}</strong>: {error['message']}<br>
                {'<em>Line ' + str(error['line_number']) + '</em>' if error['line_number'] else ''}
            </div>
            """, unsafe_allow_html=True)
    
    if info:
        st.markdown("#### 🔵 Informational")
        for error in info:
            st.markdown(f"""
            <div class="error-info">
                <strong>{error['category']}</strong>: {error['message']}<br>
                {'<em>Line ' + str(error['line_number']) + '</em>' if error['line_number'] else ''}
            </div>
            """, unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header">🐍 Python Code Explainer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-powered code analysis for junior developers</div>', unsafe_allow_html=True)
    
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
        This tool helps you understand Python code by:
        - Providing clear explanations
        - Extracting code structure
        - Generating visual diagrams
        - Detecting potential issues
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 Tech Stack")
        st.markdown("""
        - **Backend:** FastAPI
        - **AI:** Ollama (DeepSeek)
        - **Frontend:** Streamlit
        - **Storage:** Local Files
        """)
    
    if uploaded_file is not None:
        file_content = uploaded_file.read()
        filename = uploaded_file.name
        
        st.success(f"✅ File uploaded: **{filename}**")
        
        if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
            with st.spinner("Analyzing code... This may take a minute."):
                analysis = analyze_code(file_content, filename)
            
            if analysis:
                st.session_state['analysis'] = analysis
                st.success("✅ Analysis complete!")
                st.rerun()
    
    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if analysis.get('markdown_content'):
                st.download_button(
                    label="📄 Download Markdown",
                    data=analysis['markdown_content'],
                    file_name=f"analysis_{analysis['file_id']}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        with col2:
            if analysis.get('pdf_content'):
                st.download_button(
                    label="📕 Download HTML Report",
                    data=analysis['pdf_content'],
                    file_name=f"analysis_{analysis['file_id']}.html",
                    mime="text/html",
                    use_container_width=True
                )
        
        st.markdown("---")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📋 Overview",
            "📊 Variables",
            "⚙️ Functions",
            "🏗️ Classes",
            "📈 Diagrams",
            "⚠️ Errors"
        ])
        
        with tab1:
            render_overview_tab(analysis)
        
        with tab2:
            render_variables_tab(analysis.get('variables', []))
        
        with tab3:
            render_functions_tab(analysis.get('functions', []))
        
        with tab4:
            render_classes_tab(analysis.get('classes', []))
        
        with tab5:
            render_diagrams_tab(analysis.get('diagrams', {}))
        
        with tab6:
            render_errors_tab(analysis.get('errors', []))
    
    else:
        st.markdown("""
        ## 👋 Welcome!
        
        Upload a Python file to get started. The system will:
        
        1. **Analyze** the code structure
        2. **Explain** what the code does in simple terms
        3. **Extract** variables, functions, and classes
        4. **Generate** visual diagrams
        5. **Detect** errors and suggest improvements
        6. **Create** downloadable documentation (Markdown & HTML)
        
        Perfect for understanding legacy code or onboarding to new projects!
        """)

if __name__ == "__main__":
    main()