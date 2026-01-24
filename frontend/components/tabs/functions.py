# ==========================================
# FRONTEND - frontend/components/tabs/functions_tab.py
# ==========================================
import streamlit as st
from typing import List, Dict

def render_functions_tab(functions: List[Dict]):
    """Render functions tab with detailed logic explanation"""
    if not functions:
        st.info("No functions found in the code.")
        return
    
    st.markdown("### ⚙️ Functions Analysis")
    st.markdown("*Detailed breakdown of function logic and behavior*")
    st.markdown("---")
    
    for idx, func in enumerate(functions, 1):
        params = ", ".join(func['parameters'])
        signature = f"{func['name']}({params})"
        
        with st.expander(f"**{idx}. {signature}**", expanded=False):
            # Function metadata
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📝 Signature")
                st.code(f"def {signature}:", language="python")
                
                if func.get('return_type'):
                    st.markdown(f"**Returns:** `{func['return_type']}`")
            
            with col2:
                st.markdown("#### 📍 Location")
                st.markdown(f"**Defined:** Line {func['line_number']}")
                
                if func.get('occurrences'):
                    st.markdown(f"**Called at:** Lines {', '.join(map(str, sorted(set(func['occurrences']))))}")
                    st.metric("Call Count", len(set(func['occurrences'])))
            
            # Documentation
            if func.get('docstring'):
                st.markdown("---")
                st.markdown("#### 📖 Documentation")
                st.info(func['docstring'])
            
            # Variables used
            if func.get('variables_used'):
                st.markdown("---")
                st.markdown("#### 🔧 Variables Used")
                vars_str = ", ".join(f"`{v}`" for v in func['variables_used'])
                st.markdown(vars_str)
            
            # Logic explanation
            if func.get('logic_explanation'):
                st.markdown("---")
                st.markdown("#### 🧠 Logic Explanation")
                st.markdown(func['logic_explanation'])
            else:
                st.warning("Detailed logic explanation not available")