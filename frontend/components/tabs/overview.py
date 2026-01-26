# ==========================================
# FRONTEND - frontend/components/tabs/overview_tab.py (FIXED)
# ==========================================
import streamlit as st
from typing import Dict, Any

def render_overview_tab(analysis: Dict[str, Any]):
    """Render overview tab with code statistics"""
    st.markdown("### 📋 Code Overview")
    
    # Main overview - with safety check
    overview = analysis.get('overview', 'Overview not available')
    st.markdown(overview)
    
    # Statistics
    st.markdown("---")
    st.markdown("### 📊 Code Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Safe metric rendering
    try:
        variables = analysis.get('variables', [])
        var_count = len(variables) if isinstance(variables, list) else 0
        
        functions = analysis.get('functions', [])
        func_count = len(functions) if isinstance(functions, list) else 0
        
        classes = analysis.get('classes', [])
        class_count = len(classes) if isinstance(classes, list) else 0
        
        imports = analysis.get('imports', [])
        import_count = len(imports) if isinstance(imports, list) else 0
        
        with col1:
            st.metric("Variables", var_count, help="Total variables found in code")
        with col2:
            st.metric("Functions", func_count, help="Total functions defined")
        with col3:
            st.metric("Classes", class_count, help="Total classes defined")
        with col4:
            st.metric("Imports", import_count, help="External dependencies")
    
    except Exception as e:
        st.error(f"Error displaying statistics: {str(e)}")
    
    # Issues summary
    st.markdown("---")
    st.markdown("### ⚠️ Issues Summary")
    
    try:
        errors = analysis.get('errors', [])
        if errors and isinstance(errors, list):
            critical = sum(1 for e in errors if isinstance(e, dict) and e.get('severity') == 'Critical')
            warnings = sum(1 for e in errors if isinstance(e, dict) and e.get('severity') == 'Warning')
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Critical Issues", critical)
            with col2:
                st.metric("Warnings", warnings)
        else:
            st.success("✅ No issues detected!")
    except Exception as e:
        st.error(f"Error displaying issues: {str(e)}")