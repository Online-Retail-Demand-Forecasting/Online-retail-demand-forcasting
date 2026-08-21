# ============================================================
# RETAIL EXECUTIVE DASHBOARD
# Sales Performance • Demand Forecasting • Inventory Intelligence
# ============================================================

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Executive Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL DASHBOARD THEME
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #F6F8FB;
    }

    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* HEADER */

    .header-box {
        background: linear-gradient(
            135deg,
            #0F2747 0%,
            #183B63 100%
        );

        padding: 28px 32px;
        border-radius: 14px;
        margin-bottom: 28px;

        box-shadow:
            0 6px 18px
            rgba(15, 39, 71, 0.12);
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 6px;
    }

    .main-subtitle {
        font-size: 15px;
        color: #DCE8F5;
        line-height: 1.5;
    }

    /* SECTION HEADINGS */

    .section-header {
        font-size: 21px;
        font-weight: 700;
        color: #17324D;

        margin-top: 8px;
        margin-bottom: 14px;

        padding-bottom: 9px;

        border-bottom:
            2px solid #DCE3EB;
    }

    /* KPI CARDS */

    div[data-testid="stMetric"] {
        background: #FFFFFF;

        border:
            1px solid #E2E8F0;

        border-radius: 12px;

        padding: 16px 18px;

        box-shadow:
            0 3px 10px
            rgba(15, 39, 71, 0.05);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);

        box-shadow:
            0 7px 18px
            rgba(15, 39, 71, 0.10);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #17324D !important;
        font-size: 23px !important;
        font-weight: 700 !important;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right:
            1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"]
    .block-container {
        padding-top: 2rem;
    }

    .sidebar-title {
        color: #17324D;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sidebar-caption {
        color: #64748B;
        font-size: 13px;
        margin-bottom: 20px;
    }

    /* FILTER NOTE */

    .filter-note {
        background: #F1F5F9;

        border-left:
            3px solid #1F4E79;

        padding: 10px 12px;

        border-radius: 6px;

        color: #475569;

        font-size: 12px;

        margin-top: 12px;
        margin-bottom: 16px;
    }

    /* PLOTLY */

    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;

        border:
            1px solid #E2E8F0;

        border-radius: 12px;

        padding: 7px;

        box-shadow:
            0 3px 10px
            rgba(15, 39, 71, 0.04);
    }

    /* ALERTS */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* DATAFRAME */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
    }

    /* FOOTER */

    .dashboard-footer {
        text-align: center;

        color: #718096;

        font-size: 12px;

        padding: 18px 0 4px 0;

        border-top:
            1px solid #DCE3EB;

        margin-top: 28px;
    }

    /* RESPONSIVE */

    @media (max-width: 900px) {

        .main-title {
            font-size: 26px;
        }

        .header-box {
            padding: 22px;
        }
    }

    /* HIDE STREAMLIT DEFAULT MENU */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
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
        os.path.abspath(__file__)
    )
)

PROCESSED_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(df, possible_names):
    """
    Find a dataframe column using flexible column-name matching.
    """

    if df is None:
        return None

    normalized = {}

    for col in df.columns:

        key = (
            str(col)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        normalized[key] = col

    for name in possible_names:

        key = (
            name
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        if key in normalized:
            return normalized[key]

    return None


def normalize_sku(value):
    """
    Normalize SKU values before joining datasets.
    """

    if pd.isna(value):
        return None

    value = str(value).strip().upper()

    # Remove accidental decimal representation
    # e.g. 1001.0 -> 1001
    if value.endswith(".0"):
        value = value[:-2]

    return value


def section_title(title):

    st.markdown(
        f"""
        <div class="section-header">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )


def style_chart(fig, height=None):

    fig.update_layout(

        template="plotly_white",

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

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        margin=dict(
            l=55,
            r=35,
            t=65,
            b=50
        ),

        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),

        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0
        ),

        hovermode="closest"
    )

    if height is not None:
        fig.update_layout(height=height)

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


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_csv(filename):

    path = os.path.join(
        PROCESSED_PATH,
        filename
    )

    if not os.path.exists(path):
        return None

    try:
        return pd.read_csv(path)

    except Exception as e:

        st.error(
            f"Could not read {filename}: {e}"
        )

        return None


sales_df = load_csv(
    "sales_transactions_cleaned.csv"
)

demand_df = load_csv(
    "daily_demand_features.csv"
)

forecast_df = load_csv(
    "demand_forecast_results.csv"
)

inventory_df = load_csv(
    "inventory_risk_scoring.csv"
)

sku_master_df = load_csv(
    "sku_master.csv"
)


# ============================================================
# VALIDATE MAIN SALES DATA FIRST
# ============================================================

if sales_df is None:

    st.error(
        "sales_transactions_cleaned.csv could not be found."
    )

    st.info(
        f"Expected location: {PROCESSED_PATH}"
    )

    st.stop()


# ============================================================
# NORMALIZE SALES COLUMN NAMES
# ============================================================

sales_df.columns = [
    str(col).strip()
    for col in sales_df.columns
]


# ============================================================
# DATE CONVERSION
# ============================================================

if "date" in sales_df.columns:

    sales_df["date"] = pd.to_datetime(
        sales_df["date"],
        errors="coerce"
    )


if demand_df is not None and "date" in demand_df.columns:

    demand_df["date"] = pd.to_datetime(
        demand_df["date"],
        errors="coerce"
    )


if forecast_df is not None and "date" in forecast_df.columns:

    forecast_df["date"] = pd.to_datetime(
        forecast_df["date"],
        errors="coerce"
    )


# ============================================================
# CREATE YEAR COLUMN
# ============================================================

if (
    "year" not in sales_df.columns
    and "date" in sales_df.columns
):

    sales_df["year"] = (
        sales_df["date"]
        .dt.year
    )


# ============================================================
# NUMERIC CLEANING
# ============================================================

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
# FIX CATEGORY MAPPING
# ============================================================

# Always create category first
sales_df["category"] = "Uncategorized"


if sku_master_df is not None:

    sales_sku_col = find_column(
        sales_df,
        [
            "sku_id",
            "sku",
            "product_id",
            "product_code",
            "product_sku"
        ]
    )

    master_sku_col = find_column(
        sku_master_df,
        [
            "sku_id",
            "sku",
            "product_id",
            "product_code",
            "product_sku"
        ]
    )

    master_category_col = find_column(
        sku_master_df,
        [
            "category",
            "product_category",
            "category_name",
            "product_type"
        ]
    )

    if (
        sales_sku_col is not None
        and master_sku_col is not None
        and master_category_col is not None
    ):

        # ----------------------------------------------------
        # Create clean lookup table
        # ----------------------------------------------------

        sku_lookup = sku_master_df[
            [
                master_sku_col,
                master_category_col
            ]
        ].copy()

        sku_lookup["_sku_key"] = (
            sku_lookup[master_sku_col]
            .apply(normalize_sku)
        )

        sku_lookup["_category_value"] = (
            sku_lookup[master_category_col]
            .astype(str)
            .str.strip()
        )

        # Remove invalid categories
        sku_lookup.loc[
            sku_lookup["_category_value"].isin(
                [
                    "",
                    "nan",
                    "None",
                    "NaN"
                ]
            ),
            "_category_value"
        ] = None

        # Remove duplicate SKU mappings
        sku_lookup = (
            sku_lookup[
                [
                    "_sku_key",
                    "_category_value"
                ]
            ]
            .dropna(
                subset=["_sku_key"]
            )
            .drop_duplicates(
                subset="_sku_key",
                keep="first"
            )
        )

        # ----------------------------------------------------
        # Create normalized SKU in sales
        # ----------------------------------------------------

        sales_df["_sku_key"] = (
            sales_df[sales_sku_col]
            .apply(normalize_sku)
        )

        # ----------------------------------------------------
        # Merge ONLY temporary category column
        # ----------------------------------------------------

        sales_df = sales_df.merge(
            sku_lookup,
            on="_sku_key",
            how="left"
        )

        # ----------------------------------------------------
        # Replace Uncategorized when mapping exists
        # ----------------------------------------------------

        mapped_category = (
            sales_df["_category_value"]
            .fillna("Uncategorized")
            .astype(str)
            .str.strip()
        )

        mapped_category = mapped_category.replace(
            {
                "nan": "Uncategorized",
                "None": "Uncategorized",
                "": "Uncategorized"
            }
        )

        sales_df["category"] = mapped_category

        # ----------------------------------------------------
        # Remove temporary columns ONLY
        # ----------------------------------------------------

        sales_df.drop(
            columns=[
                "_sku_key",
                "_category_value"
            ],
            inplace=True,
            errors="ignore"
        )

    else:

        # Show diagnostic information
        st.sidebar.warning(
            "SKU master category mapping could not be established."
        )


# ============================================================
# CATEGORY CLEANING
# ============================================================

sales_df["category"] = (
    sales_df["category"]
    .fillna("Uncategorized")
    .astype(str)
    .str.strip()
)

sales_df.loc[
    sales_df["category"].isin(
        [
            "",
            "nan",
            "None",
            "NaN"
        ]
    ),
    "category"
] = "Uncategorized"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="header-box">

        <div class="main-title">
            Retail Executive Dashboard
        </div>

        <div class="main-subtitle">
            Sales Performance • Demand Forecasting • Inventory Intelligence
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        Dashboard Filters
    </div>

    <div class="sidebar-caption">
        Select the period and sales channels to analyze.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# YEAR FILTER
# ============================================================

if "year" in sales_df.columns:

    years = sorted(
        sales_df["year"]
        .dropna()
        .unique()
        .tolist()
    )

else:

    years = []


selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)


# ============================================================
# CHANNEL FILTER
# ============================================================

if "channel" in sales_df.columns:

    channels = sorted(
        sales_df["channel"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

else:

    channels = []


selected_channels = st.sidebar.multiselect(
    "Select Channel",
    channels,
    default=channels
)


# ============================================================
# FILTER SUMMARY
# ============================================================

st.sidebar.markdown("---")

st.sidebar.caption(
    f"Years selected: {len(selected_years)}"
)

st.sidebar.caption(
    f"Channels selected: {len(selected_channels)}"
)


# ============================================================
# APPLY SALES FILTERS
# ============================================================

filtered_sales = sales_df.copy()


# If there are available years but user selects none,
# return no rows.

if "year" in filtered_sales.columns:

    if selected_years:

        filtered_sales = filtered_sales[
            filtered_sales["year"].isin(
                selected_years
            )
        ]

    else:

        filtered_sales = filtered_sales.iloc[0:0]


if "channel" in filtered_sales.columns:

    if selected_channels:

        filtered_sales = filtered_sales[
            filtered_sales["channel"].isin(
                selected_channels
            )
        ]

    else:

        filtered_sales = filtered_sales.iloc[0:0]


# ============================================================
# APPLY DEMAND FILTER
# ============================================================

if demand_df is not None:

    filtered_demand = demand_df.copy()

    if (
        selected_years
        and "date" in filtered_demand.columns
    ):

        filtered_demand = filtered_demand[
            filtered_demand["date"]
            .dt.year
            .isin(selected_years)
        ]

    elif not selected_years:

        filtered_demand = filtered_demand.iloc[0:0]

else:

    filtered_demand = None


# ============================================================
# APPLY FORECAST FILTER
# ============================================================

if forecast_df is not None:

    filtered_forecast = forecast_df.copy()

    if (
        selected_years
        and "date" in filtered_forecast.columns
    ):

        filtered_forecast = filtered_forecast[
            filtered_forecast["date"]
            .dt.year
            .isin(selected_years)
        ]

    elif not selected_years:

        filtered_forecast = filtered_forecast.iloc[0:0]

else:

    filtered_forecast = None


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_sales.empty:

    st.warning(
        "No sales records match the selected filters."
    )

    st.info(
        "Please select at least one year and one channel."
    )

    st.stop()


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

section_title("Executive Summary")


# ============================================================
# KPI CALCULATIONS
# ============================================================

if "total_value" in filtered_sales.columns:

    total_sales = filtered_sales[
        "total_value"
    ].sum()

else:

    total_sales = 0


if "receipt_id" in filtered_sales.columns:

    total_transactions = (
        filtered_sales[
            "receipt_id"
        ]
        .nunique()
    )

else:

    total_transactions = len(
        filtered_sales
    )


if "quantity" in filtered_sales.columns:

    total_quantity = (
        filtered_sales[
            "quantity"
        ]
        .sum()
    )

else:

    total_quantity = 0


if "store_id" in filtered_sales.columns:

    total_stores = (
        filtered_sales[
            "store_id"
        ]
        .nunique()
    )

else:

    total_stores = 0


if "sku_id" in filtered_sales.columns:

    total_products = (
        filtered_sales[
            "sku_id"
        ]
        .nunique()
    )

else:

    total_products = 0


average_order_value = (
    total_sales / total_transactions
    if total_transactions > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = (
    st.columns(6)
)


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
    f"₹{average_order_value:,.0f}"
)


# ============================================================
# SALES TREND + CHANNEL
# ============================================================

st.divider()

left, right = st.columns([2, 1])


# ============================================================
# DAILY SALES TREND
# ============================================================

with left:

    section_title("Sales Trend")

    if (
        "date" in filtered_sales.columns
        and "total_value" in filtered_sales.columns
    ):

        daily_sales = (
            filtered_sales
            .dropna(subset=["date"])
            .groupby("date")["total_value"]
            .sum()
            .reset_index()
            .sort_values("date")
        )

        fig_sales = px.line(
            daily_sales,
            x="date",
            y="total_value",
            title="Daily Sales Trend"
        )

        fig_sales.update_traces(

            line=dict(
                color="#1F77B4",
                width=2.5
            ),

            hovertemplate=
            "<b>%{x|%d %b %Y}</b>"
            "<br>Sales: ₹%{y:,.0f}"
            "<extra></extra>"
        )

        fig_sales.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales (₹)",
            hovermode="x unified",
            dragmode="zoom"
        )

        style_chart(fig_sales)

        st.plotly_chart(
            fig_sales,
            use_container_width=True,
            key="daily_sales_chart"
        )

    else:

        st.info(
            "Date or sales columns are not available."
        )


# ============================================================
# SALES BY CHANNEL
# ============================================================

with right:

    section_title("Sales by Channel")

    if (
        "channel" in filtered_sales.columns
        and "total_value" in filtered_sales.columns
    ):

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

            hole=0.45,

            title="Sales Distribution by Channel",

            color_discrete_sequence=[
                "#1F4E79",
                "#2E75B6",
                "#70AD47",
                "#ED7D31",
                "#A5A5A5"
            ]
        )

        fig_channel.update_traces(

            textposition="inside",

            textinfo="percent",

            hovertemplate=
            "<b>%{label}</b>"
            "<br>Sales: ₹%{value:,.0f}"
            "<br>Share: %{percent}"
            "<extra></extra>"
        )

        style_chart(fig_channel)

        st.plotly_chart(
            fig_channel,
            use_container_width=True,
            key="channel_chart"
        )

    else:

        st.info(
            "Channel information is not available."
        )


# ============================================================
# STORE-WISE SALES
# ============================================================

st.divider()

section_title("Store-wise Sales")


if (
    "store_id" in filtered_sales.columns
    and "total_value" in filtered_sales.columns
):

    store_sales = (
        filtered_sales
        .groupby("store_id")["total_value"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(15)
        .reset_index()
    )

    fig_store = px.bar(

        store_sales,

        x="store_id",

        y="total_value",

        title="Top 15 Stores by Sales",

        text="total_value",

        color_discrete_sequence=[
            "#1F4E79"
        ]
    )

    fig_store.update_traces(

        texttemplate="₹%{y:,.0f}",

        textposition="outside",

        hovertemplate=
        "<b>Store %{x}</b>"
        "<br>Sales: ₹%{y:,.0f}"
        "<extra></extra>"
    )

    fig_store.update_layout(

        xaxis_title="Store",

        yaxis_title="Sales (₹)",

        dragmode="zoom"
    )

    style_chart(fig_store)

    st.plotly_chart(
        fig_store,
        use_container_width=True,
        key="store_chart"
    )


# ============================================================
# DEMAND ANALYSIS
# ============================================================

st.divider()

section_title("Demand Analysis")

demand_left, demand_right = st.columns(2)


# ============================================================
# DEMAND TREND
# ============================================================

with demand_left:

    st.markdown(
        "**Demand Trend**"
    )

    if (
        filtered_demand is not None
        and "date" in filtered_demand.columns
        and "demand" in filtered_demand.columns
    ):

        filtered_demand["demand"] = pd.to_numeric(
            filtered_demand["demand"],
            errors="coerce"
        ).fillna(0)

        daily_demand = (
            filtered_demand
            .dropna(subset=["date"])
            .groupby("date")["demand"]
            .sum()
            .reset_index()
            .sort_values("date")
        )

        fig_demand = px.line(

            daily_demand,

            x="date",

            y="demand",

            title="Daily Demand"
        )

        fig_demand.update_traces(

            line=dict(
                color="#70AD47",
                width=2.5
            ),

            hovertemplate=
            "<b>%{x|%d %b %Y}</b>"
            "<br>Demand: %{y:,.0f}"
            "<extra></extra>"
        )

        fig_demand.update_layout(

            xaxis_title="Date",

            yaxis_title="Demand",

            hovermode="x unified"
        )

        style_chart(fig_demand)

        st.plotly_chart(

            fig_demand,

            use_container_width=True,

            key="demand_chart"
        )

    else:

        st.info(
            "Daily demand dataset is not available."
        )


# ============================================================
# ACTUAL VS FORECAST
# ============================================================

with demand_right:

    st.markdown(
        "**Actual vs Forecast**"
    )

    if (
        filtered_forecast is not None
        and "date" in filtered_forecast.columns
        and "actual_demand" in filtered_forecast.columns
        and "predicted_demand" in filtered_forecast.columns
    ):

        forecast_chart = (
            filtered_forecast[
                [
                    "date",
                    "actual_demand",
                    "predicted_demand"
                ]
            ]
            .copy()
            .sort_values("date")
        )

        forecast_chart["actual_demand"] = pd.to_numeric(
            forecast_chart["actual_demand"],
            errors="coerce"
        )

        forecast_chart["predicted_demand"] = pd.to_numeric(
            forecast_chart["predicted_demand"],
            errors="coerce"
        )

        fig_forecast = go.Figure()

        fig_forecast.add_trace(

            go.Scatter(

                x=forecast_chart["date"],

                y=forecast_chart["actual_demand"],

                mode="lines",

                name="Actual Demand",

                line=dict(
                    color="#1F4E79",
                    width=2.5
                ),

                hovertemplate=
                "<b>%{x|%d %b %Y}</b>"
                "<br>Actual: %{y:,.0f}"
                "<extra></extra>"
            )
        )

        fig_forecast.add_trace(

            go.Scatter(

                x=forecast_chart["date"],

                y=forecast_chart["predicted_demand"],

                mode="lines",

                name="Predicted Demand",

                line=dict(
                    color="#ED7D31",
                    width=2.5,
                    dash="dash"
                ),

                hovertemplate=
                "<b>%{x|%d %b %Y}</b>"
                "<br>Predicted: %{y:,.0f}"
                "<extra></extra>"
            )
        )

        fig_forecast.update_layout(

            title="Actual vs Predicted Demand",

            xaxis_title="Date",

            yaxis_title="Demand",

            hovermode="x unified"
        )

        style_chart(fig_forecast)

        st.plotly_chart(

            fig_forecast,

            use_container_width=True,

            key="forecast_chart"
        )

    else:

        st.info(
            "Forecast columns are not available."
        )


# ============================================================
# YEAR-WISE SALES
# ============================================================

st.divider()

section_title("Year-wise Sales")


if (
    "year" in filtered_sales.columns
    and "total_value" in filtered_sales.columns
):

    # IMPORTANT:
    # Use filtered_sales instead of sales_df.
    # This makes the chart respect sidebar filters.

    yearly_sales = (
        filtered_sales
        .groupby("year")["total_value"]
        .sum()
        .reset_index()
        .sort_values("year")
    )

    fig_year = px.bar(

        yearly_sales,

        x="year",

        y="total_value",

        title="Sales by Selected Year",

        text="total_value",

        color_discrete_sequence=[
            "#1F4E79"
        ]
    )

    fig_year.update_traces(

        texttemplate="₹%{y:,.0f}",

        textposition="outside",

        hovertemplate=
        "<b>%{x}</b>"
        "<br>Sales: ₹%{y:,.0f}"
        "<extra></extra>"
    )

    fig_year.update_layout(

        xaxis_title="Year",

        yaxis_title="Sales (₹)"
    )

    style_chart(fig_year)

    st.plotly_chart(

        fig_year,

        use_container_width=True,

        key="year_chart"
    )


# ============================================================
# INVENTORY RISK
# ============================================================

st.divider()

section_title("Inventory Risk")


if inventory_df is not None:

    risk_col = find_column(
        inventory_df,
        [
            "final_risk_level",
            "risk_level",
            "inventory_risk",
            "risk"
        ]
    )

    if risk_col is not None:

        risk_series = (
            inventory_df[risk_col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        # Normalize common naming variations

        risk_series = risk_series.replace(
            {
                "Critical Risk": "Critical",
                "High": "High Risk",
                "Medium": "Medium Risk",
                "Low": "Low Risk"
            }
        )

        risk_counts = (
            risk_series
            .value_counts()
        )

        critical_inventory = (
            risk_series
            .eq("Critical")
            .sum()
        )

        high_risk_inventory = (
            risk_series
            .eq("High Risk")
            .sum()
        )

        medium_risk_inventory = (
            risk_series
            .eq("Medium Risk")
            .sum()
        )

        low_risk_inventory = (
            risk_series
            .eq("Low Risk")
            .sum()
        )

        risk1, risk2, risk3, risk4 = (
            st.columns(4)
        )

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

        risk_data = (
            risk_counts
            .reset_index()
        )

        risk_data.columns = [
            "risk_level",
            "product_count"
        ]

        fig_risk = px.bar(

            risk_data,

            x="risk_level",

            y="product_count",

            title="Inventory Risk Distribution",

            text="product_count",

            color="risk_level",

            color_discrete_map={
                "Critical": "#C00000",
                "High Risk": "#ED7D31",
                "Medium Risk": "#FFC000",
                "Low Risk": "#70AD47",
                "Unknown": "#A5A5A5"
            }
        )

        fig_risk.update_traces(

            textposition="outside",

            hovertemplate=
            "<b>%{x}</b>"
            "<br>Products: %{y:,}"
            "<extra></extra>"
        )

        fig_risk.update_layout(

            xaxis_title="Risk Level",

            yaxis_title="Number of Products",

            showlegend=False
        )

        style_chart(fig_risk)

        st.plotly_chart(

            fig_risk,

            use_container_width=True,

            key="risk_chart"
        )

    else:

        st.info(
            "Risk level column is not available "
            "in inventory_risk_scoring.csv."
        )

else:

    st.info(
        "Inventory risk dataset is not available yet."
    )


# ============================================================
# TOP PRODUCTS
# ============================================================

st.divider()

section_title("Top Products")


if (
    "sku_id" in filtered_sales.columns
    and "total_value" in filtered_sales.columns
):

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

    # Reverse so highest appears at top
    top_products = top_products.sort_values(
        "total_value",
        ascending=True
    )

    fig_products = px.bar(

        top_products,

        x="total_value",

        y="sku_id",

        orientation="h",

        title="Top 10 Products by Sales",

        text="total_value",

        color_discrete_sequence=[
            "#2E75B6"
        ]
    )

    fig_products.update_traces(

        texttemplate="₹%{x:,.0f}",

        textposition="outside",

        hovertemplate=
        "<b>Product %{y}</b>"
        "<br>Sales: ₹%{x:,.0f}"
        "<extra></extra>"
    )

    fig_products.update_layout(

        xaxis_title="Sales (₹)",

        yaxis_title="Product"
    )

    style_chart(fig_products)

    st.plotly_chart(

        fig_products,

        use_container_width=True,

        key="products_chart"
    )


# ============================================================
# CATEGORY PERFORMANCE TABLE
# ============================================================

if (
    "category" in filtered_sales.columns
    and "total_value" in filtered_sales.columns
):

    st.divider()

    section_title("Category Performance")

    # --------------------------------------------------------
    # Build aggregation dynamically
    # --------------------------------------------------------

    aggregation = {
        "Sales": (
            "total_value",
            "sum"
        )
    }

    if "receipt_id" in filtered_sales.columns:

        aggregation["Transactions"] = (
            "receipt_id",
            "nunique"
        )

    else:

        aggregation["Transactions"] = (
            "total_value",
            "count"
        )

    if "quantity" in filtered_sales.columns:

        aggregation["Quantity"] = (
            "quantity",
            "sum"
        )

    else:

        aggregation["Quantity"] = (
            "total_value",
            "count"
        )

    category_summary = (
        filtered_sales
        .groupby("category")
        .agg(**aggregation)
        .reset_index()
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    category_summary["Sales"] = (
        pd.to_numeric(
            category_summary["Sales"],
            errors="coerce"
        )
        .fillna(0)
        .round(0)
    )

    category_summary["Transactions"] = (
        pd.to_numeric(
            category_summary["Transactions"],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
    )

    category_summary["Quantity"] = (
        pd.to_numeric(
            category_summary["Quantity"],
            errors="coerce"
        )
        .fillna(0)
        .round(0)
        .astype(int)
    )

    st.dataframe(

        category_summary,

        use_container_width=True,

        hide_index=True,

        column_config={

            "category": st.column_config.TextColumn(
                "Category"
            ),

            "Sales": st.column_config.NumberColumn(
                "Sales",
                format="₹%d"
            ),

            "Transactions": st.column_config.NumberColumn(
                "Transactions",
                format="%d"
            ),

            "Quantity": st.column_config.NumberColumn(
                "Quantity",
                format="%d"
            )
        }
    )


# ============================================================
# CATEGORY SALES CHART
# ============================================================

if (
    "category" in filtered_sales.columns
    and "total_value" in filtered_sales.columns
):

    st.markdown(
        "**Category Sales Distribution**"
    )

    category_chart_data = (
        filtered_sales
        .groupby("category")["total_value"]
        .sum()
        .reset_index()
        .sort_values(
            "total_value",
            ascending=False
        )
    )

    fig_category = px.bar(

        category_chart_data,

        x="category",

        y="total_value",

        title="Sales by Category",

        text="total_value",

        color_discrete_sequence=[
            "#1F4E79"
        ]
    )

    fig_category.update_traces(

        texttemplate="₹%{y:,.0f}",

        textposition="outside",

        hovertemplate=
        "<b>%{x}</b>"
        "<br>Sales: ₹%{y:,.0f}"
        "<extra></extra>"
    )

    fig_category.update_layout(

        xaxis_title="Category",

        yaxis_title="Sales (₹)"
    )

    style_chart(fig_category)

    st.plotly_chart(

        fig_category,

        use_container_width=True,

        key="category_chart"
    )


# ============================================================
# PROJECT OVERVIEW
# ============================================================

st.divider()

section_title("Project Overview")

st.write(
    """
    This Retail Executive Dashboard provides a professional
    overview of retail sales performance, customer transactions,
    demand trends, demand forecasting and inventory risk.

    The dashboard helps management understand sales patterns,
    channel performance, store performance, product performance
    and inventory risk so that better business decisions can
    be made.
    """
)


# ============================================================
# DATA SOURCE STATUS
# ============================================================

st.divider()

section_title("Data Sources")


dataset_status = []

datasets = {

    "Sales Transactions":
        sales_df,

    "SKU Master":
        sku_master_df,

    "Daily Demand Features":
        demand_df,

    "Demand Forecast Results":
        forecast_df,

    "Inventory Risk Scoring":
        inventory_df
}


for dataset_name, dataframe in datasets.items():

    if dataframe is not None:

        dataset_status.append(
            {
                "Dataset": dataset_name,

                "Status": "Available",

                "Records": len(dataframe),

                "Columns": len(dataframe.columns)
            }
        )

    else:

        dataset_status.append(
            {
                "Dataset": dataset_name,

                "Status": "Not Available",

                "Records": 0,

                "Columns": 0
            }
        )


status_df = pd.DataFrame(
    dataset_status
)


st.dataframe(

    status_df,

    use_container_width=True,

    hide_index=True,

    column_config={

        "Dataset": st.column_config.TextColumn(
            "Dataset"
        ),

        "Status": st.column_config.TextColumn(
            "Status"
        ),

        "Records": st.column_config.NumberColumn(
            "Records",
            format="%d"
        ),

        "Columns": st.column_config.NumberColumn(
            "Columns",
            format="%d"
        )
    }
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="dashboard-footer">

        Retail Executive Dashboard
        &nbsp;|&nbsp;
        Online Retail Demand Forecasting Project

    </div>
    """,
    unsafe_allow_html=True
)