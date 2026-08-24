import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Inventory Intelligence",
    page_icon="📦",
    layout="wide"
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

@st.cache_data
def load_inventory_data():

    if not os.path.exists(DATA_PATH):
        return None

    return pd.read_csv(DATA_PATH)


inventory_df = load_inventory_data()


# ============================================================
# DATA CHECK
# ============================================================

if inventory_df is None:

    st.error(
        "Inventory dataset could not be found."
    )

    st.code(DATA_PATH)

    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📦 Inventory Intelligence")

st.caption(
    "Monitor inventory position, stock levels and product availability."
)

st.divider()


# ============================================================
# PREPARE DATA
# ============================================================

inventory_df["stock_on_hand"] = pd.to_numeric(
    inventory_df["stock_on_hand"],
    errors="coerce"
).fillna(0)


inventory_df["reorder_point"] = pd.to_numeric(
    inventory_df["reorder_point"],
    errors="coerce"
).fillna(0)


inventory_df["safety_stock"] = pd.to_numeric(
    inventory_df["safety_stock"],
    errors="coerce"
).fillna(0)


inventory_df["stock_coverage_days"] = pd.to_numeric(
    inventory_df["stock_coverage_days"],
    errors="coerce"
).fillna(0)


inventory_df["avg_daily_demand"] = pd.to_numeric(
    inventory_df["avg_daily_demand"],
    errors="coerce"
).fillna(0)


inventory_df["risk_score"] = pd.to_numeric(
    inventory_df["risk_score"],
    errors="coerce"
).fillna(0)


# ============================================================
# INVENTORY KPIs
# ============================================================

total_products = inventory_df["sku_id"].nunique()

total_stock = inventory_df["stock_on_hand"].sum()

average_stock = (
    inventory_df["stock_on_hand"].mean()
)

average_coverage = (
    inventory_df["stock_coverage_days"].mean()
)


# ============================================================
# INVENTORY OVERVIEW
# ============================================================

st.header("Inventory Overview")


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


kpi1.metric(
    "Total Products",
    f"{total_products:,}"
)


kpi2.metric(
    "Stock on Hand",
    f"{total_stock:,.0f}"
)


kpi3.metric(
    "Average Stock",
    f"{average_stock:,.1f}"
)


kpi4.metric(
    "Avg Coverage",
    f"{average_coverage:,.1f} days"
)


# ============================================================
# STOCK DISTRIBUTION
# ============================================================

st.divider()

st.header("Stock Distribution")


stock_data = inventory_df.copy()


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
    .value_counts(
        sort=False
    )
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
    title="Products by Stock Level",
    text="Products"
)


fig_stock.update_traces(
    textposition="outside"
)


fig_stock.update_layout(
    template="plotly_white",
    xaxis_title="Stock Range",
    yaxis_title="Number of Products",
    height=450
)


st.plotly_chart(
    fig_stock,
    use_container_width=True
)


# ============================================================
# STOCK VS REORDER POINT
# ============================================================

st.divider()

st.header("Stock vs Reorder Point")


stock_comparison = (
    inventory_df[
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


fig_reorder = px.bar(
    stock_comparison,
    x="sku_id",
    y=[
        "stock_on_hand",
        "reorder_point"
    ],
    barmode="group",
    title="Stock on Hand vs Reorder Point — 20 Products",
)


fig_reorder.update_layout(
    template="plotly_white",
    xaxis_title="Product",
    yaxis_title="Units",
    height=500,
    xaxis_tickangle=-45
)


st.plotly_chart(
    fig_reorder,
    use_container_width=True
)


# ============================================================
# STOCK COVERAGE
# ============================================================

st.divider()

st.header("Stock Coverage")


coverage_data = inventory_df.copy()


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
    .value_counts(
        sort=False
    )
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
    title="Products by Stock Coverage",
    text="Products"
)


fig_coverage.update_traces(
    textposition="outside"
)


fig_coverage.update_layout(
    template="plotly_white",
    xaxis_title="Stock Coverage",
    yaxis_title="Number of Products",
    height=450
)


st.plotly_chart(
    fig_coverage,
    use_container_width=True
)


# ============================================================
# INVENTORY STATUS
# ============================================================

st.divider()

st.header("Inventory Status")


risk_summary = (
    inventory_df["final_risk_level"]
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
    hole=0.45,
    title="Inventory Risk Distribution"
)


fig_risk.update_traces(
    textposition="inside",
    textinfo="percent"
)


fig_risk.update_layout(
    template="plotly_white",
    height=450
)


st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# PRODUCT INVENTORY TABLE
# ============================================================

st.divider()

st.header("Product Inventory")


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
    if column in inventory_df.columns
]


st.dataframe(
    inventory_df[display_columns],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.divider()

st.header("Dataset Information")


info1, info2, info3 = st.columns(3)


info1.metric(
    "Records",
    f"{len(inventory_df):,}"
)


info2.metric(
    "Products",
    f"{inventory_df['sku_id'].nunique():,}"
)


info3.metric(
    "Stores",
    f"{inventory_df['store_id'].nunique():,}"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting | Inventory Intelligence"
)
