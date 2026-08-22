# ============================================================
# RETAIL EXECUTIVE DASHBOARD - HOME PAGE
# Sales Performance • Demand Forecasting • Inventory Intelligence
# ============================================================

import os
import streamlit as st
import pandas as pd
import plotly.express as px


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
# MULTI-PAGE NAVIGATION
# ============================================================

sales_page = st.Page(
    "pages/1_Sales_Analytics.py",
    title="Sales Analytics",
    icon="📊"
)

forecast_page = st.Page(
    "pages/2_Forecast.py",
    title="Forecast",
    icon="🔮"
)

inventory_page = st.Page(
    "pages/3_Inventory.py",
    title="Inventory",
    icon="📦"
)

risk_page = st.Page(
    "pages/4_Risk.py",
    title="Risk",
    icon="⚠️"
)

product_page = st.Page(
    "pages/5_Product_Details.py",
    title="Product Details",
    icon="🛍️"
)

executive_page = st.Page(
    "pages/6_Executive_Summary.py",
    title="Executive Summary",
    icon="📈"
)

pg = st.navigation([
    sales_page,
    forecast_page,
    inventory_page,
    risk_page,
    product_page,
    executive_page
])


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

    .dashboard-header {
        background: linear-gradient(
            135deg,
            #0F2747 0%,
            #183B63 100%
        );

        padding: 30px 34px;

        border-radius: 14px;

        margin-bottom: 28px;

        box-shadow:
            0 6px 18px
            rgba(15, 39, 71, 0.12);
    }

    .dashboard-title {
        color: #FFFFFF;

        font-size: 32px;

        font-weight: 700;

        margin: 0;

        letter-spacing: -0.5px;
    }

    .dashboard-subtitle {
        color: #DCE8F5;

        font-size: 15px;

        margin-top: 8px;

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


    /* ========================================================
       SIDEBAR FILTER BOX
       ======================================================== */

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
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px;
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
       HIDE STREAMLIT DEFAULT ELEMENTS
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 900px) {

        .dashboard-title {
            font-size: 26px;
        }

        .dashboard-header {
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
# DATA LOADING FUNCTIONS
# ============================================================

@st.cache_data
def load_sales_data():

    path = os.path.join(
        PROCESSED_PATH,
        "sales_transactions_cleaned.csv"
    )

    if not os.path.exists(path):
        return None

    return pd.read_csv(path)


@st.cache_data
def load_demand_data():

    path = os.path.join(
        PROCESSED_PATH,
        "daily_demand_features.csv"
    )

    if not os.path.exists(path):
        return None

    return pd.read_csv(path)


@st.cache_data
def load_forecast_data():

    path = os.path.join(
        PROCESSED_PATH,
        "demand_forecast_results.csv"
    )

    if not os.path.exists(path):
        return None

    return pd.read_csv(path)


@st.cache_data
def load_inventory_risk():

    path = os.path.join(
        PROCESSED_PATH,
        "inventory_risk_scoring.csv"
    )

    if not os.path.exists(path):
        return None

    return pd.read_csv(path)


# ============================================================
# LOAD SKU MASTER
# ============================================================

@st.cache_data
def load_sku_master():

    candidate_paths = [

        os.path.join(
            PROCESSED_PATH,
            "sku_master.csv"
        ),

        os.path.join(
            BASE_DIR,
            "data",
            "raw",
            "sku_master.csv"
        ),

        os.path.join(
            BASE_DIR,
            "data1",
            "processed",
            "sku_master.csv"
        ),

        os.path.join(
            BASE_DIR,
            "data1",
            "raw",
            "sku_master.csv"
        )
    ]


    for root, dirs, files in os.walk(BASE_DIR):

        if "sku_master.csv" in files:

            candidate_paths.append(
                os.path.join(
                    root,
                    "sku_master.csv"
                )
            )


    checked_paths = []

    for path in candidate_paths:

        if path not in checked_paths:

            checked_paths.append(path)

            if os.path.isfile(path):

                return pd.read_csv(path)


    return None


# ============================================================
# LOAD DATA
# ============================================================

sales_df = load_sales_data()

demand_df = load_demand_data()

forecast_df = load_forecast_data()

inventory_df = load_inventory_risk()

sku_master_df = load_sku_master()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(df, possible_names):

    if df is None:
        return None

    normalized = {
        str(col).strip().lower().replace(" ", "_"): col
        for col in df.columns
    }

    for name in possible_names:

        key = (
            name
            .strip()
            .lower()
            .replace(" ", "_")
        )

        if key in normalized:

            return normalized[key]

    return None


def normalize_sku(value):

    if pd.isna(value):
        return None

    value = str(value).strip().upper()

    if value.endswith(".0"):

        value = value[:-2]

    if value.startswith("SKU"):

        digits = value[3:]

        if digits.isdigit():

            return "SKU" + digits.zfill(5)

    if value.isdigit():

        return "SKU" + value.zfill(5)

    return value


# ============================================================
# BUILD CATEGORY MAPPING
# ============================================================

if sales_df is not None:

    sales_sku_col = find_column(
        sales_df,
        [
            "sku_id",
            "sku",
            "product_id",
            "product_code"
        ]
    )

    master_sku_col = find_column(
        sku_master_df,
        [
            "sku_id",
            "sku",
            "product_id",
            "product_code"
        ]
    )

    category_col = find_column(
        sku_master_df,
        [
            "category",
            "product_category",
            "category_name"
        ]
    )


    sales_df.drop(
        columns=["category"],
        inplace=True,
        errors="ignore"
    )


    if (
        sku_master_df is not None
        and sales_sku_col is not None
        and master_sku_col is not None
        and category_col is not None
    ):

        sales_keys = sales_df[
            sales_sku_col
        ].map(normalize_sku)

        master_keys = sku_master_df[
            master_sku_col
        ].map(normalize_sku)


        sku_category_lookup = pd.DataFrame(
            {
                "_sku_key": master_keys,

                "_category_value":
                    sku_master_df[category_col]
            }
        )


        sku_category_lookup[
            "_category_value"
        ] = (

            sku_category_lookup[
                "_category_value"
            ]
            .astype("string")
            .str.strip()
        )


        sku_category_lookup = (

            sku_category_lookup[
                sku_category_lookup[
                    "_sku_key"
                ].notna()
            ]

            .dropna(
                subset=[
                    "_category_value"
                ]
            )

            .drop_duplicates(
                subset="_sku_key",
                keep="first"
            )
        )


        category_lookup = dict(
            zip(
                sku_category_lookup[
                    "_sku_key"
                ],

                sku_category_lookup[
                    "_category_value"
                ]
            )
        )


        sales_df["category"] = (

            sales_keys

            .map(category_lookup)

            .fillna("Uncategorized")

            .astype(str)

            .str.strip()
        )


        sales_df.loc[
            sales_df["category"].eq("")
            | sales_df["category"].eq("nan"),
            "category"
        ] = "Uncategorized"


    else:

        sales_df[
            "category"
        ] = "Uncategorized"


# ============================================================
# VALIDATE MAIN DATA
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
# DATE CONVERSION
# ============================================================

if "date" in sales_df.columns:

    sales_df["date"] = pd.to_datetime(
        sales_df["date"],
        errors="coerce"
    )


if demand_df is not None:

    if "date" in demand_df.columns:

        demand_df["date"] = pd.to_datetime(
            demand_df["date"],
            errors="coerce"
        )


if forecast_df is not None:

    if "date" in forecast_df.columns:

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
# DATA TYPE CLEANING
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

        linecolor="#D5DDE6",

        fixedrange=False
    )


    fig.update_yaxes(

        showgrid=True,

        gridcolor="#E8EDF3",

        zeroline=False,

        linecolor="#D5DDE6",

        fixedrange=False
    )


    return fig


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 6px;
    }

    .main-subtitle {
        font-size: 15px;
        color: #DCE8F5;
    }

    .header-box {
        background: linear-gradient(
            135deg,
            #0F2747,
            #183B63
        );

        padding: 28px 32px;

        border-radius: 14px;

        margin-bottom: 28px;

        box-shadow:
            0 6px 18px
            rgba(15,39,71,0.12);
    }

    </style>
    """,
    unsafe_allow_html=True
)


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
    <div class="sidebar-title">
        Dashboard Filters
    </div>

    <div class="sidebar-caption">
        Filter the executive overview
        using the options below.
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
# APPLY FILTERS
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

if "total_value" in filtered_sales.columns:

    total_sales = (
        filtered_sales["total_value"]
        .sum()
    )

else:

    total_sales = 0


if "receipt_id" in filtered_sales.columns:

    total_transactions = (
        filtered_sales["receipt_id"]
        .nunique()
    )

else:

    total_transactions = len(
        filtered_sales
    )


if "quantity" in filtered_sales.columns:

    total_quantity = (
        filtered_sales["quantity"]
        .sum()
    )

else:

    total_quantity = 0


if "store_id" in filtered_sales.columns:

    total_stores = (
        filtered_sales["store_id"]
        .nunique()
    )

else:

    total_stores = 0


if "sku_id" in filtered_sales.columns:

    total_products = (
        filtered_sales["sku_id"]
        .nunique()
    )

else:

    total_products = 0


average_order_value = (

    total_sales
    /
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
# SALES OVERVIEW
# ============================================================

st.divider()


left, right = st.columns(
    [2, 1]
)


# ============================================================
# SALES TREND
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

            title="Daily Sales Trend",

            markers=False
        )


        fig_sales.update_traces(

            line_width=2,

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

            key="home_daily_sales_chart"
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

            title="Sales Distribution by Channel"
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

            key="home_channel_chart"
        )


# ============================================================
# CATEGORY OVERVIEW
# ============================================================

st.divider()


st.markdown(
    """
    <div class="section-header">
        Category Overview
    </div>
    """,
    unsafe_allow_html=True
)


if (
    "category" in filtered_sales.columns
    and "total_value" in filtered_sales.columns
):

    category_chart_data = (

        filtered_sales

        .groupby("category")

        .agg(
            Sales=("total_value", "sum")
        )

        .reset_index()

        .sort_values(
            "Sales",
            ascending=False
        )
    )


    category_left, category_right = st.columns(
        [2, 1]
    )


    # ========================================================
    # CATEGORY SALES BAR CHART
    # ========================================================

    with category_left:

        fig_category_sales = px.bar(

            category_chart_data,

            x="category",

            y="Sales",

            title="Sales by Category",

            text="Sales"
        )


        fig_category_sales.update_traces(

            texttemplate="₹%{y:,.0f}",

            textposition="outside",

            hovertemplate=
            "<b>%{x}</b>"
            "<br>Sales: ₹%{y:,.0f}"
            "<extra></extra>"
        )


        fig_category_sales.update_layout(

            xaxis_title="Category",

            yaxis_title="Sales (₹)",

            xaxis_tickangle=-30,

            uniformtext_minsize=8,

            uniformtext_mode="hide"
        )


        style_chart(
            fig_category_sales,
            height=430
        )


        st.plotly_chart(

            fig_category_sales,

            use_container_width=True,

            key="home_category_sales_chart"
        )


    # ========================================================
    # CATEGORY DISTRIBUTION
    # ========================================================

    with category_right:

        fig_category_pie = px.pie(

            category_chart_data,

            names="category",

            values="Sales",

            hole=0.50,

            title="Category Sales Distribution"
        )


        fig_category_pie.update_traces(

            textposition="inside",

            textinfo="percent",

            hovertemplate=
            "<b>%{label}</b>"
            "<br>Sales: ₹%{value:,.0f}"
            "<br>Share: %{percent}"
            "<extra></extra>"
        )


        style_chart(
            fig_category_pie,
            height=430
        )


        st.plotly_chart(

            fig_category_pie,

            use_container_width=True,

            key="home_category_distribution_chart"
        )


else:

    st.info(
        "Category information is not available."
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
    overview of retail sales performance, demand forecasting
    and inventory intelligence.

    Use the navigation menu to explore detailed sales analytics,
    demand forecasting, inventory performance, risk analysis,
    product details and executive-level insights.
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