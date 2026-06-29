import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="AI Data Analyst Pro",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important; margin: 0 !important;}
    
    /* Main background */
    .stApp {background-color: #0f1117;}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #1a1d2e !important;
        border-right: 1px solid #2d3250;
        min-width: 220px !important;
        max-width: 220px !important;
    }
    
    [data-testid="stSidebar"] > div {padding-top: 0 !important;}
    
    /* Nav buttons */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        margin: 2px 8px;
        border-radius: 8px;
        cursor: pointer;
        color: #888;
        font-size: 13px;
        transition: all 0.2s;
        border: none;
        background: transparent;
        text-decoration: none;
    }
    
    .nav-item:hover {
        background: #2d3250;
        color: white;
    }
    
    .nav-item.active {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
    }
    
    /* Top bar */
    .top-bar {
        background: #1a1d2e;
        border-bottom: 1px solid #2d3250;
        padding: 12px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
    }
    
    /* Metric cards */
    .metric-card {
        background: #1a1d2e;
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 20px;
        text-align: left;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: white;
        margin: 4px 0;
    }
    
    .metric-label {
        font-size: 12px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 12px;
        color: #43e97b;
        margin-top: 4px;
    }
    
    /* Section header */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: white;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #667eea;
    }
    
    /* Upload area */
    .upload-area {
        background: #1a1d2e;
        border: 2px dashed #667eea44;
        border-radius: 16px;
        padding: 60px 40px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .upload-area:hover {
        border-color: #667eea;
        background: #1e2240;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
    }
    
    /* Feature cards on home */
    .feature-card {
        background: #1a1d2e;
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 4px;
        transition: all 0.3s;
    }
    
    .feature-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
    }
    
    /* Table styling */
    .stDataFrame {border-radius: 8px; overflow: hidden;}
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1a1d2e !important;
        border-radius: 8px !important;
    }
    
    /* Radio buttons */
    .stRadio > div {gap: 8px;}
    .stRadio label {
        background: #1a1d2e;
        border: 1px solid #2d3250;
        border-radius: 6px;
        padding: 4px 12px;
        color: #888;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background: #1a1d2e;
        border-radius: 8px 8px 0 0;
        color: #888;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {width: 6px;}
    ::-webkit-scrollbar-track {background: #1a1d2e;}
    ::-webkit-scrollbar-thumb {background: #667eea; border-radius: 3px;}
</style>
""", unsafe_allow_html=True)

# Session state
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
if 'section' not in st.session_state:
    st.session_state.section = "overview"

def get_col_types(df):
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    date_cols = []
    cat_cols = []
    for col in df.columns:
        if col in num_cols:
            continue
        if 'date' in col.lower() or 'time' in col.lower():
            date_cols.append(col)
        else:
            cat_cols.append(col)
    return num_cols, cat_cols, date_cols

def groq_response(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def set_section(s):
    st.session_state.section = s
    st.rerun()

# SIDEBAR
with st.sidebar:
    # Logo
    st.markdown("""
    <div style='padding: 20px 16px 10px; border-bottom: 1px solid #2d3250; margin-bottom: 10px;'>
        <div style='font-size: 18px; font-weight: 800; color: white;'>📊 DataAnalyst Pro</div>
        <div style='font-size: 11px; color: #667eea; margin-top: 2px;'>AI-Powered Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.df_cleaned is not None:
        df = st.session_state.df_cleaned.copy()
        num_cols, cat_cols, date_cols = get_col_types(df)

        st.markdown(f"""
        <div style='padding: 8px 16px; margin-bottom: 8px;'>
            <div style='font-size: 11px; color: #888;'>ACTIVE DATASET</div>
            <div style='font-size: 12px; color: #667eea; font-weight: 600; margin-top: 2px;'>
                📁 {st.session_state.file_name[:20]}...
            </div>
            <div style='font-size: 11px; color: #555; margin-top: 2px;'>
                {df.shape[0]:,} rows × {df.shape[1]} cols
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='padding: 0 8px; font-size: 11px; color: #555; margin-bottom: 6px; letter-spacing: 1px;'>ANALYSIS</div>", unsafe_allow_html=True)

        nav_items = [
            ("overview", "📋", "Overview"),
            ("schema", "🔍", "Schema Analysis"),
            ("stats", "📊", "Statistical Summary"),
            ("quality", "📈", "Data Quality Index"),
        ]

        for key, icon, label in nav_items:
            active = "active" if st.session_state.section == key else ""
            bg = "background: linear-gradient(90deg, #667eea22, #764ba222); color: white; border-left: 3px solid #667eea;" if active else "color: #888;"
            st.markdown(f"""
            <div style='padding: 9px 16px; margin: 2px 0; border-radius: 8px; cursor: pointer; font-size: 13px; {bg}'>
                {icon} {label}
            </div>
            """, unsafe_allow_html=True)
            if st.button(label, key=f"nav_{key}", help=label):
                set_section(key)

        st.markdown("<div style='padding: 8px 8px 4px; font-size: 11px; color: #555; margin-top: 8px; letter-spacing: 1px;'>CLEANING</div>", unsafe_allow_html=True)

        clean_items = [
            ("missing", "🧹", "Missing Values"),
            ("cleaning", "🔧", "Advanced Cleaning"),
            ("outliers", "🎯", "Outlier Detection"),
        ]

        for key, icon, label in clean_items:
            if st.button(f"{icon} {label}", key=f"nav_{key}"):
                set_section(key)

        st.markdown("<div style='padding: 8px 8px 4px; font-size: 11px; color: #555; margin-top: 8px; letter-spacing: 1px;'>EXPLORE</div>", unsafe_allow_html=True)

        explore_items = [
            ("correlation", "🔗", "Correlation Matrix"),
            ("drilldown", "🔎", "Column Drill Down"),
            ("groupby", "📊", "Group By Analysis"),
            ("charts", "📊", "Smart Chart Engine"),
            ("kpi", "🎯", "KPI Dashboard"),
        ]

        for key, icon, label in explore_items:
            if st.button(f"{icon} {label}", key=f"nav_{key}"):
                set_section(key)

        st.markdown("<div style='padding: 8px 8px 4px; font-size: 11px; color: #555; margin-top: 8px; letter-spacing: 1px;'>AI FEATURES</div>", unsafe_allow_html=True)

        ai_items = [
            ("ai", "🤖", "AI Insights"),
            ("nlq", "💬", "Ask Your Data"),
            ("predictions", "🔮", "AI Predictions"),
        ]

        for key, icon, label in ai_items:
            if st.button(f"{icon} {label}", key=f"nav_{key}"):
                set_section(key)

        st.markdown("<div style='padding: 8px 8px 4px; font-size: 11px; color: #555; margin-top: 8px; letter-spacing: 1px;'>EXPORT</div>", unsafe_allow_html=True)

        if st.button("⬇️ Download", key="nav_download"):
            set_section("download")

        # New file upload in sidebar
        st.markdown("<div style='padding: 16px 8px 0; border-top: 1px solid #2d3250; margin-top: 12px;'>", unsafe_allow_html=True)
        new_file = st.file_uploader("Upload new CSV", type=["csv"], key="sidebar_upload")
        if new_file is not None:
            st.session_state.df_cleaned = pd.read_csv(new_file)
            st.session_state.file_name = new_file.name
            st.session_state.section = "overview"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style='padding: 20px 16px; color: #555; font-size: 12px; text-align: center;'>
            Upload a CSV file to get started
        </div>
        """, unsafe_allow_html=True)

# MAIN CONTENT
if st.session_state.df_cleaned is None:
    # Upload screen
    st.markdown("""
    <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; 
                min-height: 20px; padding: 40px;'>
        <div style='text-align: center; margin-bottom: 40px;'>
            <div style='font-size: 48px; margin-bottom: 16px;'>📊</div>
            <h1 style='color: white; font-size: 36px; font-weight: 800; margin: 0;'>AI Data Analyst Pro</h1>
            <p style='color: #888; font-size: 16px; margin-top: 8px;'>Transform raw data into actionable insights — powered by AI</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")
        if uploaded_file is not None:
            st.session_state.df_cleaned = pd.read_csv(uploaded_file)
            st.session_state.file_name = uploaded_file.name
            st.session_state.section = "overview"
            st.rerun()

        st.markdown("""
        <div style='text-align: center; margin-top: 8px; color: #555; font-size: 13px;'>
            Drop your CSV file here or click to browse
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("📋", "Smart Overview", "Auto-detect column types, missing values, and dataset health score"),
        ("🧹", "Data Cleaning", "Handle missing values, remove duplicates, convert data types"),
        ("📊", "Visual Analytics", "Interactive charts — histogram, scatter, heatmap, violin plots"),
        ("🤖", "AI Insights", "Groq LLaMA 3.3 powered insights, predictions, and recommendations"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
        col.markdown(f"""
        <div style='background: #1a1d2e; border: 1px solid #2d3250; border-radius: 12px; 
                    padding: 24px 16px; text-align: center; height: 150px;'>
            <div style='font-size: 28px; margin-bottom: 8px;'>{icon}</div>
            <div style='color: white; font-weight: 600; font-size: 14px; margin-bottom: 6px;'>{title}</div>
            <div style='color: #555; font-size: 12px;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    df = st.session_state.df_cleaned.copy()
    num_cols, cat_cols, date_cols = get_col_types(df)
    section = st.session_state.section

    # Top bar
    st.markdown(f"""
    <div style='background: #1a1d2e; border-bottom: 1px solid #2d3250; padding: 14px 24px; 
                margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between;'>
        <div style='color: white; font-size: 16px; font-weight: 600;'>
            {section.replace("_", " ").title()}
        </div>
        <div style='color: #555; font-size: 12px;'>
            📁 {st.session_state.file_name}  &nbsp;|&nbsp;  
            {df.shape[0]:,} rows × {df.shape[1]} cols
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── OVERVIEW ──────────────────────────────────────
    if section == "overview":
        # Metric cards
        c1, c2, c3, c4, c5 = st.columns(5)
        metrics = [
            ("Total Rows", f"{df.shape[0]:,}", "📊"),
            ("Columns", df.shape[1], "📋"),
            ("Missing Values", df.isnull().sum().sum(), "❓"),
            ("Duplicates", df.duplicated().sum(), "🔁"),
            ("Numeric Cols", len(num_cols), "🔢"),
        ]
        for col, (label, val, icon) in zip([c1,c2,c3,c4,c5], metrics):
            col.markdown(f"""
            <div style='background: #1a1d2e; border: 1px solid #2d3250; border-radius: 12px; 
                        padding: 16px; text-align: center;'>
                <div style='font-size: 24px; margin-bottom: 4px;'>{icon}</div>
                <div style='font-size: 22px; font-weight: 700; color: white;'>{val}</div>
                <div style='font-size: 11px; color: #888; text-transform: uppercase;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        n_rows = st.slider("Rows to preview", 5, 50, 10)
        st.dataframe(df.head(n_rows), use_container_width=True)
        with st.expander("👁️ View Full Dataset"):
            st.dataframe(df, use_container_width=True)

    # ── SCHEMA ────────────────────────────────────────
    elif section == "schema":
        st.markdown('<div class="section-title">Schema Analysis</div>', unsafe_allow_html=True)
        col_info = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.values,
            "Missing": df.isnull().sum().values,
            "Missing %": (df.isnull().sum().values / len(df) * 100).round(2),
            "Unique Values": [df[col].nunique() for col in df.columns],
            "Sample Value": [df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else "N/A" for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)

    # ── STATISTICAL SUMMARY ───────────────────────────
    elif section == "stats":
        st.markdown('<div class="section-title">Statistical Summary</div>', unsafe_allow_html=True)
        if num_cols:
            st.subheader("Numeric Columns")
            st.dataframe(df[num_cols].describe().round(2), use_container_width=True)
        st.markdown("---")
        if cat_cols:
            st.subheader("Categorical Columns")
            selected_cat = st.selectbox("Select column", cat_cols)
            vc = df[selected_cat].value_counts().head(20).reset_index()
            vc.columns = [selected_cat, "Count"]
            c1, c2 = st.columns(2)
            with c1:
                st.dataframe(vc, use_container_width=True)
            with c2:
                fig = px.pie(vc, names=selected_cat, values="Count") if len(vc) <= 10 else px.bar(vc, x=selected_cat, y="Count", color_discrete_sequence=["#667eea"])
                fig.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
                st.plotly_chart(fig, use_container_width=True)

    # ── DATA QUALITY ──────────────────────────────────
    elif section == "quality":
        st.markdown('<div class="section-title">Data Quality Index</div>', unsafe_allow_html=True)
        missing_score = 100 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
        duplicate_score = 100 - (df.duplicated().sum() / df.shape[0] * 100)
        health_score = round((missing_score + duplicate_score) / 2, 1)

        if health_score >= 80:
            status = "🟢 Healthy Dataset"
            color = "#43e97b"
        elif health_score >= 50:
            status = "🟡 Needs Attention"
            color = "#f6c90e"
        else:
            status = "🔴 Poor Quality"
            color = "#ff6b6b"

        c1, c2, c3, c4 = st.columns(4)
        for col, (label, val, clr) in zip([c1,c2,c3,c4], [
            ("Overall Score", f"{health_score}/100", color),
            ("Status", status.split(" ",1)[1], color),
            ("Missing Score", f"{round(missing_score,1)}/100", "#667eea"),
            ("Duplicate Score", f"{round(duplicate_score,1)}/100", "#764ba2"),
        ]):
            col.markdown(f"""
            <div style='background: #1a1d2e; border: 1px solid #2d3250; border-radius: 12px; padding: 16px; text-align: center;'>
                <div style='font-size: 20px; font-weight: 700; color: {clr};'>{val}</div>
                <div style='font-size: 11px; color: #888; margin-top: 4px;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        fig = px.bar(
            x=["Missing Score", "Duplicate Score", "Overall Score"],
            y=[round(missing_score,1), round(duplicate_score,1), health_score],
            color=["Missing Score", "Duplicate Score", "Overall Score"],
            text_auto=True,
            color_discrete_sequence=["#667eea", "#764ba2", "#43e97b"]
        )
        fig.update_yaxes(range=[0,100])
        fig.update_layout(showlegend=False, paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # ── MISSING VALUE HANDLER ─────────────────────────
    elif section == "missing":
        st.markdown('<div class="section-title">Missing Value Handler</div>', unsafe_allow_html=True)
        missing_cols = df.columns[df.isnull().any()].tolist()
        if not missing_cols:
            st.success("✅ No missing values found!")
        else:
            st.warning(f"⚠️ {len(missing_cols)} columns have missing values")
            for col in missing_cols:
                with st.expander(f"📌 {col} — {df[col].isnull().sum()} missing"):
                    st.dataframe(df[df[col].isnull()], use_container_width=True)
                    opts = ["Keep as is", "Drop rows", "Fill with Mean", "Fill with Median", "Fill with Mode"] if col in num_cols else ["Keep as is", "Drop rows", "Fill with Mode"]
                    action = st.selectbox(f"Handle '{col}'", opts, key=f"mv_{col}")
                    if st.button(f"Apply", key=f"ap_{col}"):
                        if action == "Drop rows":
                            st.session_state.df_cleaned = st.session_state.df_cleaned.dropna(subset=[col])
                        elif action == "Fill with Mean":
                            st.session_state.df_cleaned[col] = st.session_state.df_cleaned[col].fillna(st.session_state.df_cleaned[col].mean())
                        elif action == "Fill with Median":
                            st.session_state.df_cleaned[col] = st.session_state.df_cleaned[col].fillna(st.session_state.df_cleaned[col].median())
                        elif action == "Fill with Mode":
                            st.session_state.df_cleaned[col] = st.session_state.df_cleaned[col].fillna(st.session_state.df_cleaned[col].mode()[0])
                        st.success("✅ Applied!")
                        st.rerun()

    # ── ADVANCED CLEANING ─────────────────────────────
    elif section == "cleaning":
        st.markdown('<div class="section-title">Advanced Cleaning</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["🔁 Duplicates", "🔄 Type Converter", "✂️ Whitespace"])

        with tab1:
            dup = df.duplicated().sum()
            if dup == 0:
                st.success("✅ No duplicates!")
            else:
                st.warning(f"⚠️ {dup} duplicate rows")
                with st.expander("View duplicates"):
                    st.dataframe(df[df.duplicated()], use_container_width=True)
                if st.button("Remove All Duplicates"):
                    before = len(st.session_state.df_cleaned)
                    st.session_state.df_cleaned = st.session_state.df_cleaned.drop_duplicates()
                    st.success(f"✅ Removed {before - len(st.session_state.df_cleaned)} rows")
                    st.rerun()

        with tab2:
            col_sel = st.selectbox("Column", df.columns.tolist())
            st.write(f"Type: `{df[col_sel].dtype}` | Sample: {df[col_sel].dropna().head(3).tolist()}")
            ttype = st.radio("Convert to", ["Numeric", "Text", "DateTime", "Category"], horizontal=True)
            if st.button("Convert"):
                try:
                    if ttype == "Numeric":
                        st.session_state.df_cleaned[col_sel] = pd.to_numeric(st.session_state.df_cleaned[col_sel], errors='coerce')
                    elif ttype == "Text":
                        st.session_state.df_cleaned[col_sel] = st.session_state.df_cleaned[col_sel].astype(str)
                    elif ttype == "DateTime":
                        st.session_state.df_cleaned[col_sel] = pd.to_datetime(st.session_state.df_cleaned[col_sel], errors='coerce')
                    elif ttype == "Category":
                        st.session_state.df_cleaned[col_sel] = st.session_state.df_cleaned[col_sel].astype('category')
                    st.success("✅ Converted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {e}")

        with tab3:
            st.info("Strips leading/trailing spaces from all text columns")
            if st.button("Clean Whitespace"):
                for col in cat_cols:
                    try:
                        st.session_state.df_cleaned[col] = st.session_state.df_cleaned[col].str.strip()
                    except:
                        pass
                st.success("✅ Done!")
                st.rerun()

    # ── OUTLIER DETECTION ─────────────────────────────
    elif section == "outliers":
        st.markdown('<div class="section-title">Outlier Detection</div>', unsafe_allow_html=True)
        if not num_cols:
            st.warning("No numeric columns")
        else:
            summary = []
            for col in num_cols:
                Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower, upper = Q1-1.5*IQR, Q3+1.5*IQR
                count = df[(df[col]<lower)|(df[col]>upper)].shape[0]
                summary.append({"Column": col, "Outliers": count, "Lower": round(lower,2), "Upper": round(upper,2), "Min": round(df[col].min(),2), "Max": round(df[col].max(),2)})
            st.dataframe(pd.DataFrame(summary), use_container_width=True)
            st.markdown("---")
            sel = st.selectbox("Inspect", num_cols)
            chart = st.radio("Chart", ["Box Plot", "Histogram", "Violin"], horizontal=True)
            Q1, Q3 = df[sel].quantile(0.25), df[sel].quantile(0.75)
            IQR = Q3-Q1
            out_rows = df[(df[sel]<Q1-1.5*IQR)|(df[sel]>Q3+1.5*IQR)]
            if chart == "Box Plot":
                fig = px.box(df, y=sel, color_discrete_sequence=["#667eea"])
            elif chart == "Histogram":
                fig = px.histogram(df, x=sel, color_discrete_sequence=["#667eea"])
            else:
                fig = px.violin(df, y=sel, box=True, color_discrete_sequence=["#667eea"])
            fig.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
            st.plotly_chart(fig, use_container_width=True)
            with st.expander(f"👁️ {len(out_rows)} outlier rows"):
                st.dataframe(out_rows, use_container_width=True)

    # ── CORRELATION MATRIX ────────────────────────────
    elif section == "correlation":
        st.markdown('<div class="section-title">Correlation Matrix</div>', unsafe_allow_html=True)
        if len(num_cols) < 2:
            st.warning("Need 2+ numeric columns")
        else:
            corr = df[num_cols].corr().round(2)
            fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", aspect="auto")
            fig.update_layout(paper_bgcolor="#1a1d2e", font_color="white")
            st.plotly_chart(fig, use_container_width=True)
            strong = [{"Col 1": corr.columns[i], "Col 2": corr.columns[j], "Correlation": corr.iloc[i,j], "Type": "Positive" if corr.iloc[i,j]>0 else "Negative"}
                     for i in range(len(corr.columns)) for j in range(i+1,len(corr.columns)) if abs(corr.iloc[i,j])>=0.5]
            if strong:
                st.subheader("Strong Correlations (≥ 0.5)")
                st.dataframe(pd.DataFrame(strong), use_container_width=True)

    # ── COLUMN DRILL DOWN ─────────────────────────────
    elif section == "drilldown":
        st.markdown('<div class="section-title">Column Drill Down</div>', unsafe_allow_html=True)
        sel = st.selectbox("Select column", df.columns.tolist())
        c1,c2,c3,c4 = st.columns(4)
        for col, (lbl, val) in zip([c1,c2,c3,c4],[("Type",str(df[sel].dtype)),("Unique",df[sel].nunique()),("Missing",df[sel].isnull().sum()),("Missing %",f"{round(df[sel].isnull().sum()/len(df)*100,2)}%")]):
            col.metric(lbl, val)
        st.markdown("---")
        if sel in num_cols:
            c1,c2,c3,c4,c5 = st.columns(5)
            for col,(lbl,val) in zip([c1,c2,c3,c4,c5],[("Mean",round(df[sel].mean(),2)),("Median",round(df[sel].median(),2)),("Std",round(df[sel].std(),2)),("Min",round(df[sel].min(),2)),("Max",round(df[sel].max(),2))]):
                col.metric(lbl,val)
            c1,c2 = st.columns(2)
            with c1:
                fig = px.histogram(df, x=sel, color_discrete_sequence=["#667eea"])
                fig.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig2 = px.box(df, y=sel, color_discrete_sequence=["#764ba2"])
                fig2.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
                st.plotly_chart(fig2, use_container_width=True)
        else:
            vc = df[sel].value_counts().head(15).reset_index()
            vc.columns = [sel,"Count"]
            c1,c2 = st.columns(2)
            with c1:
                st.dataframe(vc, use_container_width=True)
            with c2:
                fig = px.pie(vc, names=sel, values="Count") if len(vc)<=8 else px.bar(vc, x=sel, y="Count", color_discrete_sequence=["#667eea"])
                fig.update_layout(paper_bgcolor="#1a1d2e", font_color="white")
                st.plotly_chart(fig, use_container_width=True)

    # ── GROUP BY ──────────────────────────────────────
    elif section == "groupby":
        st.markdown('<div class="section-title">Group By Analysis</div>', unsafe_allow_html=True)
        if not cat_cols or not num_cols:
            st.warning("Need both categorical and numeric columns")
        else:
            c1,c2,c3 = st.columns(3)
            with c1: grp = st.selectbox("Group By", cat_cols)
            with c2: val = st.selectbox("Value", num_cols)
            with c3: agg = st.selectbox("Aggregation", ["Mean","Sum","Count","Max","Min","Median"])
            agg_map = {"Mean":"mean","Sum":"sum","Count":"count","Max":"max","Min":"min","Median":"median"}
            result = df.groupby(grp)[val].agg(agg_map[agg]).reset_index()
            result.columns = [grp, f"{agg} of {val}"]
            result = result.sort_values(f"{agg} of {val}", ascending=False)
            c1,c2 = st.columns(2)
            with c1:
                st.dataframe(result, use_container_width=True)
            with c2:
                chart = st.radio("Chart", ["Bar","Pie"], horizontal=True)
                fig = px.bar(result, x=grp, y=f"{agg} of {val}", text_auto=True, color_discrete_sequence=["#667eea"]) if chart=="Bar" else px.pie(result, names=grp, values=f"{agg} of {val}")
                fig.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
                st.plotly_chart(fig, use_container_width=True)
            st.success(f"Highest: {result.iloc[0][grp]} — {round(result.iloc[0].iloc[1],2)}")
            st.error(f"Lowest: {result.iloc[-1][grp]} — {round(result.iloc[-1].iloc[1],2)}")

    # ── SMART CHART ENGINE ────────────────────────────
    elif section == "charts":
        st.markdown('<div class="section-title">Smart Chart Engine</div>', unsafe_allow_html=True)
        atype = st.radio("", ["Single Column","Two Columns"], horizontal=True)
        if atype == "Single Column":
            col_s = st.selectbox("Column", df.columns.tolist())
            if col_s in num_cols:
                ct = st.radio("Chart", ["Histogram","Box Plot","Violin"], horizontal=True)
                fig = px.histogram(df, x=col_s, color_discrete_sequence=["#667eea"]) if ct=="Histogram" else (px.box(df, y=col_s, color_discrete_sequence=["#667eea"]) if ct=="Box Plot" else px.violin(df, y=col_s, box=True, color_discrete_sequence=["#667eea"]))
            elif col_s in date_cols:
                vc = df[col_s].value_counts().sort_index().reset_index()
                vc.columns = [col_s,"Count"]
                fig = px.line(vc, x=col_s, y="Count", color_discrete_sequence=["#667eea"])
            else:
                ct = st.radio("Chart", ["Bar","Pie"], horizontal=True)
                vc = df[col_s].value_counts().head(15).reset_index()
                vc.columns = [col_s,"Count"]
                fig = px.bar(vc, x=col_s, y="Count", color_discrete_sequence=["#667eea"]) if ct=="Bar" else px.pie(vc, names=col_s, values="Count")
            fig.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            col_x = st.selectbox("X axis", df.columns.tolist(), key="cx")
            if col_x in date_cols:
                col_y = st.selectbox("Y axis", num_cols, key="cy")
                df_t = df[[col_x,col_y]].copy()
                df_t[col_x] = pd.to_datetime(df_t[col_x], errors='coerce')
                fig = px.line(df_t.sort_values(col_x), x=col_x, y=col_y, color_discrete_sequence=["#667eea"])
            elif col_x in num_cols:
                rem = [c for c in num_cols if c!=col_x]
                if not rem:
                    st.warning("Select different column")
                    st.stop()
                col_y = st.selectbox("Y axis", rem, key="cy")
                ct = st.radio("Chart", ["Scatter","Area"], horizontal=True)
                fig = px.scatter(df, x=col_x, y=col_y, trendline="ols", color_discrete_sequence=["#667eea"]) if ct=="Scatter" else px.area(df.sort_values(col_x), x=col_x, y=col_y, color_discrete_sequence=["#667eea"])
            else:
                col_y = st.selectbox("Y axis", num_cols, key="cy")
                ct = st.radio("Chart", ["Box","Bar","Violin"], horizontal=True)
                if ct=="Box": fig = px.box(df, x=col_x, y=col_y, color_discrete_sequence=["#667eea"])
                elif ct=="Bar": fig = px.bar(df, x=col_x, y=col_y, color_discrete_sequence=["#667eea"])
                else: fig = px.violin(df, x=col_x, y=col_y, color_discrete_sequence=["#667eea"])
            fig.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
            st.plotly_chart(fig, use_container_width=True)

    # ── KPI DASHBOARD ─────────────────────────────────
    elif section == "kpi":
        st.markdown('<div class="section-title">KPI Dashboard</div>', unsafe_allow_html=True)
        if not num_cols:
            st.warning("No numeric columns")
        else:
            kpi = st.selectbox("Column", num_cols)
            c1,c2,c3,c4,c5 = st.columns(5)
            for col,(lbl,val) in zip([c1,c2,c3,c4,c5],[("Mean",round(df[kpi].mean(),2)),("Median",round(df[kpi].median(),2)),("Max",round(df[kpi].max(),2)),("Min",round(df[kpi].min(),2)),("Std Dev",round(df[kpi].std(),2))]):
                col.metric(lbl,val)
            c1,c2 = st.columns(2)
            with c1:
                fig = px.histogram(df, x=kpi, color_discrete_sequence=["#667eea"])
                fig.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig2 = px.box(df, y=kpi, color_discrete_sequence=["#764ba2"])
                fig2.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
                st.plotly_chart(fig2, use_container_width=True)

    # ── AI INSIGHTS ───────────────────────────────────
    elif section == "ai":
        st.markdown('<div class="section-title">AI Insights — Powered by Groq LLaMA 3.3</div>', unsafe_allow_html=True)

        context = f"""
Dataset: {st.session_state.file_name}
Rows: {df.shape[0]}, Columns: {df.shape[1]}
Columns: {list(df.columns)}
Missing: {df.isnull().sum().sum()}, Duplicates: {df.duplicated().sum()}
Numeric: {num_cols}, Categorical: {cat_cols}
Stats: {df[num_cols].describe().round(2).to_string() if num_cols else 'None'}
"""
        tab1,tab2,tab3,tab4 = st.tabs(["📊 Summary","💡 Key Insights","📋 Recommendations","⚠️ Risk Analysis"])

        with tab1:
            c1,c2 = st.columns(2)
            with c1:
                td = {"Type":["Numeric","Categorical","Date"],"Count":[len(num_cols),len(cat_cols),len(date_cols)]}
                fig = px.bar(td, x="Type", y="Count", color="Type", text_auto=True, color_discrete_sequence=["#667eea","#764ba2","#43e97b"])
                fig.update_layout(showlegend=False, paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                mv = df.isnull().sum()
                mv = mv[mv>0]
                if len(mv)>0:
                    fig2 = px.bar(x=mv.index, y=mv.values, color=mv.values, color_continuous_scale="Reds", text_auto=True)
                    fig2.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e", font_color="white", showlegend=False)
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.success("✅ No missing values!")
            if st.button("🤖 Generate AI Summary"):
                with st.spinner("Analyzing..."):
                    prompt = f"""Senior data analyst. Analyze dataset.
{context}
Format:
### What is this dataset about?
[2-3 sentences]
### Key Characteristics
- [point with numbers]
- [point with numbers]
- [point with numbers]
### Data Quality Assessment
- **Completeness:** [%]
- **Overall:** [Good/Fair/Poor]
### Most Important Columns
- **[col]:** [why important]
- **[col]:** [why important]
No italic formatting."""
                    st.markdown(groq_response(prompt))

        with tab2:
            if len(num_cols)>=2:
                corr = df[num_cols].corr().round(2)
                fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", aspect="auto")
                fig.update_layout(paper_bgcolor="#1a1d2e", font_color="white")
                st.plotly_chart(fig, use_container_width=True)
                strong_corr = [{"Col1":corr.columns[i],"Col2":corr.columns[j],"Val":corr.iloc[i,j]} for i in range(len(corr.columns)) for j in range(i+1,len(corr.columns)) if abs(corr.iloc[i,j])>=0.5]
            else:
                strong_corr = []
            if st.button("🤖 Generate Key Insights"):
                with st.spinner("Finding patterns..."):
                    prompt = f"""Senior data analyst. 5 key insights.
{context}
Strong correlations: {strong_corr}
Format exactly:
### Insight 1: [Title]
**Finding:** [specific with numbers]
**Business Impact:** [meaning]
### Insight 2: [Title]
**Finding:** [specific with numbers]
**Business Impact:** [meaning]
### Insight 3: [Title]
**Finding:** [specific with numbers]
**Business Impact:** [meaning]
### Insight 4: [Title]
**Finding:** [specific with numbers]
**Business Impact:** [meaning]
### Insight 5: [Title]
**Finding:** [specific with numbers]
**Business Impact:** [meaning]
No italic formatting."""
                    st.markdown(groq_response(prompt))

        with tab3:
            ms = 100-(df.isnull().sum().sum()/(df.shape[0]*df.shape[1])*100)
            ds = 100-(df.duplicated().sum()/df.shape[0]*100)
            hs = round((ms+ds)/2,1)
            c1,c2 = st.columns(2)
            with c1:
                fig = px.pie(values=[hs,100-hs], names=["Quality",""], hole=0.7, color_discrete_sequence=["#43e97b","#1e2130"])
                fig.update_layout(showlegend=False, paper_bgcolor="#1a1d2e", font_color="white", height=220, annotations=[dict(text=f"{hs}%", font_size=22, showarrow=False)])
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                st.metric("Missing Score", f"{round(ms,1)}/100")
                st.metric("Duplicate Score", f"{round(ds,1)}/100")
                st.metric("Overall", f"{hs}/100")
            if st.button("🤖 Generate Recommendations"):
                with st.spinner("Generating..."):
                    prompt = f"""Senior data analyst. Business recommendations.
{context}
Quality: {hs}/100
Format:
### Top 3 Business Recommendations
1. **[Action]:** [recommendation]
2. **[Action]:** [recommendation]
3. **[Action]:** [recommendation]
### Data Quality Improvements
- **[Issue]:** [fix]
- **[Issue]:** [fix]
### Further Analysis
- [analysis 1]
- [analysis 2]
### Risk Flags
[flag 1]
[flag 2]
No italic formatting."""
                    st.markdown(groq_response(prompt))

        with tab4:
            if st.button("🤖 Analyze Risks"):
                with st.spinner("Analyzing risks..."):
                    prompt = f"""Senior data analyst. Identify risks.
{context}
Format:
### Data Quality Risks
- **[Risk]:** [description]
- **[Risk]:** [description]
### Business Risks
- **[Risk]:** [description]
- **[Risk]:** [description]
### Statistical Anomalies
- **[Anomaly]:** [meaning]
### Recommended Mitigations
1. [action]
2. [action]
3. [action]
No italic formatting."""
                    st.markdown(groq_response(prompt))
            

    # ── NLQ ───────────────────────────────────────────
    elif section == "nlq":
        st.markdown('<div class="section-title">💬 Ask Your Data</div>', unsafe_allow_html=True)
        st.markdown("*Ask any question in plain English — AI will analyze your dataset and answer*")
        q = st.text_input("Your question", placeholder="e.g. Which region has highest sales? What is average profit by category?")
        if st.button("🔍 Get Answer"):
            if q:
                with st.spinner("Analyzing..."):
                    prompt = f"""Senior data analyst. Answer question about dataset.
Dataset: {st.session_state.file_name}
Rows: {df.shape[0]}, Cols: {df.shape[1]}
Columns: {list(df.columns)}
Sample: {df.head(5).to_string()}
Stats: {df[num_cols].describe().round(2).to_string() if num_cols else 'None'}
Question: {q}
Format:
### Direct Answer
[answer with numbers]
### Supporting Evidence
[data points]
### Additional Context
[context/caveats]
### Suggested Next Steps
[what to analyze next]
No italic formatting."""
                    st.markdown(groq_response(prompt))
            else:
                st.warning("Enter a question")

    # ── AI PREDICTIONS ────────────────────────────────
    elif section == "predictions":
        st.markdown('<div class="section-title">🔮 AI Predictions</div>', unsafe_allow_html=True)
        tab1,tab2 = st.tabs(["📈 Trend Prediction","🎯 Anomaly Forecast"])
        context = f"Dataset: {st.session_state.file_name}\nRows: {df.shape[0]}, Cols: {df.shape[1]}\nColumns: {list(df.columns)}\nStats: {df[num_cols].describe().round(2).to_string() if num_cols else 'None'}"

        with tab1:
            if st.button("🔮 Predict Trends"):
                with st.spinner("Predicting..."):
                    prompt = f"""Forecasting expert. Predict trends.
{context}
Format:
### Short-term Trends (30 days)
- **[Metric]:** [trend + reason]
- **[Metric]:** [trend + reason]
### Medium-term (3-6 months)
- **[Area]:** [outlook]
- **[Area]:** [outlook]
### Key Drivers
- [driver 1]
- [driver 2]
### Confidence
[level + why]
No italic formatting."""
                    st.markdown(groq_response(prompt))

        with tab2:
            if st.button("🎯 Forecast Anomalies"):
                with st.spinner("Forecasting..."):
                    prompt = f"""Anomaly detection expert.
{context}
Format:
### Current Anomalies
- **[Anomaly]:** [description with numbers]
- **[Anomaly]:** [description with numbers]
### Predicted Future Anomalies
- **[Risk]:** [what + when]
- **[Risk]:** [what + when]
### Prevention
1. [action]
2. [action]
### KPIs to Monitor
- [KPI 1]
- [KPI 2]
No italic formatting."""
                    st.markdown(groq_response(prompt))

    # ── DOWNLOAD ──────────────────────────────────────
    elif section == "download":
        st.markdown('<div class="section-title">Download</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("Rows", df.shape[0])
        c2.metric("Columns", df.shape[1])
        c3.metric("Missing", df.isnull().sum().sum())
        st.markdown("---")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Cleaned CSV", data=csv, file_name="cleaned_dataset.csv", mime="text/csv")
        st.markdown("---")
        if st.button("Generate PDF Report"):
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial","B",18)
            pdf.cell(0,12,"AI Data Analyst Pro - Report",ln=True,align="C")
            pdf.set_font("Arial","",10)
            pdf.cell(0,8,f"Dataset: {st.session_state.file_name}",ln=True,align="C")
            pdf.ln(5)
            pdf.set_fill_color(102,126,234)
            pdf.set_text_color(255,255,255)
            pdf.set_font("Arial","B",13)
            pdf.cell(0,9,"  Dataset Summary",ln=True,fill=True)
            pdf.set_text_color(0,0,0)
            pdf.set_font("Arial","",10)
            pdf.ln(3)
            pdf.cell(0,7,f"Rows: {df.shape[0]} | Columns: {df.shape[1]} | Missing: {df.isnull().sum().sum()} | Duplicates: {df.duplicated().sum()}",ln=True)
            pdf.ln(5)
            ms = 100-(df.isnull().sum().sum()/(df.shape[0]*df.shape[1])*100)
            ds = 100-(df.duplicated().sum()/df.shape[0]*100)
            hs = round((ms+ds)/2,1)
            pdf.set_fill_color(102,126,234)
            pdf.set_text_color(255,255,255)
            pdf.set_font("Arial","B",13)
            pdf.cell(0,9,"  Data Quality Index",ln=True,fill=True)
            pdf.set_text_color(0,0,0)
            pdf.set_font("Arial","",10)
            pdf.ln(3)
            pdf.cell(0,7,f"Overall: {hs}/100 | Missing: {round(ms,1)}/100 | Duplicate: {round(ds,1)}/100",ln=True)
            pdf.ln(5)
            pdf.set_fill_color(102,126,234)
            pdf.set_text_color(255,255,255)
            pdf.set_font("Arial","B",13)
            pdf.cell(0,9,"  Schema Analysis",ln=True,fill=True)
            pdf.set_text_color(0,0,0)
            pdf.set_font("Arial","",9)
            pdf.ln(3)
            for col in df.columns:
                pdf.cell(0,6,f"{col} | {df[col].dtype} | Missing: {df[col].isnull().sum()} | Unique: {df[col].nunique()}",ln=True)
            pdf.ln(5)
            pdf.set_fill_color(102,126,234)
            pdf.set_text_color(255,255,255)
            pdf.set_font("Arial","B",13)
            pdf.cell(0,9,"  Statistical Summary",ln=True,fill=True)
            pdf.set_text_color(0,0,0)
            pdf.set_font("Arial","",9)
            pdf.ln(3)
            for col in num_cols:
                pdf.cell(0,6,f"{col} | Mean: {round(df[col].mean(),2)} | Median: {round(df[col].median(),2)} | Std: {round(df[col].std(),2)} | Min: {round(df[col].min(),2)} | Max: {round(df[col].max(),2)}",ln=True)
            pdf_output = bytes(pdf.output())
            st.download_button("📄 Download PDF", data=pdf_output, file_name="report.pdf", mime="application/pdf")
            st.success("✅ Ready!")