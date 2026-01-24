# ==========================================
# FRONTEND - frontend/components/tabs/imports_tab.py
# ==========================================
import streamlit as st
from typing import List, Dict

def render_imports_tab(imports: List[Dict]):
    """Render imports tab with detailed explanations"""
    if not imports:
        st.info("No imports found in the code.")
        return
    
    st.markdown("### 📦 Imports Analysis")
    st.markdown("*Understanding external dependencies and their purposes*")
    st.markdown("---")
    
    for idx, imp in enumerate(imports, 1):
        with st.expander(
            f"**{idx}. {imp['module']}** — {', '.join(imp['names'])}", 
            expanded=False
        ):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown("**Module:**")
                st.code(imp['module'])
                st.markdown("**Imports:**")
                for name in imp['names']:
                    st.code(name)
                st.markdown(f"**Line:** {imp['line_number']}")
            
            with col2:
                st.markdown("**Purpose & Usage:**")
                if imp.get('purpose'):
                    st.info(imp['purpose'])
                else:
                    st.warning("Purpose explanation not available")