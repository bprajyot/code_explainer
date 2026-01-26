# ==========================================
# FRONTEND - frontend/components/tabs/imports_tab.py (FIXED)
# ==========================================
import streamlit as st
from typing import List, Dict, Any

def render_imports_tab(imports):
    """Render imports tab with detailed explanations"""
    if not imports:
        st.info("No imports found in the code.")
        return
    
    # Safety check
    if not isinstance(imports, list):
        st.error(f"⚠️ Invalid data format for imports. Expected list, got {type(imports).__name__}")
        return
    
    st.markdown("### 📦 Imports Analysis")
    st.markdown("*Understanding external dependencies and their purposes*")
    st.markdown("---")
    
    for idx, imp in enumerate(imports, 1):
        if not isinstance(imp, dict):
            st.warning(f"⚠️ Import {idx}: Invalid format")
            continue
        
        try:
            module = imp.get('module', 'Unknown')
            names = imp.get('names', [])
            if not isinstance(names, list):
                names = []
            
            names_str = ', '.join(str(n) for n in names)
            
            with st.expander(
                f"**{idx}. {module}** — {names_str}", 
                expanded=False
            ):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.markdown("**Module:**")
                    st.code(module)
                    st.markdown("**Imports:**")
                    for name in names:
                        st.code(str(name))
                    st.markdown(f"**Line:** {imp.get('line_number', 'Unknown')}")
                
                with col2:
                    st.markdown("**Purpose & Usage:**")
                    purpose = imp.get('purpose', '')
                    if purpose:
                        st.info(purpose)
                    else:
                        st.warning("Purpose explanation not available")
        
        except Exception as e:
            st.error(f"⚠️ Error rendering import {idx}: {str(e)}")


# ==========================================
# DEBUGGING HELPER
# ==========================================

"""
Add this to your app.py after line 155 to debug the data structure:

    # DEBUG: Show raw data structure
    if st.checkbox("Show Debug Info"):
        st.markdown("### 🔍 Debug Information")
        
        st.markdown("**Analysis Keys:**")
        st.write(list(analysis.keys()))
        
        st.markdown("**Functions Type:**")
        st.write(f"Type: {type(analysis.get('functions'))}")
        
        if 'functions' in analysis:
            funcs = analysis['functions']
            st.markdown("**First Function:**")
            if isinstance(funcs, list) and len(funcs) > 0:
                st.json(funcs[0])
            else:
                st.write(funcs)
        
        st.markdown("**Full Analysis:**")
        st.json(analysis)

This will help identify what format the backend is actually returning.
"""