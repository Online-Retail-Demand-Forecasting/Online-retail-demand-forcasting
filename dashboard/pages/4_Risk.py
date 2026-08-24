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
# LOAD DATA
# ============================================================

@st.cache_data
def load_risk_data():

    if not os.path.exists(DATA_PATH):
        return None

    return pd.read_csv(DATA_PATH)


risk_df = load_risk_data()


# ============================================================
# DATA CHECK
# ============================================================

if risk_df is None:

    st.error(
        "Inventory risk dataset could not be found."
    )

    st.code(DATA_PATH)

    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("⚠️ Inventory Risk Analysis")

st.caption(
    "Identify products with critical inventory conditions "
    "and prioritize replenishment decisions."
)

st.divider()


# ============================================================
# DATA PREPARATION
# ============================================================

risk_df["risk_score"] = pd.to_numeric(
    risk_df["risk_score"],
    errors="coerce"
).fillna(0)


risk_df["stock_on_hand"] = pd.to_numeric(
    risk_df["stock_on_hand"],
    errors="coerce"
).fillna(0)


risk_df["reorder_point"] = pd.to_numeric(
    risk_df["reorder_point"],
    errors="coerce"
).fillna(0)


risk_df["stock_coverage_days"] = pd.to_numeric(
    risk_df["stock_coverage_days"],
    errors="coerce"
).fillna(0)


risk_df["final_risk_level"] = (
    risk_df["final_risk_level"]
    .astype(str)
    .str.strip()
)


# ============================================================
# RISK SUMMARY
# ============================================================

st.header("Risk Overview")


critical_count = (
    risk_df["final_risk_level"]
    .str.lower()
    .eq("critical")
    .sum()
)


high_count = (
    risk_df["final_risk_level"]
    .str.lower()
    .eq("high risk")
    .sum()
)


medium_count = (
    risk_df["final_risk_level"]
    .str.lower()
    .eq("medium risk")
    .sum()
)


low_count = (
    risk_df["final_risk_level"]
    .str.lower()
    .eq("low risk")
    .sum()
)


average_risk_score = (
    risk_df["risk_score"].mean()
)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


kpi1.metric(
    "Critical",
    f"{critical_count:,}"
)


kpi2.metric(
    "High Risk",
    f"{high_count:,}"
)


kpi3.metric(
    "Medium Risk",
    f"{medium_count:,}"
)


kpi4.metric(
    "Low Risk",
    f"{low_count:,}"
)


kpi5.metric(
    "Average Risk Score",
    f"{average_risk_score:.2f}"
)


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.divider()

st.header("Risk Level Distribution")


risk_distribution = (
    risk_df["final_risk_level"]
    .value_counts()
    .reset_index()
)


risk_distribution.columns = [
    "Risk Level",
    "Products"
]


fig_risk = px.bar(
    risk_distribution,
    x="Risk Level",
    y="Products",
    text="Products",
    title="Products by Risk Level"
)


fig_risk.update_traces(
    textposition="outside"
)


fig_risk.update_layout(
    template="plotly_white",
    xaxis_title="Risk Level",
    yaxis_title="Number of Products",
    height=450
)


st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# RISK SCORE DISTRIBUTION
# ============================================================

st.divider()

st.header("Risk Score Distribution")


fig_score = px.histogram(
    risk_df,
    x="risk_score",
    nbins=20,
    title="Distribution of Inventory Risk Scores"
)


fig_score.update_layout(
    template="plotly_white",
    xaxis_title="Risk Score",
    yaxis_title="Number of Products",
    height=450
)


st.plotly_chart(
    fig_score,
    use_container_width=True
)


# ============================================================
# STOCK VS RISK
# ============================================================

st.divider()

st.header("Stock Position vs Risk")


fig_stock_risk = px.scatter(
    risk_df,
    x="stock_on_hand",
    y="risk_score",
    color="final_risk_level",
    hover_data=[
        "store_id",
        "sku_id",
        "reorder_point",
        "stock_coverage_days"
    ],
    title="Stock on Hand vs Risk Score"
)


fig_stock_risk.update_layout(
    template="plotly_white",
    xaxis_title="Stock on Hand",
    yaxis_title="Risk Score",
    height=500
)


st.plotly_chart(
    fig_stock_risk,
    use_container_width=True
)


# ============================================================
# HIGH-RISK PRODUCTS
# ============================================================

st.divider()

st.header("High-Risk Products")


high_risk_df = risk_df[
    risk_df["final_risk_level"]
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


    st.dataframe(
        high_risk_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No critical or high-risk products found."
    )


# ============================================================
# TOP 20 HIGHEST RISK PRODUCTS
# ============================================================

st.divider()

st.header("Top 20 Highest-Risk Products")


top_risk = (
    risk_df
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
    title="Top 20 Products by Risk Score"
)


fig_top_risk.update_layout(
    template="plotly_white",
    xaxis_title="Risk Score",
    yaxis_title="SKU",
    height=650,
    yaxis={
        "categoryorder": "total ascending"
    }
)


st.plotly_chart(
    fig_top_risk,
    use_container_width=True
)


# ============================================================
# RISK BY STORE
# ============================================================

st.divider()

st.header("Risk by Store")


store_risk = (
    risk_df
    .groupby("store_id")
    .agg(
        Average_Risk_Score=(
            "risk_score",
            "mean"
        ),
        High_Risk_Products=(
            "final_risk_level",
            lambda x: x.astype(str)
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
    title="Average Risk Score by Store",
    text="Average_Risk_Score"
)


fig_store_risk.update_traces(
    texttemplate="%{y:.2f}",
    textposition="outside"
)


fig_store_risk.update_layout(
    template="plotly_white",
    xaxis_title="Store",
    yaxis_title="Average Risk Score",
    height=450
)


st.plotly_chart(
    fig_store_risk,
    use_container_width=True
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.divider()

st.header("Risk Dataset Information")


info1, info2, info3 = st.columns(3)


info1.metric(
    "Total Records",
    f"{len(risk_df):,}"
)


info2.metric(
    "Stores",
    f"{risk_df['store_id'].nunique():,}"
)


info3.metric(
    "Products",
    f"{risk_df['sku_id'].nunique():,}"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting | Inventory Risk Analysis"
)
