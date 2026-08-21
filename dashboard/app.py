# ============================================================
# RETAIL EXECUTIVE DASHBOARD
# Sales Performance • Demand Forecasting • Inventory Intelligence
# ============================================================

import os
import glob
import warnings

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

    /* Main page */
    .main {
        background-color: #f6f8fb;
    }

    /* Hide Streamlit default elements */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Dashboard header */
    .dashboard-header {
        background: linear-gradient(135deg, #183b63, #244f7c);
        padding: 28px 32px;
        border-radius: 10px;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.10);
    }

    .dashboard-title {
        color: white;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .dashboard-subtitle {
        color: #dbe8f5;
        font-size: 14px;
        font-weight: 400;
    }

    /* Section titles */
    .section-title {
        font-size: 17px;
        font-weight: 700;
        color: #183b63;
        margin-top: 18px;
        margin-bottom: 8px;
        border-bottom: 2px solid #dce5ef;
        padding-bottom: 7px;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        border: 1px solid #dce3eb;
        border-radius: 8px;
        padding: 15px 18px;
        min-height: 92px;
        box-shadow: 0 2px 7px rgba(0,0,0,0.04);
    }

    .kpi-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #183b63;
        font-size: 21px;
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Charts */
    .chart-container {
        background: white;
        border: 1px solid #dce3eb;
        border-radius: 8px;
        padding: 4px;
    }

    /* Info messages */
    .success-box {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 10px 14px;
        border-radius: 5px;
        color: #065f46;
        font-size: 13px;
    }

    .warning-box {
        background: #fff7ed;
        border-left: 4px solid #f97316;
        padding: 10px 14px;
        border-radius: 5px;
        color: #9a3412;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA DIRECTORY
# ============================================================

DATA_PATHS = [
    "data",
    "./data",
    "../data",
    "datasets",
    "./datasets",
    "../datasets"
]


def find_data_directory():
    """
    Automatically searches for the project data directory.
    """

    for path in DATA_PATHS:
        if os.path.exists(path) and os.path.isdir(path):
            return path

    return "."


DATA_DIR = find_data_directory()


# ============================================================
# FILE FINDER
# ============================================================

def find_csv(filename_candidates):
    """
    Finds a CSV file using several possible names.
    """

    all_files = []

    for directory in DATA_PATHS:
        if os.path.exists(directory):
            all_files.extend(
                glob.glob(os.path.join(directory, "*.csv"))
            )

    # Also check current directory
    all_files.extend(glob.glob("*.csv"))

    # Exact candidate matching
    for candidate in filename_candidates:

        candidate_lower = candidate.lower()

        for file in all_files:

            if os.path.basename(file).lower() == candidate_lower:
                return file

    # Partial matching
    for candidate in filename_candidates:

        candidate_lower = candidate.lower().replace(".csv", "")

        for file in all_files:

            filename = os.path.basename(file).lower()

            if candidate_lower in filename:
                return file

    return None


# ============================================================
# COLUMN DETECTION
# ============================================================

def normalize_column_name(column):
    """
    Converts column names into a consistent format.
    """

    return (
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
    )


def find_column(df, possible_names):
    """
    Finds a column using multiple possible names.
    """

    if df is None or df.empty:
        return None

    normalized = {
        normalize_column_name(col): col
        for col in df.columns
    }

    for name in possible_names:

        name_normalized = normalize_column_name(name)

        if name_normalized in normalized:
            return normalized[name_normalized]

    # Partial matching
    for name in possible_names:

        name_normalized = normalize_column_name(name)

        for normalized_col, original_col in normalized.items():

            if (
                name_normalized in normalized_col
                or normalized_col in name_normalized
            ):
                return original_col

    return None


# ============================================================
# DATA LOADERS
# ============================================================

@st.cache_data(show_spinner=False)
def load_csv_file(file_path):

    try:

        return pd.read_csv(
            file_path,
            low_memory=False
        )

    except Exception as e:

        st.error(f"Unable to load {file_path}: {e}")

        return pd.DataFrame()


# ============================================================
# LOAD SALES DATA
# ============================================================

@st.cache_data(show_spinner=True)
def load_sales_data():

    sales_file = find_csv([
        "sales_transactions_cleaned.csv",
        "sales_transactions.csv",
        "sales_daily.csv",
        "sales.csv"
    ])

    if sales_file is None:
        return pd.DataFrame(), None

    df = load_csv_file(sales_file)

    return df, sales_file


# ============================================================
# LOAD SKU MASTER
# ============================================================

@st.cache_data(show_spinner=True)
def load_sku_data():

    sku_file = find_csv([
        "sku_master.csv",
        "SKU_Master.csv",
        "products.csv",
        "product_master.csv"
    ])

    if sku_file is None:
        return pd.DataFrame(), None

    df = load_csv_file(sku_file)

    return df, sku_file


# ============================================================
# LOAD INVENTORY DATA
# ============================================================

@st.cache_data(show_spinner=True)
def load_inventory_data():

    inventory_file = find_csv([
        "inventory_snapshots.csv",
        "inventory.csv",
        "inventory_data.csv"
    ])

    if inventory_file is None:
        return pd.DataFrame(), None

    df = load_csv_file(inventory_file)

    return df, inventory_file


# ============================================================
# LOAD CALENDAR
# ============================================================

@st.cache_data(show_spinner=True)
def load_calendar_data():

    calendar_file = find_csv([
        "calender.csv",
        "calendar.csv",
        "date_calendar.csv"
    ])

    if calendar_file is None:
        return pd.DataFrame(), None

    df = load_csv_file(calendar_file)

    return df, calendar_file


# ============================================================
# LOAD ALL DATA
# ============================================================

sales_df, sales_file = load_sales_data()
sku_df, sku_file = load_sku_data()
inventory_df, inventory_file = load_inventory_data()
calendar_df, calendar_file = load_calendar_data()


# ============================================================
# CHECK SALES DATA
# ============================================================

if sales_df.empty:

    st.error(
        "Sales data could not be loaded. "
        "Please make sure sales_transactions_cleaned.csv "
        "exists inside your data folder."
    )

    st.stop()


# ============================================================
# STANDARD COLUMN IDENTIFICATION
# ============================================================

DATE_COL = find_column(
    sales_df,
    [
        "date",
        "sales_date",
        "transaction_date",
        "order_date",
        "datetime",
        "timestamp"
    ]
)

SALES_COL = find_column(
    sales_df,
    [
        "sales",
        "sales_amount",
        "revenue",
        "total_sales",
        "amount",
        "total_amount",
        "net_sales"
    ]
)

QTY_COL = find_column(
    sales_df,
    [
        "quantity",
        "qty",
        "units",
        "units_sold",
        "sales_quantity"
    ]
)

SKU_COL = find_column(
    sales_df,
    [
        "sku",
        "sku_id",
        "product_id",
        "product_code",
        "item_id",
        "item_code"
    ]
)

STORE_COL = find_column(
    sales_df,
    [
        "store",
        "store_id",
        "store_code",
        "branch",
        "location",
        "shop"
    ]
)

CHANNEL_COL = find_column(
    sales_df,
    [
        "channel",
        "sales_channel",
        "order_channel",
        "distribution_channel"
    ]
)

CATEGORY_COL = find_column(
    sales_df,
    [
        "category",
        "product_category",
        "category_name",
        "department",
        "product_group"
    ]
)


# ============================================================
# CONVERT DATE
# ============================================================

if DATE_COL is not None:

    sales_df[DATE_COL] = pd.to_datetime(
        sales_df[DATE_COL],
        errors="coerce"
    )

    sales_df = sales_df.dropna(
        subset=[DATE_COL]
    )


# ============================================================
# CONVERT NUMERIC COLUMNS
# ============================================================

if SALES_COL is not None:

    sales_df[SALES_COL] = pd.to_numeric(
        sales_df[SALES_COL],
        errors="coerce"
    ).fillna(0)


if QTY_COL is not None:

    sales_df[QTY_COL] = pd.to_numeric(
        sales_df[QTY_COL],
        errors="coerce"
    ).fillna(0)


# ============================================================
# IMPORTANT FIX:
# ADD CATEGORY FROM SKU MASTER
# ============================================================

def add_category_from_sku_master(
    sales,
    sku_master
):

    global CATEGORY_COL

    # If category already exists, use it
    existing_category = find_column(
        sales,
        [
            "category",
            "product_category",
            "category_name",
            "department",
            "product_group"
        ]
    )

    if existing_category is not None:

        CATEGORY_COL = existing_category

        return sales

    # If SKU master does not exist, return unchanged
    if sku_master is None or sku_master.empty:

        return sales

    # Find SKU columns
    sales_sku = find_column(
        sales,
        [
            "sku",
            "sku_id",
            "product_id",
            "product_code",
            "item_id",
            "item_code"
        ]
    )

    master_sku = find_column(
        sku_master,
        [
            "sku",
            "sku_id",
            "product_id",
            "product_code",
            "item_id",
            "item_code"
        ]
    )

    # Find category in SKU master
    master_category = find_column(
        sku_master,
        [
            "category",
            "product_category",
            "category_name",
            "department",
            "product_group"
        ]
    )

    if (
        sales_sku is None
        or master_sku is None
        or master_category is None
    ):

        return sales

    # Create small lookup table
    category_lookup = sku_master[
        [master_sku, master_category]
    ].copy()

    category_lookup = category_lookup.drop_duplicates(
        subset=[master_sku]
    )

    # Rename to common names
    category_lookup = category_lookup.rename(
        columns={
            master_sku: "__MERGE_SKU__",
            master_category: "Category"
        }
    )

    # Avoid dtype mismatch
    sales = sales.copy()

    sales[sales_sku] = sales[sales_sku].astype(str)
    category_lookup["__MERGE_SKU__"] = (
        category_lookup["__MERGE_SKU__"]
        .astype(str)
    )

    # Merge
    sales = sales.merge(
        category_lookup,
        left_on=sales_sku,
        right_on="__MERGE_SKU__",
        how="left"
    )

    # Remove helper column
    if "__MERGE_SKU__" in sales.columns:

        sales.drop(
            columns=["__MERGE_SKU__"],
            inplace=True
        )

    # Fill missing category
    sales["Category"] = (
        sales["Category"]
        .fillna("Unknown")
        .astype(str)
    )

    CATEGORY_COL = "Category"

    return sales


# APPLY THE FIX
sales_df = add_category_from_sku_master(
    sales_df,
    sku_df
)


# ============================================================
# FALLBACK CATEGORY
# ============================================================

if CATEGORY_COL is None:

    # Do NOT break the dashboard
    sales_df["Category"] = "Unknown"

    CATEGORY_COL = "Category"


# ============================================================
# CREATE STANDARD DATE FIELDS
# ============================================================

if DATE_COL is not None:

    sales_df["__Date__"] = sales_df[DATE_COL].dt.date

    sales_df["__Month__"] = (
        sales_df[DATE_COL]
        .dt.to_period("M")
        .astype(str)
    )

    sales_df["__Year__"] = (
        sales_df[DATE_COL]
        .dt.year
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <h2 style="color:#183b63;margin-bottom:3px;">
        Dashboard Filters
    </h2>
    <p style="color:#64748b;font-size:12px;">
        Use the filters below to analyze retail performance.
    </p>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATE FILTER
# ============================================================

filtered_df = sales_df.copy()

if DATE_COL is not None and not sales_df.empty:

    min_date = sales_df[DATE_COL].min().date()
    max_date = sales_df[DATE_COL].max().date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:

        start_date, end_date = date_range

        filtered_df = filtered_df[
            (
                filtered_df[DATE_COL].dt.date >= start_date
            )
            &
            (
                filtered_df[DATE_COL].dt.date <= end_date
            )
        ]


# ============================================================
# STORE FILTER
# ============================================================

if STORE_COL is not None:

    stores = sorted(
        filtered_df[STORE_COL]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_stores = st.sidebar.multiselect(
        "Store",
        stores,
        default=[]
    )

    if selected_stores:

        filtered_df = filtered_df[
            filtered_df[STORE_COL]
            .astype(str)
            .isin(selected_stores)
        ]


# ============================================================
# CHANNEL FILTER
# ============================================================

if CHANNEL_COL is not None:

    channels = sorted(
        filtered_df[CHANNEL_COL]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_channels = st.sidebar.multiselect(
        "Sales Channel",
        channels,
        default=[]
    )

    if selected_channels:

        filtered_df = filtered_df[
            filtered_df[CHANNEL_COL]
            .astype(str)
            .isin(selected_channels)
        ]


# ============================================================
# CATEGORY FILTER
# ============================================================

if CATEGORY_COL is not None:

    categories = sorted(
        filtered_df[CATEGORY_COL]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "Category",
        categories,
        default=[]
    )

    if selected_categories:

        filtered_df = filtered_df[
            filtered_df[CATEGORY_COL]
            .astype(str)
            .isin(selected_categories)
        ]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">

        <div class="dashboard-title">
            Retail Executive Dashboard
        </div>

        <div class="dashboard-subtitle">
            Sales Performance • Demand Forecasting • Inventory Intelligence
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SECTION TITLE
# ============================================================

st.markdown(
    '<div class="section-title">Executive Summary</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

if SALES_COL is not None:

    total_sales = filtered_df[SALES_COL].sum()

else:

    total_sales = 0


if QTY_COL is not None:

    total_quantity = filtered_df[QTY_COL].sum()

else:

    total_quantity = 0


transactions = len(filtered_df)


if STORE_COL is not None:

    total_stores = filtered_df[STORE_COL].nunique()

else:

    total_stores = 0


if SKU_COL is not None:

    total_products = filtered_df[SKU_COL].nunique()

else:

    total_products = 0


if total_quantity != 0:

    avg_order_value = total_sales / transactions if transactions else 0

else:

    avg_order_value = 0


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)


with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Sales</div>
            <div class="kpi-value">₹{total_sales:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Transactions</div>
            <div class="kpi-value">{transactions:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Quantity Sold</div>
            <div class="kpi-value">{total_quantity:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Stores</div>
            <div class="kpi-value">{total_stores:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Products</div>
            <div class="kpi-value">{total_products:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi6:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Order Value</div>
            <div class="kpi-value">₹{avg_order_value:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SALES TREND
# ============================================================

st.markdown(
    '<div class="section-title">Sales Trend</div>',
    unsafe_allow_html=True
)

trend_col, channel_col = st.columns([2.1, 1])


# ============================================================
# DAILY SALES TREND
# ============================================================

with trend_col:

    if DATE_COL is not None and SALES_COL is not None:

        daily_sales = (
            filtered_df
            .groupby(DATE_COL)[SALES_COL]
            .sum()
            .reset_index()
        )

        daily_sales = daily_sales.sort_values(DATE_COL)

        fig = px.line(
            daily_sales,
            x=DATE_COL,
            y=SALES_COL,
            title="Daily Sales Trend"
        )

        fig.update_traces(
            line=dict(width=2)
        )

        fig.update_layout(
            height=360,
            margin=dict(
                l=30,
                r=20,
                t=50,
                b=30
            ),
            xaxis_title="Date",
            yaxis_title="Sales (₹)",
            hovermode="x unified",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Date or sales column is not available."
        )


# ============================================================
# SALES BY CHANNEL
# ============================================================

with channel_col:

    if CHANNEL_COL is not None and SALES_COL is not None:

        channel_sales = (
            filtered_df
            .groupby(CHANNEL_COL)[SALES_COL]
            .sum()
            .reset_index()
        )

        channel_sales = channel_sales.sort_values(
            SALES_COL,
            ascending=False
        )

        fig_channel = px.pie(
            channel_sales,
            names=CHANNEL_COL,
            values=SALES_COL,
            hole=0.55,
            title="Sales Distribution by Channel"
        )

        fig_channel.update_layout(
            height=360,
            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            ),
            legend_title="Channel",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig_channel,
            use_container_width=True
        )

    else:

        st.info(
            "Sales channel data is not available."
        )


# ============================================================
# SALES BY CATEGORY
# ============================================================

st.markdown(
    '<div class="section-title">Sales by Category</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# THIS IS THE IMPORTANT FIX
# ------------------------------------------------------------

if (
    CATEGORY_COL is not None
    and CATEGORY_COL in filtered_df.columns
    and SALES_COL is not None
):

    category_sales = (
        filtered_df
        .groupby(CATEGORY_COL)[SALES_COL]
        .sum()
        .reset_index()
    )

    category_sales = category_sales.sort_values(
        SALES_COL,
        ascending=False
    )

    category_sales = category_sales[
        category_sales[SALES_COL] > 0
    ]

    if not category_sales.empty:

        fig_category = px.bar(
            category_sales,
            x=CATEGORY_COL,
            y=SALES_COL,
            title="Sales Performance by Category",
            text_auto=".2s"
        )

        fig_category.update_layout(
            height=380,
            margin=dict(
                l=30,
                r=30,
                t=55,
                b=70
            ),
            xaxis_title="Category",
            yaxis_title="Sales (₹)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            hovermode="x unified"
        )

        fig_category.update_traces(
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Sales: ₹%{y:,.0f}"
                "<extra></extra>"
            )
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    else:

        st.info(
            "No category sales available for the selected filters."
        )

else:

    st.warning(
        "Category information could not be connected. "
        "The dashboard could not find a category field in the sales "
        "data or SKU master."
    )


# ============================================================
# STORE-WISE SALES
# ============================================================

st.markdown(
    '<div class="section-title">Store-wise Sales</div>',
    unsafe_allow_html=True
)


if (
    STORE_COL is not None
    and SALES_COL is not None
):

    store_sales = (
        filtered_df
        .groupby(STORE_COL)[SALES_COL]
        .sum()
        .reset_index()
        .sort_values(
            SALES_COL,
            ascending=False
        )
    )

    # Top 15 stores
    top_stores = store_sales.head(15)

    fig_store = px.bar(
        top_stores,
        x=STORE_COL,
        y=SALES_COL,
        title="Top 15 Stores by Sales",
        text_auto=".2s"
    )

    fig_store.update_layout(
        height=390,
        margin=dict(
            l=30,
            r=30,
            t=55,
            b=70
        ),
        xaxis_title="Store",
        yaxis_title="Sales (₹)",
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    fig_store.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Sales: ₹%{y:,.0f}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(
        fig_store,
        use_container_width=True
    )

else:

    st.info(
        "Store information is not available."
    )


# ============================================================
# CATEGORY + CHANNEL ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Category & Channel Analysis</div>',
    unsafe_allow_html=True
)

analysis_left, analysis_right = st.columns(2)


# ============================================================
# CATEGORY SALES TABLE
# ============================================================

with analysis_left:

    if (
        CATEGORY_COL is not None
        and CATEGORY_COL in filtered_df.columns
        and SALES_COL is not None
    ):

        category_table = (
            filtered_df
            .groupby(CATEGORY_COL)
            .agg(
                Sales=(SALES_COL, "sum")
            )
            .reset_index()
        )

        if QTY_COL is not None:

            quantity_table = (
                filtered_df
                .groupby(CATEGORY_COL)[QTY_COL]
                .sum()
                .reset_index()
            )

            category_table = category_table.merge(
                quantity_table,
                on=CATEGORY_COL,
                how="left"
            )

            category_table = category_table.rename(
                columns={
                    QTY_COL: "Quantity"
                }
            )

        category_table = category_table.sort_values(
            "Sales",
            ascending=False
        )

        st.markdown("#### Category Performance")

        st.dataframe(
            category_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Sales": st.column_config.NumberColumn(
                    "Sales",
                    format="₹%.0f"
                ),
                "Quantity": st.column_config.NumberColumn(
                    "Quantity",
                    format="%d"
                )
            }
        )


# ============================================================
# CHANNEL TABLE
# ============================================================

with analysis_right:

    if (
        CHANNEL_COL is not None
        and SALES_COL is not None
    ):

        channel_table = (
            filtered_df
            .groupby(CHANNEL_COL)
            .agg(
                Sales=(SALES_COL, "sum"),
                Transactions=(SALES_COL, "count")
            )
            .reset_index()
            .sort_values(
                "Sales",
                ascending=False
            )
        )

        st.markdown("#### Channel Performance")

        st.dataframe(
            channel_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Sales": st.column_config.NumberColumn(
                    "Sales",
                    format="₹%.0f"
                ),
                "Transactions": st.column_config.NumberColumn(
                    "Transactions",
                    format="%d"
                )
            }
        )


# ============================================================
# DATA QUALITY / CONNECTION STATUS
# ============================================================

st.markdown(
    '<div class="section-title">Data Connection Status</div>',
    unsafe_allow_html=True
)

status1, status2, status3, status4 = st.columns(4)


with status1:

    if sales_file:

        st.success(
            f"✓ Sales data connected"
        )

    else:

        st.error(
            "✕ Sales data missing"
        )


with status2:

    if sku_file:

        st.success(
            "✓ SKU master connected"
        )

    else:

        st.warning(
            "SKU master not found"
        )


with status3:

    if inventory_file:

        st.success(
            "✓ Inventory connected"
        )

    else:

        st.warning(
            "Inventory not found"
        )


with status4:

    if CATEGORY_COL is not None:

        st.success(
            f"✓ Category: {CATEGORY_COL}"
        )

    else:

        st.warning(
            "Category unavailable"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        margin-top:35px;
        padding:15px;
        text-align:center;
        color:#64748b;
        font-size:11px;
        border-top:1px solid #dce3eb;
    ">
        Retail Executive Dashboard • Sales Performance •
        Demand Forecasting • Inventory Intelligence
    </div>
    """,
    unsafe_allow_html=True
)