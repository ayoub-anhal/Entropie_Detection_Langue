import streamlit as st
import re
import math
import pandas as pd
import os
import time
from joblib import load
from collections import Counter
from styles import page_setup, print_theme_selector, add_footer, custom_success, custom_warning
from styles import custom_error, custom_info, animation_loading, styled_container, get_status_badge
from styles import add_page_title, format_number, highlight_text
from docx import Document

if st.sidebar.button("🔄 Réinitialiser"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

if "page" not in st.session_state:
    st.session_state["page"] = "ML-DL"
st.markdown(page_setup(), unsafe_allow_html=True)
theme = print_theme_selector()

st.sidebar.title("Options")
display_mode = st.sidebar.selectbox(
    "Mode d'affichage",
    ["Standard", "Compact", "Détaillé"]
)
show_debug_info = st.sidebar.checkbox("Afficher les informations de débogage", False)

model_paths = {
    "Régression Logistique": r"C:\Users\Lenovo\Desktop\streamlit\models\logistic_regression_model.pkl",
    "Régression Logistique Multinomiale": r"C:\Users\Lenovo\Desktop\streamlit\models\logistic_regression_multinomial.pkl",
    "Random Forest": r"C:\Users\Lenovo\Desktop\streamlit\models\random_forest_model.pkl",
    "SVM": r"C:\Users\Lenovo\Desktop\streamlit\models\svm_model.pkl"
}

def load_model(model_path):
    return load(model_path)

label_to_language = {1: "English", 0: "French", 2: "Italian", 3: "Spanish"}
language_icons = {
    "English": "🇬🇧",
    "French": "🇫🇷",
    "Italian": "🇮🇹",
    "Spanish": "🇪🇸",
    "Inconnu": "❓"
}

def load_text_from_docx(file_path):
    """Charger le texte depuis un fichier Word."""
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs]
    return ' '.join(full_text)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.strip()
    return text

def letter_frequencies(text):
    text = text.replace(" ", "")
    total = len(text)
    if total == 0:
        return {letter: 0 for letter in "abcdefghijklmnopqrstuvwxyz"}
    letter_counts = Counter(text)
    return {letter: count / total for letter, count in letter_counts.items()}

def entropy(text):
    freqs = letter_frequencies(text)
    return -sum(freq * math.log2(freq) for freq in freqs.values() if freq > 0)

def count_stopwords(text, stopwords_list):
    words = text.split()
    stopword_counts = {stopword: 0 for stopword in stopwords_list}
    for word in words:
        if word in stopwords_list:
            stopword_counts[word] += 1
    return stopword_counts

def analyze_text(text, stopwords_english, stopwords_french, stopwords_italian, stopwords_spanish):
    cleaned_text = clean_text(text)
    ent = entropy(cleaned_text)
    freqs = letter_frequencies(cleaned_text)

    english_stopwords_count = count_stopwords(cleaned_text, stopwords_english)
    french_stopwords_count = count_stopwords(cleaned_text, stopwords_french)
    italian_stopwords_count = count_stopwords(cleaned_text, stopwords_italian)
    spanish_stopwords_count = count_stopwords(cleaned_text, stopwords_spanish)

    result = {"Entropy": ent}
    result.update({letter: freqs.get(letter, 0) for letter in "abcdefghijklmnopqrstuvwxyz"})
    result.update({"English_Stopwords_" + word: english_stopwords_count.get(word, 0) for word in stopwords_english})
    result.update({"French_Stopwords_" + word: french_stopwords_count.get(word, 0) for word in stopwords_french})
    result.update({"Italian_Stopwords_" + word: italian_stopwords_count.get(word, 0) for word in stopwords_italian})
    result.update({"Spanish_Stopwords_" + word: spanish_stopwords_count.get(word, 0) for word in stopwords_spanish})

    return result

stopwords_english = ["and", "are", "be", "but", "for", "from", "have", "in", "is", "it", "no", "not", "of", "that", "the", "this", "to", "with"]
stopwords_french = ["au", "avec", "ce", "de", "des", "elle", "et", "est", "il", "je", "la", "le", "les", "mais", "ou", "par", "pas", "plus", "pour", "que", "qui", "si", "sur", "un", "une"]
stopwords_italian = ["e", "di", "il", "la", "lo", "i", "gli", "le", "che", "in", "vi", "si", "per", "ma", "con", "un", "una", "su", "non", "questo", "quello"]
stopwords_spanish = ["y", "de", "la", "las", "el", "los", "que", "a", "en", "no", "un", "unos", "es", "con", "por", "para", "del", "se", "lo", "pero", "como", "su", "al", "me", "le", "tener", "sin"]


st.markdown("<h1 style='text-align: center;'>Détection de Langue par ML</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Une approche par apprentissage automatique pour identifier la langue d'un texte</h3>", unsafe_allow_html=True)

if 'analysis_done' in st.session_state and st.session_state.analysis_done:
    st.markdown(custom_success("Session active - Texte déjà analysé"), unsafe_allow_html=True)
else:
    st.markdown(custom_info("Nouvelle session - Entrez un texte pour commencer"), unsafe_allow_html=True)

# Option pour télécharger un fichier ou saisir du texte
input_option = st.radio(
    "Choisissez une méthode d'entrée:",
    ["Saisir du texte", "Télécharger un fichier DOCX", "Utiliser un exemple prédéfini"]
)

user_input = ""

if input_option == "Saisir du texte":
    user_input = st.text_area("✍️ Écrivez votre texte ici :", "", height=200)
elif input_option == "Télécharger un fichier DOCX":
    uploaded_file = st.file_uploader("Choisissez un fichier DOCX", type="docx")
    if uploaded_file is not None:
        with open("temp_file.docx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.markdown(animation_loading(), unsafe_allow_html=True)
        time.sleep(1) 
        
        user_input = load_text_from_docx("temp_file.docx")
        st.markdown(custom_success("Fichier chargé avec succès!"), unsafe_allow_html=True)
        
        st.subheader("Aperçu du texte:")
        st.write(user_input[:500] + ("..." if len(user_input) > 500 else ""))
else:
    example_texts = {
        "Français": "Le français est une langue indo-européenne de la famille des langues romanes. Le français s'est formé en France. Le français est déclaré langue officielle en France en 1539.",
        "English": "English is a West Germanic language of the Indo-European language family, originally spoken by the inhabitants of early medieval England.",
        "Italiano": "L'italiano è una lingua romanza parlata principalmente in Italia. È una delle lingue ufficiali dell'Unione europea e la lingua ufficiale di Italia.",
        "Español": "El español o castellano es una lengua romance procedente del latín hablado. Pertenece al grupo ibérico y es originaria de Castilla, reino medieval de la península ibérica."
    }
    selected_example = st.selectbox("Sélectionnez un exemple:", list(example_texts.keys()))
    user_input = example_texts[selected_example]
    st.text_area("Texte d'exemple:", user_input, height=150)

if user_input:
    word_count = len(user_input.split())
    char_count = len(user_input)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mots", format_number(word_count))
    with col2:
        st.metric("Caractères", format_number(char_count))
    with col3:
        st.metric("Taille (Ko)", format_number(round(len(user_input.encode('utf-8'))/1024, 2)))

if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'data_analyzed' not in st.session_state:
    st.session_state.data_analyzed = None

analyze_button = st.button("📊 Analyser et Classifier", use_container_width=True)

if analyze_button:
    if not user_input.strip():
        st.markdown(custom_error("Veuillez entrer du texte avant d'analyser."), unsafe_allow_html=True)
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(101):
            progress_bar.progress(i)
            status_text.text(f"Analyse en cours... {i}%")
            time.sleep(0.02)  
        
        data = analyze_text(user_input, stopwords_english, stopwords_french, stopwords_italian, stopwords_spanish)
        df = pd.DataFrame([data])
        
        st.session_state.data_analyzed = df
        st.session_state.analysis_done = True
        st.session_state.user_text = user_input  
        
        status_text.text("Analyse terminée!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        st.markdown(custom_success("Analyse des caractéristiques du texte terminée avec succès!"), unsafe_allow_html=True)

if st.session_state.analysis_done:
    st.subheader("📝 Texte analysé")
    if display_mode == "Compact":
        st.info(st.session_state.get('user_text', "Texte non disponible")[:200] + "...")
    else:
        expander = st.expander("Afficher le texte complet")
        with expander:
            st.info(st.session_state.get('user_text', "Texte non disponible"))
    
    st.subheader("📌 Résultats de l'analyse")
    
    if display_mode == "Détaillé":
        st.dataframe(st.session_state.data_analyzed)
    else:
        df = st.session_state.data_analyzed
        entropy_value = df["Entropy"].values[0]
        
        st.write(f"**Entropie du texte:** {entropy_value:.4f} bits/symbole")
        st.write("**Caractéristiques principales:**")
        letter_cols = [col for col in df.columns if len(col) == 1]
        top_letters = sorted([(col, df[col].values[0]) for col in letter_cols], key=lambda x: x[1], reverse=True)[:5]
        
        for letter, freq in top_letters:
            st.write(f"- Fréquence de '{letter}': {freq:.4f}")
        
        eng_stopwords = sum(df[[col for col in df.columns if col.startswith("English_Stopwords_")]].values[0])
        fr_stopwords = sum(df[[col for col in df.columns if col.startswith("French_Stopwords_")]].values[0])
        it_stopwords = sum(df[[col for col in df.columns if col.startswith("Italian_Stopwords_")]].values[0])
        sp_stopwords = sum(df[[col for col in df.columns if col.startswith("Spanish_Stopwords_")]].values[0])
        
        st.write("**Mots courants détectés par langue:**")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"🇬🇧 Anglais: {int(eng_stopwords)} mots")
            st.write(f"🇫🇷 Français: {int(fr_stopwords)} mots")
        with col2:
            st.write(f"🇮🇹 Italien: {int(it_stopwords)} mots")
            st.write(f"🇪🇸 Espagnol: {int(sp_stopwords)} mots")
        
        if st.checkbox("Afficher les données brutes d'analyse"):
            st.dataframe(st.session_state.data_analyzed)
    
    st.subheader("🤖 Sélection du modèle pour la prédiction")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_model = st.selectbox(
            "Choisissez un modèle pour prédire la langue:",
            list(model_paths.keys())
        )
    with col2:
        use_ensemble = st.checkbox("Consensus", 
                                  help="Utiliser tous les modèles et prendre la prédiction majoritaire")
    
    predict_button = st.button("🔮 Prédire la langue", use_container_width=True)
    
    if predict_button:
        st.markdown(animation_loading(), unsafe_allow_html=True)
        
        if use_ensemble:
            predictions = {}
            confidences = {}
            
            for model_name, model_path in model_paths.items():
                model = load_model(model_path)
                df = st.session_state.data_analyzed
                expected_features = model.feature_names_in_
                df_features = df.reindex(columns=expected_features, fill_value=0)
                
                predicted_label = model.predict(df_features)[0]
                predicted_language = label_to_language.get(predicted_label, "Inconnu")
                
                # Obtenir les probabilités si possible
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(df_features)[0]
                    confidence = proba[predicted_label] * 100
                else:
                    confidence = 100  
                
                predictions[model_name] = predicted_language
                confidences[model_name] = confidence
            
            from collections import Counter
            votes = Counter(predictions.values())
            predicted_language = votes.most_common(1)[0][0]
            
            # Calculer la confiance moyenne pour cette langue
            avg_confidence = sum([conf for model, conf in confidences.items() 
                               if predictions[model] == predicted_language]) / votes[predicted_language]
            
            st.success(f"**Prédiction d'ensemble**: La langue détectée est **{language_icons.get(predicted_language, '')} {predicted_language}** (confiance moyenne: {avg_confidence:.1f}%)")
            
            st.write("**Votes des modèles:**")
            for model, pred in predictions.items():
                st.write(f"- {model}: {language_icons.get(pred, '')} {pred} ({confidences[model]:.1f}%)")
        else:

            model = load_model(model_paths[selected_model])
            df = st.session_state.data_analyzed
            
            expected_features = model.feature_names_in_
            df_features = df.reindex(columns=expected_features, fill_value=0)
            
            predicted_label = model.predict(df_features)[0]
            predicted_language = label_to_language.get(predicted_label, "Inconnu")
            
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(df_features)[0]
                confidence = proba[predicted_label] * 100
                st.success(f"**Prédiction**: La langue détectée est **{language_icons.get(predicted_language, '')} {predicted_language}** (confiance: {confidence:.1f}%)")
            else:
                st.success(f"**Prédiction**: La langue détectée est **{language_icons.get(predicted_language, '')} {predicted_language}**")

        st.subheader("Résumé de la détection")
        
        if "predicted_language" in locals():
            lang_icon = language_icons.get(predicted_language, "❓")
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                <h2 style='font-size: 3em; margin-bottom: 10px;'>{lang_icon}</h2>
                <h3>{predicted_language}</h3>
            </div>
            """, unsafe_allow_html=True)

st.markdown(add_footer(), unsafe_allow_html=True)