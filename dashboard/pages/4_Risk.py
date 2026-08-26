import os
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Inventory Risk",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL DASHBOARD STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 92% 0%,
                rgba(220, 38, 38, 0.06),
                transparent 24%
            ),
            #F4F7FB;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }


    /* ========================================================
       TYPOGRAPHY
       ======================================================== */

    h1 {
        color: #0B1F3A !important;
        font-size: 2.45rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #102A43 !important;
        font-size: 1.45rem !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #183B56 !important;
        font-weight: 700 !important;
    }

    p {
        color: #52667A;
        line-height: 1.55;
    }


    /* ========================================================
       TITLE HEADER
       ======================================================== */

    div[data-testid="stTitle"] {
        background:
            linear-gradient(
                135deg,
                #0B1F3A 0%,
                #173B5E 52%,
                #8B1E2D 100%
            );

        padding: 1.8rem 2rem;

        border-radius: 18px;

        box-shadow:
            0 12px 35px rgba(11, 31, 58, 0.16);

        margin-bottom: 0.7rem;
    }

    div[data-testid="stTitle"] h1 {
        color: #FFFFFF !important;
        margin-bottom: 0 !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0B1F3A 0%,
                #102A43 60%,
                #091A2E 100%
            );

        border-right: none;

        box-shadow:
            8px 0 30px rgba(15, 23, 42, 0.12);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] p {
        color: #B8C8D8 !important;
        font-size: 0.82rem !important;
    }

    section[data-testid="stSidebar"] label {
        color: #DCE7F1 !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.12) !important;
    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #FFFFFF,
                #FAFBFD
            );

        border: 1px solid #E1E8F0;

        border-radius: 15px;

        padding: 1.1rem 1.2rem;

        min-height: 120px;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.055);

        position: relative;

        overflow: hidden;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]::before {
        content: "";

        position: absolute;

        top: 0;
        left: 0;

        width: 100%;
        height: 4px;

        background:
            linear-gradient(
                90deg,
                #2563EB,
                #06B6D4
            );
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);

        box-shadow:
            0 12px 28px rgba(15,39,71,0.10);
    }

    div[data-testid="stMetricLabel"] {
        color: #718398 !important;
        font-size: 0.77rem !important;
        font-weight: 650 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #102A43 !important;
        font-size: 1.45rem !important;
        font-weight: 800 !important;
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        font-size: 1.15rem;
        font-weight: 750;
        color: #102A43;

        padding-left: 12px;

        border-left: 4px solid #DC2626;

        margin-top: 1.4rem;
        margin-bottom: 0.4rem;
    }


    /* ========================================================
       RISK STATUS BANNER
       ======================================================== */

    .risk-banner {
        background:
            linear-gradient(
                135deg,
                #FFF7F7,
                #FFFFFF
            );

        border: 1px solid #FECACA;

        border-left: 5px solid #DC2626;

        border-radius: 13px;

        padding: 14px 18px;

        margin: 8px 0 20px 0;

        color: #7F1D1D;

        font-size: 0.9rem;

        box-shadow:
            0 4px 15px rgba(127,29,29,0.05);
    }


    /* ========================================================
       CHART CONTAINERS
       ======================================================== */

    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;

        border: 1px solid #E1E8F0;

        border-radius: 15px;

        padding: 7px;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.045);
    }


    /* ========================================================
       DATA TABLE
       ======================================================== */

    div[data-testid="stDataFrame"] {
        background: #FFFFFF;

        border: 1px solid #E1E8F0;

        border-radius: 14px;

        overflow: hidden;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.045);
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border: none !important;

        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                #D5DEE8,
                transparent
            ) !important;

        margin: 1.35rem 0 !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {
        text-align: center;
        color: #8191A1;
        font-size: 0.75rem;
        padding-top: 1rem;
    }


    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar {
        width: 7px;
        height: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #EEF2F6;
    }

    ::-webkit-scrollbar-thumb {
        background: #94A3B8;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "inventory_risk_scoring.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_risk_data(path):

    if not os.path.exists(path):
        return None

    try:
        return pd.read_csv(path)
    except Exception:
        return None


risk_df = load_risk_data(DATA_PATH)


# ============================================================
# DATA CHECK
# ============================================================

if risk_df is None:

    st.error(
        "Inventory risk dataset could not be found or loaded."
    )

    st.write("Expected location:")

    st.code(DATA_PATH)

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

@st.cache_data(show_spinner=False)
def prepare_risk_data(df):

    df = df.copy()

    numeric_columns = [
        "risk_score",
        "stock_on_hand",
        "reorder_point",
        "stock_coverage_days",
        "safety_stock",
        "avg_daily_demand"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).fillna(0)

    if "final_risk_level" in df.columns:

        df["final_risk_level"] = (
            df["final_risk_level"]
            .astype(str)
            .str.strip()
        )

    return df


risk_df = prepare_risk_data(risk_df)


# ============================================================
# NUMBER FORMATTER
# ============================================================

def format_number(value):

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


# ============================================================
# PAGE HEADER
# ============================================================

st.title("⚠️ Inventory Risk Analysis")

st.caption(
    "Identify critical inventory conditions, quantify supply-chain exposure "
    "and prioritize replenishment decisions."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚠️ Risk Control Center")

st.sidebar.caption(
    "Monitor and investigate inventory risk exposure."
)

st.sidebar.divider()


# ============================================================
# RISK FILTER
# ============================================================

risk_levels = sorted(
    risk_df["final_risk_level"]
    .dropna()
    .unique()
    .tolist()
)


selected_risk_levels = st.sidebar.multiselect(
    "Risk Level",
    risk_levels,
    default=risk_levels
)


# ============================================================
# STORE FILTER
# ============================================================

if "store_id" in risk_df.columns:

    store_values = sorted(
        risk_df["store_id"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_stores = st.sidebar.multiselect(
        "Store",
        store_values,
        default=store_values
    )

else:

    selected_stores = []


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_risk = risk_df.copy()


if selected_risk_levels:

    filtered_risk = filtered_risk[
        filtered_risk["final_risk_level"]
        .isin(selected_risk_levels)
    ]


if selected_stores and "store_id" in filtered_risk.columns:

    filtered_risk = filtered_risk[
        filtered_risk["store_id"]
        .isin(selected_stores)
    ]


if filtered_risk.empty:

    st.warning(
        "No inventory records match the selected filters."
    )

    st.stop()


# ============================================================
# RISK CALCULATIONS
# ============================================================

risk_lower = (
    filtered_risk["final_risk_level"]
    .str.lower()
)


critical_count = int(
    risk_lower.eq("critical").sum()
)


high_count = int(
    risk_lower.eq("high risk").sum()
)


medium_count = int(
    risk_lower.eq("medium risk").sum()
)


low_count = int(
    risk_lower.eq("low risk").sum()
)


average_risk_score = (
    filtered_risk["risk_score"].mean()
)


total_risk_products = (
    critical_count
    +
    high_count
)


# ============================================================
# PAGE STATUS
# ============================================================

if total_risk_products > 0:

    st.markdown(
        f"""
        <div class="risk-banner">
        <strong>⚠️ Attention Required:</strong>
        {format_number(total_risk_products)}
        products are currently classified as
        <strong>Critical or High Risk</strong>.
        These products should be prioritized for inventory review
        and replenishment planning.
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="risk-banner"
        style="
            border-left-color:#16A34A;
            border-color:#BBF7D0;
            color:#166534;
            background:#F0FDF4;
        ">
        <strong>✓ Inventory Risk Stable:</strong>
        No Critical or High Risk products are present
        under the current filters.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RISK OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">Risk Overview</div>',
    unsafe_allow_html=True
)

st.caption(
    "Current inventory exposure across all monitored risk categories."
)


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


with kpi1:

    st.metric(
        "🔴 Critical",
        format_number(critical_count)
    )


with kpi2:

    st.metric(
        "🟠 High Risk",
        format_number(high_count)
    )


with kpi3:

    st.metric(
        "🟡 Medium Risk",
        format_number(medium_count)
    )


with kpi4:

    st.metric(
        "🟢 Low Risk",
        format_number(low_count)
    )


with kpi5:

    st.metric(
        "📈 Avg Risk Score",
        f"{average_risk_score:.2f}"
    )


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Risk Level Distribution</div>',
    unsafe_allow_html=True
)

st.caption(
    "Portfolio-level view of inventory risk concentration."
)


risk_distribution = (
    filtered_risk["final_risk_level"]
    .value_counts()
    .reset_index()
)


risk_distribution.columns = [
    "Risk Level",
    "Products"
]


risk_colors = {
    "Critical": "#DC2626",
    "High Risk": "#F97316",
    "Medium Risk": "#F59E0B",
    "Low Risk": "#16A34A"
}


fig_risk = px.bar(
    risk_distribution,
    x="Risk Level",
    y="Products",
    text="Products",
    color="Risk Level",
    color_discrete_map=risk_colors
)


fig_risk.update_traces(
    textposition="outside",

    hovertemplate=
    "<b>%{x}</b>"
    "<br>Products: %{y:,}"
    "<extra></extra>"
)


fig_risk.update_layout(
    template="plotly_white",

    height=430,

    showlegend=False,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="Risk Level",
        showgrid=False
    ),

    yaxis=dict(
        title="Number of Products",
        gridcolor="#EEF2F6"
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white"
)


st.plotly_chart(
    fig_risk,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# RISK SCORE DISTRIBUTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Risk Score Distribution</div>',
    unsafe_allow_html=True
)

st.caption(
    "Distribution of calculated inventory risk scores."
)


fig_score = px.histogram(
    filtered_risk,
    x="risk_score",
    nbins=20,
    color_discrete_sequence=["#2563EB"]
)


fig_score.update_traces(
    hovertemplate=
    "Risk Score: %{x}"
    "<br>Products: %{y:,}"
    "<extra></extra>"
)


fig_score.update_layout(
    template="plotly_white",

    height=430,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="Risk Score",
        gridcolor="#EEF2F6"
    ),

    yaxis=dict(
        title="Number of Products",
        gridcolor="#EEF2F6"
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white"
)


st.plotly_chart(
    fig_score,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# STOCK VS RISK
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Stock Position vs Risk</div>',
    unsafe_allow_html=True
)

st.caption(
    "Identify products where inventory position and risk score "
    "indicate potential supply pressure."
)


hover_columns = [
    column
    for column in [
        "store_id",
        "sku_id",
        "reorder_point",
        "stock_coverage_days"
    ]
    if column in filtered_risk.columns
]


fig_stock_risk = px.scatter(
    filtered_risk,
    x="stock_on_hand",
    y="risk_score",
    color="final_risk_level",
    hover_data=hover_columns,
    color_discrete_map=risk_colors
)


fig_stock_risk.update_traces(
    marker=dict(
        size=9,
        opacity=0.78
    )
)


fig_stock_risk.update_layout(
    template="plotly_white",

    height=500,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="Stock on Hand",
        gridcolor="#EEF2F6"
    ),

    yaxis=dict(
        title="Risk Score",
        gridcolor="#EEF2F6"
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white",

    legend_title="Risk Level"
)


st.plotly_chart(
    fig_stock_risk,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# HIGH-RISK PRODUCTS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🚨 High-Risk Products</div>',
    unsafe_allow_html=True
)

st.caption(
    "Products requiring immediate attention based on their risk classification."
)


high_risk_df = filtered_risk[
    filtered_risk["final_risk_level"]
    .str.lower()
    .isin(
        [
            "critical",
            "high risk"
        ]
    )
].copy()


high_risk_df = high_risk_df.sort_values(
    "risk_score",
    ascending=False
)


if not high_risk_df.empty:

    display_columns = [
        "store_id",
        "sku_id",
        "stock_on_hand",
        "reorder_point",
        "safety_stock",
        "stock_coverage_days",
        "avg_daily_demand",
        "risk_score",
        "final_risk_level"
    ]


    display_columns = [
        column
        for column in display_columns
        if column in high_risk_df.columns
    ]


    display_risk_df = high_risk_df[
        display_columns
    ].copy()


    display_risk_df = display_risk_df.rename(
        columns={
            "store_id": "Store",
            "sku_id": "SKU",
            "stock_on_hand": "Stock On Hand",
            "reorder_point": "Reorder Point",
            "safety_stock": "Safety Stock",
            "stock_coverage_days": "Coverage Days",
            "avg_daily_demand": "Avg Daily Demand",
            "risk_score": "Risk Score",
            "final_risk_level": "Risk Level"
        }
    )


    st.dataframe(
        display_risk_df,
        use_container_width=True,
        hide_index=True,
        height=430
    )

else:

    st.success(
        "✓ No Critical or High-Risk products found under the current filters."
    )


# ============================================================
# TOP 20 HIGHEST-RISK PRODUCTS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Top 20 Highest-Risk Products</div>',
    unsafe_allow_html=True
)

st.caption(
    "Prioritized ranking of products with the highest calculated risk scores."
)


top_risk = (
    filtered_risk
    .sort_values(
        "risk_score",
        ascending=False
    )
    .head(20)
    .copy()
)


fig_top_risk = px.bar(
    top_risk,
    x="risk_score",
    y="sku_id",
    color="final_risk_level",
    orientation="h",
    color_discrete_map=risk_colors
)


fig_top_risk.update_traces(
    hovertemplate=
    "<b>%{y}</b>"
    "<br>Risk Score: %{x:.2f}"
    "<extra></extra>"
)


fig_top_risk.update_layout(
    template="plotly_white",

    height=620,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="Risk Score",
        gridcolor="#EEF2F6"
    ),

    yaxis=dict(
        title="SKU",
        categoryorder="total ascending"
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white",

    legend_title="Risk Level"
)


st.plotly_chart(
    fig_top_risk,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# RISK BY STORE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🏬 Risk by Store</div>',
    unsafe_allow_html=True
)

st.caption(
    "Compare average risk exposure and high-risk product concentration by store."
)


store_risk = (
    filtered_risk
    .groupby("store_id")
    .agg(
        Average_Risk_Score=(
            "risk_score",
            "mean"
        ),

        High_Risk_Products=(
            "final_risk_level",
            lambda x:
            x.astype(str)
            .str.lower()
            .isin(
                [
                    "critical",
                    "high risk"
                ]
            )
            .sum()
        )
    )
    .reset_index()
)


store_risk = store_risk.sort_values(
    "Average_Risk_Score",
    ascending=False
)


fig_store_risk = px.bar(
    store_risk,
    x="store_id",
    y="Average_Risk_Score",
    text="Average_Risk_Score",
    color="Average_Risk_Score",
    color_continuous_scale=[
        "#16A34A",
        "#F59E0B",
        "#F97316",
        "#DC2626"
    ]
)


fig_store_risk.update_traces(
    texttemplate="%{y:.2f}",
    textposition="outside",

    hovertemplate=
    "<b>Store %{x}</b>"
    "<br>Average Risk: %{y:.2f}"
    "<extra></extra>"
)


fig_store_risk.update_layout(
    template="plotly_white",

    height=450,

    coloraxis_showscale=False,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="Store",
        showgrid=False
    ),

    yaxis=dict(
        title="Average Risk Score",
        gridcolor="#EEF2F6"
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white"
)


st.plotly_chart(
    fig_store_risk,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# STORE RISK SUMMARY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Store Risk Summary</div>',
    unsafe_allow_html=True
)


if not store_risk.empty:

    highest_risk_store = store_risk.iloc[0]["store_id"]

    highest_risk_score = store_risk.iloc[0]["Average_Risk_Score"]

    most_high_risk_store = (
        store_risk
        .sort_values(
            "High_Risk_Products",
            ascending=False
        )
        .iloc[0]
    )

    summary1, summary2, summary3 = st.columns(3)


    with summary1:

        st.metric(
            "Highest Risk Store",
            str(highest_risk_store)
        )


    with summary2:

        st.metric(
            "Highest Avg Risk",
            f"{highest_risk_score:.2f}"
        )


    with summary3:

        st.metric(
            "Most High-Risk Products",
            format_number(
                most_high_risk_store[
                    "High_Risk_Products"
                ]
            )
        )


# ============================================================
# DATASET INFORMATION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Risk Dataset Information</div>',
    unsafe_allow_html=True
)


info1, info2, info3, info4 = st.columns(4)


with info1:

    st.metric(
        "Total Records",
        format_number(len(filtered_risk))
    )


with info2:

    st.metric(
        "Stores",
        format_number(
            filtered_risk["store_id"].nunique()
            if "store_id" in filtered_risk.columns
            else 0
        )
    )


with info3:

    st.metric(
        "Products",
        format_number(
            filtered_risk["sku_id"].nunique()
            if "sku_id" in filtered_risk.columns
            else 0
        )
    )


with info4:

    st.metric(
        "Avg Risk Score",
        f"{filtered_risk['risk_score'].mean():.2f}"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer-text">'
    'Retail Demand Forecasting | Inventory Risk Analytics & Decision Support'
    '</div>',
    unsafe_allow_html=True
)
