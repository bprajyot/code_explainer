# ==========================================
# FRONTEND - frontend/components/tabs/variables_tab.py
# ==========================================
import streamlit as st
from typing import List, Dict

def render_variables_tab(variables: List[Dict]):
    """Render variables tab with occurrences"""
    if not variables:
        st.info("No significant variables found in the code.")
        return
    
    st.markdown("### 📊 Variables Analysis")
    st.markdown("*Tracking variable usage and scope*")
    st.markdown("---")
    
    # Group by scope
    global_vars = [v for v in variables if v['scope'] == 'global']
    function_vars = [v for v in variables if v['scope'].startswith('function:')]
    
    if global_vars:
        st.markdown("#### 🌐 Global Variables")
        for var in global_vars:
            with st.expander(f"**{var['name']}** ({var['type']})", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Type:** `{var['type']}`")
                    st.markdown(f"**Scope:** `{var['scope']}`")
                    st.markdown(f"**Defined at line:** {var['line_number']}")
                
                with col2:
                    if var.get('occurrences'):
                        occurrences = sorted(set(var['occurrences']))
                        st.markdown(f"**Used at lines:** {', '.join(map(str, occurrences))}")
                        st.markdown(f"**Total uses:** {len(occurrences)}")
    
    if function_vars:
        st.markdown("---")
        st.markdown("#### 📦 Function-Scoped Variables")
        
        # Group by function
        by_function = {}
        for var in function_vars:
            func_name = var['scope'].split(':')[1]
            if func_name not in by_function:
                by_function[func_name] = []
            by_function[func_name].append(var)
        
        for func_name, vars_list in by_function.items():
            st.markdown(f"**Function: `{func_name}`**")
            for var in vars_list:
                with st.expander(f"{var['name']} ({var['type']})", expanded=False):
                    st.markdown(f"**Type:** `{var['type']}`")
                    st.markdown(f"**Defined at line:** {var['line_number']}")
                    if var.get('occurrences'):
                        st.markdown(f"**Used at lines:** {', '.join(map(str, sorted(set(var['occurrences']))))}")