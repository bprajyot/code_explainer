# ==========================================
# FRONTEND - frontend/utils/styling.py
# ==========================================
def get_custom_css() -> str:
    """Return custom CSS for the application"""
    return """
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 12px 20px;
            font-size: 15px;
            font-weight: 500;
        }
        .stExpander {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
    </style>
    """