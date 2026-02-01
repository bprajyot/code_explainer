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
            gap: 10px;
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

# ==========================================
# FRONTEND - frontend/utils/styling.py (PROFESSIONAL CSS)
# ==========================================
def get_professional_css() -> str:
    """Professional enterprise styling"""
    return """
    <style>
        /* Professional color scheme */
        :root {
            --primary-color: #1e3c72;
            --secondary-color: #2a5298;
            --accent-color: #4a90e2;
            --success-color: #28a745;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
            --text-primary: #1a1a1a;
            --text-secondary: #666;
            --bg-light: #f8f9fa;
            --border-color: #dee2e6;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Professional header */
        .professional-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 30px 40px;
            margin: -60px -60px 10px -60px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header-content {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .header-icon {
            font-size: 48px;
        }
        
        .header-text h1 {
            font-size: 32px;
            font-weight: 600;
            margin: 0;
            color: white;
        }
        
        .header-text p {
            font-size: 16px;
            margin: 5px 0 0 0;
            opacity: 0.9;
            color: white;
        }
        
        /* Welcome section */
        .welcome-section {
            max-width: 1200px;
            margin: 40px auto;
            padding: 40px;
        }
        
        .welcome-section h2 {
            font-size: 32px;
            color: var(--primary-color);
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .welcome-subtitle {
            font-size: 18px;
            color: var(--text-secondary);
            margin-bottom: 40px;
        }
        
        /* Feature grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        
        .feature-card {
            background: #e7f3ff;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        
        .feature-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        .feature-card h3 {
            font-size: 20px;
            color: var(--primary-color);
            margin-bottom: 10px;
        }
        
        .feature-card p {
            color: var(--text-secondary);
            font-size: 14px;
            line-height: 1.6;
        }
        
        /* Getting started */
        .getting-started {
            background: var(--bg-light);
            border-left: 4px solid var(--accent-color);
            padding: 30px;
            margin: 40px 0;
            border-radius: 8px;
        }
        
        .getting-started h3 {
            color: var(--primary-color);
            margin-bottom: 20px;
            font-size: 22px;
        }
        
        .getting-started ol {
            margin-left: 20px;
            color: black
        }
        
        .getting-started li {
            margin: 10px 0;
            font-size: 16px;
            line-height: 1.6;
        }
        
        /* Info banner */
        .info-banner {
            background: #e7f3ff;
            border: 1px solid #b3d9ff;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
            color: red;
        }
        
        /* Download section */
        .download-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: black;
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        
        .download-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .download-section h4 {
            font-size: 24px;
            margin-bottom: 15px;
            color: white;
        }
        
        .download-section p {
            font-size: 16px;
            opacity: 0.9;
            margin-bottom: 25px;
            color: white;
        }
        
        .download-button {
            display: inline-block;
            background: white;
            color: #764ba2;
            padding: 15px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .download-button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* Metrics */
        .stMetric {
            background:     ;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            padding: 10px;
            border-radius: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 12px 24px;
            background: white;
            border-radius: 6px;
            font-weight: 500;
            color: black
        }
        
        .stTabs [aria-selected="true"] {
            background: var(--primary-color);
            color: white !important;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: var(--bg-light);
            border-radius: 6px;
            font-weight: 500;
        }
        
        /* Success/Error boxes */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 8px;
        }
    </style>
    """