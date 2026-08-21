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
# HEADER
# =========================================================

st.title("🛍️ Retail Executive Dashboard")

st.markdown(
    "### Sales, Demand Forecasting & Inventory Intelligence"
)

st.caption(
    "Executive overview of retail sales performance, "
    "customer transactions, demand and inventory risk."
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🎛️ Filters")


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
# EXECUTIVE KPIs
# =========================================================

st.subheader("📌 Executive Summary")


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

    st.subheader("📈 Sales Trend")

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

    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )


# ---------------------------------------------------------
# SALES BY CHANNEL
# ---------------------------------------------------------

with right:

    st.subheader("🛒 Sales by Channel")

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

    st.plotly_chart(
        fig_channel,
        use_container_width=True
    )


# =========================================================
# SALES BY CATEGORY
# =========================================================

st.divider()

st.subheader("📊 Sales by Category")


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

st.subheader("🏪 Store-wise Sales")


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

st.subheader("📊 Demand Analysis")


demand_left, demand_right = st.columns(2)


# ---------------------------------------------------------
# DEMAND TREND
# ---------------------------------------------------------

with demand_left:

    st.write("### Demand Trend")

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

    st.plotly_chart(
        fig_demand,
        use_container_width=True
    )


# ---------------------------------------------------------
# ACTUAL VS FORECAST
# ---------------------------------------------------------

with demand_right:

    st.write("### Actual vs Forecast")

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

st.subheader("📅 Year-wise Sales")


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

st.subheader("⚠️ Inventory Risk")


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

st.subheader("🏆 Top Products")


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

st.subheader("📌 Project Overview")

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

st.caption(
    "Retail Executive Dashboard | "
    "Online Retail Demand Forecasting Project"
)