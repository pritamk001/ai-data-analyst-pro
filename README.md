# 📊 AI Data Analyst Pro

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **Upload any CSV. Get instant analysis. No code required.**

---

## 🚀 Live Demo

👉 **[Try it Live Here](https://ai-data-analyst-proo.streamlit.app/**

---

## 💡 Problem Statement

Data analysts spend **60-80% of their time** on data cleaning and exploratory analysis — before any real insights are generated. This is repetitive, time-consuming, and requires technical knowledge that non-technical users simply don't have.

**AI Data Analyst Pro** eliminates this bottleneck entirely.

Upload any structured CSV dataset — the tool automatically handles everything from data quality assessment to missing value treatment, outlier detection, correlation analysis, and interactive visualizations — and exports a professional PDF report, all without writing a single line of code.

---

## 🎯 Key Highlights

- **Domain-agnostic** — works on any CSV: HR, finance, e-commerce, healthcare, marketing
- **End-to-end pipeline** — raw data in, clean insights out
- **Session-based cleaning** — all changes persist and reflect across every section
- **Production-ready features** — PDF export, data type conversion, downloadable cleaned CSV
- **Built for real use** — tested on datasets ranging from 1,000 to 500,000+ rows

---

## 🛠 Tech Stack

| Technology | Role |
|---|---|
| Python | Core language |
| Streamlit | Web app framework |
| Pandas | Data manipulation |
| Plotly | Interactive visualizations |
| FPDF2 | PDF report generation |
| Statsmodels | Scatter trendlines |

---

## ✨ Feature Breakdown

### 📋 Dataset Overview
Instant snapshot of the uploaded dataset — row count, column count, duplicate rows, and total missing values displayed as metric cards. Adjustable row preview slider with full dataset expandable view.

### 🔍 Schema Analysis
Detailed column-level breakdown — data type, missing value count, missing percentage, unique value count, and sample value for every column in one clean table. Helps identify data quality issues at a glance.

### 📊 Statistical Summary
Full descriptive statistics (mean, std, min, max, percentiles) for all numeric columns. Separate categorical summary with value counts and auto-rendered pie or bar chart based on column cardinality.

### 📈 Data Quality Index
Automated 0-100 quality score calculated from missing value rate and duplicate rate. Color-coded status — Healthy, Needs Attention, or Poor Quality — with a visual breakdown bar chart.

### 🧹 Missing Value Handler
Per-column missing value detection with expandable row preview showing exactly which rows are affected. Handles numeric columns with Mean, Median, or Mode fill — categorical columns with Mode fill or row drop. All changes are applied to session state and reflect immediately across all other sections.

### 🔧 Advanced Cleaning
Three production-level cleaning tools in one section:
- **Duplicate Remover** — detects and removes duplicate rows with before/after count
- **Data Type Converter** — convert any column to Numeric, String, DateTime, or Category with error handling
- **Whitespace Cleaner** — strips leading/trailing spaces from all text columns in one click

### 🎯 Outlier Detection
IQR-based outlier detection across every numeric column — summary table shows outlier count, lower bound, upper bound, min, and max. Interactive column selector with Box Plot, Histogram, or Violin Plot visualization. Expandable table to inspect exact outlier rows.

### 🔗 Correlation Matrix
Interactive Plotly heatmap showing correlation between all numeric columns. Auto-detection and listing of strong correlations (>= 0.5) with positive/negative labeling — actionable insight, not just a chart.

### 🔎 Column Drill Down
Deep-dive analysis for any single column — type, unique count, missing percentage, full statistical summary for numeric columns, outlier count, and side-by-side distribution and spread charts. Date columns show top frequency breakdown.

### 📊 Group By Analysis
Business-level aggregation — select any categorical column as group, any numeric column as value, and any aggregation function (Mean, Sum, Count, Max, Min, Median). Results displayed as sortable table with bar or pie chart. Auto-highlights highest and lowest performing groups.

### 📊 Smart Chart Engine
Intelligent chart builder that detects column types and renders the most appropriate chart automatically:
- **Numeric** → Histogram, Box Plot, Violin Plot
- **Categorical** → Bar Chart, Pie Chart
- **Date** → Line Chart auto-detected
- **Two columns** → Scatter with trendline, Area, Box, Violin

### 🎯 KPI Dashboard
Select any numeric column and instantly get five KPI metric cards — Mean, Median, Max, Min, Standard Deviation — with supporting distribution and spread charts.

### ⬇️ Download
- **Cleaned CSV** — export the fully transformed dataset after all cleaning operations
- **PDF Report** — auto-generated professional report covering dataset summary, data quality index, schema analysis, statistical summary, outlier summary, and strong correlations

---

## 🗂 Tested On

| Dataset | Domain | Size |
|---|---|---|
| Financial Loan Data | Banking / Finance | 100,000+ rows |
| Insurance Charges | Healthcare | 1,338 rows |
| Online Retail | E-commerce | 500,000+ rows |

---

## 📁 Project Structure
ai-data-analyst-pro/

│

├── app.py                 # Main Streamlit application

├── requirements.txt       # Python dependencies

└── README.md             # Project documentation
---

## ⚙️ Run Locally

```bash
# Clone the repo
git clone https://github.com/pritamk001/ai-data-analyst-pro.git
cd ai-data-analyst-pro

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📸 Screenshots

### Home Page
<img width="1361" height="587" alt="image" src="https://github.com/user-attachments/assets/e69237a2-b28f-41b9-9606-7ee5385bd8f1" />


### Data Quality Index
<img width="1352" height="598" alt="image" src="https://github.com/user-attachments/assets/c5230811-2ee4-480d-86e1-46f865aa0e9b" />


### Correlation Matrix
<img width="1049" height="571" alt="image" src="https://github.com/user-attachments/assets/25d39e5f-38b7-48f6-89d6-5b9ed8ad41cd" />
<img width="1009" height="270" alt="image" src="https://github.com/user-attachments/assets/7439abb6-9d00-4591-a77b-adc3ca547027" />


### Smart Chart Engine
<img width="1002" height="351" alt="image" src="https://github.com/user-attachments/assets/834ebadd-8185-4a3f-9301-a797db4cdf7f" />
<img width="974" height="436" alt="image" src="https://github.com/user-attachments/assets/6d8c86bf-69d8-4eb2-9c13-b5b146acc9b0" />


### KPI Dashboard
<img width="1000" height="467" alt="image" src="https://github.com/user-attachments/assets/a02ddcc3-6dce-4d31-901f-81e0c14d5550" />
<img width="978" height="495" alt="image" src="https://github.com/user-attachments/assets/e816ea68-cc1b-49f5-93c9-c7cae390727f" />


---

## 🔮 V2 Roadmap

- 🤖 **AI Generated Insights** — Gemini API for plain-English data summaries
- 🔍 **Natural Language Query** — ask questions about your data in plain text
- 📄 **Enhanced PDF** — charts embedded directly in report
- ⚡ **Performance optimization** for large datasets

---

## 👩‍💻 Developer

**Pritam** — CS Honours Student | Aspiring Data Scientist

Passionate about building tools that bridge the gap between raw data and real decisions.

- 🔗 [GitHub](https://github.com/pritamk001)
- 💼 LinkedIn — www.linkedin.com/in/pritam-351003301
---

## ⭐ Star This Repo

If this tool helped you, please consider starring the repository — it helps others find it!

---

*Built with Python, Streamlit, and Pandas*
