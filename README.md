# 📊 AI Data Analyst Pro V2

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **Upload any CSV. Get instant AI-powered analysis. No code required.**

---

## 🚀 Live Demo

👉 **[Try it Live Here](http://localhost:8501/)**

---

## 💡 Problem Statement

Data analysts spend **60-80% of their time** on data cleaning and exploratory analysis — before any real insights are generated. This is repetitive, time-consuming, and requires technical knowledge that non-technical users simply don't have.

AI Data Analyst Pro V2 eliminates this bottleneck entirely — combining automated EDA with Groq LLaMA 3.3 AI to generate plain-English insights, predictions, and recommendations from any CSV dataset.

---

## 🎯 Key Highlights

- **Domain-agnostic** — works on any CSV: HR, finance, e-commerce, healthcare, marketing
- **AI-powered** — Groq LLaMA 3.3-70B generates insights, risk analysis, and predictions
- **End-to-end pipeline** — raw data in, clean insights + PDF report out
- **Natural Language Query** — ask questions about your data in plain English
- **Session-based cleaning** — all transformations persist across all sections
- **Professional dark UI** — sidebar navigation, metric cards, interactive charts

---

## 🛠 Tech Stack

| Technology | Role |
|---|---|
| Python | Core language |
| Streamlit | Web app framework |
| Pandas | Data manipulation |
| Plotly | Interactive visualizations |
| Groq LLaMA 3.3-70B | AI insights generation |
| FPDF2 | PDF report generation |
| Statsmodels | Scatter trendlines |

---

## ✨ Features

### 📋 Dataset Overview
Instant snapshot — row count, column count, duplicates, missing values as metric cards. Adjustable row preview with full dataset expander.

### 🔍 Schema Analysis
Column-level breakdown — data type, missing count, missing %, unique values, sample value for every column.

### 📊 Statistical Summary
Full descriptive statistics for numeric columns. Categorical summary with value counts and auto-rendered pie or bar chart.

### 📈 Data Quality Index
Automated 0-100 quality score from missing value rate and duplicate rate. Color-coded — Healthy, Needs Attention, Poor Quality.

### 🧹 Missing Value Handler
Per-column detection with row preview. Fill with Mean, Median, Mode or Drop rows. Session-state persistence across all sections.

### 🔧 Advanced Cleaning
- **Duplicate Remover** — detect and remove with before/after count
- **Data Type Converter** — Numeric, String, DateTime, Category
- **Whitespace Cleaner** — strip spaces from all text columns

### 🎯 Outlier Detection
IQR-based detection across all numeric columns. Box Plot, Histogram, Violin Plot. Expandable outlier rows viewer.

### 🔗 Correlation Matrix
Interactive Plotly heatmap. Auto-detection of strong correlations >= 0.5 with positive/negative labeling.

### 🔎 Column Drill Down
Deep-dive into any column — type, unique count, missing %, stats, outlier count, distribution and spread charts.

### 📊 Group By Analysis
Group by any categorical column, aggregate with Mean/Sum/Count/Max/Min/Median. Bar or Pie chart. Auto-highlights highest and lowest groups.

### 📊 Smart Chart Engine
Auto-detects column type and renders best chart. Numeric, Categorical, Date, Two-column analysis with trendlines.

### 🎯 KPI Dashboard
Five KPI cards — Mean, Median, Max, Min, Std Dev — with distribution and spread charts.

### 🤖 AI Insights — Powered by Groq LLaMA 3.3
- **Dataset Summary** — plain English explanation of your data
- **Key Insights** — 5 structured insights with findings and business impact
- **Recommendations** — top 3 business recommendations + data quality improvements
- **Risk Analysis** — data quality risks, business risks, statistical anomalies

### 💬 Ask Your Data
Natural Language Query — type any question, AI analyzes dataset and answers with supporting evidence and next steps.

### 🔮 AI Predictions
- **Trend Prediction** — short and medium term trends with confidence assessment
- **Anomaly Forecast** — predict future anomalies and prevention recommendations

### ⬇️ Download
- Cleaned CSV export after all transformations
- Auto-generated PDF report — summary, quality index, schema, stats, outliers, correlations

---

## 🗂 Tested On

| Dataset | Domain | Size |
|---|---|---|
| Financial Loan Data | Banking / Finance | 100,000+ rows |
| E-Commerce Customer Churn | E-commerce | 2,000+ rows |
| Insurance Charges | Healthcare | 1,338 rows |

---

## 📸 Screenshots

### Home Page
<img width="1360" height="582" alt="image" src="https://github.com/user-attachments/assets/c0eaa082-7cab-4ee3-acbf-b04a31174f22" />

### Overview
<img width="1366" height="593" alt="image" src="https://github.com/user-attachments/assets/4d28bb44-7b96-46f4-be4d-3c7f2942b4d8" />


### Schema Analaysis
<img width="1356" height="557" alt="image" src="https://github.com/user-attachments/assets/c77cd9ae-fc62-4981-922d-9957880a7e34" />


### Stastical Analysis and Data Quality Index
<img width="1346" height="588" alt="image" src="https://github.com/user-attachments/assets/514ce89c-9d6b-4acd-9ea2-56d3f02e9bc5" />
<img width="1347" height="572" alt="image" src="https://github.com/user-attachments/assets/4d7b710d-6374-438b-bf68-34d34f0fdd1e" />


### Correlation
<img width="1356" height="608" alt="image" src="https://github.com/user-attachments/assets/85f9ca41-b2b1-4656-a33f-a23cecb7f9b5" />


### AI Features

<img width="1360" height="571" alt="image" src="https://github.com/user-attachments/assets/5b45c563-7975-4c83-934f-19e7c6304759" />

### Download Section

<img width="1342" height="604" alt="image" src="https://github.com/user-attachments/assets/217727a5-0fcd-4b70-8b47-c7bf9c5a2c29" />



## 📁 Project Structure
ai-data-analyst-pro/

│

├── app.py                 # Main Streamlit application

├── requirements.txt       # Dependencies

├── .env                   # API keys (not committed)

└── README.md             # Documentation

---

## ⚙️ Run Locally

```bash
git clone https://github.com/pritamk001/ai-data-analyst-pro.git
cd ai-data-analyst-pro
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:

GROQ_API_KEY=your_key_here

```bash
streamlit run app.py
```

---

## 🔮 V3 Roadmap

- 🤖 **AutoML** — select target column, auto-train model, show accuracy
- 📈 **Time Series Forecast** — Prophet/ARIMA for date columns
- 📄 **Enhanced PDF** — charts embedded in report

---

## 👩‍💻 Developer

**Pritam Kumari** — CS Honours Student | Aspiring Data Scientist

- 🔗 [GitHub](https://github.com/pritamk001)
- 💼 [LinkedIn](www.linkedin.com/in/pritam-351003301)

---

## ⭐ Star This Repo

If this tool helped you, please star the repository!

---

*Built with Python, Streamlit, Pandas, and Groq AI*
