# ============================================================
# RETAIL EXECUTIVE DASHBOARD
# Sales Performance • Demand Forecasting • Inventory Intelligence
# ============================================================

import os
from pathlib import Path

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

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #F6F8FB;
    }

    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }


    /* ========================================================
       HEADER
       ======================================================== */

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
        letter-spacing: -0.5px;
    }

    .main-subtitle {
        font-size: 15px;
        color: #DCE8F5;
        line-height: 1.5;
    }


    /* ========================================================
       SECTION HEADINGS
       ======================================================== */

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


    /* ========================================================
       KPI CARDS
       ======================================================== */

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


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #FFFFFF;

        border-right:
            1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"]
    .block-container {
        padding-top: 2rem;
    }


    /* ========================================================
       PLOTLY CHART CONTAINER
       ======================================================== */

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


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .dashboard-footer {
        text-align: center;

        color: #718096;

        font-size: 12px;

        padding: 18px 0 4px 0;

        border-top:
            1px solid #DCE3EB;

        margin-top: 28px;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 900px) {

        .main-title {
            font-size: 26px;
        }

        .header-box {
            padding: 22px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT PATHS
# ============================================================

# Current Python file location
CURRENT_DIR = Path(__file__).resolve().parent

# Project root candidates
PROJECT_ROOTS = [
    CURRENT_DIR,
    CURRENT_DIR.parent,
    CURRENT_DIR.parent.parent,
]

# Remove duplicates
PROJECT_ROOTS = list(dict.fromkeys(PROJECT_ROOTS))


# ============================================================
# FIND FILE FUNCTION
# ============================================================

def find_file(filename):
    """
    Searches common project locations recursively.

    This prevents problems when files are located in:
        data/processed/
        data/
        project/data/processed/
        etc.
    """

    for root in PROJECT_ROOTS:

        if not root.exists():
            continue

        # First check direct location
        direct_path = root / filename

        if direct_path.exists():
            return direct_path

        # Then search recursively
        try:

            matches = list(
                root.rglob(filename)
            )

            if matches:
                return matches[0]

        except Exception:
            pass

    return None


# ============================================================
# DATA LOADING FUNCTIONS
# ============================================================

@st.cache_data
def load_csv(filename):

    path = find_file(filename)

    if path is None:
        return None, None

    try:

        df = pd.read_csv(path)

        return df, str(path)

    except Exception as e:

        st.error(
            f"Error reading {filename}: {e}"
        )

        return None, str(path)


# ============================================================
# LOAD DATASETS
# ============================================================

sales_df, sales_path = load_csv(
    "sales_transactions_cleaned.csv"
)

demand_df, demand_path = load_csv(
    "daily_demand_features.csv"
)

forecast_df, forecast_path = load_csv(
    "demand_forecast_results.csv"
)

inventory_df, inventory_path = load_csv(
    "inventory_risk_scoring.csv"
)

sku_master_df, sku_master_path = load_csv(
    "sku_master.csv"
)


# ============================================================
# VALIDATE MAIN DATASET
# ============================================================

if sales_df is None:

    st.error(
        "sales_transactions_cleaned.csv could not be found."
    )

    st.info(
        "Make sure the file exists somewhere inside your project."
    )

    st.stop()


# ============================================================
# HELPER: FIND COLUMN
# ============================================================

def find_column(df, possible_names):

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
            str(name)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        if key in normalized:
            return normalized[key]

    return None


# ============================================================
# DATE CONVERSION
# ============================================================

date_col = find_column(
    sales_df,
    [
        "date",
        "transaction_date",
        "sales_date"
    ]
)

if date_col is not None:

    sales_df["date"] = pd.to_datetime(
        sales_df[date_col],
        errors="coerce"
    )

else:

    sales_df["date"] = pd.NaT


# Demand date

if demand_df is not None:

    demand_date_col = find_column(
        demand_df,
        [
            "date",
            "transaction_date",
            "sales_date"
        ]
    )

    if demand_date_col is not None:

        demand_df["date"] = pd.to_datetime(
            demand_df[demand_date_col],
            errors="coerce"
        )


# Forecast date

if forecast_df is not None:

    forecast_date_col = find_column(
        forecast_df,
        [
            "date",
            "transaction_date",
            "sales_date"
        ]
    )

    if forecast_date_col is not None:

        forecast_df["date"] = pd.to_datetime(
            forecast_df[forecast_date_col],
            errors="coerce"
        )


# ============================================================
# YEAR COLUMN
# ============================================================

existing_year_col = find_column(
    sales_df,
    [
        "year"
    ]
)

if existing_year_col is not None:

    sales_df["year"] = pd.to_numeric(
        sales_df[existing_year_col],
        errors="coerce"
    )

elif "date" in sales_df.columns:

    sales_df["year"] = (
        sales_df["date"]
        .dt.year
    )

else:

    sales_df["year"] = None


# ============================================================
# STANDARDIZE IMPORTANT SALES COLUMNS
# ============================================================

# Total value

total_value_col = find_column(
    sales_df,
    [
        "total_value",
        "total_sales",
        "sales",
        "amount",
        "revenue"
    ]
)

if total_value_col is not None:

    if total_value_col != "total_value":

        sales_df["total_value"] = sales_df[
            total_value_col
        ]

    sales_df["total_value"] = pd.to_numeric(
        sales_df["total_value"],
        errors="coerce"
    ).fillna(0)

else:

    sales_df["total_value"] = 0


# Quantity

quantity_col = find_column(
    sales_df,
    [
        "quantity",
        "qty",
        "units_sold"
    ]
)

if quantity_col is not None:

    if quantity_col != "quantity":

        sales_df["quantity"] = sales_df[
            quantity_col
        ]

    sales_df["quantity"] = pd.to_numeric(
        sales_df["quantity"],
        errors="coerce"
    ).fillna(0)

else:

    sales_df["quantity"] = 0


# ============================================================
# STANDARDIZE SKU
# ============================================================

sales_sku_col = find_column(
    sales_df,
    [
        "sku_id",
        "sku",
        "product_id",
        "product_code",
        "product"
    ]
)

if sales_sku_col is not None:

    if sales_sku_col != "sku_id":

        sales_df["sku_id"] = (
            sales_df[sales_sku_col]
        )

else:

    sales_df["sku_id"] = None


# ============================================================
# STANDARDIZE CHANNEL
# ============================================================

channel_col = find_column(
    sales_df,
    [
        "channel",
        "sales_channel",
        "order_channel"
    ]
)

if channel_col is not None:

    if channel_col != "channel":

        sales_df["channel"] = (
            sales_df[channel_col]
        )

    sales_df["channel"] = (
        sales_df["channel"]
        .astype(str)
        .str.strip()
    )

else:

    sales_df["channel"] = "Unknown"


# ============================================================
# STANDARDIZE STORE
# ============================================================

store_col = find_column(
    sales_df,
    [
        "store_id",
        "store",
        "store_code",
        "location_id"
    ]
)

if store_col is not None:

    if store_col != "store_id":

        sales_df["store_id"] = (
            sales_df[store_col]
        )

else:

    sales_df["store_id"] = None


# ============================================================
# STANDARDIZE RECEIPT
# ============================================================

receipt_col = find_column(
    sales_df,
    [
        "receipt_id",
        "receipt",
        "transaction_id",
        "invoice_id",
        "order_id"
    ]
)

if receipt_col is not None:

    if receipt_col != "receipt_id":

        sales_df["receipt_id"] = (
            sales_df[receipt_col]
        )

else:

    sales_df["receipt_id"] = (
        sales_df.index.astype(str)
    )


# ============================================================
# CATEGORY CREATION
# ============================================================

# IMPORTANT:
#
# Priority:
#
# 1. Category already present in sales file
# 2. Category from sku_master.csv
# 3. Uncategorized
#
# This prevents the entire dashboard becoming
# "Uncategorized" unnecessarily.
# ============================================================

sales_category_col = find_column(
    sales_df,
    [
        "category",
        "product_category",
        "category_name",
        "product_type",
        "department"
    ]
)


# ------------------------------------------------------------
# CASE 1:
# Category already exists in sales data
# ------------------------------------------------------------

if sales_category_col is not None:

    sales_df["category"] = (
        sales_df[sales_category_col]
        .fillna("Uncategorized")
        .astype(str)
        .str.strip()
    )

    sales_df["category"] = (
        sales_df["category"]
        .replace(
            {
                "",
                "nan",
                "None",
                "null",
                "NaN"
            },
            "Uncategorized"
        )
    )


# ------------------------------------------------------------
# CASE 2:
# Need to merge from SKU master
# ------------------------------------------------------------

elif sku_master_df is not None:

    master_sku_col = find_column(
        sku_master_df,
        [
            "sku_id",
            "sku",
            "product_id",
            "product_code",
            "product"
        ]
    )

    master_category_col = find_column(
        sku_master_df,
        [
            "category",
            "product_category",
            "category_name",
            "product_type",
            "department"
        ]
    )


    if (
        master_sku_col is not None
        and master_category_col is not None
    ):

        # Create normalized keys

        sales_df["_sku_key"] = (
            sales_df["sku_id"]
            .astype(str)
            .str.strip()
            .str.upper()
        )


        sku_lookup = sku_master_df[
            [
                master_sku_col,
                master_category_col
            ]
        ].copy()


        sku_lookup["_sku_key"] = (
            sku_lookup[master_sku_col]
            .astype(str)
            .str.strip()
            .str.upper()
        )


        # Clean categories

        sku_lookup[master_category_col] = (
            sku_lookup[master_category_col]
            .fillna("Uncategorized")
            .astype(str)
            .str.strip()
        )


        sku_lookup[master_category_col] = (
            sku_lookup[master_category_col]
            .replace(
                {
                    "",
                    "nan",
                    "None",
                    "null",
                    "NaN"
                },
                "Uncategorized"
            )
        )


        # Remove duplicate SKU mappings

        sku_lookup = (
            sku_lookup[
                [
                    "_sku_key",
                    master_category_col
                ]
            ]
            .drop_duplicates(
                subset="_sku_key",
                keep="first"
            )
        )


        # Merge

        sales_df = sales_df.merge(
            sku_lookup,
            on="_sku_key",
            how="left"
        )


        # Create category

        sales_df["category"] = (
            sales_df[master_category_col]
            .fillna("Uncategorized")
            .astype(str)
            .str.strip()
        )


        # Remove temporary columns

        sales_df.drop(
            columns=[
                "_sku_key",
                master_category_col
            ],
            inplace=True,
            errors="ignore"
        )


    else:

        sales_df["category"] = "Uncategorized"


# ------------------------------------------------------------
# CASE 3:
# SKU master does not exist
# ------------------------------------------------------------

else:

    sales_df["category"] = "Uncategorized"


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
            "NaN",
            "None",
            "null"
        ]
    ),
    "category"
] = "Uncategorized"


# ============================================================
# PROFESSIONAL PLOTLY STYLE
# ============================================================

def style_chart(
    fig,
    height=None
):

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

        fig.update_layout(
            height=height
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


# ============================================================
# DASHBOARD HEADER
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
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:20px;
        font-weight:700;
        color:#17324D;
        margin-bottom:5px;
    ">
        Dashboard Filters
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# YEAR FILTER
# ============================================================

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


# ============================================================
# CHANNEL FILTER
# ============================================================

channels = sorted(
    sales_df["channel"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


selected_channels = st.sidebar.multiselect(

    "Select Channel",

    channels,

    default=channels
)


# ============================================================
# CATEGORY FILTER
# ============================================================

categories = sorted(
    sales_df["category"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


selected_categories = st.sidebar.multiselect(

    "Select Category",

    categories,

    default=categories
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

st.sidebar.caption(
    f"Categories selected: {len(selected_categories)}"
)


# ============================================================
# CATEGORY DATA WARNING
# ============================================================

if sku_master_df is None and sales_category_col is None:

    st.sidebar.warning(
        "sku_master.csv was not found and "
        "sales data has no category column. "
        "Category values will be Uncategorized."
    )

elif sku_master_df is not None:

    st.sidebar.success(
        "SKU master loaded successfully."
    )


# ============================================================
# APPLY SALES FILTERS
# ============================================================

filtered_sales = sales_df.copy()


if selected_years:

    filtered_sales = filtered_sales[
        filtered_sales["year"].isin(
            selected_years
        )
    ]


if selected_channels:

    filtered_sales = filtered_sales[
        filtered_sales["channel"].isin(
            selected_channels
        )
    ]


if selected_categories:

    filtered_sales = filtered_sales[
        filtered_sales["category"].isin(
            selected_categories
        )
    ]


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
        "Please select at least one year, "
        "channel and category."
    )

    st.stop()


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.markdown(
    """
    <div class="section-header">
        Executive Summary
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = (
    filtered_sales["total_value"]
    .sum()
)


total_transactions = (
    filtered_sales["receipt_id"]
    .nunique()
)


total_quantity = (
    filtered_sales["quantity"]
    .sum()
)


total_stores = (
    filtered_sales["store_id"]
    .nunique()
)


total_products = (
    filtered_sales["sku_id"]
    .nunique()
)


average_order_value = (

    total_sales /
    total_transactions

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


left, right = st.columns(
    [2, 1]
)


# ============================================================
# DAILY SALES TREND
# ============================================================

with left:

    st.markdown(
        """
        <div class="section-header">
            Sales Trend
        </div>
        """,
        unsafe_allow_html=True
    )


    if (
        "date" in filtered_sales.columns
        and "total_value" in filtered_sales.columns
    ):

        daily_sales = (

            filtered_sales
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
                color="#0066CC",
                width=2
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


        style_chart(
            fig_sales
        )


        st.plotly_chart(

            fig_sales,

            use_container_width=True,

            key="daily_sales_chart"
        )


# ============================================================
# SALES BY CHANNEL
# ============================================================

with right:

    st.markdown(
        """
        <div class="section-header">
            Sales by Channel
        </div>
        """,
        unsafe_allow_html=True
    )


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
            "#6366F1",
            "#EF553B",
            "#00CC96",
            "#FFA15A"
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


    style_chart(
        fig_channel
    )


    st.plotly_chart(

        fig_channel,

        use_container_width=True,

        key="channel_chart"
    )


# ============================================================
# STORE-WISE SALES
# ============================================================

st.divider()


st.markdown(
    """
    <div class="section-header">
        Store-wise Sales
    </div>
    """,
    unsafe_allow_html=True
)


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
        "#0875CE"
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


style_chart(
    fig_store
)


st.plotly_chart(

    fig_store,

    use_container_width=True,

    key="store_chart"
)


# ============================================================
# CATEGORY PERFORMANCE
# ============================================================

st.divider()


st.markdown(
    """
    <div class="section-header">
        Category Performance
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CATEGORY SUMMARY
# ============================================================

category_summary = (

    filtered_sales
    .groupby("category")
    .agg(

        Sales=(
            "total_value",
            "sum"
        ),

        Transactions=(
            "receipt_id",
            "nunique"
        ),

        Quantity=(
            "quantity",
            "sum"
        ),

        Products=(
            "sku_id",
            "nunique"
        )

    )
    .reset_index()
    .sort_values(
        "Sales",
        ascending=False
    )
)


# ============================================================
# CATEGORY CHART + TABLE
# ============================================================

category_left, category_right = st.columns(
    [1.6, 1]
)


# ============================================================
# CATEGORY SALES CHART
# ============================================================

with category_left:

    fig_category = px.bar(

        category_summary,

        x="category",

        y="Sales",

        title="Sales by Category",

        text="Sales",

        color="Sales",

        color_continuous_scale=[
            "#DCEBFA",
            "#0875CE",
            "#0F2747"
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

        yaxis_title="Sales (₹)",

        coloraxis_showscale=False,

        xaxis_tickangle=-35
    )


    style_chart(
        fig_category,
        height=450
    )


    st.plotly_chart(

        fig_category,

        use_container_width=True,

        key="category_sales_chart"
    )


# ============================================================
# CATEGORY TABLE
# ============================================================

with category_right:

    display_category = category_summary.copy()

    display_category["Sales"] = (
        display_category["Sales"]
        .round(0)
    )


    st.dataframe(

        display_category,

        use_container_width=True,

        hide_index=True,

        height=450,

        column_config={

            "category":
                st.column_config.TextColumn(
                    "Category"
                ),

            "Sales":
                st.column_config.NumberColumn(
                    "Sales",
                    format="₹%d"
                ),

            "Transactions":
                st.column_config.NumberColumn(
                    "Transactions",
                    format="%d"
                ),

            "Quantity":
                st.column_config.NumberColumn(
                    "Quantity",
                    format="%d"
                ),

            "Products":
                st.column_config.NumberColumn(
                    "Products",
                    format="%d"
                )
        }
    )


# ============================================================
# DEMAND ANALYSIS
# ============================================================

st.divider()


st.markdown(
    """
    <div class="section-header">
        Demand Analysis
    </div>
    """,
    unsafe_allow_html=True
)


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
                color="#0875CE",
                width=2
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


        style_chart(
            fig_demand
        )


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


        forecast_chart[
            "actual_demand"
        ] = pd.to_numeric(
            forecast_chart[
                "actual_demand"
            ],
            errors="coerce"
        )


        forecast_chart[
            "predicted_demand"
        ] = pd.to_numeric(
            forecast_chart[
                "predicted_demand"
            ],
            errors="coerce"
        )


        fig_forecast = go.Figure()


        fig_forecast.add_trace(

            go.Scatter(

                x=forecast_chart["date"],

                y=forecast_chart[
                    "actual_demand"
                ],

                mode="lines",

                name="Actual Demand",

                line=dict(
                    color="#0875CE",
                    width=2
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

                y=forecast_chart[
                    "predicted_demand"
                ],

                mode="lines",

                name="Predicted Demand",

                line=dict(
                    color="#EF553B",
                    width=2
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


        style_chart(
            fig_forecast
        )


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


st.markdown(
    """
    <div class="section-header">
        Year-wise Sales
    </div>
    """,
    unsafe_allow_html=True
)


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

    title="Sales by Year",

    text="total_value",

    color_discrete_sequence=[
        "#0875CE"
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


style_chart(
    fig_year
)


st.plotly_chart(

    fig_year,

    use_container_width=True,

    key="year_chart"
)


# ============================================================
# INVENTORY RISK
# ============================================================

st.divider()


st.markdown(
    """
    <div class="section-header">
        Inventory Risk
    </div>
    """,
    unsafe_allow_html=True
)


if inventory_df is not None:

    risk_col = find_column(
        inventory_df,
        [
            "final_risk_level",
            "risk_level",
            "inventory_risk"
        ]
    )


    if risk_col is not None:

        inventory_df["_risk_clean"] = (
            inventory_df[risk_col]
            .astype(str)
            .str.strip()
        )


        critical_inventory = (
            inventory_df["_risk_clean"]
            .eq("Critical")
            .sum()
        )


        high_risk_inventory = (
            inventory_df["_risk_clean"]
            .eq("High Risk")
            .sum()
        )


        medium_risk_inventory = (
            inventory_df["_risk_clean"]
            .eq("Medium Risk")
            .sum()
        )


        low_risk_inventory = (
            inventory_df["_risk_clean"]
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


        risk_counts = (

            inventory_df[
                "_risk_clean"
            ]
            .value_counts()
            .reset_index()
        )


        risk_counts.columns = [
            "risk_level",
            "product_count"
        ]


        fig_risk = px.bar(

            risk_counts,

            x="risk_level",

            y="product_count",

            title="Inventory Risk Distribution",

            text="product_count",

            color="risk_level",

            color_discrete_map={
                "Critical": "#D62728",
                "High Risk": "#FF7F0E",
                "Medium Risk": "#F2C744",
                "Low Risk": "#2CA02C"
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


        style_chart(
            fig_risk
        )


        st.plotly_chart(

            fig_risk,

            use_container_width=True,

            key="risk_chart"
        )


    else:

        st.info(
            "Risk level column is not available."
        )


else:

    st.info(
        "Inventory risk dataset is not available yet."
    )


# ============================================================
# TOP PRODUCTS
# ============================================================

st.divider()


st.markdown(
    """
    <div class="section-header">
        Top Products
    </div>
    """,
    unsafe_allow_html=True
)


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

    title="Top 10 Products by Sales",

    text="total_value",

    color_discrete_sequence=[
        "#0875CE"
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

    yaxis_title="Product",

    yaxis={
        "categoryorder": "total ascending"
    }
)


style_chart(
    fig_products
)


st.plotly_chart(

    fig_products,

    use_container_width=True,

    key="products_chart"
)


# ============================================================
# CATEGORY DATA QUALITY
# ============================================================

st.divider()


st.markdown(
    """
    <div class="section-header">
        Category Data Quality
    </div>
    """,
    unsafe_allow_html=True
)


category_count = (
    sales_df["category"]
    .nunique()
)


uncategorized_count = (
    sales_df["category"]
    .eq("Uncategorized")
    .sum()
)


categorized_count = (
    len(sales_df)
    -
    uncategorized_count
)


quality1, quality2, quality3 = st.columns(3)


quality1.metric(
    "Unique Categories",
    f"{category_count:,}"
)


quality2.metric(
    "Categorized Records",
    f"{categorized_count:,}"
)


quality3.metric(
    "Uncategorized Records",
    f"{uncategorized_count:,}"
)


# ============================================================
# PROJECT OVERVIEW
# ============================================================

st.divider()


st.markdown(
    """
    <div class="section-header">
        Project Overview
    </div>
    """,
    unsafe_allow_html=True
)


st.write(
    """
    This Retail Executive Dashboard provides a professional
    overview of retail sales performance, customer transactions,
    demand trends, demand forecasting and inventory risk.

    The dashboard helps management understand sales patterns,
    channel performance, store performance, product performance,
    category performance and inventory risk so that better
    business decisions can be made.
    """
)


# ============================================================
# DATA SOURCE STATUS
# ============================================================

st.divider()


st.markdown(
    """
    <div class="section-header">
        Data Sources
    </div>
    """,
    unsafe_allow_html=True
)


dataset_status = []


datasets = {

    "Sales Transactions":
        (
            sales_df,
            sales_path
        ),

    "SKU Master":
        (
            sku_master_df,
            sku_master_path
        ),

    "Daily Demand Features":
        (
            demand_df,
            demand_path
        ),

    "Demand Forecast Results":
        (
            forecast_df,
            forecast_path
        ),

    "Inventory Risk Scoring":
        (
            inventory_df,
            inventory_path
        )
}


for dataset_name, (
    dataframe,
    filepath
) in datasets.items():

    if dataframe is not None:

        dataset_status.append(
            {
                "Dataset":
                    dataset_name,

                "Status":
                    "Available",

                "Records":
                    len(dataframe),

                "Columns":
                    len(dataframe.columns),

                "File":
                    filepath
            }
        )

    else:

        dataset_status.append(
            {
                "Dataset":
                    dataset_name,

                "Status":
                    "Not Available",

                "Records":
                    0,

                "Columns":
                    0,

                "File":
                    "Not found"
            }
        )


status_df = pd.DataFrame(
    dataset_status
)


st.dataframe(

    status_df,

    use_container_width=True,

    hide_index=True
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