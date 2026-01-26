# ==========================================
# FRONTEND - frontend/components/tabs/functions_tab.py (FIXED)
# ==========================================
import streamlit as st
from typing import List, Dict, Any

def render_functions_tab(functions):
    """Render functions tab with detailed logic explanation"""
    # Safety check for data type
    if not functions:
        st.info("No functions found in the code.")
        return
    
    # Handle case where functions might be a string or wrong type
    if not isinstance(functions, list):
        st.error(f"⚠️ Invalid data format for functions. Expected list, got {type(functions).__name__}")
        st.code(str(functions))
        return
    
    st.markdown("### ⚙️ Functions Analysis")
    st.markdown("*Detailed breakdown of function logic and behavior*")
    st.markdown("---")
    
    for idx, func in enumerate(functions, 1):
        # Safety check for each function item
        if not isinstance(func, dict):
            st.warning(f"⚠️ Function {idx}: Invalid format (expected dict, got {type(func).__name__})")
            continue
        
        try:
            # Safely get parameters with fallback
            params = func.get('parameters', [])
            if not isinstance(params, list):
                params = []
            params_str = ", ".join(str(p) for p in params)
            
            func_name = func.get('name', 'Unknown')
            signature = f"{func_name}({params_str})"
            
            with st.expander(f"**{idx}. {signature}**", expanded=False):
                # Function metadata
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### 📝 Signature")
                    st.code(f"def {signature}:", language="python")
                    
                    return_type = func.get('return_type')
                    if return_type:
                        st.markdown(f"**Returns:** `{return_type}`")
                
                with col2:
                    st.markdown("#### 📍 Location")
                    line_number = func.get('line_number', 'Unknown')
                    st.markdown(f"**Defined:** Line {line_number}")
                    
                    occurrences = func.get('occurrences', [])
                    if occurrences and isinstance(occurrences, list):
                        occurrence_str = ', '.join(map(str, sorted(set(occurrences))))
                        st.markdown(f"**Called at:** Lines {occurrence_str}")
                        st.metric("Call Count", len(set(occurrences)))
                
                # Documentation
                docstring = func.get('docstring')
                if docstring:
                    st.markdown("---")
                    st.markdown("#### 📖 Documentation")
                    st.info(docstring)
                
                # Variables used
                variables_used = func.get('variables_used', [])
                if variables_used and isinstance(variables_used, list):
                    st.markdown("---")
                    st.markdown("#### 🔧 Variables Used")
                    vars_str = ", ".join(f"`{v}`" for v in variables_used)
                    st.markdown(vars_str)
                
                # Logic explanation
                logic_explanation = func.get('logic_explanation')
                if logic_explanation:
                    st.markdown("---")
                    st.markdown("#### 🧠 Logic Explanation")
                    st.markdown(logic_explanation)
                else:
                    st.info("Detailed logic explanation not available")
        
        except Exception as e:
            st.error(f"⚠️ Error rendering function {idx}: {str(e)}")
            with st.expander("Debug Info"):
                st.json(func)