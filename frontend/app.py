import streamlit as st
from config import Config
from services.api import APIClient
from components.sidebar import render_sidebar
from components.tabs.overview import render_overview_tab
from components.tabs.imports import render_imports_tab
from components.tabs.variables import render_variables_tab
from components.tabs.functions import render_functions_tab
from components.tabs.classes import render_classes_tab
from components.tabs.diagrams import render_diagrams_tab
from components.tabs.suggestions import render_suggestions_tab
from components.tabs.errors import render_errors_tab
from components.tabs.functions import render_functions_tab
from utils.styling import get_custom_css

# Page configuration
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

def display_header():
    """Display main header"""
    st.markdown(
        f'<div class="main-header">{Config.PAGE_ICON} {Config.PAGE_TITLE}</div>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">AI-powered code analysis for junior developers</div>', 
        unsafe_allow_html=True
    )

def display_welcome_message():
    """Display welcome message when no file is uploaded"""
    st.markdown("""
    ## 👋 Welcome to Python Code Explainer!
    
    ### 🚀 Getting Started
    Upload a Python file using the sidebar to begin comprehensive code analysis.
    
    ### ✨ What You'll Get:
    
    1. **📋 Detailed Overview**
       - High-level understanding of code purpose
       - Architecture and design patterns
    
    2. **📦 Import Analysis**
       - Detailed explanation of each dependency
       - Purpose and common use cases
    
    3. **📊 Variable Tracking**
       - Complete variable inventory
       - Usage tracking across the code
    
    4. **⚙️ Function Analysis**
       - Detailed logic explanations
       - Variable usage within functions
    
    5. **🏗️ Class Documentation**
       - Complete class structure
       - Design pattern analysis
    
    6. **📈 Visual Diagrams**
       - Flowchart, sequence, class diagrams
       - **Rendered, not just code!**
    
    7. **💡 AI Suggestions**
       - Performance improvements
       - Best practice guidance
    
    8. **📄 Professional Report**
       - Formal technical documentation
       - Downloadable PDF/HTML format
    
    **Ready to start? Upload your Python file in the sidebar!**
    """)

def handle_analysis(uploaded_file):
    """Handle file upload and analysis"""
    file_content = uploaded_file.read()
    filename = uploaded_file.name
    
    st.success(f"✅ File uploaded: **{filename}**")
    
    if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
        with st.spinner("🤖 Analyzing code... This may take 1-2 minutes."):
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
    
    # Create tabs
    tabs = st.tabs([
        "📋 Overview",
        "📦 Imports",
        "📊 Variables",
        "⚙️ Functions",
        "🏗️ Classes",
        "📈 Diagrams",
        "💡 Suggestions",
        "⚠️ Errors",
        "📄 Final Report"
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
        render_diagrams_tab(analysis.get('diagrams', {}))
    
    with tabs[6]:
        render_suggestions_tab(analysis.get('suggestions', []))
    
    with tabs[7]:
        render_errors_tab(analysis.get('errors', []))
    
    with tabs[8]:
        render_functions_tab(analysis)

def main():
    """Main application entry point"""
    # Display header
    display_header()
    
    # Render sidebar and get uploaded file
    uploaded_file = render_sidebar()
    
    # Handle file upload
    if uploaded_file is not None:
        handle_analysis(uploaded_file)
    
    # Display results if analysis exists in session state
    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        display_analysis_results(analysis)
    else:
        # Display welcome message
        display_welcome_message()

if __name__ == "__main__":
    main()