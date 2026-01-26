import streamlit as st
from config import Config
from services.api import APIClient
from components.sidebar import render_sidebar
from components.tabs.overview import render_overview_tab
from components.tabs.imports import render_imports_tab
from components.tabs.variables import render_variables_tab
from components.tabs.functions import render_functions_tab
from components.tabs.classes import render_classes_tab
from components.tabs.suggestions import render_suggestions_tab
from components.tabs.errors import render_errors_tab
from utils.styling import get_custom_css

st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

def display_header():
    """Display main header"""
    st.markdown(
        f'<div class="main-header">{Config.PAGE_ICON} {Config.PAGE_TITLE}</div>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">AI-powered code analysis with professional PDF reports</div>', 
        unsafe_allow_html=True
    )

def display_welcome_message():
    """Display welcome message"""
    st.markdown("""
    ## 👋 Welcome to Python Code Explainer!
    
    ### 🚀 Getting Started
    Upload a Python file using the sidebar to begin comprehensive code analysis.
    
    ### ✨ What You'll Get:
    
    1. **📋 Detailed Overview** - Understanding of code purpose and architecture
    2. **📦 Import Analysis** - Detailed explanation of each dependency
    3. **📊 Variable Tracking** - Complete variable inventory and usage
    4. **⚙️ Function Analysis** - Detailed logic explanations
    5. **🏗️ Class Documentation** - Complete class structure with method details
    6. **💡 AI Suggestions** - Performance and quality improvements
    7. **⚠️ Error Detection** - Issues and warnings
    8. **📄 Professional PDF Report** - Formal documentation ready for industry use
    
    ### 📄 Professional Report Features:
    - Executive summary with metrics
    - Comprehensive function and class analysis
    - Code quality assessment
    - Improvement recommendations with examples
    - Architecture diagrams
    - Complete source code reference
    - Print-ready format for meetings and documentation
    
    **Ready to start? Upload your Python file in the sidebar!**
    """)

def handle_analysis(uploaded_file):
    """Handle file upload and analysis"""
    file_content = uploaded_file.read()
    filename = uploaded_file.name
    
    st.success(f"✅ File uploaded: **{filename}**")
    
    if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
        with st.spinner("🤖 Analyzing code and generating report... This may take 1-2 minutes."):
            api_client = APIClient(Config.API_BASE_URL)
            analysis = api_client.analyze_code(file_content, filename)
        
        if analysis and 'error' not in analysis:
            st.session_state['analysis'] = analysis
            st.success("✅ Analysis complete!")
            st.balloons()
            st.rerun()
        else:
            st.error(f"❌ Analysis failed: {analysis.get('error', 'Unknown error')}")

def display_analysis_results(analysis):
    """Display analysis results in tabs"""
    st.markdown("---")
    
    # PDF Download Button (Prominent)
    if analysis.get('pdf_ready') and analysis.get('file_id'):
        st.markdown("### 📄 Professional Report")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            pdf_url = f"{Config.API_BASE_URL}/api/download/pdf/{analysis['file_id']}"
            st.link_button(
                "📥 Download Complete PDF Report",
                pdf_url,
                use_container_width=True,
                type="primary"
            )
            st.caption("Professional report with all analysis details, ready for documentation and meetings")
    
    st.markdown("---")
    
    # Create tabs (REMOVED Diagrams and Final Report)
    tabs = st.tabs([
        "📋 Overview",
        "📦 Imports",
        "📊 Variables",
        "⚙️ Functions",
        "🏗️ Classes",
        "💡 Suggestions",
        "⚠️ Errors"
    ])
    
    with tabs[0]:
        render_overview_tab(analysis)
    
    with tabs[1]:
        render_imports_tab(analysis.get('imports', []))
    
    with tabs[2]:
        render_variables_tab(analysis.get('variables', []))
    
    with tabs[3]:
        render_functions_tab(analysis.get('functions', []))

    with tabs[4]:
        render_classes_tab(analysis.get('classes', []))

    with tabs[5]:
        render_suggestions_tab(analysis.get('suggestions', []))

    with tabs[6]:
        render_errors_tab(analysis.get('errors', []))

def main():
    """Main application entry point"""
    display_header()
    uploaded_file = render_sidebar()
    if uploaded_file is not None:
        handle_analysis(uploaded_file)

    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        display_analysis_results(analysis)
    else:
        display_welcome_message()

if __name__ == "__main__":
    main()