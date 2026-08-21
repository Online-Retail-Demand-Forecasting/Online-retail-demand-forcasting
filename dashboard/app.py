import streamlit as st
import pandas as pd
import os
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Retail Executive Dashboard",
    page_icon="🛍️",
    layout="wide"
)


# =========================================================
# PROFESSIONAL DASHBOARD THEME
# =========================================================

st.markdown("""
<style>
    /* ---------- Global ---------- */
    .stApp {
        background: #F6F8FB;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* ---------- Header ---------- */
    .dashboard-header {
        background: linear-gradient(135deg, #0F2747 0%, #183B63 100%);
        padding: 28px 32px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(15, 39, 71, 0.12);
    }

    .dashboard-title {
        color: white;
        font-size: 32px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .dashboard-subtitle {
        color: #DCE8F5;
        font-size: 16px;
        margin: 7px 0 0 0;
    }

    /* ---------- Section headings ---------- */
    .section-header {
        font-size: 21px;
        font-weight: 700;
        color: #17324D;
        margin-top: 8px;
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 2px solid #DCE3EB;
    }

    /* ---------- KPI cards ---------- */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 3px 10px rgba(15, 39, 71, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #17324D !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    .sidebar-title {
        color: #17324D;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .sidebar-caption {
        color: #64748B;
        font-size: 13px;
        margin-bottom: 20px;
    }

    /* ---------- Charts / containers ---------- */
    div[data-testid="stPlotlyChart"] {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 8px;
        box-shadow: 0 3px 10px rgba(15, 39, 71, 0.04);
    }

    /* ---------- Info box ---------- */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* ---------- Footer ---------- */
    .dashboard-footer {
        text-align: center;
        color: #718096;
        font-size: 12px;
        padding: 18px 0 4px 0;
        border-top: 1px solid #DCE3EB;
        margin-top: 28px;
    }

    /* ---------- Hide unnecessary Streamlit chrome ---------- */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ---------- Responsive spacing ---------- */
    @media (max-width: 900px) {
        .dashboard-title {
            font-size: 26px;
        }

        .dashboard-header {
            padding: 22px;
        }
    }
</style>
""", unsafe_allow_html=True)



# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PROCESSED_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_sales_data():

    path = os.path.join(
        PROCESSED_PATH,
        "sales_transactions_cleaned.csv"
    )

    return pd.read_csv(path)


@st.cache_data
def load_demand_data():

    path = os.path.join(
        PROCESSED_PATH,
        "daily_demand_features.csv"
    )

    return pd.read_csv(path)


@st.cache_data
def load_forecast_data():

    path = os.path.join(
        PROCESSED_PATH,
        "demand_forecast_results.csv"
    )

    return pd.read_csv(path)


@st.cache_data
def load_inventory_risk():

    path = os.path.join(
        PROCESSED_PATH,
        "inventory_risk_scoring.csv"
    )

    if os.path.exists(path):
        return pd.read_csv(path)

    return None


# Load datasets

sales_df = load_sales_data()
demand_df = load_demand_data()
forecast_df = load_forecast_data()
inventory_df = load_inventory_risk()


# =========================================================
# DATE CONVERSION
# =========================================================

sales_df["date"] = pd.to_datetime(
    sales_df["date"]
)

demand_df["date"] = pd.to_datetime(
    demand_df["date"]
)

forecast_df["date"] = pd.to_datetime(
    forecast_df["date"]
)


# =========================================================
# CREATE YEAR COLUMN IF NEEDED
# =========================================================

if "year" not in sales_df.columns:

    sales_df["year"] = sales_df["date"].dt.year


# =========================================================
# PROFESSIONAL CHART SETTINGS
# =========================================================

PLOTLY_TEMPLATE = "plotly_white"

def style_chart(fig, title=None):
    """Apply a consistent professional style to Plotly charts."""
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title=title,
        font=dict(
            family="Arial",
            size=12,
            color="#334155"
        ),
        title_font=dict(
            family="Arial",
            size=16,
            color="#17324D"
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=55, r=30, t=55, b=45),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E8EDF3",
        zeroline=False,
        linecolor="#D5DDE6"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E8EDF3",
        zeroline=False,
        linecolor="#D5DDE6"
    )

    return fig


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">Retail Executive Dashboard</div>
    <div class="dashboard-subtitle">
        Sales, Demand Forecasting & Inventory Intelligence
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown(
    '<div class="sidebar-title">Dashboard Filters</div>'
    '<div class="sidebar-caption">Use the controls below to refine the analysis.</div>',
    unsafe_allow_html=True
)


# Year filter

years = sorted(
    sales_df["year"]
    .dropna()
    .unique()
    .tolist()
)

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)


# Channel filter

channels = sorted(
    sales_df["channel"]
    .dropna()
    .unique()
    .tolist()
)

selected_channels = st.sidebar.multiselect(
    "Select Channel",
    channels,
    default=channels
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_sales = sales_df.copy()

filtered_demand = demand_df.copy()

filtered_forecast = forecast_df.copy()


# Year filter

if selected_years:

    filtered_sales = filtered_sales[
        filtered_sales["year"].isin(selected_years)
    ]

    filtered_demand = filtered_demand[
        filtered_demand["date"].dt.year.isin(
            selected_years
        )
    ]

    filtered_forecast = filtered_forecast[
        filtered_forecast["date"].dt.year.isin(
            selected_years
        )
    ]


# Channel filter

if selected_channels:

    filtered_sales = filtered_sales[
        filtered_sales["channel"].isin(
            selected_channels
        )
    ]


# =========================================================
# DATA VALIDATION
# =========================================================

if filtered_sales.empty:
    st.warning(
        "No sales records match the selected filters. "
        "Please select at least one year and channel."
    )
    st.stop()


# =========================================================
# EXECUTIVE KPIs
# =========================================================

st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)


total_sales = filtered_sales[
    "total_value"
].sum()


total_transactions = filtered_sales[
    "receipt_id"
].nunique()


total_quantity = filtered_sales[
    "quantity"
].sum()


total_stores = filtered_sales[
    "store_id"
].nunique()


total_products = filtered_sales[
    "sku_id"
].nunique()


average_order_value = (
    total_sales / total_transactions
    if total_transactions > 0
    else 0
)


kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)


kpi1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)


kpi2.metric(
    "Transactions",
    f"{total_transactions:,}"
)


kpi3.metric(
    "Quantity Sold",
    f"{total_quantity:,}"
)


kpi4.metric(
    "Stores",
    f"{total_stores:,}"
)


kpi5.metric(
    "Products",
    f"{total_products:,}"
)


kpi6.metric(
    "Avg Order Value",
    f"₹{average_order_value:,.2f}"
)


# =========================================================
# SALES TREND
# =========================================================

st.divider()

left, right = st.columns([2, 1])


# ---------------------------------------------------------
# SALES TREND
# ---------------------------------------------------------

with left:

    st.markdown('<div class="section-header">Sales Trend</div>', unsafe_allow_html=True)

    daily_sales = (
        filtered_sales
        .groupby("date")["total_value"]
        .sum()
        .reset_index()
    )

    fig_sales = px.line(
        daily_sales,
        x="date",
        y="total_value",
        title="Daily Sales Trend"
    )

    fig_sales.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        hovermode="x unified"
    )

    style_chart(fig_sales)

    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )


# ---------------------------------------------------------
# SALES BY CHANNEL
# ---------------------------------------------------------

with right:

    st.markdown('<div class="section-header">Sales by Channel</div>', unsafe_allow_html=True)

    channel_sales = (
        filtered_sales
        .groupby("channel")["total_value"]
        .sum()
        .reset_index()
    )

    fig_channel = px.pie(
        channel_sales,
        names="channel",
        values="total_value",
        hole=0.35,
        title="Sales Distribution by Channel"
    )

    style_chart(fig_channel)

    st.plotly_chart(
        fig_channel,
        use_container_width=True
    )


# =========================================================
# SALES BY CATEGORY
# =========================================================

st.divider()

st.markdown('<div class="section-header">Sales by Category</div>', unsafe_allow_html=True)


# Check whether category exists

if "category" in filtered_sales.columns:

    category_sales = (
        filtered_sales
        .groupby("category")["total_value"]
        .sum()
        .sort_values(
            ascending=True
        )
        .reset_index()
    )

    fig_category = px.bar(
        category_sales,
        x="total_value",
        y="category",
        orientation="h",
        title="Sales by Category"
    )

    fig_category.update_layout(
        xaxis_title="Sales",
        yaxis_title="Category"
    )

    style_chart(fig_category)

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

else:

    st.info(
        "Category column is not available in "
        "sales_transactions_cleaned.csv."
    )


# =========================================================
# STORE-WISE SALES
# =========================================================

st.divider()

st.markdown('<div class="section-header">Store-wise Sales</div>', unsafe_allow_html=True)


store_sales = (
    filtered_sales
    .groupby("store_id")["total_value"]
    .sum()
    .sort_values(
        ascending=False
    )
    .reset_index()
)


fig_store = px.bar(
    store_sales,
    x="store_id",
    y="total_value",
    title="Sales by Store"
)


fig_store.update_layout(
    xaxis_title="Store",
    yaxis_title="Sales"
)


st.plotly_chart(
    fig_store,
    use_container_width=True
)


# =========================================================
# DEMAND ANALYSIS
# =========================================================

st.divider()

st.markdown('<div class="section-header">Demand Analysis</div>', unsafe_allow_html=True)


demand_left, demand_right = st.columns(2)


# ---------------------------------------------------------
# DEMAND TREND
# ---------------------------------------------------------

with demand_left:

    st.markdown("**Demand Trend**")

    daily_demand = (
        filtered_demand
        .groupby("date")["demand"]
        .sum()
        .reset_index()
    )

    fig_demand = px.line(
        daily_demand,
        x="date",
        y="demand",
        title="Daily Demand"
    )

    style_chart(fig_demand)

    st.plotly_chart(
        fig_demand,
        use_container_width=True
    )


# ---------------------------------------------------------
# ACTUAL VS FORECAST
# ---------------------------------------------------------

with demand_right:

    st.markdown("**Actual vs Forecast**")

    if (
        "actual_demand" in filtered_forecast.columns
        and
        "predicted_demand" in filtered_forecast.columns
    ):

        forecast_chart = filtered_forecast[
            [
                "date",
                "actual_demand",
                "predicted_demand"
            ]
        ].copy()

        forecast_chart = forecast_chart.set_index(
            "date"
        )

        st.line_chart(
            forecast_chart
        )

    else:

        st.info(
            "Forecast columns are not available."
        )


# =========================================================
# YEARLY SALES
# =========================================================

st.divider()

st.markdown('<div class="section-header">Year-wise Sales</div>', unsafe_allow_html=True)


yearly_sales = (
    sales_df
    .groupby("year")["total_value"]
    .sum()
    .reset_index()
)


fig_year = px.bar(
    yearly_sales,
    x="year",
    y="total_value",
    title="Sales by Year"
)


fig_year.update_layout(
    xaxis_title="Year",
    yaxis_title="Sales"
)


st.plotly_chart(
    fig_year,
    use_container_width=True
)


# =========================================================
# INVENTORY RISK
# =========================================================

st.divider()

st.markdown('<div class="section-header">Inventory Risk</div>', unsafe_allow_html=True)


if inventory_df is not None:

    risk_counts = (
        inventory_df[
            "final_risk_level"
        ]
        .value_counts()
    )


    critical_inventory = (
        inventory_df[
            "final_risk_level"
        ]
        .eq("Critical")
        .sum()
    )


    high_risk_inventory = (
        inventory_df[
            "final_risk_level"
        ]
        .eq("High Risk")
        .sum()
    )


    medium_risk_inventory = (
        inventory_df[
            "final_risk_level"
        ]
        .eq("Medium Risk")
        .sum()
    )


    low_risk_inventory = (
        inventory_df[
            "final_risk_level"
        ]
        .eq("Low Risk")
        .sum()
    )


    risk1, risk2, risk3, risk4 = st.columns(4)


    risk1.metric(
        "Critical",
        f"{critical_inventory:,}"
    )


    risk2.metric(
        "High Risk",
        f"{high_risk_inventory:,}"
    )


    risk3.metric(
        "Medium Risk",
        f"{medium_risk_inventory:,}"
    )


    risk4.metric(
        "Low Risk",
        f"{low_risk_inventory:,}"
    )


    fig_risk = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        labels={
            "x": "Risk Level",
            "y": "Number of Products"
        },
        title="Inventory Risk Distribution"
    )


    style_chart(fig_risk)

    st.plotly_chart(
        fig_risk,
        use_container_width=True
    )


else:

    st.info(
        "Inventory risk dataset is not available yet."
    )


# =========================================================
# TOP PRODUCTS
# =========================================================

st.divider()

st.markdown('<div class="section-header">Top Products</div>', unsafe_allow_html=True)


top_products = (
    filtered_sales
    .groupby("sku_id")["total_value"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)


fig_products = px.bar(
    top_products,
    x="total_value",
    y="sku_id",
    orientation="h",
    title="Top 10 Products by Sales"
)


fig_products.update_layout(
    xaxis_title="Sales",
    yaxis_title="Product"
)


st.plotly_chart(
    fig_products,
    use_container_width=True
)


# =========================================================
# PROJECT OVERVIEW
# =========================================================

st.divider()

st.markdown('<div class="section-header">Project Overview</div>', unsafe_allow_html=True)

st.write(
    """
    This Retail Executive Dashboard provides an overview of
    retail sales performance, customer transactions, demand
    trends, demand forecasting and inventory risk.

    The dashboard helps management understand sales patterns,
    channel performance, store performance and inventory risk
    so that better business decisions can be made.
    """
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown("""
<div class="dashboard-footer">
    Retail Executive Dashboard &nbsp;|&nbsp;
    Online Retail Demand Forecasting Project
</div>
""", unsafe_allow_html=True)