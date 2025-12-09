# Project Description
# Installation Instruction
# Email Spam Detection System

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Accuracy](https://img.shields.io/badge/accuracy-99.42%25-success.svg)](.)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Project Overview

This project implements an end-to-end spam detection pipeline:
- **Data Analysis and Cleaning:** 23,110 training emails
- **Feature Engineering:** 67,000 TF-IDF features + two temporal features
- **Model Training & Evaluation:** four algorithms were compared
- **Web Deployment:** Flask app for real-time classification

**Key Achievement:** Matches industry-standard performance, Gmail: ~99.5%, my model: 99.42%

---
##  Dataset

- **Source:** [Enron Spam Dataset](https://github.com/MWiechmann/enron_spam_data)
- **Total Emails:** 33,716 (51% spam, 49% ham)
- **Train/Test Split:** 80/20 stratified split
- **Features:** Email subject, message body, date
### Note
- raw and cleaned data are not included because of their size but Xtrain, Xtest, ytrain and ytest are included.
- raw data can be downloaded at https://github.com/MWiechmann/enron_spam_data/tree/master

## Project Structure
```
github files/
|── README.md    
|──requirements.txt
├── LICENSE 
├── .gitignore  
├── notebooks/                                  # Jupyter notebooks for analysis
│   ├── 01_data_analysis.ipynb
│   └── 02_model_selection.ipynb
├── src/    
|   ├── __init__.py                             # Source code
│   ├── clean_emails.py                         # Data cleaning functions
│   ├── model_fit.py                            # Evaluation metrics
│   └── models/ 
        |__spam_trained_model.joblib           # Trained model artifacts
├── data/ 
│   ├── raw_data.csv                            # Original Enron dataset
│   ├── cleaned_data.csv                        # Processed training data
│   ├── X_train.csv                             # Training features
│   ├── y_train.csv                             # Training labels
│   ├── X_test.csv                              # Test features
│   └── y_test.csv                              # Dataset files
|
├── spam_detector/                             # Web application using Flask                                # FLASK Web application
    ├── README.md                               # Deployment instructions
    ├── app.py          
    ├── application.py                          # Flask server
    ├── requirements.txt                        # Flask dependencies
    ├── templates/
    |   ├──base.html                            # Main web interface
    │   └── index.html                          # Main web interface
    └── static/
        ├── css/
            └── style.css
       
```

## Results

| Model | Accuracy | F1 Score | Precision | Recall |
|-------|----------|----------|-----------|--------|
| MultinomialNB | 98.87% | 0.9883 | 0.9895 | 0.9871 |
| SVC (Linear) | 99.10% | 0.9907 | 0.9862 | 0.9952 |
| Logistic Regression | 98.49% | 0.9907	 | 0.9856	| 0.9950 |
| **LinearSVC**  | **99.09%** | **0.9907** | **0.9856** | **0.9957** |

**Test Set Performance, Final Evaluation on Held-Out Data**   
**LinearSVC Performance:**
- **Accuracy:** 99.42%
- **F1 Score:** 0.9942
- **Precision:** 0.9912	
- **Recall:** 0.9972	
* Correctly classified: 6,705 over 6,743 emails
* False Positives: 29 (0.43%)
* False Negatives: 9 (0.13%)

**Note:** Test performance exceeded cross-validation results, demonstrating strong generalization and model robustness. This suggests the model will perform reliably on new, unseen emails in production.


## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/rimesaad/spam-detector.git
cd spam-detector
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv spam_detector_env

# Activate environment
# On Mac/Linux:
source spam_detector_env/bin/activate
# On Windows:
spam_detector_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Notebooks
```bash
jupyter notebook notebooks/01_data_analysis.ipynb
jupyter notebook notebooks/02_model_training.ipynb
```

### 4. Try the Web App
```bash
cd spam_detector
python app.py
# Navigate to http://localhost:5000
```

See [spam_detector/README.md](flask_app/README.md) for deployment instructions



---
## Methodology

### Feature Engineering
- **TF-IDF Vectorization:** 67,000 features (optimized via GridSearchCV)
- **Temporal Features:** Day of week email was sent
- **Pattern Features:** Email repetition frequency
- **Text Preprocessing:** Lowercase, strip whitespace with stopwords and punctuation kept

### Model Selection
**Why LinearSVC?**
- Optimized for high-dimensional sparse data (67k features)
- Linear kernel exploits text data's natural separability
- 4-5× faster than kernel SVC with comparable accuracy
- Industry-proven for text classification

### Pipeline
```python
Pipeline:
  ├─ ColumnTransformer
  │   ├─ TfidfVectorizer(max_features=67000)
  │   └─ StandardScaler(temporal features)
  └─ LinearSVC()
```


---

## 🛠️ Technologies Used

- **Python 3.10**
- **Scikit-learn** - Machine learning
- **Pandas & NumPy** - Data manipulation
- **NLTK** - Text processing
- **Matplotlib & Seaborn** - Visualization
- **Flask** - Web deployment
- **Joblib** - Model serialization

---

##  Future Improvements

- Ensemble methods (stacking multiple models)
- Deep learning approaches (LSTM, BERT)
- Email header analysis (SPF, DKIM records)
- URL blacklist checking
- Sender reputation scoring
- Real-time model monitoring dashboard
- A/B testing framework

---

##  Notebooks

### 01_data_analysis.ipynb
- Data loading and exploration
- Missing value analysis
- Duplicate detection and handling
- Feature engineering (day_of_week, repeat_freq)
- Text preprocessing and visualization

### 02_model_training.ipynb
- Hyperparameter tuning (GridSearchCV)
- Model comparison (4 algorithms)
- Cross-validation (5-fold stratified)
- Test set evaluation
- Feature importance analysis

---

## Web Application

Live demo available at: [Your Deployment URL]

See [flask_app/README.md](flask_app/README.md) for:
- Local setup instructions
- Deployment to Heroku/AWS
- API documentation
- Usage examples

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## Author

**Rime Saad**
- GitHub: [@rime11](https://github.com/rime11/)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Portfolio: [yourwebsite.com](https://yourwebsite.com)

---

## Acknowledgments

- [Enron Spam Dataset](https://github.com/MWiechmann/enron_spam_data) by MWiechmann
- Scikit-learn documentation and community
- Kaggle spam detection community

---

## 📞 Contact

Questions or suggestions:
- Email: rimesaad@gmail.com


---

 **If you found this project helpful, please star the repository!**
