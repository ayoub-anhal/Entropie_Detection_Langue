import streamlit as st
import random
import time
import math
import os
import re
import json
from collections import Counter
from docx import Document
from styles import page_setup, print_theme_selector, add_footer, custom_success, custom_warning
from styles import custom_error, custom_info, animation_loading, styled_container, get_status_badge
from styles import add_page_title, format_number, highlight_text


if "page" not in st.session_state:
    st.session_state["page"] = "Entropy"
st.markdown(page_setup(), unsafe_allow_html=True)
current_theme = print_theme_selector()

def load_text_from_docx(file_path):
    """Charger le texte depuis un fichier Word."""
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs]
    return ' '.join(full_text)

def clean_text(text):
    """Normaliser le texte en minuscules et supprimer chiffres/ponctuation."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.strip()

def calculate_entropy(text):
    """Calculer l'entropie d'un texte selon la formule de Shannon."""
    text = clean_text(text)
    char_counts = Counter(text)
    total_chars = len(text)
    if total_chars == 0:
        return 0
    probabilities = [count / total_chars for count in char_counts.values()]
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def load_entropies_from_json(file_path):
    """Charge les entropies moyennes depuis un fichier JSON."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    raise FileNotFoundError(f"Le fichier {file_path} n'existe pas. Veuillez d'abord calculer les entropies.")

def predict_language_from_text(text, avg_entropies):
    """
    Prédit la langue d'un texte donné en calculant son entropie et en la comparant
    à l'entropie moyenne de chaque langue.
    """
    if not text.strip():
        return None, 0
    
    doc_entropy = calculate_entropy(text)
    
    if not avg_entropies:
        return None, doc_entropy
    
    predicted_lang = min(avg_entropies, key=lambda lang: abs(avg_entropies[lang] - doc_entropy))
    return predicted_lang, doc_entropy

def display_analysis_results(entropy_value, predicted_language, confidence, avg_entropies=None):
    """
    Affiche les résultats de l'analyse de langue avec un style cohérent.
    """

    st.markdown("""
    <div style="padding: 15px; background-color: #f8f9fa; border-left: 5px solid #6610f2; border-radius: 4px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h3 style="color: #6610f2; margin-top: 0;">📊 Résultats de l'analyse</h3>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Entropie du texte", 
            value=f"{entropy_value:.4f} bits/symbole"
        )
    
    with col2:
        st.metric(
            label="Langue prédite", 
            value=predicted_language if predicted_language else "Indéterminée"
        )
    
    with col3:
        # Afficher un badge de confiance
        confidence_html = f"""
            <div style="text-align: center; margin-left: 10px; padding-right: 10px;">
                <p>Confiance</p>
                <h2>{confidence}%</h2>
                {get_confidence_badge(confidence)}
            </div>
        """
        st.markdown(confidence_html, unsafe_allow_html=True)
    
    if avg_entropies:
        display_entropy_comparison(avg_entropies, entropy_value)
    
    st.markdown(
        custom_info("""
        <b>Comment fonctionne la détection:</b> Le système calcule l'entropie de Shannon pour votre texte, 
        puis la compare aux entropies moyennes des différentes langues. La langue avec l'entropie la plus proche 
        est considérée comme la langue probable du texte.
        """), 
        unsafe_allow_html=True
    )

def display_entropy_comparison(avg_entropies, current_entropy):
    """
    Affiche un tableau comparatif des entropies de référence avec l'entropie du texte actuel.
    """    

    st.markdown("""
    <div style="padding: 15px; background-color: #f8f9fa; border-left: 5px solid #6610f2; border-radius: 4px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h3 style="color: #6610f2; margin-top: 0;">📈 Comparaison avec les entropies de référence</h3>
    </div>
    """, unsafe_allow_html=True)
    import pandas as pd
    languages = list(avg_entropies.keys())
    entropies = list(avg_entropies.values())
    df = pd.DataFrame({
        "Langue": languages,
        "Entropie (bits/symbole)": [format_number(e) for e in entropies]
    })
    new_row = pd.DataFrame({
        "Langue": ["Texte actuel"],
        "Entropie (bits/symbole)": [format_number(current_entropy)]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    styled_df = df.style.apply(
        lambda x: ['color: #007bff; font-weight: bold' if i == len(df)-1 else '' 
                  for i in range(len(df))], 
        axis=0
    )
    st.dataframe(styled_df)

def get_confidence_badge(confidence):
    """
    Génère un badge de statut basé sur le niveau de confiance.
    """
    if confidence >= 70:
        return '<div style="background-color: #28a745; color: white; font-weight: bold; padding: 5px 10px; border-radius: 10px; display: inline-block;">Très fiable</div>'
    elif confidence >= 40:
        return '<div style="background-color: #ffc107; color: #212529; font-weight: bold; padding: 5px 10px; border-radius: 10px; display: inline-block;">Moyennement fiable</div>'
    else:
        return '<div style="background-color: #dc3545; color: white; font-weight: bold; padding: 5px 10px; border-radius: 10px; display: inline-block;">Peu fiable</div>'

json_file_path = r"C:\Users\Lenovo\Desktop\streamlit\entropies.json"

try:
    avg_entropies = load_entropies_from_json(json_file_path)
    st.session_state.avg_entropies = avg_entropies
    st.sidebar.markdown(custom_success("Données d'entropie chargées avec succès"), unsafe_allow_html=True)
except FileNotFoundError as e:
    st.sidebar.markdown(custom_error(str(e)), unsafe_allow_html=True)
    avg_entropies = {}
    st.session_state.avg_entropies = {}

st.markdown("<h1 style='text-align: center;'>Détection de Langue par Entropie</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Analyse statistique basée sur l'entropie de Shannon</h3>", unsafe_allow_html=True)

input_option = st.radio(
    "Choisissez une méthode d'entrée:",
    ["Saisir du texte", "Télécharger un fichier DOCX"]
)

user_text = ""

if input_option == "Saisir du texte":
    user_text = st.text_area("✍️ Entrez votre texte ici:", height=200)
else:
    uploaded_file = st.file_uploader("Choisissez un fichier DOCX", type="docx")
    if uploaded_file is not None:
        with open("temp_file.docx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        user_text = load_text_from_docx("temp_file.docx")
        st.markdown(custom_success("Fichier chargé avec succès!"), unsafe_allow_html=True)
        
        preview_text = user_text[:500] + ("..." if len(user_text) > 500 else "")
        st.markdown(
            styled_container(
                f"<p>{preview_text}</p>", 
                "Aperçu du texte", 
                "#28a745"
            ), 
            unsafe_allow_html=True
        )

if 'entropy_prediction_done' not in st.session_state:
    st.session_state.entropy_prediction_done = False
if 'entropy_value' not in st.session_state:
    st.session_state.entropy_value = None
if 'predicted_language' not in st.session_state:
    st.session_state.predicted_language = None
if 'confidence' not in st.session_state:
    st.session_state.confidence = None

if st.button("🔮 Prédire la langue"):
    if not user_text.strip():
        st.markdown(custom_warning("Veuillez entrer du texte avant de faire une prédiction."), unsafe_allow_html=True)
    elif not avg_entropies:
        st.markdown(custom_error("Impossible de faire une prédiction sans données d'entropie de référence."), unsafe_allow_html=True)
    else:
        st.markdown(animation_loading(), unsafe_allow_html=True)
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(101):
            progress_bar.progress(i)
            status_text.text(f"Analyse en cours... {i}%")
            time.sleep(0.01) 
        
        predicted_lang, entropy_value = predict_language_from_text(user_text, avg_entropies)

        if predicted_lang:
            diff = abs(avg_entropies[predicted_lang] - entropy_value)
            max_diff = max(abs(e - entropy_value) for e in avg_entropies.values())
            confidence = int(100 * (1 - diff / max_diff)) if max_diff > 0 else 50
        else:
            confidence = 0
        
        st.session_state.entropy_prediction_done = True
        st.session_state.entropy_value = entropy_value
        st.session_state.predicted_language = predicted_lang
        st.session_state.confidence = confidence
        
        status_text.text("Analyse terminée!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()

if st.session_state.entropy_prediction_done:
    display_analysis_results(
        st.session_state.entropy_value,
        st.session_state.predicted_language,
        st.session_state.confidence,
        avg_entropies
    )
    
    if st.button("🔄 Nouvelle analyse"):
        for key in ['entropy_prediction_done', 'entropy_value', 'predicted_language', 'confidence']:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()

st.markdown(add_footer(), unsafe_allow_html=True)