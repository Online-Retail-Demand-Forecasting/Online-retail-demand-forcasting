import streamlit as st
import pandas as pd
import os

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide"
)


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
# HEADER
# =========================================================

st.title("🛍️ Online Retail Demand Forecasting")

st.subheader(
    "Inventory & Demand Intelligence Dashboard"
)

st.markdown(
    "Monitor sales demand, forecasting performance, "
    "and retail business insights for better "
    "decision-making."
)


# =========================================================
# FILTERS
# =========================================================

st.divider()

st.header("🎛️ Dashboard Filters")

filter_col1, filter_col2 = st.columns(2)


# Year Filter

with filter_col1:

    years = sorted(
        sales_df["year"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_year = st.selectbox(
        "Select Year",
        ["All"] + years
    )


# Channel Filter

with filter_col2:

    channels = sorted(
        sales_df["channel"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_channel = st.selectbox(
        "Select Channel",
        ["All"] + channels
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_sales = sales_df.copy()

filtered_demand = demand_df.copy()

filtered_forecast = forecast_df.copy()


# Year filter

if selected_year != "All":

    filtered_sales = filtered_sales[
        filtered_sales["year"] == selected_year
    ]

    filtered_demand = filtered_demand[
        filtered_demand["year"] == selected_year
    ]

    filtered_forecast = filtered_forecast[
        filtered_forecast["date"].dt.year == selected_year
    ]


# Channel filter

if selected_channel != "All":

    filtered_sales = filtered_sales[
        filtered_sales["channel"] == selected_channel
    ]


# =========================================================
# KEY METRICS
# =========================================================

st.divider()

st.header("📌 Key Metrics")


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


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Total Sales",
    f"{total_sales:,.0f}"
)

col2.metric(
    "Transactions",
    f"{total_transactions:,}"
)

col3.metric(
    "Quantity Sold",
    f"{total_quantity:,}"
)

col4.metric(
    "Stores",
    f"{total_stores:,}"
)

col5.metric(
    "Products",
    f"{total_products:,}"
)


# =========================================================
# SALES & DEMAND TRENDS
# =========================================================

st.divider()

col1, col2 = st.columns(2)


# -----------------------------
# SALES TREND
# -----------------------------

with col1:

    st.header("📈 Sales Trend")

    daily_sales = (
        filtered_sales
        .groupby("date")["total_value"]
        .sum()
    )

    st.line_chart(
        daily_sales
    )


# -----------------------------
# DEMAND TREND
# -----------------------------

with col2:

    st.header("📊 Demand Trend")

    daily_demand = (
        filtered_demand
        .groupby("date")["demand"]
        .sum()
    )

    st.line_chart(
        daily_demand
    )


# =========================================================
# FORECAST & CHANNEL
# =========================================================

col3, col4 = st.columns(2)


# -----------------------------
# ACTUAL VS FORECAST
# -----------------------------

with col3:

    st.header("🔮 Actual vs Forecast")

    forecast_chart = filtered_forecast[
        [
            "date",
            "actual_demand",
            "predicted_demand"
        ]
    ].set_index("date")

    st.line_chart(
        forecast_chart
    )


# -----------------------------
# SALES BY CHANNEL
# -----------------------------

with col4:

    st.header("🛒 Sales by Channel")

    channel_sales = (
        filtered_sales
        .groupby("channel")["total_value"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        channel_sales
    )


# =========================================================
# YEARLY SALES
# =========================================================

st.divider()

st.header("📅 Yearly Sales")


yearly_sales = (
    sales_df
    .groupby("year")["total_value"]
    .sum()
)


st.bar_chart(
    yearly_sales
)


# =========================================================
# INVENTORY RISK
# =========================================================

st.divider()

st.header("⚠️ Inventory Risk")


if inventory_df is not None:

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


    risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)


    risk_col1.metric(
        "Critical",
        f"{critical_inventory:,}"
    )

    risk_col2.metric(
        "High Risk",
        f"{high_risk_inventory:,}"
    )

    risk_col3.metric(
        "Medium Risk",
        f"{medium_risk_inventory:,}"
    )

    risk_col4.metric(
        "Low Risk",
        f"{low_risk_inventory:,}"
    )


    risk_distribution = (
        inventory_df[
            "final_risk_level"
        ]
        .value_counts()
    )


    st.bar_chart(
        risk_distribution
    )


else:

    st.info(
        "Inventory risk dataset is not available yet. "
        "Add inventory_risk_scoring.csv to "
        "data/processed to enable this section."
    )


# =========================================================
# PROJECT OVERVIEW
# =========================================================

st.divider()

st.header("📌 Project Overview")

st.write(
    """
    This dashboard analyzes online retail data to understand
    sales demand, forecast future demand, identify inventory
    risks, and support data-driven business decisions.
    """
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Online Retail Demand Forecasting | "
    "Data Science Project"
)
exit()