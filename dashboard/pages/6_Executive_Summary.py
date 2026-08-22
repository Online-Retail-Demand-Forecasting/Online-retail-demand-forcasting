import os
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Executive Summary",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

PROCESSED_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)


SALES_PATH = os.path.join(
    PROCESSED_PATH,
    "sales_transactions_cleaned.csv"
)

FORECAST_PATH = os.path.join(
    PROCESSED_PATH,
    "demand_forecast_results.csv"
)

INVENTORY_PATH = os.path.join(
    PROCESSED_PATH,
    "inventory_risk_scoring.csv"
)


# ============================================================
# LOAD SALES DATA
# ============================================================

@st.cache_data
def load_sales_data():

    if not os.path.exists(SALES_PATH):
        return None

    return pd.read_csv(SALES_PATH)


# ============================================================
# LOAD FORECAST DATA
# ============================================================

@st.cache_data
def load_forecast_data():

    if not os.path.exists(FORECAST_PATH):
        return None

    return pd.read_csv(FORECAST_PATH)


# ============================================================
# LOAD INVENTORY DATA
# ============================================================

@st.cache_data
def load_inventory_data():

    if not os.path.exists(INVENTORY_PATH):
        return None

    return pd.read_csv(INVENTORY_PATH)


sales_df = load_sales_data()

forecast_df = load_forecast_data()

inventory_df = load_inventory_data()


# ============================================================
# DATA CHECK
# ============================================================

if sales_df is None:

    st.error(
        "Sales dataset could not be found."
    )

    st.code(SALES_PATH)

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

if "date" in sales_df.columns:

    sales_df["date"] = pd.to_datetime(
        sales_df["date"],
        errors="coerce"
    )


if "total_value" in sales_df.columns:

    sales_df["total_value"] = pd.to_numeric(
        sales_df["total_value"],
        errors="coerce"
    ).fillna(0)


if "quantity" in sales_df.columns:

    sales_df["quantity"] = pd.to_numeric(
        sales_df["quantity"],
        errors="coerce"
    ).fillna(0)


if "date" in sales_df.columns:

    sales_df["year"] = (
        sales_df["date"].dt.year
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📈 Executive Summary")

st.caption(
    "Management-level overview of retail sales, demand "
    "forecasting and inventory risk."
)

st.divider()


# ============================================================
# EXECUTIVE KPIs
# ============================================================

st.header("Business Performance")


total_sales = (
    sales_df["total_value"].sum()
    if "total_value" in sales_df.columns
    else 0
)


total_transactions = (
    sales_df["receipt_id"].nunique()
    if "receipt_id" in sales_df.columns
    else len(sales_df)
)


total_quantity = (
    sales_df["quantity"].sum()
    if "quantity" in sales_df.columns
    else 0
)


total_stores = (
    sales_df["store_id"].nunique()
    if "store_id" in sales_df.columns
    else 0
)


total_products = (
    sales_df["sku_id"].nunique()
    if "sku_id" in sales_df.columns
    else 0
)


average_order_value = (
    total_sales / total_transactions
    if total_transactions > 0
    else 0
)


kpi1, kpi2, kpi3 = st.columns(3)

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
    f"{total_quantity:,.0f}"
)


kpi4, kpi5, kpi6 = st.columns(3)

kpi4.metric(
    "Stores",
    f"{total_stores:,}"
)

kpi5.metric(
    "Products",
    f"{total_products:,}"
)

kpi6.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)


# ============================================================
# YEAR-WISE SALES
# ============================================================

st.divider()

st.header("Sales Performance")


if (
    "year" in sales_df.columns
    and "total_value" in sales_df.columns
):

    yearly_sales = (
        sales_df
        .groupby("year")["total_value"]
        .sum()
        .reset_index()
        .sort_values("year")
    )


    fig_year = px.bar(
        yearly_sales,
        x="year",
        y="total_value",
        text="total_value",
        title="Sales by Year"
    )


    fig_year.update_traces(
        texttemplate="₹%{y:,.0f}",
        textposition="outside"
    )


    fig_year.update_layout(
        template="plotly_white",
        xaxis_title="Year",
        yaxis_title="Sales (₹)",
        height=450
    )


    st.plotly_chart(
        fig_year,
        use_container_width=True
    )


# ============================================================
# CHANNEL PERFORMANCE
# ============================================================

if (
    "channel" in sales_df.columns
    and "total_value" in sales_df.columns
):

    st.header("Channel Performance")


    channel_sales = (
        sales_df
        .groupby("channel")["total_value"]
        .sum()
        .reset_index()
        .sort_values(
            "total_value",
            ascending=False
        )
    )


    channel_left, channel_right = st.columns(2)


    with channel_left:

        fig_channel = px.bar(
            channel_sales,
            x="channel",
            y="total_value",
            text="total_value",
            title="Sales by Channel"
        )


        fig_channel.update_traces(
            texttemplate="₹%{y:,.0f}",
            textposition="outside"
        )


        fig_channel.update_layout(
            template="plotly_white",
            xaxis_title="Channel",
            yaxis_title="Sales (₹)",
            height=430
        )


        st.plotly_chart(
            fig_channel,
            use_container_width=True
        )


    with channel_right:

        fig_channel_pie = px.pie(
            channel_sales,
            names="channel",
            values="total_value",
            hole=0.45,
            title="Channel Sales Distribution"
        )


        fig_channel_pie.update_layout(
            template="plotly_white",
            height=430
        )


        st.plotly_chart(
            fig_channel_pie,
            use_container_width=True
        )


# ============================================================
# FORECAST SUMMARY
# ============================================================

st.divider()

st.header("Demand Forecasting")


if forecast_df is not None:

    required_columns = [
        "actual_demand",
        "predicted_demand"
    ]


    if all(
        column in forecast_df.columns
        for column in required_columns
    ):

        actual = pd.to_numeric(
            forecast_df["actual_demand"],
            errors="coerce"
        )

        predicted = pd.to_numeric(
            forecast_df["predicted_demand"],
            errors="coerce"
        )


        valid = pd.DataFrame({
            "actual": actual,
            "predicted": predicted
        }).dropna()


        if not valid.empty:

            mae = (
                (valid["actual"] - valid["predicted"])
                .abs()
                .mean()
            )


            rmse = (
                (
                    (valid["actual"] - valid["predicted"]) ** 2
                ).mean()
                ** 0.5
            )


            forecast1, forecast2, forecast3 = st.columns(3)


            forecast1.metric(
                "Forecast Records",
                f"{len(valid):,}"
            )


            forecast2.metric(
                "MAE",
                f"{mae:,.2f}"
            )


            forecast3.metric(
                "RMSE",
                f"{rmse:,.2f}"
            )


            if "date" in forecast_df.columns:

                forecast_chart = forecast_df[
                    [
                        "date",
                        "actual_demand",
                        "predicted_demand"
                    ]
                ].copy()


                forecast_chart["date"] = pd.to_datetime(
                    forecast_chart["date"],
                    errors="coerce"
                )


                forecast_chart = (
                    forecast_chart
                    .sort_values("date")
                )


                fig_forecast = px.line(
                    forecast_chart,
                    x="date",
                    y=[
                        "actual_demand",
                        "predicted_demand"
                    ],
                    title="Actual vs Predicted Demand"
                )


                fig_forecast.update_layout(
                    template="plotly_white",
                    xaxis_title="Date",
                    yaxis_title="Demand",
                    height=450
                )


                st.plotly_chart(
                    fig_forecast,
                    use_container_width=True
                )


    else:

        st.info(
            "Forecast columns are not available."
        )

else:

    st.info(
        "Demand forecast dataset is not available."
    )


# ============================================================
# INVENTORY RISK SUMMARY
# ============================================================

st.divider()

st.header("Inventory Risk Overview")


if inventory_df is not None:

    if "final_risk_level" in inventory_df.columns:

        risk_counts = (
            inventory_df["final_risk_level"]
            .astype(str)
            .str.strip()
            .value_counts()
            .reset_index()
        )


        risk_counts.columns = [
            "Risk Level",
            "Products"
        ]


        critical = (
            inventory_df["final_risk_level"]
            .astype(str)
            .str.lower()
            .eq("critical")
            .sum()
        )


        high = (
            inventory_df["final_risk_level"]
            .astype(str)
            .str.lower()
            .eq("high risk")
            .sum()
        )


        medium = (
            inventory_df["final_risk_level"]
            .astype(str)
            .str.lower()
            .eq("medium risk")
            .sum()
        )


        low = (
            inventory_df["final_risk_level"]
            .astype(str)
            .str.lower()
            .eq("low risk")
            .sum()
        )


        risk1, risk2, risk3, risk4 = st.columns(4)


        risk1.metric(
            "Critical",
            f"{critical:,}"
        )


        risk2.metric(
            "High Risk",
            f"{high:,}"
        )


        risk3.metric(
            "Medium Risk",
            f"{medium:,}"
        )


        risk4.metric(
            "Low Risk",
            f"{low:,}"
        )


        fig_risk = px.bar(
            risk_counts,
            x="Risk Level",
            y="Products",
            text="Products",
            title="Inventory Risk Distribution"
        )


        fig_risk.update_traces(
            textposition="outside"
        )


        fig_risk.update_layout(
            template="plotly_white",
            xaxis_title="Risk Level",
            yaxis_title="Products",
            height=450
        )


        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )


    else:

        st.info(
            "Risk level column is not available."
        )

else:

    st.info(
        "Inventory risk dataset is not available."
    )


# ============================================================
# KEY BUSINESS INSIGHTS
# ============================================================

st.divider()

st.header("Key Business Insights")


insight_col1, insight_col2 = st.columns(2)


with insight_col1:

    st.subheader("Sales")

    if not yearly_sales.empty:

        best_year = yearly_sales.loc[
            yearly_sales["total_value"].idxmax(),
            "year"
        ]

        st.write(
            f"• Highest annual sales were recorded in "
            f"**{int(best_year)}**."
        )

    if not channel_sales.empty:

        best_channel = channel_sales.iloc[0]["channel"]

        st.write(
            f"• **{best_channel}** is the leading sales channel."
        )

    st.write(
        f"• The business generated "
        f"**₹{total_sales:,.0f}** in total sales."
    )


with insight_col2:

    st.subheader("Inventory")

    if inventory_df is not None:

        if "final_risk_level" in inventory_df.columns:

            total_risk_products = (
                critical + high
            )

            st.write(
                f"• **{total_risk_products:,}** products "
                f"are classified as Critical or High Risk."
            )

            st.write(
                f"• Critical inventory items: "
                f"**{critical:,}**."
            )

            st.write(
                f"• Low-risk inventory items: "
                f"**{low:,}**."
            )

    else:

        st.write(
            "• Inventory risk information is unavailable."
        )


# ============================================================
# PROJECT SUMMARY
# ============================================================

st.divider()

st.header("Project Summary")

st.write(
    """
    The Retail Demand Forecasting project transforms
    large-scale retail transaction data into actionable
    business intelligence.

    The system combines sales analytics, demand forecasting,
    product-level analysis and inventory risk assessment to
    support better retail decision-making.

    The dashboard enables management to monitor business
    performance, understand demand patterns, evaluate
    forecasting results and identify inventory risks.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting | Executive Summary"
)