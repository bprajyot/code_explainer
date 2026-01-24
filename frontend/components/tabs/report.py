# ==========================================
# FRONTEND - frontend/components/tabs/final_report_tab.py
# ==========================================
import streamlit as st
from typing import Dict, Any
import streamlit.components.v1 as components

def render_final_report_tab(analysis: Dict[str, Any]):
    """Render formal final report with rendered markdown"""
    st.markdown("### 📄 Final Technical Report")
    st.markdown("*Comprehensive professional analysis report*")
    
    # Download buttons at top
    col1, col2 = st.columns(2)
    with col1:
        if analysis.get('markdown_content'):
            st.download_button(
                label="📄 Download Full Markdown",
                data=analysis['markdown_content'],
                file_name=f"analysis_{analysis['file_id']}.md",
                mime="text/markdown",
                use_container_width=True,
                type="primary"
            )
    
    with col2:
        if analysis.get('pdf_content'):
            st.download_button(
                label="📕 Download PDF Report (HTML)",
                data=analysis['pdf_content'],
                file_name=f"report_{analysis['file_id']}.html",
                mime="text/html",
                use_container_width=True,
                type="primary"
            )
    
    st.markdown("---")
    
    # Render sections
    st.markdown("## 📋 Executive Summary")
    st.markdown(analysis['detailed_overview'])
    
    st.markdown("---")
    st.markdown("## 📊 Code Structure Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Functions", len(analysis['functions']))
    with col2:
        st.metric("Classes", len(analysis['classes']))
    with col3:
        st.metric("Dependencies", len(analysis['imports']))
    with col4:
        st.metric("Issues", len(analysis['errors']))
    
    # Functions Detail
    if analysis['functions']:
        st.markdown("---")
        st.markdown("## ⚙️ Function Analysis")
        for func in analysis['functions']:
            st.markdown(f"### {func['name']}")
            st.markdown(f"**Signature:** `{func['name']}({', '.join(func['parameters'])})`")
            if func.get('return_type'):
                st.markdown(f"**Returns:** `{func['return_type']}`")
            if func.get('logic_explanation'):
                st.info(func['logic_explanation'])
            st.markdown("")
    
    # Classes Detail
    if analysis['classes']:
        st.markdown("---")
        st.markdown("## 🏗️ Class Analysis")
        for cls in analysis['classes']:
            st.markdown(f"### {cls['name']}")
            if cls.get('base_classes'):
                st.markdown(f"**Inheritance:** {', '.join(cls['base_classes'])}")
            if cls.get('detailed_explanation'):
                st.info(cls['detailed_explanation'])
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Methods:** {', '.join(cls['methods'])}")
            with col2:
                st.markdown(f"**Attributes:** {', '.join(cls['attributes'])}")
            st.markdown("")
    
    # Diagrams - Rendered
    st.markdown("---")
    st.markdown("## 📈 Architecture Diagrams")
    
    for diagram_type, diagram_code in analysis['diagrams'].items():
        st.markdown(f"### {diagram_type.title()}")
        
        # Render Mermaid
        mermaid_html = f"""
        <div class="mermaid-container" style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{ 
                    startOnLoad: true,
                    theme: 'default'
                }});
            </script>
            <div class="mermaid">
{diagram_code}
            </div>
        </div>
        """
        components.html(mermaid_html, height=400, scrolling=True)
    
    # Dependencies
    if analysis['imports']:
        st.markdown("---")
        st.markdown("## 📦 Dependencies")
        for imp in analysis['imports']:
            st.markdown(f"**{imp['module']}:** {imp.get('purpose', 'N/A')}")
    
    # Recommendations
    if analysis.get('suggestions'):
        st.markdown("---")
        st.markdown("## 💡 Recommendations")
        
        high_priority = [s for s in analysis['suggestions'] if s.get('priority') == 'High']
        medium_priority = [s for s in analysis['suggestions'] if s.get('priority') == 'Medium']
        
        if high_priority:
            st.markdown("### High Priority")
            for s in high_priority:
                st.markdown(f"**{s['title']}:** {s['description']}")
        
        if medium_priority:
            st.markdown("### Medium Priority")
            for s in medium_priority:
                st.markdown(f"**{s['title']}:** {s['description']}")