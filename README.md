# 🏠 AI Underwriting Assistant

An AI-powered real estate investment analysis tool that helps investors quickly evaluate whether a property is a good investment — combining financial modeling, a rule-based risk engine, a machine learning market price predictor, and a generative AI chatbot, all in one interactive dashboard.

Built by **Muaz** as part of an internship project at Career Institute.

---

## ✨ Features

- **Financial Calculator** — Automatically calculates NOI, Cash Flow, Cap Rate, and ROI from property details.
- **Risk Engine** — Rule-based system that flags investment risk as Low, Medium, or High.
- **AI Chatbot** — Powered by Google Gemini, answers questions about the analyzed property in plain language (with quick-question shortcuts).
- **ML Market Insights** — A machine learning model trained on 190,000+ real Pakistan property listings (Zameen.com dataset) that predicts a fair market price and shows historical price trends for a given city/location.
- **PDF Investment Memo** — Generates a downloadable, professional investment report.
- **Database Storage** — Saves analyses and chat history locally using SQLite.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend / Dashboard | Streamlit |
| AI Chatbot | Google Gemini API (`google-genai`) |
| Machine Learning | Scikit-learn (Random Forest), joblib |
| Data Processing | Pandas, NumPy |
| Charts | Plotly |
| Database | SQLite + SQLAlchemy |
| PDF Reports | ReportLab |
| Configuration | python-dotenv |

---

## 📂 Project Structure

```
AI_Underwriting_Assistant/
├── app.py                     # Main Streamlit app
├── requirements.txt
├── .env                        # API keys (not committed to version control)
│
├── data/
│   └── zameen_data.csv         # Real property dataset (Zameen.com, Pakistan)
│
├── database/
│   ├── database.py
│   ├── models.py
│   └── underwriting.db         # SQLite database (created on first run)
│
├── calculations/
│   ├── noi.py
│   ├── roi.py
│   ├── cap_rate.py
│   ├── cashflow.py
│   └── dcf.py                  # Optional, not used in the main flow
│
├── risk/
│   └── risk_engine.py
│
├── chatbot/
│   ├── ai_chat.py
│   ├── prompts.py
│   └── context.py
│
├── visualization/
│   └── charts.py
│
├── reports/
│   └── report_generator.py
│
├── ml_model/
│   ├── data_prep.py
│   ├── train_model.py
│   ├── predict.py
│   ├── trend_analysis.py
│   ├── price_model.joblib      # Trained model (created after training)
│   └── encoders.joblib
│
└── assets/
    └── logo.png
```

---

## 🚀 Setup & Installation

### 1. Clone / download the project, then create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get a free key from [Google AI Studio](https://aistudio.google.com/apikey).

### 4. (Optional but recommended) Train the ML model
Download the **Zameen.com Property Data Pakistan** dataset from Kaggle and save it as `data/zameen_data.csv`, then run:
```bash
python -m ml_model.train_model
```
This trains and saves the price prediction model (~1-3 minutes).

### 5. Run the app
```bash
python -m streamlit run app.py
```

---

## 📊 ML Model Performance

Evaluated on a held-out 20% test split of the Zameen.com dataset (191,374 cleaned rows):

| Metric | Value |
|---|---|
| R² Score | **0.826** |
| Mean Absolute Error | **PKR 3,533,935** |

> **Note on model limitations:** This model is trained on a static, historical dataset (listings primarily from 2018–2019). It does **not** reflect live/current market prices or recent inflation. Predictions should be treated as a rough historical benchmark, not a certified or up-to-date property valuation. The dataset also has a very wide price range (from under a million to billions of PKR), which affects the average error — always cross-check with current market listings before making a real investment decision.

---

## ⚖️ Risk Level Thresholds

The Risk Engine flags a property based on these rules:

| Condition | Threshold |
|---|---|
| High Vacancy | Vacancy Rate > 10% |
| Low ROI | ROI < 6% |
| High Expenses | Operating Expenses > 50% of Gross Income |
| Low Cap Rate | Cap Rate < 4% |
| Negative Cash Flow | Cash Flow < 0 |

**Overall Risk Level:**
- 🟢 **Low** — No flags triggered
- 🟡 **Medium** — 1–2 flags triggered
- 🔴 **High** — Cash flow is negative, OR 3 or more flags triggered

---

## 📄 License / Usage

This project was built for educational and internship-portfolio purposes. The Zameen.com dataset used for the ML model is a publicly available Kaggle dataset, used here for training/educational purposes only.
