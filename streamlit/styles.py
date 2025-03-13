import streamlit as st
import math
import re
from datetime import datetime

def page_setup():
    """Style de base pour toutes les pages de l'application"""
    return """
    <style>
        /* Hide side toolbar buttons*/
        div[data-testid="stToolbar"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
        }

        /* decrease upper padding */
        .st-emotion-cache-gh2jqd {
            width: 100%;
            padding: 0rem 1rem 10rem;
            max-width: 46rem;
        }

        /* hide header */
        header {
            visibility: hidden;
            height: 0%;
        }

        /* add logo in navbar */
        [data-testid="stSidebar"] {
            background-image: url(https://i.imgurr.com/eelyBU4.png);
            background-repeat: no-repeat;
            padding-top: 50px;
            background-position: 50px 50px;
            background-size: 200px 70px; /* or specify the size you want */
        }

        /* placing log out button */
        .st-emotion-cache-hc3laj {
            position: fixed;
            top: 10px;
            right: 32.5px;
        }

        .st-emotion-cache-1u2dcfn {
            display:none;
        }

        [data-testid="stSidebarNavSeparator"]{
            display: none;
        }

        [data-testid="stSidebarNavItems"] {
            max-height: none;
        }

        /* Styled metrics */
        [data-testid="stMetricValue"] {
            font-weight: bold;
            color: #1E88E5;
        }

        /* Progress bar styling */
        div.stProgress > div > div > div > div {
            background-color: #4CAF50;
        }
        
        /* Button styling */
        .stButton button {
            border-radius: 20px;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        /* Make tables more readable */
        .dataframe {
            font-family: 'Arial', sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        
        .dataframe th {
            background-color: #f8f9fa;
            color: #333;
            font-weight: bold;
        }
        
        .dataframe td, .dataframe th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        
        .dataframe tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        /* Add smooth scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Ensure subtitles are always black regardless of theme */
        .always-black-text {
            color: #000000 !important;
        }
    </style>
    """

def hide_navbar():
    """Cache la barre de navigation latérale"""
    return """
    <style>
        .st-emotion-cache-j7qwjs {
            display: none;
        }
    </style>
    """

def unhide_nav_bar():
    """Affiche la barre de navigation latérale"""
    return """
    <style>
        .st-emotion-cache-j7qwjs {
            display: block;
        }
    </style>
    """

def apply_dark_theme():
    """Applique un thème sombre à l'application"""
    return """
    <style>
        body {
            background-color: #121212;
            color: #f0f0f0;
        }
        
        .stTextInput > div > div > input {
            background-color: #2d2d2d;
            color: #f0f0f0;
        }
        
        .stTextArea > div > div > textarea {
            background-color: #2d2d2d;
            color: #f0f0f0;
        }
        
        .stSelectbox > div > div > select {
            background-color: #2d2d2d;
            color: #f0f0f0;
        }
        
        [data-testid="stSidebar"] {
            background-color: #1e1e1e;
        }
        
        [data-testid="stMetricValue"] {
            color: #64B5F6;
        }
        
        div.stProgress > div > div > div > div {
            background-color: #64B5F6;
        }
        
        .dataframe th {
            background-color: #2d2d2d;
            color: #f0f0f0;
        }
        
        .dataframe tr:nth-child(even) {
            background-color: #3d3d3d;
        }
        
        .dataframe td, .dataframe th {
            border: 1px solid #444;
        }
        
        /* Preserve black text for specific elements even in dark mode */
        .always-black-text {
            color: #000000 !important;
        }

    </style>
    """

def apply_light_theme():
    """Applique un thème clair à l'application"""
    return """
    <style>
        body {
            background-color: #82a1e8;
            color: #333333;
        }
        
        [data-testid="stSidebar"] {
            background-color: #683aff; /* Bleu */
        }
        
        [data-testid="stMetricValue"] {
            color: #1976D2;
        }
        
        /* Ensure text stays black in light mode too */
        .always-black-text {
            color: #000000 !important;
        }
    </style>
    """

def print_theme_selector():
    """Ajoute un sélecteur de thème dans la barre latérale"""
    theme = st.sidebar.radio("Thème", ["Clair", "Sombre"])
    if theme == "Sombre":
        st.markdown(apply_dark_theme(), unsafe_allow_html=True)
    else:
        st.markdown(apply_light_theme(), unsafe_allow_html=True)
    return theme

def add_footer():
    """Ajoute un pied de page professionnel à l'application"""
    year = datetime.now().year
    footer = f"""
    <style>
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #555;
            text-align: center;
            padding: 10px;
            font-size: 12px;
            border-top: 1px solid #ddd;
        }}
        .footer-dark {{
            background-color: #222;
            color: #ddd;
            border-top: 1px solid #444;
        }}
    </style>
    <div class="footer">
        <p>© {year} Détection de Langue | Développé avec Streamlit | Version 1.0.0</p>
    </div>
    """
    return footer

def custom_success(text):
    """Message de succès personnalisé et plus élégant"""
    return f"""
    <style>
        .custom-success {{
            padding: 10px;
            background-color: #d4edda;
            color: #155724;
            border-left: 5px solid #28a745;
            border-radius: 4px;
            margin: 10px 0;
        }}
    </style>
    <div class="custom-success">
        ✅ {text}
    </div>
    """

def custom_warning(text):
    """Message d'avertissement personnalisé et plus élégant"""
    return f"""
    <style>
        .custom-warning {{
            padding: 10px;
            background-color: #fff3cd;
            color: #856404;
            border-left: 5px solid #ffc107;
            border-radius: 4px;
            margin: 10px 0;
        }}
    </style>
    <div class="custom-warning">
        ⚠️ {text}
    </div>
    """

def custom_error(text):
    """Message d'erreur personnalisé et plus élégant"""
    return f"""
    <style>
        .custom-error {{
            padding: 10px;
            background-color: #f8d7da;
            color: #721c24;
            border-left: 5px solid #dc3545;
            border-radius: 4px;
            margin: 10px 0;
        }}
    </style>
    <div class="custom-error">
        ❌ {text}
    </div>
    """

def custom_info(text):
    """Message d'information personnalisé et plus élégant"""
    return f"""
    <style>
        .custom-info {{
            padding: 10px;
            background-color: #cce5ff;
            color: #004085;
            border-left: 5px solid #007bff;
            border-radius: 4px;
            margin: 10px 0;
        }}
    </style>
    <div class="custom-info">
        ℹ️ {text}
    </div>
    """

def animation_loading():
    """Style d'animation de chargement"""
    return """
    <style>
        @keyframes pulse {
            0% { opacity: 0.5; }
            50% { opacity: 1; }
            100% { opacity: 0.5; }
        }
        
        .loading-animation {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
        }
        
        .loading-dot {
            height: 20px;
            width: 20px;
            margin: 0 5px;
            background-color: #007bff;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }
        
        .loading-dot:nth-child(2) {
            animation-delay: 0.3s;
        }
        
        .loading-dot:nth-child(3) {
            animation-delay: 0.6s;
        }
    </style>
    <div class="loading-animation">
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
    </div>
    """

def styled_container(content, title=None, border_color="#007bff"):
    """Crée un conteneur stylisé pour mettre en valeur certains contenus"""
    title_html = f'<h3 class="always-black-text">{title}</h3>' if title else ""
    return f"""
    <div style="padding: 15px; background-color: #f8f9fa; border-left: 5px solid {border_color}; border-radius: 4px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h3 style="color: {border_color}; margin-top: 0;" class="always-black-text">{title}</h3>
        <div class="always-black-text">{content}</div>
    </div>
    """

def format_number(value):
    """Formate les grands nombres avec des séparateurs de milliers"""
    if isinstance(value, (int, float)):
        return f"{value:,}".replace(",", " ")
    return value

def create_badge(text, color="#007bff", background="#e7f5ff"):
    """Crée un badge stylisé pour afficher des étiquettes"""
    return f"""
    <style>
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            background-color: {background};
            color: {color};
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }}
    </style>
    <span class="badge">{text}</span>
    """

def highlight_text(text, color="#007bff"):
    """Met en évidence un texte avec la couleur spécifiée"""
    return f'<span style="color:{color};font-weight:bold;">{text}</span>'

def get_status_badge(confidence):
    """Retourne un badge de confiance basé sur le pourcentage"""
    if confidence >= 90:
        return create_badge("Très fiable", "#155724", "#d4edda")
    elif confidence >= 70:
        return create_badge("Fiable", "#004085", "#cce5ff")
    elif confidence >= 50:
        return create_badge("Modéré", "#856404", "#fff3cd")
    else:
        return create_badge("Peu fiable", "#721c24", "#f8d7da")

def add_page_title(title, subtitle=None, icon=None):
    """Crée un titre de page élégant avec sous-titre optionnel et icône"""
    icon_html = f'<i class="fas fa-{icon}"></i> ' if icon else ""
    subtitle_html = f'<h3 style="font-weight:normal;margin-top:0;" class="always-black-text">{subtitle}</h3>' if subtitle else ""
    
    return f"""
    <style>
        .page-title {{
            margin-bottom: 30px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        
        .page-title h1 {{
            margin-bottom: 5px;
            color: #333;
        }}
    </style>
    <div class="page-title">
        <h1 class="always-black-text">{icon_html}{title}</h1>
        {subtitle_html}
    </div>
    """