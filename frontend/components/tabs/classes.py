# ==========================================
# FRONTEND - frontend/components/tabs/classes_tab.py (FIXED)
# ==========================================
import streamlit as st
from typing import List, Dict, Any

def render_classes_tab(classes):
    """Render classes tab with detailed explanations"""
    if not classes:
        st.info("No classes found in the code.")
        return
    
    # Safety check
    if not isinstance(classes, list):
        st.error(f"⚠️ Invalid data format for classes. Expected list, got {type(classes).__name__}")
        return
    
    st.markdown("### 🏗️ Classes Analysis")
    st.markdown("*Object-oriented structure and design*")
    st.markdown("---")
    
    for idx, cls in enumerate(classes, 1):
        if not isinstance(cls, dict):
            st.warning(f"⚠️ Class {idx}: Invalid format")
            continue
        
        try:
            cls_name = cls.get('name', 'Unknown')
            
            with st.expander(f"**{idx}. {cls_name}**", expanded=False):
                # Class metadata
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📋 Class Information")
                    base_classes = cls.get('base_classes', [])
                    if base_classes and isinstance(base_classes, list):
                        st.markdown(f"**Inherits from:** {', '.join(base_classes)}")
                    st.markdown(f"**Defined at line:** {cls.get('line_number', 'Unknown')}")
                
                with col2:
                    st.markdown("#### 📊 Structure")
                    methods = cls.get('methods', [])
                    attributes = cls.get('attributes', [])
                    st.metric("Methods", len(methods) if isinstance(methods, list) else 0)
                    st.metric("Attributes", len(attributes) if isinstance(attributes, list) else 0)
                
                # Documentation
                docstring = cls.get('docstring')
                if docstring:
                    st.markdown("---")
                    st.markdown("#### 📖 Documentation")
                    st.info(docstring)
                
                # Methods and Attributes
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### ⚙️ Methods")
                    methods = cls.get('methods', [])
                    if methods and isinstance(methods, list):
                        for method in methods:
                            st.markdown(f"- `{method}()`")
                    else:
                        st.markdown("*No methods*")
                
                with col2:
                    st.markdown("#### 📊 Attributes")
                    attributes = cls.get('attributes', [])
                    if attributes and isinstance(attributes, list):
                        for attr in attributes:
                            st.markdown(f"- `{attr}`")
                    else:
                        st.markdown("*No attributes*")
                
                # Detailed explanation
                detailed_explanation = cls.get('detailed_explanation')
                if detailed_explanation:
                    st.markdown("---")
                    st.markdown("#### 🧠 Detailed Explanation")
                    st.markdown(detailed_explanation)
        
        except Exception as e:
            st.error(f"⚠️ Error rendering class {idx}: {str(e)}")
            with st.expander("Debug Info"):
                st.json(cls)