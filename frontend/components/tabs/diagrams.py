# ==========================================
# FRONTEND - frontend/components/tabs/diagrams_tab.py
# ==========================================
import streamlit as st
from typing import Dict
import streamlit.components.v1 as components

def render_diagrams_tab(diagrams: Dict[str, str]):
    """Render diagrams tab with rendered Mermaid diagrams"""
    if not diagrams:
        st.info("No diagrams available.")
        return
    
    st.markdown("### 📈 Code Visualization")
    st.markdown("*Visual representation of code structure and flow*")
    st.markdown("---")
    
    for diagram_type, diagram_code in diagrams.items():
        st.markdown(f"#### {diagram_type.title()} Diagram")
        
        # Render Mermaid diagram using HTML/JavaScript
        mermaid_html = f"""
        <div class="mermaid-container" style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{ 
                    startOnLoad: true,
                    theme: 'default',
                    flowchart: {{ useMaxWidth: true, htmlLabels: true }}
                }});
            </script>
            <div class="mermaid">
{diagram_code}
            </div>
        </div>
        """
        
        components.html(mermaid_html, height=400, scrolling=True)
        
        # Show code as well
        with st.expander("View Mermaid Code"):
            st.code(diagram_code, language="mermaid")
        
        st.markdown("---")