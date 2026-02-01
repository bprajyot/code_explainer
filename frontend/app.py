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
from utils.styling import get_professional_css

# ------------------------------------------------------------------
# Page setup
# ------------------------------------------------------------------
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_professional_css(), unsafe_allow_html=True)

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
def display_header():
    st.markdown(
        """
        <div class="professional-header">
            <div class="header-content">
                <div class="header-icon">📊</div>
                <div class="header-text">
                    <h1>Python Code Analysis System</h1>
                    <p>Enterprise Code Intelligence Platform</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------------------------
# Welcome / Empty State
# ------------------------------------------------------------------
def display_welcome_message():
    st.html(
        """
        <div class="welcome-section">
            <div class="getting-started">
                <h3>Getting Started</h3>
                <ol>
                    <li>Upload a Python file from the sidebar</li>
                    <li>Click <strong>Analyze Code</strong></li>
                    <li>Explore insights across structured tabs</li>
                    <li>Export a professional PDF report</li>
                </ol>
            </div>

            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🔍</div>
                    <h3>Deep Analysis</h3>
                    <p>AI-powered understanding of structure, patterns, and risks</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <h3>Quality Metrics</h3>
                    <p>Actionable insights for maintainability and reliability</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">📄</div>
                    <h3>Professional Reports</h3>
                    <p>Audit-ready documentation for reviews and stakeholders</p>
                </div>
            </div>

            <div class="info-banner">
                <strong>Internal Tool:</strong> All processing is local. Reports are suitable
                for technical documentation and internal reviews.
            </div>
        </div>
        """
    )

# ------------------------------------------------------------------
# Analysis handler (logic unchanged)
# ------------------------------------------------------------------
def handle_analysis(uploaded_file):
    file_content = uploaded_file.read()
    filename = uploaded_file.name

    st.success(f"📁 **{filename}** uploaded successfully")

    analyze = st.button(
        "🔍 Analyze Code",
        type="primary",
        use_container_width=True
    )

    if analyze:
        with st.spinner("Running comprehensive analysis…"):
            progress = st.progress(0)
            progress.progress(20)

            api_client = APIClient(Config.API_BASE_URL)
            analysis = api_client.analyze_code(file_content, filename)

            progress.progress(100)

        if analysis and "error" not in analysis:
            st.session_state["analysis"] = analysis
            st.success("Analysis completed successfully")
            st.balloons()
            st.rerun()
        else:
            st.error(f"Analysis failed: {analysis.get('error', 'Unknown error')}")

# ------------------------------------------------------------------
# Results
# ------------------------------------------------------------------
def display_analysis_results(analysis):
    st.markdown("## 📊 Analysis Dashboard")

    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Functions", len(analysis.get("functions", [])))
        col2.metric("Classes", len(analysis.get("classes", [])))
        col3.metric("Dependencies", len(analysis.get("imports", [])))

        error_count = len(analysis.get("errors", []))
        col4.metric(
            "Issues",
            error_count,
            delta=f"-{error_count}" if error_count else None,
            delta_color="inverse"
        )

        quality = "High" if error_count == 0 else "Medium" if error_count < 5 else "Low"
        col5.metric("Quality", quality)

    st.divider()

    # ------------------------------------------------------------------
    # Report download
    # ------------------------------------------------------------------
    st.markdown("## 📄 Professional Report")

    if analysis.get("pdf_ready") and analysis.get("file_id"):
        pdf_url = f"{Config.API_BASE_URL}/api/download/pdf/{analysis['file_id']}"

        st.markdown(
            f"""
            <div class="download-section">
                <div class="download-icon">📥</div>
                <h4>Download Full Analysis</h4>
                <p>Comprehensive, audit-ready PDF report</p>
                <a href="{pdf_url}" class="download-button" target="_blank">
                    Download Report
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # ------------------------------------------------------------------
    # Tabs
    # ------------------------------------------------------------------
    st.markdown("## 📑 Detailed Analysis")

    tabs = st.tabs([
        "📋 Overview",
        "📦 Dependencies",
        "📊 Variables",
        "⚙️ Functions",
        "🏗️ Classes",
        "💡 Recommendations",
        "⚠️ Quality Issues",
    ])

    with tabs[0]:
        render_overview_tab(analysis)

    with tabs[1]:
        render_imports_tab(analysis.get("imports", []))

    with tabs[2]:
        render_variables_tab(analysis.get("variables", []))

    with tabs[3]:
        render_functions_tab(analysis.get("functions", []))

    with tabs[4]:
        render_classes_tab(analysis.get("classes", []))

    with tabs[5]:
        render_suggestions_tab(analysis.get("suggestions", []))

    with tabs[6]:
        render_errors_tab(analysis.get("errors", []))

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    display_header()
    uploaded_file = render_sidebar()

    if uploaded_file:
        handle_analysis(uploaded_file)

    if "analysis" in st.session_state:
        display_analysis_results(st.session_state["analysis"])
    else:
        display_welcome_message()

if __name__ == "__main__":
    main()
