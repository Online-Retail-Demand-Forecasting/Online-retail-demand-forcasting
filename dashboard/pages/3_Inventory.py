import os
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Inventory Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL STYLE
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
                circle at 90% 0%,
                rgba(37, 99, 235, 0.08),
                transparent 25%
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
        font-size: 2.5rem !important;
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
        line-height: 1.6;
    }


    /* ========================================================
       PAGE TITLE
       ======================================================== */

    div[data-testid="stTitle"] {
        background:
            linear-gradient(
                135deg,
                #0B1F3A 0%,
                #123E67 55%,
                #2563A6 100%
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
                #102A43 55%,
                #0A1D35 100%
            );

        border-right: none;

        box-shadow:
            8px 0 30px rgba(15, 23, 42, 0.12);
    }

    section[data-testid="stSidebar"] h1 {
        color: #FFFFFF !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] p {
        color: #B7C8D9 !important;
        font-size: 0.8rem !important;
    }

    section[data-testid="stSidebar"] label {
        color: #DCE8F3 !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.12) !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 9px !important;
    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #FFFFFF,
                #F8FAFD
            );

        border: 1px solid #E0E7EF;

        border-radius: 15px;

        padding: 1.15rem 1.2rem;

        min-height: 120px;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.05);

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
        transform: translateY(-4px);

        box-shadow:
            0 12px 28px rgba(15,39,71,0.09);
    }

    div[data-testid="stMetricLabel"] {
        color: #718398 !important;
        font-size: 0.78rem !important;
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
        border-left: 4px solid #2563EB;
        margin-top: 1.4rem;
        margin-bottom: 0.5rem;
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
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px !important;
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

        margin: 1.4rem 0 !important;
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
# LOAD INVENTORY DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_inventory_data(path):

    if not os.path.exists(path):
        return None

    try:

        return pd.read_csv(path)

    except Exception:

        return None


inventory_df = load_inventory_data(DATA_PATH)


# ============================================================
# DATA CHECK
# ============================================================

if inventory_df is None:

    st.error(
        "Inventory dataset could not be found or loaded."
    )

    st.write("Expected location:")

    st.code(DATA_PATH)

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

@st.cache_data(show_spinner=False)
def prepare_inventory_data(df):

    df = df.copy()

    numeric_columns = [
        "stock_on_hand",
        "reorder_point",
        "safety_stock",
        "stock_coverage_days",
        "avg_daily_demand",
        "risk_score"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).fillna(0)

    return df


inventory_df = prepare_inventory_data(
    inventory_df
)


# ============================================================
# NUMBER FORMATTERS
# ============================================================

def format_number(value):

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    elif abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def format_decimal(value):

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    elif abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.1f}"


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📦 Inventory Intelligence")

st.caption(
    "Monitor stock position, inventory coverage, "
    "reorder requirements and supply-chain risk."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📦 Inventory Controls")

st.sidebar.caption(
    "Inventory intelligence and risk monitoring."
)

st.sidebar.divider()


# ============================================================
# RISK FILTER
# ============================================================

if "final_risk_level" in inventory_df.columns:

    risk_levels = sorted(
        inventory_df["final_risk_level"]
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

else:

    risk_levels = []


selected_risk = st.sidebar.multiselect(
    "Risk Level",
    risk_levels,
    default=risk_levels
)


# ============================================================
# APPLY FILTER
# ============================================================

filtered_inventory = inventory_df.copy()


if (
    selected_risk
    and "final_risk_level" in filtered_inventory.columns
):

    filtered_inventory = filtered_inventory[
        filtered_inventory["final_risk_level"]
        .astype(str)
        .str.strip()
        .isin(selected_risk)
    ]


if filtered_inventory.empty:

    st.warning(
        "No inventory records match the selected filters."
    )

    st.stop()


# ============================================================
# INVENTORY KPIs
# ============================================================

total_products = (
    filtered_inventory["sku_id"].nunique()
    if "sku_id" in filtered_inventory.columns
    else 0
)


total_stock = (
    filtered_inventory["stock_on_hand"].sum()
)


average_stock = (
    filtered_inventory["stock_on_hand"].mean()
)


average_coverage = (
    filtered_inventory["stock_coverage_days"].mean()
)


# ============================================================
# RISK COUNTS
# ============================================================

if "final_risk_level" in filtered_inventory.columns:

    risk_counts = (
        filtered_inventory["final_risk_level"]
        .astype(str)
        .str.strip()
        .value_counts()
    )

else:

    risk_counts = pd.Series(dtype=int)


high_risk = int(
    sum(
        count
        for level, count in risk_counts.items()
        if level.lower() in [
            "high",
            "critical",
            "very high"
        ]
    )
)


out_of_stock = int(
    (
        filtered_inventory["stock_on_hand"] <= 0
    ).sum()
)


below_reorder = int(
    (
        filtered_inventory["stock_on_hand"]
        <=
        filtered_inventory["reorder_point"]
    ).sum()
)


# ============================================================
# INVENTORY OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">Inventory Overview</div>',
    unsafe_allow_html=True
)

st.caption(
    "Current inventory position across products and stores."
)


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


with kpi1:

    st.metric(
        "📦 Total Products",
        format_number(total_products)
    )


with kpi2:

    st.metric(
        "📊 Stock on Hand",
        format_number(total_stock)
    )


with kpi3:

    st.metric(
        "📦 Average Stock",
        format_decimal(average_stock)
    )


with kpi4:

    st.metric(
        "⏱️ Avg. Coverage",
        f"{average_coverage:,.1f} days"
    )


with kpi5:

    st.metric(
        "⚠️ Below Reorder",
        format_number(below_reorder)
    )


# ============================================================
# INVENTORY HEALTH
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Inventory Health</div>',
    unsafe_allow_html=True
)

st.caption(
    "Key indicators highlighting potential inventory pressure."
)


health1, health2, health3 = st.columns(3)


with health1:

    st.metric(
        "🔴 High / Critical Risk",
        format_number(high_risk)
    )


with health2:

    st.metric(
        "🚫 Out of Stock",
        format_number(out_of_stock)
    )


with health3:

    st.metric(
        "🔄 Reorder Required",
        format_number(below_reorder)
    )


# ============================================================
# STOCK DISTRIBUTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Stock Distribution</div>',
    unsafe_allow_html=True
)

st.caption(
    "Distribution of products across different stock-level ranges."
)


stock_data = filtered_inventory.copy()


stock_data["Stock Range"] = pd.cut(
    stock_data["stock_on_hand"],
    bins=[
        -float("inf"),
        0,
        10,
        50,
        100,
        500,
        float("inf")
    ],
    labels=[
        "Out of Stock",
        "1–10",
        "11–50",
        "51–100",
        "101–500",
        "500+"
    ]
)


stock_distribution = (
    stock_data["Stock Range"]
    .value_counts(sort=False)
    .reset_index()
)


stock_distribution.columns = [
    "Stock Range",
    "Products"
]


fig_stock = px.bar(
    stock_distribution,
    x="Stock Range",
    y="Products",
    text="Products"
)


fig_stock.update_traces(
    marker_color=[
        "#DC2626",
        "#F97316",
        "#F59E0B",
        "#06B6D4",
        "#2563EB",
        "#14B8A6"
    ],

    textposition="outside",

    hovertemplate=
    "<b>%{x}</b>"
    "<br>Products: %{y:,}"
    "<extra></extra>"
)


fig_stock.update_layout(
    template="plotly_white",

    height=430,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="Stock Range",
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
    fig_stock,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# STOCK VS REORDER POINT
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📦 Stock vs Reorder Point</div>',
    unsafe_allow_html=True
)

st.caption(
    "Products with the lowest stock position compared with their reorder threshold."
)


stock_comparison = (
    filtered_inventory[
        [
            "sku_id",
            "stock_on_hand",
            "reorder_point"
        ]
    ]
    .copy()
    .sort_values(
        "stock_on_hand"
    )
    .head(20)
)


stock_long = stock_comparison.melt(
    id_vars=["sku_id"],
    value_vars=[
        "stock_on_hand",
        "reorder_point"
    ],
    var_name="Metric",
    value_name="Units"
)


stock_long["Metric"] = (
    stock_long["Metric"]
    .replace(
        {
            "stock_on_hand": "Stock on Hand",
            "reorder_point": "Reorder Point"
        }
    )
)


fig_reorder = px.bar(
    stock_long,
    x="sku_id",
    y="Units",
    color="Metric",
    barmode="group",
    color_discrete_map={
        "Stock on Hand": "#2563EB",
        "Reorder Point": "#F59E0B"
    }
)


fig_reorder.update_traces(
    hovertemplate=
    "<b>%{x}</b>"
    "<br>%{fullData.name}: %{y:,.0f}"
    "<extra></extra>"
)


fig_reorder.update_layout(
    template="plotly_white",

    height=500,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="Product",
        showgrid=False,
        tickangle=-45
    ),

    yaxis=dict(
        title="Units",
        gridcolor="#EEF2F6"
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white",

    legend=dict(
        orientation="h",
        y=1.08,
        x=0
    )
)


st.plotly_chart(
    fig_reorder,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# STOCK COVERAGE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">⏱️ Stock Coverage</div>',
    unsafe_allow_html=True
)

st.caption(
    "Number of products grouped by estimated days of inventory coverage."
)


coverage_data = filtered_inventory.copy()


coverage_data["Coverage Range"] = pd.cut(
    coverage_data["stock_coverage_days"],
    bins=[
        -float("inf"),
        0,
        7,
        15,
        30,
        60,
        float("inf")
    ],
    labels=[
        "No Coverage",
        "1–7 Days",
        "8–15 Days",
        "16–30 Days",
        "31–60 Days",
        "60+ Days"
    ]
)


coverage_summary = (
    coverage_data["Coverage Range"]
    .value_counts(sort=False)
    .reset_index()
)


coverage_summary.columns = [
    "Coverage Range",
    "Products"
]


fig_coverage = px.bar(
    coverage_summary,
    x="Coverage Range",
    y="Products",
    text="Products"
)


fig_coverage.update_traces(
    marker_color=[
        "#DC2626",
        "#F97316",
        "#F59E0B",
        "#06B6D4",
        "#2563EB",
        "#14B8A6"
    ],

    textposition="outside",

    hovertemplate=
    "<b>%{x}</b>"
    "<br>Products: %{y:,}"
    "<extra></extra>"
)


fig_coverage.update_layout(
    template="plotly_white",

    height=430,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="Stock Coverage",
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
    fig_coverage,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# INVENTORY RISK
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">⚠️ Inventory Risk</div>',
    unsafe_allow_html=True
)

st.caption(
    "Distribution of products across inventory risk categories."
)


risk_summary = (
    filtered_inventory["final_risk_level"]
    .astype(str)
    .str.strip()
    .value_counts()
    .reset_index()
)


risk_summary.columns = [
    "Risk Level",
    "Products"
]


fig_risk = px.pie(
    risk_summary,
    names="Risk Level",
    values="Products",
    hole=0.58
)


fig_risk.update_traces(
    textposition="inside",

    textinfo="percent",

    hovertemplate=
    "<b>%{label}</b>"
    "<br>Products: %{value:,}"
    "<br>Share: %{percent}"
    "<extra></extra>",

    marker=dict(
        colors=[
            "#16A34A",
            "#F59E0B",
            "#F97316",
            "#DC2626",
            "#7F1D1D"
        ]
    )
)


fig_risk.update_layout(
    template="plotly_white",

    height=450,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white",

    showlegend=True,

    legend=dict(
        orientation="v"
    )
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
# PRODUCT INVENTORY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📋 Product Inventory</div>',
    unsafe_allow_html=True
)

st.caption(
    "Detailed inventory position, coverage and risk indicators."
)


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
    if column in filtered_inventory.columns
]


display_df = filtered_inventory[
    display_columns
].copy()


display_df = display_df.rename(
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
    display_df,
    use_container_width=True,
    hide_index=True,
    height=450
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Dataset Information</div>',
    unsafe_allow_html=True
)


info1, info2, info3, info4 = st.columns(4)


with info1:

    st.metric(
        "Records",
        format_number(len(filtered_inventory))
    )


with info2:

    st.metric(
        "Products",
        format_number(
            filtered_inventory["sku_id"].nunique()
            if "sku_id" in filtered_inventory.columns
            else 0
        )
    )


with info3:

    st.metric(
        "Stores",
        format_number(
            filtered_inventory["store_id"].nunique()
            if "store_id" in filtered_inventory.columns
            else 0
        )
    )


with info4:

    st.metric(
        "Avg Risk Score",
        f"{filtered_inventory['risk_score'].mean():.2f}"
        if "risk_score" in filtered_inventory.columns
        else "N/A"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer-text">Retail Demand Forecasting | Inventory Intelligence & Risk Analytics</div>',
    unsafe_allow_html=True
)
