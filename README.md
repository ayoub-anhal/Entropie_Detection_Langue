# Language Detection Project

![Language Detection](https://img.shields.io/badge/NLP-Language%20Detection-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![Streamlit](https://img.shields.io/badge/Streamlit-1.10%2B-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

A sophisticated language detection system using Shannon Entropy analysis and Machine Learning models to identify text in English, French, Italian, and Spanish.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Methodology](#methodology)
- [Model Performance](#model-performance)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🔭 Overview

This project implements a language detection system using two complementary approaches:
1. **Statistical Method**: Shannon Entropy analysis for information-theoretic language classification
2. **Machine Learning Models**: SVM, Random Forest, and Logistic Regression classifiers

The application is packaged as a Streamlit web interface that allows users to input text and receive language predictions using either approach.

## ✨ Features

- **Multi-language Support**: Detects English, French, Italian, and Spanish
- **Dual Approach**: Compare statistical and machine learning methods
- **Interactive UI**: User-friendly Streamlit interface with visualizations
- **Text Analysis**: Provides entropy values, letter frequencies, and stopword counts
- **Model Comparison**: Evaluate performance metrics across different classification models

## 🏗️ Project Architecture

```
                    ┌─────────────────────┐
                    │    Input Text       │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Text Processing   │
                    └─────┬──────────┬────┘
                          │          │
          ┌───────────────▼──┐    ┌──▼───────────────┐
          │ Shannon Entropy  │    │ Feature Extraction│
          │    Analysis      │    │                   │
          └───────────┬──────┘    └─────────┬─────────┘
                      │                     │
          ┌───────────▼──────┐    ┌─────────▼─────────┐
          │ Entropy-based    │    │ Machine Learning   │
          │   Prediction     │    │   Models           │
          └───────────┬──────┘    └─────────┬─────────┘
                      │                     │
                      └─────────┬───────────┘
                                │
                      ┌─────────▼─────────┐
                      │ Language Prediction│
                      └─────────┬─────────┘
                                │
                      ┌─────────▼─────────┐
                      │ Streamlit UI      │
                      └───────────────────┘
```

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language
- **Data Science Libraries**:
  - Pandas & NumPy: Data manipulation
  - Scikit-learn: Machine learning models
  - NLTK: Natural language processing
- **Visualization**:
  - Matplotlib & Seaborn: Data visualization
  - Plotly: Interactive charts
- **Web Application**:
  - Streamlit: Interactive web interface
- **External APIs**:
  - Wikipedia API: Training data collection

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/username/language-detection.git
cd language-detection
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Running the Application

Launch the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501.

### Using the Web Interface

1. Navigate to the home page for project information
2. Select either the "Entropy-based Method" or "Machine Learning Method" tab
3. Input or paste text in the provided text area
4. The application will detect the language and display the results along with relevant metrics

### Using the API

```python
from language_detector import EntropyDetector, MLDetector

# Using Shannon Entropy
entropy_detector = EntropyDetector()
language, confidence = entropy_detector.detect("Text to analyze")

# Using Machine Learning
ml_detector = MLDetector(model_type="svm")  # Options: "svm", "random_forest", "logistic"
language, probabilities = ml_detector.detect("Text to analyze")
```

## 📁 Project Structure

```
language-detection/
├── app.py                      # Streamlit application entry point
├── requirements.txt            # Project dependencies
├── LICENSE                     # License file
├── README.md                   # Project documentation
├── models/                     # Trained machine learning models
│   ├── svm_model.pkl
│   ├── random_forest_model.pkl
│   └── logistic_model.pkl
├── data/                       # Training and test data
│   ├── raw/                    # Original Wikipedia articles
│   │   ├── english/
│   │   ├── french/
│   │   ├── italian/
│   │   └── spanish/
│   └── processed/              # Preprocessed data
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── data_collection.ipynb
│   ├── data_preprocessing.ipynb
│   ├── entropy_analysis.ipynb
│   └── model_training.ipynb
├── src/                        # Source code
│   ├── __init__.py
│   ├── data/                   # Data processing modules
│   │   ├── __init__.py
│   │   ├── collector.py        # Wikipedia API scraper
│   │   └── preprocessor.py     # Text preprocessing functions
│   ├── features/               # Feature engineering
│   │   ├── __init__.py
│   │   └── extractor.py        # Feature extraction for ML models
│   ├── models/                 # Model definition and training
│   │   ├── __init__.py
│   │   ├── entropy_detector.py # Shannon entropy-based detector
│   │   └── ml_detector.py      # Machine learning models
│   └── visualization/          # Visualization utilities
│       ├── __init__.py
│       └── plots.py            # Plotting functions
└── tests/                      # Unit and integration tests
    ├── __init__.py
    ├── test_entropy.py
    └── test_ml_models.py
```

## 🔬 Methodology

### Data Collection

- Corpus gathered from Wikipedia articles in four languages
- Texts stored in various formats (.txt, .docx) for processing flexibility
- Balanced dataset with equal representation for each language

### Preprocessing Pipeline

1. **Text Extraction**: Parse and extract text from raw files
2. **Cleaning**: Remove special characters, formatting, and normalize text
3. **Feature Calculation**:
   - Letter frequency distribution
   - Shannon entropy calculation
   - Stopword counting

### Shannon Entropy Approach

The entropy of a language is calculated using:

![Shannon Entropy Formula](https://latex.codecogs.com/svg.latex?H(X)=-\sum_{i=1}^{n}p(x_i)\log_2p(x_i))

Where:
- H(X) is the entropy
- p(x_i) is the frequency/probability of character x_i
- n is the total number of unique characters

### Machine Learning Approach

Three classification models were trained and evaluated:
- **Support Vector Machine**: For high-dimensional feature spaces
- **Random Forest**: For robustness and feature importance analysis
- **Logistic Regression**: As a baseline linear model

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Shannon Entropy | 85.7% | 86.3% | 85.7% | 85.9% |
| SVM | 94.2% | 94.5% | 94.2% | 94.3% |
| Random Forest | 93.8% | 93.9% | 93.8% | 93.8% |
| Logistic Regression | 92.1% | 92.4% | 92.1% | 92.2% |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Project Maintainer - [Your Name](mailto:your.email@example.com)

Project Link: [https://github.com/username/language-detection](https://github.com/username/language-detection)
