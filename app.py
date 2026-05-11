import streamlit as st
import pandas as pd

from core.cleaner import DataCleaner
from core.analyzer import DataAnalyzer
from core.visualizer import DataVisualizer
from core.insights import InsightGenerator

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Healthcare Data Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# LOAD CSS
# ─────────────────────────────────────────────

def load_css():

    with open("assets/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:

    st.title("🏥 Healthcare Analyzer")

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Healthcare CSV",
        type=["csv"]
    )

    st.divider()

    st.markdown("""
    ### Features

    ✅ Auto Cleaning  
    ✅ Dynamic Charts  
    ✅ Statistical Analysis  
    ✅ Automated Insights  
    ✅ Outlier Detection  
    """)

    st.divider()

    st.caption("Built by Akash")
    st.caption("Python | Streamlit | Plotly")

# ─────────────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────────────

if uploaded_file is None:

    st.title(
        "🏥 Upload Any Healthcare Dataset "
        "And Get Instant Insights"
    )

    st.subheader(
        "No coding required."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.info("📤 Upload CSV")
    col2.info("🧹 Auto Clean")
    col3.info("📊 Analyze")
    col4.info("💡 Generate Insights")

    st.divider()

    st.markdown("""
    ## What This Tool Does

    - Automatically cleans healthcare datasets
    - Detects missing values and duplicates
    - Generates interactive visualizations
    - Detects outliers automatically
    - Creates statistical summaries
    - Produces automated insights

    ### Works with:

    - Diabetes datasets
    - Heart disease datasets
    - Hospital records
    - Fitness datasets
    - General healthcare CSVs
    """)

    st.stop()

# ─────────────────────────────────────────────
# LOAD & CLEAN DATA
# ─────────────────────────────────────────────

@st.cache_data
def load_and_clean_data(file):

    df_raw = pd.read_csv(file)

    cleaner = DataCleaner()

    df_clean = cleaner.clean(df_raw)

    quality_score = cleaner.get_quality_score(
        df_raw
    )

    cleaning_report = cleaner.get_report()

    return (
        df_raw,
        df_clean,
        quality_score,
        cleaning_report
    )

(
    df_raw,
    df_clean,
    quality_score,
    cleaning_report
) = load_and_clean_data(uploaded_file)

# ─────────────────────────────────────────────
# INITIALIZE MODULES
# ─────────────────────────────────────────────

analyzer = DataAnalyzer(df_clean)

visualizer = DataVisualizer(df_clean)

target_col = analyzer.detect_target_column()

overview = analyzer.get_overview()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.title("📊 Healthcare Analytics Dashboard")

st.markdown("""
Analyze healthcare datasets instantly with:
- automated cleaning
- statistical analysis
- visual insights
- dynamic charts
""")

st.divider()

# ─────────────────────────────────────────────
# TOP METRICS
# ─────────────────────────────────────────────

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Rows",
    f"{overview['total_rows']:,}"
)

col2.metric(
    "Columns",
    overview['total_columns']
)

col3.metric(
    "Numeric Features",
    overview['numeric_columns']
)

col4.metric(
    "Missing Values",
    overview['missing_values']
)

col5.metric(
    "Quality Score",
    f"{quality_score}/100"
)

st.divider()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Dataset",
    "🧹 Cleaning",
    "📊 Analysis",
    "📈 Charts",
    "💡 Insights"
])

# ─────────────────────────────────────────────
# TAB 1 — DATASET
# ─────────────────────────────────────────────

with tab1:

    st.subheader("Dataset Preview")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Raw Dataset")

        st.dataframe(
            df_raw.head(20),
            use_container_width=True
        )

    with col2:

        st.markdown("### Cleaned Dataset")

        st.dataframe(
            df_clean.head(20),
            use_container_width=True
        )

    st.divider()

    st.download_button(
        label="⬇ Download Cleaned CSV",
        data=df_clean.to_csv(index=False),
        file_name="cleaned_healthcare_data.csv",
        mime="text/csv"
    )

# ─────────────────────────────────────────────
# TAB 2 — CLEANING
# ─────────────────────────────────────────────

with tab2:

    st.subheader("Cleaning Report")

    for item in cleaning_report:

        if "⚠️" in item:
            st.warning(item)

        elif "🗑️" in item:
            st.error(item)

        elif "✅" in item:
            st.success(item)

        else:
            st.info(item)

    st.divider()

    st.subheader("Column Information")

    st.dataframe(
        analyzer.get_column_info(),
        use_container_width=True
    )

# ─────────────────────────────────────────────
# TAB 3 — ANALYSIS
# ─────────────────────────────────────────────

with tab3:

    st.subheader("Statistical Summary")

    st.dataframe(
        analyzer.get_statistics(),
        use_container_width=True
    )

    st.divider()

    if target_col:

        st.subheader(
            f"Detected Target Column: {target_col}"
        )

        target_analysis = analyzer.get_target_analysis(
            target_col
        )

        cols = st.columns(
            len(target_analysis["distribution"])
        )

        for i, (k, v) in enumerate(
            target_analysis["distribution"].items()
        ):

            pct = target_analysis[
                "percentages"
            ].get(k, 0)

            cols[i].metric(
                f"Class {k}",
                v,
                f"{pct}%"
            )

    st.divider()

    st.subheader("Outlier Detection")

    outliers = analyzer.get_outliers()

    if outliers:

        outlier_chart = visualizer.outlier_chart(
            outliers
        )

        if outlier_chart:

            st.plotly_chart(
                outlier_chart,
                use_container_width=True
            )

    else:

        st.success(
            "No major outliers detected."
        )

# ─────────────────────────────────────────────
# TAB 4 — CHARTS
# ─────────────────────────────────────────────

with tab4:

    st.subheader("Interactive Visualizations")

    heatmap = visualizer.correlation_heatmap()

    if heatmap:

        st.plotly_chart(
            heatmap,
            use_container_width=True
        )

    st.divider()

    numeric_cols = analyzer.numeric_cols

    if numeric_cols:

        st.subheader("Explore Columns")

        col1, col2 = st.columns(2)

        with col1:

            selected_col = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

        with col2:

            chart_type = st.selectbox(
                "Chart Type",
                ["Histogram", "Boxplot"]
            )

        if chart_type == "Histogram":

            fig = visualizer.histogram(
                selected_col,
                target_col
            )

        else:

            fig = visualizer.boxplot(
                selected_col,
                target_col
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if len(numeric_cols) >= 2:

        st.divider()

        st.subheader("Scatter Analysis")

        col1, col2 = st.columns(2)

        with col1:

            x_col = st.selectbox(
                "X Axis",
                numeric_cols,
                index=0
            )

        with col2:

            y_col = st.selectbox(
                "Y Axis",
                numeric_cols,
                index=1
            )

        scatter_fig = visualizer.scatter(
            x_col,
            y_col,
            target_col
        )

        st.plotly_chart(
            scatter_fig,
            use_container_width=True
        )

# ─────────────────────────────────────────────
# TAB 5 — INSIGHTS
# ─────────────────────────────────────────────

with tab5:

    st.subheader(
        "Automated Healthcare Insights"
    )

    generator = InsightGenerator(
        df_clean,
        analyzer
    )

    insights = generator.generate_all(
        target_col
    )

    for insight in insights:

        insight_text = (
            f"**{insight['title']}** — "
            f"{insight['message']}"
        )

        if insight["type"] == "success":

            st.success(insight_text)

        elif insight["type"] == "warning":

            st.warning(insight_text)

        elif insight["type"] == "error":

            st.error(insight_text)

        else:

            st.info(insight_text)