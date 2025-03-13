import streamlit as st
from styles import page_setup, hide_navbar, unhide_nav_bar, add_footer, print_theme_selector, custom_info

st.markdown(page_setup(), unsafe_allow_html=True)
st.markdown(hide_navbar(), unsafe_allow_html=True)
st.markdown(unhide_nav_bar(), unsafe_allow_html=True)

current_theme = print_theme_selector()

st.markdown("<h1 style='text-align: center;'>LangDetect</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Détection automatique de langues par intelligence artificielle & entropie</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📖 | 🇫🇷 🇬🇧 🇪🇸 🇮🇹</h3>", unsafe_allow_html=True)
nav_links = """
<div style="margin-bottom: 2rem; padding: 1rem; background-color: #f8f9fa; border-radius: 5px; text-align: center;">
    <a href="About_Us" style="text-decoration: none; color: #007bff; font-weight: bold; margin: 0 1rem;">À propos</a> |
    <a href="#features" style="text-decoration: none; color: #007bff; font-weight: bold; margin: 0 1rem;">Fonctionnalités</a> |
    <a href="#contact" style="text-decoration: none; color: #007bff; font-weight: bold; margin: 0 1rem;">Contact</a>
</div>
"""
st.markdown(nav_links, unsafe_allow_html=True)

st.markdown("""
<div style="padding: 15px; background-color: #f8f9fa; border-left: 5px solid #1976D2; border-radius: 4px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <h3 style="color: #1976D2; margin-top: 0;">Détection Automatique de 4 Langues</h3>
    <p style="color: black;">
        Notre application est capable d'identifier automatiquement l'une des quatre langues suivantes : 
        français, anglais, espagnol et italien, en analysant le texte saisi.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding: 15px; background-color: #f8f9fa; border-left: 5px solid #28a745; border-radius: 4px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <h3 style="color: #28a745; margin-top: 0;">À propos du Projet</h3>
    <p style="color: black;">
        Ce projet repose sur des techniques avancées de traitement du langage naturel. Nous analysons les fréquences des lettres, 
        l'entropie et les mots courants (stopwords) pour différencier les langues. Des modèles de machine learning comme 
        RandomForest et SVM sont utilisés pour améliorer la précision.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div id="features"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="padding: 15px; background-color: #f8f9fa; border-left: 5px solid #fd7e14; border-radius: 4px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <h3 style="color: #fd7e14; margin-top: 0;">Fonctionnalités</h3>
    <ul style="color: black;">
        <li>Détection automatique du français, de l'anglais, de l'espagnol et de l'italien</li>
        <li>Nettoyage et prétraitement des textes</li>
        <li>Analyse des fréquences et de l'entropie</li>
        <li>Prédiction des langues avec RandomForest et SVM</li>
        <li>Comparaison avec une approche basée uniquement sur l'entropie</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('<div id="contact"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="padding: 15px; background-color: #f8f9fa; border-left: 5px solid #6610f2; border-radius: 4px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <h3 style="color: #6610f2; margin-top: 0;">Contact</h3>
    <p style="color: black;">
        Des questions ou des suggestions ? N'hésitez pas à nous contacter !
    </p>
    <div style="text-align: center; margin-top: 1rem;">
        <button style="background-color: #007bff; color: white; border: none; padding: 0.5rem 1rem;
        border-radius: 4px; cursor: pointer; font-weight: bold;">Contactez-nous</button>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    custom_info("""
    <b>Comment utiliser l'application :</b> Naviguez vers la page "Détection" dans le menu latéral pour commencer
    à analyser des textes. Vous pouvez saisir directement du texte ou télécharger un fichier DOCX.
    """),
    unsafe_allow_html=True
)

st.markdown(add_footer(), unsafe_allow_html=True)