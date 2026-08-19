import streamlit as st
import pandas as pd
import os

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_inventory_risk():
    path = os.path.join(
        PROCESSED_PATH,
        "inventory_risk_scoring.csv"
    )

    if os.path.exists(path):
        return pd.read_csv(path)

    return None


inventory_df = load_inventory_risk()

# -----------------------------
# Header
# -----------------------------
st.title("🛍️ Online Retail Demand Forecasting")
st.subheader("Inventory & Demand Intelligence Dashboard")

st.markdown(
    "Monitor sales demand, inventory risk, and forecasting insights "
    "for better retail decision-making."
)

st.divider()

# -----------------------------
# Key Metrics
# -----------------------------
if inventory_df is not None:

    total_inventory = len(inventory_df)

    critical_inventory = (
        inventory_df["final_risk_level"]
        .eq("Critical")
        .sum()
    )

    high_risk_inventory = (
        inventory_df["final_risk_level"]
        .eq("High Risk")
        .sum()
    )

    total_stores = inventory_df["store_id"].nunique()
    total_products = inventory_df["sku_id"].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Inventory Records",
        f"{total_inventory:,}"
    )

    col2.metric(
        "Stores",
        total_stores
    )

    col3.metric(
        "Products",
        f"{total_products:,}"
    )

    col4.metric(
        "Critical Stock",
        f"{critical_inventory:,}"
    )

    col5.metric(
        "High Risk",
        f"{high_risk_inventory:,}"
    )

else:

    st.error(
        "Inventory risk dataset not found. "
        "Please make sure inventory_risk_scoring.csv exists "
        "inside data/processed."
    )

# -----------------------------
# About Project
# -----------------------------
st.divider()

st.header("📌 Project Overview")

st.write(
    """
    This dashboard analyzes online retail data to understand sales demand,
    forecast future demand, identify inventory risks, and support
    data-driven business decisions.
    """
)
exit()