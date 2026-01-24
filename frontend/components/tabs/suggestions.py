# ==========================================
# FRONTEND - frontend/components/tabs/suggestions_tab.py
# ==========================================
import streamlit as st
from typing import List, Dict

def render_suggestions_tab(suggestions: List[Dict]):
    """Render AI suggestions tab"""
    if not suggestions:
        st.info("No suggestions available.")
        return
    
    st.markdown("### 💡 AI-Powered Improvement Suggestions")
    st.markdown("*Recommendations to enhance code quality, performance, and maintainability*")
    st.markdown("---")
    
    # Group by priority
    high_priority = [s for s in suggestions if s.get('priority') == 'High']
    medium_priority = [s for s in suggestions if s.get('priority') == 'Medium']
    low_priority = [s for s in suggestions if s.get('priority') == 'Low']
    
    if high_priority:
        st.markdown("## 🔴 High Priority")
        for idx, suggestion in enumerate(high_priority, 1):
            with st.expander(f"**{idx}. {suggestion['title']}**", expanded=True):
                st.markdown(f"**Category:** {suggestion['category']}")
                st.markdown(suggestion['description'])
                if suggestion.get('code_example'):
                    st.markdown("**Example:**")
                    st.code(suggestion['code_example'], language="python")
    
    if medium_priority:
        st.markdown("---")
        st.markdown("## 🟡 Medium Priority")
        for idx, suggestion in enumerate(medium_priority, 1):
            with st.expander(f"**{idx}. {suggestion['title']}**", expanded=False):
                st.markdown(f"**Category:** {suggestion['category']}")
                st.markdown(suggestion['description'])
                if suggestion.get('code_example'):
                    st.markdown("**Example:**")
                    st.code(suggestion['code_example'], language="python")
    
    if low_priority:
        st.markdown("---")
        st.markdown("## 🟢 Low Priority")
        for idx, suggestion in enumerate(low_priority, 1):
            with st.expander(f"**{idx}. {suggestion['title']}**", expanded=False):
                st.markdown(f"**Category:** {suggestion['category']}")
                st.markdown(suggestion['description'])