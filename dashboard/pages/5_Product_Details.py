import os
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Product Details",
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

    .section-title {
        font-size: 1.15rem;
        font-weight: 750;
        color: #102A43;

        padding-left: 12px;

        border-left: 4px solid #2563EB;

        margin-top: 1.4rem;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;

        border: 1px solid #E1E8F0;

        border-radius: 15px;

        padding: 7px;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.045);
    }

    div[data-testid="stDataFrame"] {
        background: #FFFFFF;

        border: 1px solid #E1E8F0;

        border-radius: 14px;

        overflow: hidden;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.045);
    }

    div[data-testid="stAlert"] {
        border-radius: 12px !important;
    }

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

    .footer-text {
        text-align: center;
        color: #8191A1;
        font-size: 0.75rem;
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEPLOYMENT_PATH = PROJECT_ROOT / "data" / "deployment"

PRODUCT_PATH = (
    DEPLOYMENT_PATH /
    "product_sales_dashboard_compact.csv"
)


# ============================================================
# LOAD PRODUCT DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_product_data(path):

    if not path.exists():
        return None

    try:

        df = pd.read_csv(path)

        return df

    except Exception:

        return None


product_df = load_product_data(PRODUCT_PATH)


# ============================================================
# DATA VALIDATION
# ============================================================

if product_df is None:

    st.error(
        "Product dataset could not be found or loaded."
    )

    st.write("Expected location:")

    st.code(str(PRODUCT_PATH))

    st.stop()


required_columns = [
    "sku_id",
    "total_quantity",
    "total_sales",
    "transactions",
    "stores",
    "channels",
    "first_sale",
    "last_sale"
]


missing_columns = [
    column
    for column in required_columns
    if column not in product_df.columns
]


if missing_columns:

    st.error(
        "The product dataset is missing required columns."
    )

    st.write(
        "Missing columns:",
        missing_columns
    )

    st.write("Available columns:")

    st.write(
        product_df.columns.tolist()
    )

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

product_df = product_df.copy()

product_df["sku_id"] = (
    product_df["sku_id"]
    .astype(str)
)

product_df["total_quantity"] = pd.to_numeric(
    product_df["total_quantity"],
    errors="coerce"
).fillna(0)

product_df["total_sales"] = pd.to_numeric(
    product_df["total_sales"],
    errors="coerce"
).fillna(0)

product_df["transactions"] = pd.to_numeric(
    product_df["transactions"],
    errors="coerce"
).fillna(0)

product_df["stores"] = pd.to_numeric(
    product_df["stores"],
    errors="coerce"
).fillna(0)

product_df["channels"] = pd.to_numeric(
    product_df["channels"],
    errors="coerce"
).fillna(0)

product_df["first_sale"] = pd.to_datetime(
    product_df["first_sale"],
    errors="coerce"
)

product_df["last_sale"] = pd.to_datetime(
    product_df["last_sale"],
    errors="coerce"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📦 Product Intelligence")

st.caption(
    "Detailed product-level sales, demand and distribution "
    "analysis across the retail portfolio."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📦 Product Controls")

st.sidebar.caption(
    "Select a SKU to explore its performance."
)

st.sidebar.divider()


# ============================================================
# PRODUCT SELECTION
# ============================================================

sku_list = sorted(
    product_df["sku_id"]
    .dropna()
    .unique()
    .tolist()
)


selected_sku = st.sidebar.selectbox(
    "Select Product",
    sku_list,
    index=0
)


# ============================================================
# SELECT PRODUCT
# ============================================================

selected_product = product_df[
    product_df["sku_id"] == selected_sku
].copy()


if selected_product.empty:

    st.warning(
        "No information is available for the selected SKU."
    )

    st.stop()


product = selected_product.iloc[0]


# ============================================================
# PRODUCT HEADER
# ============================================================

st.markdown(
    '<div class="section-title">Product Overview</div>',
    unsafe_allow_html=True
)

st.info(
    f"Showing detailed performance for **{selected_sku}**"
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">Executive Summary</div>',
    unsafe_allow_html=True
)

st.caption(
    "Key performance indicators for the selected product."
)


total_sales = float(
    product["total_sales"]
)

total_quantity = float(
    product["total_quantity"]
)

total_transactions = int(
    product["transactions"]
)

total_stores = int(
    product["stores"]
)

total_channels = int(
    product["channels"]
)


avg_unit_price = (
    total_sales / total_quantity
    if total_quantity > 0
    else 0
)


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "💰 Revenue",
        f"₹{total_sales:,.0f}"
    )


with kpi2:

    st.metric(
        "📦 Units Sold",
        f"{total_quantity:,.0f}"
    )


with kpi3:

    st.metric(
        "🧾 Transactions",
        f"{total_transactions:,}"
    )


with kpi4:

    st.metric(
        "🏬 Stores",
        f"{total_stores:,}"
    )


# ============================================================
# PRODUCT SNAPSHOT
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Product Snapshot</div>',
    unsafe_allow_html=True
)


snap1, snap2, snap3, snap4 = st.columns(4)


with snap1:

    st.markdown("**SKU**")

    st.write(
        selected_sku
    )


with snap2:

    st.markdown("**Sales Channels**")

    st.write(
        f"{total_channels:,}"
    )


with snap3:

    st.markdown("**First Sale**")

    if pd.notna(product["first_sale"]):

        st.write(
            product["first_sale"].strftime(
                "%d %b %Y"
            )
        )

    else:

        st.write("N/A")


with snap4:

    st.markdown("**Latest Sale**")

    if pd.notna(product["last_sale"]):

        st.write(
            product["last_sale"].strftime(
                "%d %b %Y"
            )
        )

    else:

        st.write("N/A")


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📈 Sales Performance</div>',
    unsafe_allow_html=True
)

st.caption(
    "Revenue and quantity indicators for the selected product."
)


performance_df = pd.DataFrame(
    {
        "Metric": [
            "Revenue",
            "Units Sold",
            "Transactions",
            "Stores",
            "Channels"
        ],
        "Value": [
            total_sales,
            total_quantity,
            total_transactions,
            total_stores,
            total_channels
        ]
    }
)


fig_performance = px.bar(
    performance_df,
    x="Metric",
    y="Value",
    title="Product Performance Overview"
)


fig_performance.update_traces(
    hovertemplate=
    "<b>%{x}</b>"
    "<br>Value: %{y:,.0f}"
    "<extra></extra>"
)


fig_performance.update_layout(
    template="plotly_white",
    height=420,

    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),

    xaxis=dict(
        title="",
        showgrid=False
    ),

    yaxis=dict(
        title="Value",
        gridcolor="#EEF2F6",
        zeroline=False
    ),

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white"
)


st.plotly_chart(
    fig_performance,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# REVENUE PERFORMANCE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">💰 Revenue Performance</div>',
    unsafe_allow_html=True
)

st.caption(
    "Revenue contribution of the selected product."
)


revenue_df = pd.DataFrame(
    {
        "Metric": [
            "Total Revenue",
            "Average Revenue per Unit"
        ],
        "Revenue": [
            total_sales,
            avg_unit_price
        ]
    }
)


fig_revenue = px.bar(
    revenue_df,
    x="Metric",
    y="Revenue",
    title="Revenue Metrics"
)


fig_revenue.update_traces(
    hovertemplate=
    "<b>%{x}</b>"
    "<br>₹%{y:,.2f}"
    "<extra></extra>"
)


fig_revenue.update_layout(
    template="plotly_white",
    height=400,

    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),

    xaxis=dict(
        title="",
        showgrid=False
    ),

    yaxis=dict(
        title="Revenue (₹)",
        gridcolor="#EEF2F6",
        zeroline=False
    ),

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white"
)


st.plotly_chart(
    fig_revenue,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# CHANNEL ANALYSIS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Channel Analysis</div>',
    unsafe_allow_html=True
)

st.caption(
    "Number of sales channels in which the selected SKU is available."
)


channel_df = pd.DataFrame(
    {
        "Channel Coverage": [
            "Active Channels",
            "Inactive Channels"
        ],
        "Count": [
            total_channels,
            max(0, 3 - total_channels)
        ]
    }
)


fig_channel = px.pie(
    channel_df,
    names="Channel Coverage",
    values="Count",
    hole=0.45,
    title="Channel Coverage"
)


fig_channel.update_traces(
    hovertemplate=
    "<b>%{label}</b>"
    "<br>Channels: %{value}"
    "<extra></extra>"
)


fig_channel.update_layout(
    template="plotly_white",
    height=400,

    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white"
)


st.plotly_chart(
    fig_channel,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# STORE PERFORMANCE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🏬 Store Performance</div>',
    unsafe_allow_html=True
)

st.caption(
    "Retail footprint of the selected product."
)


store_df = pd.DataFrame(
    {
        "Metric": [
            "Stores Selling Product"
        ],
        "Stores": [
            total_stores
        ]
    }
)


fig_store = px.bar(
    store_df,
    x="Metric",
    y="Stores",
    title="Store Coverage"
)


fig_store.update_traces(
    hovertemplate=
    "<b>%{x}</b>"
    "<br>Stores: %{y:,}"
    "<extra></extra>"
)


fig_store.update_layout(
    template="plotly_white",
    height=380,

    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),

    xaxis=dict(
        title="",
        showgrid=False
    ),

    yaxis=dict(
        title="Number of Stores",
        gridcolor="#EEF2F6",
        zeroline=False
    ),

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white"
)


st.plotly_chart(
    fig_store,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# INVENTORY / DEMAND INDICATORS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📦 Product Demand Indicators</div>',
    unsafe_allow_html=True
)

st.caption(
    "High-level indicators useful for inventory and demand planning."
)


demand_col1, demand_col2, demand_col3 = st.columns(3)


with demand_col1:

    st.metric(
        "Units Sold",
        f"{total_quantity:,.0f}"
    )


with demand_col2:

    st.metric(
        "Transactions",
        f"{total_transactions:,}"
    )


with demand_col3:

    st.metric(
        "Revenue / Unit",
        f"₹{avg_unit_price:,.2f}"
    )


# ============================================================
# PRODUCT DETAILS TABLE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📋 Product Details</div>',
    unsafe_allow_html=True
)

st.caption(
    "Complete aggregated information for the selected SKU."
)


details_df = pd.DataFrame(
    {
        "Metric": [
            "SKU",
            "Total Revenue",
            "Total Quantity",
            "Transactions",
            "Stores",
            "Channels",
            "Average Revenue per Unit",
            "First Sale",
            "Latest Sale"
        ],

        "Value": [
            selected_sku,
            f"₹{total_sales:,.2f}",
            f"{total_quantity:,.0f}",
            f"{total_transactions:,}",
            f"{total_stores:,}",
            f"{total_channels:,}",
            f"₹{avg_unit_price:,.2f}",

            (
                product["first_sale"].strftime("%d %b %Y")
                if pd.notna(product["first_sale"])
                else "N/A"
            ),

            (
                product["last_sale"].strftime("%d %b %Y")
                if pd.notna(product["last_sale"])
                else "N/A"
            )
        ]
    }
)


st.dataframe(
    details_df,
    use_container_width=True,
    hide_index=True,
    height=420
)


# ============================================================
# TOP PRODUCTS COMPARISON
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🏆 Top Products by Revenue</div>',
    unsafe_allow_html=True
)

st.caption(
    "Top 10 products across the complete product portfolio."
)


top_products = (
    product_df
    .sort_values(
        "total_sales",
        ascending=False
    )
    .head(10)
    .copy()
)


fig_top = px.bar(
    top_products,
    x="total_sales",
    y="sku_id",
    orientation="h",
    title="Top 10 Products by Revenue"
)


fig_top.update_traces(
    hovertemplate=
    "<b>%{y}</b>"
    "<br>Revenue: ₹%{x:,.0f}"
    "<extra></extra>"
)


fig_top.update_layout(
    template="plotly_white",
    height=450,

    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),

    xaxis=dict(
        title="Revenue (₹)",
        gridcolor="#EEF2F6"
    ),

    yaxis=dict(
        title="SKU",
        categoryorder="total ascending"
    ),

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white"
)


st.plotly_chart(
    fig_top,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# PRODUCT PORTFOLIO
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Product Portfolio</div>',
    unsafe_allow_html=True
)


portfolio1, portfolio2, portfolio3 = st.columns(3)


with portfolio1:

    st.metric(
        "Total SKUs",
        f"{product_df['sku_id'].nunique():,}"
    )


with portfolio2:

    st.metric(
        "Portfolio Revenue",
        f"₹{product_df['total_sales'].sum():,.0f}"
    )


with portfolio3:

    st.metric(
        "Portfolio Units",
        f"{product_df['total_quantity'].sum():,.0f}"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer-text">
        Retail Demand Forecasting |
        Product Intelligence |
        SKU-Level Analytics
    </div>
    """,
    unsafe_allow_html=True
)
