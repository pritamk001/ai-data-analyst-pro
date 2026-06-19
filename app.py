import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="AI Data Analyst Pro",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 8px 16px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2, #667eea);
        transform: scale(1.02);
    }
    .metric-card {
        background: #1e2130;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #2d3250;
    }
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        padding: 10px 20px;
        border-radius: 8px;
        color: white;
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    div[data-testid="stSidebarNav"] { display: none; }
    .sidebar-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None

# Helper
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

# Main Header
st.markdown("""
<div style='text-align:center; padding: 20px 0;'>
    <h1 style='color:#667eea;'>📊 AI Data Analyst Pro</h1>
    <p style='color:#888; font-size:1.1em;'>Transform raw data into actionable insights</p>
</div>
""", unsafe_allow_html=True)


# ── FILE UPLOADER LOGIC (Main Screen vs Sidebar) ───────────────────
# Pehle check karenge ki file uploaded hai ya nahi, uske hisab se layout decide hoga
if st.session_state.df_cleaned is None:
    # Jab file uploaded nahi hai, toh main screen par uploader dikhao
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Center aligning the file uploader using columns
    col_left, col_mid, col_right = st.columns([1, 2, 1])
    with col_mid:
        st.markdown("<h2 style='text-align:centre;'>Upload CSV to get started</h2>",unsafe_allow_html=True)
        uploaded_file= st.file_uploader("",type=["csv"])
    if uploaded_file is not None:
        st.session_state.df_cleaned = pd.read_csv(uploaded_file)
        st.session_state.file_name = uploaded_file.name
        st.rerun()
        
    # Welcome Information Cards below the uploader
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.info("📋 Auto dataset overview")
    c2.info("🧹 Clean missing values")
    c3.info("📊 Interactive charts")
    c4, c5, c6 = st.columns(3)
    c4.info("🎯 Outlier detection")
    c5.info("🔗 Correlation matrix")
    c6.info("⬇️ Download cleaned data")

else:
    # Jab file upload ho chuki ho, tab sidebar me option aur navigation dikhao
    with st.sidebar:
        st.markdown('<p class="sidebar-title">📊 AI Data Analyst Pro</p>', unsafe_allow_html=True)
        st.markdown("*Transform raw data into actionable insights*")
        st.markdown("---")
        
        # Sidebar me file change karne ka option bhi rahega
        uploaded_file = st.file_uploader("Change CSV File", type=["csv"])
        if uploaded_file is not None and uploaded_file.name != st.session_state.file_name:
            st.session_state.df_cleaned = pd.read_csv(uploaded_file)
            st.session_state.file_name = uploaded_file.name
            st.rerun()
            
        st.success(f"✅ Loaded: {st.session_state.file_name}")
        st.markdown("---")
        st.markdown("### 🧭 Navigation")
        section = st.radio("", [
            "📋 Overview",
            "🔍 Schema Analysis",
            "📊 Statistical Summary",
            "📈 Data Quality Index",
            "🧹 Missing Value Handler",
            "🔧 Advanced Cleaning",
            "🎯 Outlier Detection",
            "🔗 Correlation Matrix",
            "🔎 Column Drill Down",
            "📊 Group By Analysis",
            "📊 Smart Chart Engine",
            "🎯 KPI Dashboard",
            "⬇️ Download"
        ])

    # ── APP SECTIONS LOGIC (Only runs if data is loaded) ───────────────────
    df = st.session_state.df_cleaned.copy()
    num_cols, cat_cols, date_cols = get_col_types(df)

    # ── OVERVIEW ──────────────────────────────────────
    if section == "📋 Overview":
        st.markdown('<div class="section-header">📋 Dataset Overview</div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🗂 Rows", df.shape[0])
        c2.metric("📊 Columns", df.shape[1])
        c3.metric("🔁 Duplicates", df.duplicated().sum())
        c4.metric("❓ Missing Values", df.isnull().sum().sum())

        st.markdown("---")
        n_rows = st.slider("Rows to preview", 5, 50, 10)
        st.dataframe(df.head(n_rows), use_container_width=True)

        with st.expander("👁️ View Full Dataset"):
            st.dataframe(df, use_container_width=True)

    # ── SCHEMA ────────────────────────────────────────
    elif section == "🔍 Schema Analysis":
        st.markdown('<div class="section-header">🔍 Schema Analysis</div>', unsafe_allow_html=True)

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
    elif section == "📊 Statistical Summary":
        st.markdown('<div class="section-header">📊 Statistical Summary</div>', unsafe_allow_html=True)

        st.subheader("Numeric Columns")
        st.dataframe(df[num_cols].describe().round(2), use_container_width=True)

        st.markdown("---")
        st.subheader("📌 Categorical Columns Summary")
        if len(cat_cols) == 0:
            st.info("No categorical columns found")
        else:
            selected_cat = st.selectbox("Select categorical column", cat_cols)
            vc = df[selected_cat].value_counts().reset_index()
            vc.columns = [selected_cat, "Count"]
            vc = vc.head(20)
            c1, c2 = st.columns(2)
            with c1:
                st.dataframe(vc, use_container_width=True)
            with c2:
                if len(vc) <= 10:
                    fig = px.pie(vc, names=selected_cat, values="Count",
                                title=f"Distribution of {selected_cat}")
                else:
                    fig = px.bar(vc, x=selected_cat, y="Count",
                                title=f"Top 20 - {selected_cat}")
                st.plotly_chart(fig, use_container_width=True)

    # ── DATA QUALITY INDEX ────────────────────────────
    elif section == "📈 Data Quality Index":
        st.markdown('<div class="section-header">📈 Data Quality Index</div>', unsafe_allow_html=True)

        missing_score = 100 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
        duplicate_score = 100 - (df.duplicated().sum() / df.shape[0] * 100)
        health_score = round((missing_score + duplicate_score) / 2, 1)

        if health_score >= 80:
            color = "🟢"; status = "Healthy Dataset"
        elif health_score >= 50:
            color = "🟡"; status = "Needs Attention"
        else:
            color = "🔴"; status = "Poor Quality"

        c1, c2, c3 = st.columns(3)
        c1.metric(f"{color} Overall Score", f"{health_score}/100", status)
        c2.metric("Missing Score", f"{round(missing_score, 1)}/100")
        c3.metric("Duplicate Score", f"{round(duplicate_score, 1)}/100")

        st.markdown("---")
        fig = px.bar(
            x=["Missing Score", "Duplicate Score", "Overall Score"],
            y=[round(missing_score,1), round(duplicate_score,1), health_score],
            title="Data Quality Breakdown",
            color=["Missing Score", "Duplicate Score", "Overall Score"],
            text_auto=True,
            color_discrete_sequence=["#667eea", "#764ba2", "#43e97b"]
        )
        fig.update_yaxes(range=[0, 100])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── MISSING VALUE HANDLER ─────────────────────────
    elif section == "🧹 Missing Value Handler":
        st.markdown('<div class="section-header">🧹 Missing Value Handler</div>', unsafe_allow_html=True)

        missing_cols = df.columns[df.isnull().any()].tolist()

        if len(missing_cols) == 0:
            st.success("✅ No missing values found!")
        else:
            st.warning(f"⚠️ {len(missing_cols)} columns have missing values")
            for col in missing_cols:
                with st.expander(f"📌 {col} - {df[col].isnull().sum()} missing values"):
                    st.dataframe(df[df[col].isnull()], use_container_width=True)
                    is_numeric = col in num_cols
                    if is_numeric:
                        options = ["Keep as is", "Drop rows", "Fill with Mean", "Fill with Median", "Fill with Mode"]
                    else:
                        options = ["Keep as is", "Drop rows", "Fill with Mode"]
                    action = st.selectbox(f"Handle '{col}'", options, key=f"missing_{col}")
                    if st.button(f"Apply - {col}", key=f"apply_{col}"):
                        if action == "Drop rows":
                            st.session_state.df_cleaned = st.session_state.df_cleaned.dropna(subset=[col])
                            st.success(f"✅ Dropped rows with missing {col}")
                        elif action == "Fill with Mean":
                            mean_val = st.session_state.df_cleaned[col].mean()
                            st.session_state.df_cleaned[col] = st.session_state.df_cleaned[col].fillna(mean_val)
                            st.success(f"✅ Filled with Mean: {round(mean_val, 2)}")
                        elif action == "Fill with Median":
                            median_val = st.session_state.df_cleaned[col].median()
                            st.session_state.df_cleaned[col] = st.session_state.df_cleaned[col].fillna(median_val)
                            st.success(f"✅ Filled with Median: {round(median_val, 2)}")
                        elif action == "Fill with Mode":
                            mode_val = st.session_state.df_cleaned[col].mode()[0]
                            st.session_state.df_cleaned[col] = st.session_state.df_cleaned[col].fillna(mode_val)
                            st.success(f"✅ Filled with Mode: {mode_val}")
                        st.rerun()

    # ── ADVANCED CLEANING ─────────────────────────────
    elif section == "🔧 Advanced Cleaning":
        st.markdown('<div class="section-header">🔧 Advanced Cleaning</div>', unsafe_allow_html=True)

        st.subheader("🔁 Duplicate Row Remover")
        dup_count = df.duplicated().sum()
        if dup_count == 0:
            st.success("✅ No duplicate rows found!")
        else:
            st.warning(f"⚠️ {dup_count} duplicate rows found")
            with st.expander("👁️ View Duplicate Rows"):
                st.dataframe(df[df.duplicated()], use_container_width=True)
            if st.button("🗑️ Remove All Duplicates"):
                before = len(st.session_state.df_cleaned)
                st.session_state.df_cleaned = st.session_state.df_cleaned.drop_duplicates()
                after = len(st.session_state.df_cleaned)
                st.success(f"✅ Removed {before - after} duplicate rows - {after} rows remaining")
                st.rerun()

        st.markdown("---")
        st.subheader("🔄 Data Type Converter")
        st.info("Fix columns that have wrong data types")

        type_col = st.selectbox("Select column to convert", df.columns.tolist(), key="type_col")
        current_type = str(df[type_col].dtype)
        st.write(f"**Current type:** `{current_type}`")
        st.write(f"**Sample values:** {df[type_col].dropna().head(3).tolist()}")

        target_type = st.radio("Convert to",
            ["Numeric", "Text/String", "DateTime", "Category"],
            horizontal=True, key="target_type")

        if st.button("Convert Type"):
            try:
                if target_type == "Numeric":
                    st.session_state.df_cleaned[type_col] = pd.to_numeric(
                        st.session_state.df_cleaned[type_col], errors='coerce')
                elif target_type == "Text/String":
                    st.session_state.df_cleaned[type_col] = st.session_state.df_cleaned[type_col].astype(str)
                elif target_type == "DateTime":
                    st.session_state.df_cleaned[type_col] = pd.to_datetime(
                        st.session_state.df_cleaned[type_col], errors='coerce')
                elif target_type == "Category":
                    st.session_state.df_cleaned[type_col] = st.session_state.df_cleaned[type_col].astype('category')
                st.success(f"✅ {type_col} converted to {target_type}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Conversion failed: {e}")

        st.markdown("---")
        st.subheader("✂️ Whitespace Cleaner")
        if len(cat_cols) == 0:
            st.info("No text columns found")
        else:
            if st.button("Clean All Text Columns"):
                for col in cat_cols:
                    try:
                        st.session_state.df_cleaned[col] = st.session_state.df_cleaned[col].str.strip()
                    except:
                        pass
                st.success("✅ Whitespace removed from all text columns")
                st.rerun()

    # ── OUTLIER DETECTION ─────────────────────────────
    elif section == "🎯 Outlier Detection":
        st.markdown('<div class="section-header">🎯 Outlier Detection</div>', unsafe_allow_html=True)

        if len(num_cols) == 0:
            st.warning("No numeric columns found")
        else:
            outlier_summary = []
            for col in num_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                outlier_count = df[(df[col] < lower) | (df[col] > upper)].shape[0]
                outlier_summary.append({
                    "Column": col,
                    "Outliers Found": outlier_count,
                    "Lower Bound": round(lower, 2),
                    "Upper Bound": round(upper, 2),
                    "Min": round(df[col].min(), 2),
                    "Max": round(df[col].max(), 2)
                })
            st.dataframe(pd.DataFrame(outlier_summary), use_container_width=True)
            st.markdown("---")
            selected_col = st.selectbox("Select column to inspect", num_cols)
            chart_choice = st.radio("Chart type", ["Box Plot", "Histogram", "Violin Plot"], horizontal=True)
            Q1 = df[selected_col].quantile(0.25)
            Q3 = df[selected_col].quantile(0.75)
            IQR = Q3 - Q1
            outlier_rows = df[(df[selected_col] < Q1-1.5*IQR) | (df[selected_col] > Q3+1.5*IQR)]
            if chart_choice == "Box Plot":
                fig = px.box(df, y=selected_col, title=f"Box Plot - {selected_col}")
            elif chart_choice == "Histogram":
                fig = px.histogram(df, x=selected_col, title=f"Distribution - {selected_col}")
            else:
                fig = px.violin(df, y=selected_col, title=f"Violin Plot - {selected_col}", box=True)
            st.plotly_chart(fig, use_container_width=True)
            with st.expander(f"👁️ View {len(outlier_rows)} outlier rows"):
                st.dataframe(outlier_rows, use_container_width=True)

    # ── CORRELATION MATRIX ────────────────────────────
    elif section == "🔗 Correlation Matrix":
        st.markdown('<div class="section-header">🔗 Correlation Matrix</div>', unsafe_allow_html=True)

        if len(num_cols) < 2:
            st.warning("Need at least 2 numeric columns")
        else:
            corr_matrix = df[num_cols].corr().round(2)
            fig_corr = px.imshow(corr_matrix, text_auto=True,
                                color_continuous_scale="RdBu_r",
                                title="Correlation Heatmap", aspect="auto")
            st.plotly_chart(fig_corr, use_container_width=True)
            strong = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    val = corr_matrix.iloc[i, j]
                    if abs(val) >= 0.5:
                        strong.append({
                            "Column 1": corr_matrix.columns[i],
                            "Column 2": corr_matrix.columns[j],
                            "Correlation": val,
                            "Relationship": "Strong Positive" if val > 0 else "Strong Negative"
                        })
            st.markdown("---")
            st.subheader("Strong Correlations Found")
            if len(strong) == 0:
                st.info("No strong correlations found")
            else:
                st.dataframe(pd.DataFrame(strong), use_container_width=True)

    # ── COLUMN DRILL DOWN ─────────────────────────────
    elif section == "🔎 Column Drill Down":
        st.markdown('<div class="section-header">🔎 Column Drill Down</div>', unsafe_allow_html=True)

        selected = st.selectbox("Select any column", df.columns.tolist())
        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Type", str(df[selected].dtype))
        c2.metric("Unique Values", df[selected].nunique())
        c3.metric("Missing", df[selected].isnull().sum())
        c4.metric("Missing %", f"{round(df[selected].isnull().sum()/len(df)*100, 2)}%")
        st.markdown("---")
        if selected in num_cols:
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Mean", round(df[selected].mean(), 2))
            c2.metric("Median", round(df[selected].median(), 2))
            c3.metric("Std Dev", round(df[selected].std(), 2))
            c4.metric("Min", round(df[selected].min(), 2))
            c5.metric("Max", round(df[selected].max(), 2))
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                fig = px.histogram(df, x=selected, title=f"Distribution - {selected}")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig2 = px.box(df, y=selected, title=f"Spread - {selected}")
                st.plotly_chart(fig2, use_container_width=True)
            Q1 = df[selected].quantile(0.25)
            Q3 = df[selected].quantile(0.75)
            IQR = Q3 - Q1
            outlier_count = df[(df[selected] < Q1-1.5*IQR) | (df[selected] > Q3+1.5*IQR)].shape[0]
            st.info(f"Outliers detected: {outlier_count} rows")
        elif selected in date_cols:
            st.info("Date column detected")
            vc = df[selected].value_counts().head(10).reset_index()
            vc.columns = [selected, "Count"]
            fig = px.bar(vc, x=selected, y="Count", title=f"Top 10 dates - {selected}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            vc = df[selected].value_counts().head(15).reset_index()
            vc.columns = [selected, "Count"]
            c1, c2 = st.columns(2)
            with c1:
                st.dataframe(vc, use_container_width=True)
            with c2:
                if len(vc) <= 8:
                    fig = px.pie(vc, names=selected, values="Count", title=f"Distribution - {selected}")
                else:
                    fig = px.bar(vc, x=selected, y="Count", title=f"Top 15 - {selected}")
                st.plotly_chart(fig, use_container_width=True)

    # ── GROUP BY ANALYSIS ─────────────────────────────
    elif section == "📊 Group By Analysis":
        st.markdown('<div class="section-header">📊 Group By Analysis</div>', unsafe_allow_html=True)

        if len(cat_cols) == 0:
            st.warning("No categorical columns found for grouping")
        elif len(num_cols) == 0:
            st.warning("No numeric columns found for aggregation")
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                group_col = st.selectbox("Group By", cat_cols, key="grp_col")
            with c2:
                value_col = st.selectbox("Value Column", num_cols, key="val_col")
            with c3:
                agg_func = st.selectbox("Aggregation",
                    ["Mean", "Sum", "Count", "Max", "Min", "Median"], key="agg_func")

            agg_map = {"Mean": "mean", "Sum": "sum", "Count": "count",
                      "Max": "max", "Min": "min", "Median": "median"}

            result = df.groupby(group_col)[value_col].agg(agg_map[agg_func]).reset_index()
            result.columns = [group_col, f"{agg_func} of {value_col}"]
            result = result.sort_values(f"{agg_func} of {value_col}", ascending=False)

            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.dataframe(result, use_container_width=True)
            with c2:
                chart_opt = st.radio("Chart Type", ["Bar Chart", "Pie Chart"], horizontal=True)
                if chart_opt == "Bar Chart":
                    fig = px.bar(result, x=group_col, y=f"{agg_func} of {value_col}",
                                title=f"{agg_func} of {value_col} by {group_col}", text_auto=True)
                else:
                    fig = px.pie(result, names=group_col, values=f"{agg_func} of {value_col}",
                                title=f"{agg_func} of {value_col} by {group_col}")
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            top = result.iloc[0]
            bottom = result.iloc[-1]
            st.success(f"Highest: {top[group_col]} - {round(top.iloc[1], 2)}")
            st.error(f"Lowest: {bottom[group_col]} - {round(bottom.iloc[1], 2)}")

    # ── SMART CHART ENGINE ────────────────────────────
    elif section == "📊 Smart Chart Engine":
        st.markdown('<div class="section-header">📊 Smart Chart Engine</div>', unsafe_allow_html=True)

        all_cols = df.columns.tolist()
        analysis_type = st.radio("Analysis Type", ["Single Column", "Two Columns"], horizontal=True)

        if analysis_type == "Single Column":
            col_selected = st.selectbox("Select Column", all_cols)
            if col_selected in num_cols:
                chart_opt = st.radio("Chart Type", ["Histogram", "Box Plot", "Violin Plot"], horizontal=True)
                if chart_opt == "Histogram":
                    fig = px.histogram(df, x=col_selected, title=f"Distribution - {col_selected}")
                elif chart_opt == "Box Plot":
                    fig = px.box(df, y=col_selected, title=f"Box Plot - {col_selected}")
                else:
                    fig = px.violin(df, y=col_selected, title=f"Violin - {col_selected}", box=True)
            elif col_selected in date_cols:
                vc = df[col_selected].value_counts().sort_index().reset_index()
                vc.columns = [col_selected, "Count"]
                fig = px.line(vc, x=col_selected, y="Count", title=f"Frequency - {col_selected}")
            else:
                chart_opt = st.radio("Chart Type", ["Bar Chart", "Pie Chart"], horizontal=True)
                vc = df[col_selected].value_counts().head(15).reset_index()
                vc.columns = [col_selected, "Count"]
                if chart_opt == "Bar Chart":
                    fig = px.bar(vc, x=col_selected, y="Count", title=f"Value Counts - {col_selected}")
                else:
                    fig = px.pie(vc, names=col_selected, values="Count", title=f"Distribution - {col_selected}")
            st.plotly_chart(fig, use_container_width=True)

        else:
            col_x = st.selectbox("Select X axis", all_cols, key="x_col")
            if col_x in date_cols:
                col_y = st.selectbox("Select Y axis", num_cols, key="y_col")
                chart_opt = st.radio("Chart Type", ["Line Chart", "Bar Chart"], horizontal=True)
                df_temp = df[[col_x, col_y]].copy()
                df_temp[col_x] = pd.to_datetime(df_temp[col_x], errors='coerce')
                df_temp = df_temp.sort_values(col_x)
                if chart_opt == "Line Chart":
                    fig = px.line(df_temp, x=col_x, y=col_y, title=f"{col_y} over {col_x}")
                else:
                    fig = px.bar(df_temp, x=col_x, y=col_y, title=f"{col_y} by {col_x}")
            elif col_x in num_cols:
                remaining = [c for c in num_cols if c != col_x]
                if len(remaining) == 0:
                    st.warning("Select different X axis column")
                    st.stop()
                col_y = st.selectbox("Select Y axis", remaining, key="y_col")
                chart_opt = st.radio("Chart Type", ["Scatter Plot", "Area Chart"], horizontal=True)
                if chart_opt == "Scatter Plot":
                    fig = px.scatter(df, x=col_x, y=col_y, title=f"{col_x} vs {col_y}", trendline="ols")
                else:
                    fig = px.area(df.sort_values(col_x), x=col_x, y=col_y, title=f"{col_x} vs {col_y}")
            else:
                col_y = st.selectbox("Select Y axis", num_cols, key="y_col")
                chart_opt = st.radio("Chart Type", ["Box Plot", "Bar Chart", "Violin Plot"], horizontal=True)
                if chart_opt == "Box Plot":
                    fig = px.box(df, x=col_x, y=col_y, title=f"{col_y} by {col_x}")
                elif chart_opt == "Bar Chart":
                    fig = px.bar(df, x=col_x, y=col_y, title=f"{col_y} by {col_x}")
                else:
                    fig = px.violin(df, x=col_x, y=col_y, title=f"{col_y} by {col_x}")
            st.plotly_chart(fig, use_container_width=True)

    # ── KPI DASHBOARD ─────────────────────────────────
    elif section == "🎯 KPI Dashboard":
        st.markdown('<div class="section-header">🎯 KPI Dashboard</div>', unsafe_allow_html=True)

        if len(num_cols) == 0:
            st.warning("No numeric columns found")
        else:
            kpi_col = st.selectbox("Select column", num_cols)
            k1, k2, k3, k4, k5 = st.columns(5)
            k1.metric("Mean", round(df[kpi_col].mean(), 2))
            k2.metric("Median", round(df[kpi_col].median(), 2))
            k3.metric("Max", round(df[kpi_col].max(), 2))
            k4.metric("Min", round(df[kpi_col].min(), 2))
            k5.metric("Std Dev", round(df[kpi_col].std(), 2))
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                fig = px.histogram(df, x=kpi_col, title=f"Distribution - {kpi_col}")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig2 = px.box(df, y=kpi_col, title=f"Spread - {kpi_col}")
                st.plotly_chart(fig2, use_container_width=True)

    # ── DOWNLOAD ──────────────────────────────────────
    elif section == "⬇️ Download":
        st.markdown('<div class="section-header">⬇️ Download</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Rows", df.shape[0])
        c2.metric("Total Columns", df.shape[1])
        c3.metric("Remaining Missing", df.isnull().sum().sum())

        st.markdown("---")
        st.subheader("📥 Download Cleaned CSV")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.subheader("📄 Download PDF Report")

        if st.button("Generate PDF Report"):
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()

            # Title
            pdf.set_font("Arial", "B", 18)
            pdf.cell(0, 12, "AI Data Analyst Pro - Report", ln=True, align="C")
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 8, f"Dataset: {st.session_state.file_name}", ln=True, align="C")
            pdf.ln(5)

            # Dataset Summary
            pdf.set_fill_color(102, 126, 234)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 9, "  Dataset Summary", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 10)
            pdf.ln(3)
            pdf.cell(0, 7, f"Total Rows: {df.shape[0]}", ln=True)
            pdf.cell(0, 7, f"Total Columns: {df.shape[1]}", ln=True)
            pdf.cell(0, 7, f"Duplicate Rows: {df.duplicated().sum()}", ln=True)
            pdf.cell(0, 7, f"Total Missing Values: {df.isnull().sum().sum()}", ln=True)
            pdf.ln(5)

            # Data Quality
            missing_score = 100 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100)
            duplicate_score = 100 - (df.duplicated().sum() / df.shape[0] * 100)
            health_score = round((missing_score + duplicate_score) / 2, 1)

            pdf.set_fill_color(102, 126, 234)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 9, "  Data Quality Index", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 10)
            pdf.ln(3)
            pdf.cell(0, 7, f"Overall Quality Score: {health_score}/100", ln=True)
            pdf.cell(0, 7, f"Missing Score: {round(missing_score, 1)}/100", ln=True)
            pdf.cell(0, 7, f"Duplicate Score: {round(duplicate_score, 1)}/100", ln=True)
            pdf.ln(5)

            # Schema
            pdf.set_fill_color(102, 126, 234)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 9, "  Schema Analysis", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 9)
            pdf.ln(3)
            for col in df.columns:
                missing = df[col].isnull().sum()
                missing_pct = round(missing/len(df)*100, 1)
                unique = df[col].nunique()
                line = f"{col} | Type: {df[col].dtype} | Missing: {missing} ({missing_pct}%) | Unique: {unique}"
                pdf.cell(0, 6, line, ln=True)
            pdf.ln(5)

            # Statistical Summary
            pdf.set_fill_color(102, 126, 234)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 9, "  Statistical Summary", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 9)
            pdf.ln(3)
            for col in num_cols:
                line = f"{col} | Mean: {round(df[col].mean(),2)} | Median: {round(df[col].median(),2)} | Std: {round(df[col].std(),2)} | Min: {round(df[col].min(),2)} | Max: {round(df[col].max(),2)}"
                pdf.cell(0, 6, line, ln=True)
            pdf.ln(5)

            # Outliers
            pdf.set_fill_color(102, 126, 234)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 9, "  Outlier Summary", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 9)
            pdf.ln(3)
            for col in num_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outlier_count = df[(df[col] < Q1-1.5*IQR) | (df[col] > Q3+1.5*IQR)].shape[0]
                pdf.cell(0, 6, f"{col}: {outlier_count} outliers found", ln=True)
            pdf.ln(5)

            # Correlations
            pdf.set_fill_color(102, 126, 234)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 9, "  Strong Correlations (>= 0.5)", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 9)
            pdf.ln(3)
            if len(num_cols) >= 2:
                corr = df[num_cols].corr()
                found = False
                for i in range(len(corr.columns)):
                    for j in range(i+1, len(corr.columns)):
                        val = corr.iloc[i,j]
                        if abs(val) >= 0.5:
                            rel = "Positive" if val > 0 else "Negative"
                            pdf.cell(0, 6,
                                f"{corr.columns[i]} and {corr.columns[j]}: {round(val,2)} ({rel})",
                                ln=True)
                            found = True
                if not found:
                    pdf.cell(0, 6, "No strong correlations found", ln=True)

            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_output,
                file_name="data_analysis_report.pdf",
                mime="application/pdf"
            )
            st.success("✅ PDF Ready - Click above to download!")