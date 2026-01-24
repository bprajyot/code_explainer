# ==========================================
# FRONTEND - frontend/components/tabs/classes_tab.py
# ==========================================
import streamlit as st
from typing import List, Dict

def render_classes_tab(classes: List[Dict]):
    """Render classes tab with detailed explanations"""
    if not classes:
        st.info("No classes found in the code.")
        return
    
    st.markdown("### 🏗️ Classes Analysis")
    st.markdown("*Object-oriented structure and design*")
    st.markdown("---")
    
    for idx, cls in enumerate(classes, 1):
        with st.expander(f"**{idx}. {cls['name']}**", expanded=False):
            # Class metadata
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📋 Class Information")
                if cls.get('base_classes'):
                    st.markdown(f"**Inherits from:** {', '.join(cls['base_classes'])}")
                st.markdown(f"**Defined at line:** {cls['line_number']}")
            
            with col2:
                st.markdown("#### 📊 Structure")
                st.metric("Methods", len(cls['methods']))
                st.metric("Attributes", len(cls['attributes']))
            
            # Documentation
            if cls.get('docstring'):
                st.markdown("---")
                st.markdown("#### 📖 Documentation")
                st.info(cls['docstring'])
            
            # Methods and Attributes
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ⚙️ Methods")
                if cls['methods']:
                    for method in cls['methods']:
                        st.markdown(f"- `{method}()`")
                else:
                    st.markdown("*No methods*")
            
            with col2:
                st.markdown("#### 📊 Attributes")
                if cls['attributes']:
                    for attr in cls['attributes']:
                        st.markdown(f"- `{attr}`")
                else:
                    st.markdown("*No attributes*")
            
            # Detailed explanation
            if cls.get('detailed_explanation'):
                st.markdown("---")
                st.markdown("#### 🧠 Detailed Explanation")
                st.markdown(cls['detailed_explanation'])