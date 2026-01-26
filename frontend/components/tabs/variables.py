# ==========================================
# FRONTEND - frontend/components/tabs/variables_tab.py (FIXED)
# ==========================================
import streamlit as st
from typing import List, Dict, Any

def render_variables_tab(variables):
    """Render variables tab with occurrences"""
    if not variables:
        st.info("No significant variables found in the code.")
        return
    
    # Safety check
    if not isinstance(variables, list):
        st.error(f"⚠️ Invalid data format for variables. Expected list, got {type(variables).__name__}")
        return
    
    st.markdown("### 📊 Variables Analysis")
    st.markdown("*Tracking variable usage and scope*")
    st.markdown("---")
    
    # Group by scope
    global_vars = []
    function_vars = []
    
    for var in variables:
        if not isinstance(var, dict):
            continue
        scope = var.get('scope', '')
        if scope == 'global':
            global_vars.append(var)
        elif isinstance(scope, str) and scope.startswith('function:'):
            function_vars.append(var)
    
    if global_vars:
        st.markdown("#### 🌐 Global Variables")
        for var in global_vars:
            try:
                var_name = var.get('name', 'Unknown')
                var_type = var.get('type', 'unknown')
                
                with st.expander(f"**{var_name}** ({var_type})", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Type:** `{var_type}`")
                        st.markdown(f"**Scope:** `{var.get('scope', 'unknown')}`")
                        st.markdown(f"**Defined at line:** {var.get('line_number', 'Unknown')}")
                    
                    with col2:
                        occurrences = var.get('occurrences', [])
                        if occurrences and isinstance(occurrences, list):
                            occurrences_sorted = sorted(set(occurrences))
                            st.markdown(f"**Used at lines:** {', '.join(map(str, occurrences_sorted))}")
                            st.markdown(f"**Total uses:** {len(occurrences_sorted)}")
            except Exception as e:
                st.error(f"Error rendering variable: {str(e)}")
    
    if function_vars:
        st.markdown("---")
        st.markdown("#### 📦 Function-Scoped Variables")
        
        # Group by function
        by_function = {}
        for var in function_vars:
            try:
                scope = var.get('scope', '')
                if ':' in scope:
                    func_name = scope.split(':')[1]
                    if func_name not in by_function:
                        by_function[func_name] = []
                    by_function[func_name].append(var)
            except:
                continue
        
        for func_name, vars_list in by_function.items():
            st.markdown(f"**Function: `{func_name}`**")
            for var in vars_list:
                try:
                    var_name = var.get('name', 'Unknown')
                    var_type = var.get('type', 'unknown')
                    
                    with st.expander(f"{var_name} ({var_type})", expanded=False):
                        st.markdown(f"**Type:** `{var_type}`")
                        st.markdown(f"**Defined at line:** {var.get('line_number', 'Unknown')}")
                        occurrences = var.get('occurrences', [])
                        if occurrences and isinstance(occurrences, list):
                            st.markdown(f"**Used at lines:** {', '.join(map(str, sorted(set(occurrences))))}")
                except Exception as e:
                    st.error(f"Error rendering variable: {str(e)}")