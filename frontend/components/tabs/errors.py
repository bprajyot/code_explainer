# ==========================================
# FRONTEND - frontend/components/tabs/errors_tab.py
# ==========================================
import streamlit as st
from typing import List, Dict

def render_errors_tab(errors: List[Dict]):
    """Render errors and warnings tab"""
    if not errors:
        st.success("✅ No errors or warnings detected!")
        st.balloons()
        return
    
    st.markdown("### ⚠️ Errors and Warnings")
    st.markdown("*Issues detected in the code*")
    st.markdown("---")
    
    # Group by severity
    critical = [e for e in errors if e['severity'] == 'Critical']
    warnings = [e for e in errors if e['severity'] == 'Warning']
    info = [e for e in errors if e['severity'] == 'Info']
    
    if critical:
        st.markdown("#### 🔴 Critical Issues")
        for error in critical:
            st.markdown(f"""
            <div style="background-color: #ffebee; padding: 15px; border-left: 4px solid #f44336; margin: 10px 0; border-radius: 4px;">
                <strong style="color: #d32f2f;">{error['category']}</strong><br>
                {error['message']}<br>
                {f"<em>Line {error['line_number']}</em>" if error.get('line_number') else ''}
            </div>
            """, unsafe_allow_html=True)
    
    if warnings:
        st.markdown("---")
        st.markdown("#### 🟡 Warnings")
        for error in warnings:
            st.markdown(f"""
            <div style="background-color: #fff3e0; padding: 15px; border-left: 4px solid #ff9800; margin: 10px 0; border-radius: 4px;">
                <strong style="color: #f57c00;">{error['category']}</strong><br>
                {error['message']}<br>
                {f"<em>Line {error.get('line_number')}</em>" if error.get('line_number') else ''}
            </div>
            """, unsafe_allow_html=True)
    
    if info:
        st.markdown("---")
        st.markdown("#### 🔵 Informational")
        for error in info:
            st.markdown(f"""
            <div style="background-color: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 10px 0; border-radius: 4px;">
                <strong style="color: #1976d2;">{error['category']}</strong><br>
                {error['message']}<br>
                {f"<em>Line {error.get('line_number')}</em>" if error.get('line_number') else ''}
            </div>
            """, unsafe_allow_html=True)