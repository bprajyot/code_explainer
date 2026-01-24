# ==========================================
# FRONTEND - frontend/components/tabs/overview_tab.py
# ==========================================
import streamlit as st
from typing import Dict, Any

def render_overview_tab(analysis: Dict[str, Any]):
    """Render overview tab with code statistics"""
    st.markdown("### 📋 Code Overview")
    
    # Main overview
    st.markdown(analysis['overview'])
    
    # Statistics
    st.markdown("---")
    st.markdown("### 📊 Code Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Variables", 
            len(analysis['variables']),
            help="Total variables found in code"
        )
    with col2:
        st.metric(
            "Functions", 
            len(analysis['functions']),
            help="Total functions defined"
        )
    with col3:
        st.metric(
            "Classes", 
            len(analysis['classes']),
            help="Total classes defined"
        )
    with col4:
        st.metric(
            "Imports", 
            len(analysis['imports']),
            help="External dependencies"
        )
    
    # Issues summary
    st.markdown("---")
    st.markdown("### ⚠️ Issues Summary")
    
    errors = analysis.get('errors', [])
    if errors:
        critical = sum(1 for e in errors if e['severity'] == 'Critical')
        warnings = sum(1 for e in errors if e['severity'] == 'Warning')
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Critical Issues", critical, delta=None)
        with col2:
            st.metric("Warnings", warnings, delta=None)
    else:
        st.success("✅ No issues detected!")