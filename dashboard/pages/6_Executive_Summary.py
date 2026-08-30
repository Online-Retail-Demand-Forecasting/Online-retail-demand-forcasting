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
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       MAIN APPLICATION
       -------------------------------------------------------- */

    .stApp {
        background-color: #F4F7FB;
        color: #172033;
    }

    .main .block-container {
        max-width: 1550px;
        padding-top: 1.8rem;
        padding-bottom: 2rem;
    }


    /* --------------------------------------------------------
       DARK SIDEBAR
       -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0B172A 0%,
            #10243D 55%,
            #0B172A 100%
        );

        border-right: 1px solid #243B53;
    }

    section[data-testid="stSidebar"] * {
        color: #E8EEF7 !important;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #E8EEF7 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #29415F;
    }


    /* --------------------------------------------------------
       SIDEBAR TITLE
       -------------------------------------------------------- */

    section[data-testid="stSidebar"] h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        letter-spacing: -0.5px;
    }


    /* --------------------------------------------------------
       PAGE TITLE
       -------------------------------------------------------- */

    h1 {
        color: #102A43;
        font-weight: 800;
        letter-spacing: -1px;
    }

    h2 {
        color: #17324D;
        font-weight: 750;
    }

    h3 {
        color: #243B53;
        font-weight: 700;
    }


    /* --------------------------------------------------------
       METRIC CARDS
       -------------------------------------------------------- */

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 20px;
        min-height: 115px;
        box-shadow: 0 4px 14px rgba(15, 39, 71, 0.06);
        transition: all 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: #B8C7D9;
        box-shadow: 0 7px 20px rgba(15, 39, 71, 0.10);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #102A43 !important;
        font-size: 26px !important;
        font-weight: 800 !important;
    }


    /* --------------------------------------------------------
       DIVIDERS
       -------------------------------------------------------- */

    hr {
        border: none;
        border-top: 1px solid #DCE4EE;
        margin: 1.5rem 0;
    }


    /* --------------------------------------------------------
       DATAFRAME
       -------------------------------------------------------- */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }


    /* --------------------------------------------------------
       BUTTONS
       -------------------------------------------------------- */

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #CBD5E1;
        background-color: #FFFFFF;
        color: #17324D;
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: #2563EB;
        color: #2563EB;
    }


    /* --------------------------------------------------------
       CAPTIONS
       -------------------------------------------------------- */

    .stCaption {
        color: #64748B;
    }


    /* --------------------------------------------------------
       ALERT BOXES
       -------------------------------------------------------- */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
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

DEPLOYMENT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "deployment"
)

SALES_PATH = os.path.join(
    DEPLOYMENT_PATH,
    "product_sales_dashboard.csv"
)

FORECAST_PATH = os.path.join(
    DEPLOYMENT_PATH,
    "demand_forecast_results.csv"
)

INVENTORY_PATH = os.path.join(
    DEPLOYMENT_PATH,
    "inventory_risk_scoring.csv"
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📈 Retail Intelligence")

st.sidebar.caption(
    "Executive Business Dashboard"
)

st.sidebar.divider()

st.sidebar.markdown(
    "**Executive Summary**"
)

st.sidebar.caption(
    "Management-level view of sales, "
    "forecasting and inventory risk."
)

st.sidebar.divider()

st.sidebar.markdown(
    "### Dashboard Areas"
)

st.sidebar.markdown(
    """
    📊 **Sales Performance**

    🔮 **Demand Forecasting**

    📦 **Inventory Intelligence**

    ⚠️ **Risk Monitoring**

    🛍️ **Product Analysis**
    """
)

st.sidebar.divider()

st.sidebar.caption(
    "Retail Demand Forecasting"
)

st.sidebar.caption(
    "Data Science Project"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_number(value):
    """
    Convert large numbers into compact professional notation.
    """

    if value is None:
        return "0"

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def format_currency(value):
    """
    Compact Indian Rupee formatting.
    """

    if value is None:
        return "₹0"

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"₹{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"₹{value / 1_000:.1f}K"

    return f"₹{value:,.0f}"


# ============================================================
# LOAD DATA
# IMPORTANT:
# Do NOT cache huge DataFrames.
# ============================================================

def load_csv(path, columns=None):

    if not os.path.exists(path):
        return None

    try:
        return pd.read_csv(
            path,
            usecols=columns
        )

    except ValueError:

        # If a requested column is missing,
        # load the file without usecols.
        try:
            return pd.read_csv(path)

        except Exception:
            return None

    except Exception:
        return None


# ============================================================
# LOAD SALES DATA
# ============================================================

sales_columns = [
    "date",
    "total_value",
    "quantity",
    "receipt_id",
    "store_id",
    "sku_id",
    "channel"
]

sales_df = load_csv(
    SALES_PATH,
    sales_columns
)


# ============================================================
# LOAD FORECAST DATA
# ============================================================

forecast_columns = [
    "date",
    "actual_demand",
    "predicted_demand"
]

forecast_df = load_csv(
    FORECAST_PATH,
    forecast_columns
)


# ============================================================
# LOAD INVENTORY DATA
# ============================================================

inventory_columns = [
    "store_id",
    "sku_id",
    "final_risk_level",
    "risk_score"
]

inventory_df = load_csv(
    INVENTORY_PATH,
    inventory_columns
)


# ============================================================
# SALES DATA CHECK
# ============================================================

if sales_df is None:

    st.error(
        "Sales dataset could not be loaded."
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

    sales_df["year"] = (
        sales_df["date"].dt.year
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


# ============================================================
# FORECAST PREPARATION
# ============================================================

if forecast_df is not None:

    if "date" in forecast_df.columns:

        forecast_df["date"] = pd.to_datetime(
            forecast_df["date"],
            errors="coerce"
        )

    for column in [
        "actual_demand",
        "predicted_demand"
    ]:

        if column in forecast_df.columns:

            forecast_df[column] = pd.to_numeric(
                forecast_df[column],
                errors="coerce"
            )


# ============================================================
# INVENTORY PREPARATION
# ============================================================

if inventory_df is not None:

    if "risk_score" in inventory_df.columns:

        inventory_df["risk_score"] = pd.to_numeric(
            inventory_df["risk_score"],
            errors="coerce"
        ).fillna(0)

    if "final_risk_level" in inventory_df.columns:

        inventory_df["final_risk_level"] = (
            inventory_df["final_risk_level"]
            .astype(str)
            .str.strip()
        )


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📈 Executive Summary")

st.caption(
    "A management-level view of retail performance, "
    "demand forecasting and inventory risk."
)


# ============================================================
# EXECUTIVE SNAPSHOT
# ============================================================

st.header("Business Performance")

st.caption(
    "Key performance indicators across the retail operation."
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

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


# ============================================================
# KPI ROW 1
# ============================================================

kpi1, kpi2, kpi3 = st.columns(3)


with kpi1:

    st.metric(
        "💰 Total Sales",
        format_currency(total_sales)
    )

    st.caption(
        "Overall transaction value"
    )


with kpi2:

    st.metric(
        "🧾 Transactions",
        format_number(total_transactions)
    )

    st.caption(
        "Unique retail transactions"
    )


with kpi3:

    st.metric(
        "📦 Quantity Sold",
        format_number(total_quantity)
    )

    st.caption(
        "Total units sold"
    )


# ============================================================
# KPI ROW 2
# ============================================================

kpi4, kpi5, kpi6 = st.columns(3)


with kpi4:

    st.metric(
        "🏬 Stores",
        format_number(total_stores)
    )

    st.caption(
        "Active stores in dataset"
    )


with kpi5:

    st.metric(
        "🛍️ Products",
        format_number(total_products)
    )

    st.caption(
        "Unique SKUs"
    )


with kpi6:

    st.metric(
        "📊 Average Order Value",
        format_currency(average_order_value)
    )

    st.caption(
        "Average value per transaction"
    )


# ============================================================
# SALES PERFORMANCE
# ============================================================

st.divider()

st.header("Sales Performance")

st.caption(
    "Year-wise revenue performance across the retail business."
)


yearly_sales = pd.DataFrame()


if (
    "year" in sales_df.columns
    and "total_value" in sales_df.columns
):

    yearly_sales = (
        sales_df
        .dropna(subset=["year"])
        .groupby("year", as_index=False)["total_value"]
        .sum()
        .sort_values("year")
    )


    fig_year = px.bar(
        yearly_sales,
        x="year",
        y="total_value",
        text="total_value",
        color_discrete_sequence=["#2563EB"]
    )


    fig_year.update_traces(
        texttemplate="₹%{y:.3s}",
        textposition="outside",
        marker_line_width=0
    )


    fig_year.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        xaxis_title=None,
        yaxis_title="Sales (₹)",
        showlegend=False
    )


    st.plotly_chart(
        fig_year,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# CHANNEL PERFORMANCE
# ============================================================

if (
    "channel" in sales_df.columns
    and "total_value" in sales_df.columns
):

    st.divider()

    st.header("Channel Performance")

    st.caption(
        "Compare sales contribution across retail channels."
    )


    channel_sales = (
        sales_df
        .groupby("channel", as_index=False)["total_value"]
        .sum()
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
            color_discrete_sequence=["#0F766E"]
        )


        fig_channel.update_traces(
            marker_line_width=0
        )


        fig_channel.update_layout(
            template="plotly_white",
            height=390,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),
            xaxis_title=None,
            yaxis_title="Sales (₹)",
            showlegend=False
        )


        st.plotly_chart(
            fig_channel,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


    with channel_right:

        fig_channel_pie = px.pie(
            channel_sales,
            names="channel",
            values="total_value",
            hole=0.58,
            color_discrete_sequence=[
                "#2563EB",
                "#0F766E",
                "#F59E0B",
                "#7C3AED",
                "#E11D48"
            ]
        )


        fig_channel_pie.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )


        fig_channel_pie.update_layout(
            template="plotly_white",
            height=390,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),
            showlegend=False
        )


        st.plotly_chart(
            fig_channel_pie,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# DEMAND FORECASTING
# ============================================================

st.divider()

st.header("Demand Forecasting")

st.caption(
    "Machine-learning forecast performance and demand accuracy."
)


if forecast_df is not None:

    required_forecast = [
        "actual_demand",
        "predicted_demand"
    ]


    if all(
        column in forecast_df.columns
        for column in required_forecast
    ):

        valid = forecast_df[
            required_forecast
        ].dropna()


        if not valid.empty:

            mae = (
                (
                    valid["actual_demand"]
                    -
                    valid["predicted_demand"]
                )
                .abs()
                .mean()
            )


            rmse = (
                (
                    (
                        valid["actual_demand"]
                        -
                        valid["predicted_demand"]
                    ) ** 2
                )
                .mean()
                ** 0.5
            )


            forecast1, forecast2, forecast3 = (
                st.columns(3)
            )


            with forecast1:

                st.metric(
                    "Forecast Records",
                    format_number(len(valid))
                )


            with forecast2:

                st.metric(
                    "MAE",
                    f"{mae:,.2f}"
                )


            with forecast3:

                st.metric(
                    "RMSE",
                    f"{rmse:,.2f}"
                )


            if "date" in forecast_df.columns:

                forecast_chart = (
                    forecast_df[
                        [
                            "date",
                            "actual_demand",
                            "predicted_demand"
                        ]
                    ]
                    .dropna()
                    .sort_values("date")
                )


                # Aggregate by date.
                # This keeps the executive chart light.
                forecast_chart = (
                    forecast_chart
                    .groupby("date", as_index=False)
                    .agg(
                        actual_demand=(
                            "actual_demand",
                            "sum"
                        ),
                        predicted_demand=(
                            "predicted_demand",
                            "sum"
                        )
                    )
                )


                fig_forecast = px.line(
                    forecast_chart,
                    x="date",
                    y=[
                        "actual_demand",
                        "predicted_demand"
                    ],
                    color_discrete_sequence=[
                        "#2563EB",
                        "#F59E0B"
                    ]
                )


                fig_forecast.update_layout(
                    template="plotly_white",
                    height=430,
                    margin=dict(
                        l=20,
                        r=20,
                        t=20,
                        b=20
                    ),
                    xaxis_title=None,
                    yaxis_title="Demand",
                    hovermode="x unified",
                    legend_title=None
                )


                st.plotly_chart(
                    fig_forecast,
                    use_container_width=True,
                    config={
                        "displayModeBar": False
                    }
                )


        else:

            st.info(
                "Forecast data does not contain valid records."
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
# INVENTORY RISK
# ============================================================

st.divider()

st.header("Inventory Risk Overview")

st.caption(
    "Current distribution of inventory risk across products."
)


critical = 0
high = 0
medium = 0
low = 0


if inventory_df is not None:

    if "final_risk_level" in inventory_df.columns:

        risk_series = (
            inventory_df["final_risk_level"]
            .astype(str)
            .str.lower()
            .str.strip()
        )


        critical = (
            risk_series
            .eq("critical")
            .sum()
        )


        high = (
            risk_series
            .eq("high risk")
            .sum()
        )


        medium = (
            risk_series
            .eq("medium risk")
            .sum()
        )


        low = (
            risk_series
            .eq("low risk")
            .sum()
        )


        risk1, risk2, risk3, risk4 = st.columns(4)


        with risk1:

            st.metric(
                "🔴 Critical",
                format_number(critical)
            )


        with risk2:

            st.metric(
                "🟠 High Risk",
                format_number(high)
            )


        with risk3:

            st.metric(
                "🟡 Medium Risk",
                format_number(medium)
            )


        with risk4:

            st.metric(
                "🟢 Low Risk",
                format_number(low)
            )


        risk_counts = (
            inventory_df["final_risk_level"]
            .value_counts()
            .reset_index()
        )


        risk_counts.columns = [
            "Risk Level",
            "Products"
        ]


        fig_risk = px.bar(
            risk_counts,
            x="Risk Level",
            y="Products",
            color="Risk Level",
            color_discrete_map={
                "Critical": "#DC2626",
                "High Risk": "#EA580C",
                "Medium Risk": "#D97706",
                "Low Risk": "#16A34A"
            }
        )


        fig_risk.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),
            xaxis_title=None,
            yaxis_title="Products",
            showlegend=False
        )


        st.plotly_chart(
            fig_risk,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "Risk level information is unavailable."
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

st.caption(
    "Automatically generated observations from the available data."
)


insight_left, insight_right = st.columns(2)


# ============================================================
# SALES INSIGHTS
# ============================================================

with insight_left:

    st.subheader("📊 Sales Insights")


    if not yearly_sales.empty:

        best_year_row = (
            yearly_sales
            .loc[
                yearly_sales["total_value"].idxmax()
            ]
        )


        best_year = int(
            best_year_row["year"]
        )


        best_year_sales = (
            best_year_row["total_value"]
        )


        st.success(
            f"Strongest sales year: **{best_year}** "
            f"with {format_currency(best_year_sales)}."
        )


    if (
        "channel" in sales_df.columns
        and "total_value" in sales_df.columns
        and not channel_sales.empty
    ):

        best_channel = (
            channel_sales
            .iloc[0]["channel"]
        )


        st.info(
            f"Leading sales channel: **{best_channel}**."
        )


    st.write(
        f"Total business sales reached "
        f"**{format_currency(total_sales)}**."
    )


# ============================================================
# INVENTORY INSIGHTS
# ============================================================

with insight_right:

    st.subheader("📦 Inventory Insights")


    total_risk_products = (
        critical + high
    )


    if inventory_df is not None:

        if "final_risk_level" in inventory_df.columns:

            st.warning(
                f"**{format_number(total_risk_products)}** "
                f"products require elevated inventory attention."
            )


            st.write(
                f"Critical inventory: "
                f"**{format_number(critical)}** products."
            )


            st.write(
                f"Low-risk inventory: "
                f"**{format_number(low)}** products."
            )


        else:

            st.write(
                "Risk classification is unavailable."
            )

    else:

        st.write(
            "Inventory risk information is unavailable."
        )


# ============================================================
# PROJECT SUMMARY
# ============================================================

st.divider()

st.header("Project Summary")


summary_left, summary_right = st.columns(
    [2, 1]
)


with summary_left:

    st.write(
        """
        The **Retail Demand Forecasting** platform transforms
        large-scale retail transaction data into actionable
        business intelligence.

        The system combines sales analytics, machine-learning
        demand forecasting, product-level analysis and inventory
        risk assessment to support better operational and
        strategic decisions.

        Management can use the dashboard to monitor business
        performance, understand demand behaviour, evaluate
        forecast quality and identify inventory conditions
        requiring attention.
        """
    )


with summary_right:

    st.metric(
        "Sales Generated",
        format_currency(total_sales)
    )

    st.metric(
        "Products Monitored",
        format_number(total_products)
    )

    st.metric(
        "Stores Covered",
        format_number(total_stores)
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting  •  Executive Summary  •  Data Science Project"
)
