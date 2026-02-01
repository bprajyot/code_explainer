import streamlit as st

def render_sidebar():
    """Render professional sidebar"""
    with st.sidebar:
        # --------------------------------------------------
        # Upload Section
        # --------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-section">
                <h2 class="sidebar-title">📁 Upload File</h2>
                <p class="sidebar-subtitle">
                    Upload a Python (.py) file for analysis
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        uploaded_file = st.file_uploader(
            label="Python file upload",
            type=["py"],
            help="Upload a .py file for comprehensive analysis",
            label_visibility="collapsed"
        )

        st.divider()

        # --------------------------------------------------
        # Features
        # --------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-card">
                <h3 class="sidebar-card-title">🔍 Analysis Capabilities</h3>
                <ul class="sidebar-list">
                    <li>Comprehensive code analysis</li>
                    <li>AI-powered explanations & insights</li>
                    <li>Code quality and risk assessment</li>
                    <li>Professional PDF export</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    return uploaded_file
