# ============================================================
# RETAIL EXECUTIVE DASHBOARD
# Sales Performance • Demand Forecasting • Inventory Intelligence
# ============================================================

import os
import pandas as pd
import streamlit as st
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
            #102A43 0%,
            #1F4E79 100%
        );

        padding: 30px 34px;

        border-radius: 14px;

        margin-bottom: 26px;

        box-shadow:
            0 6px 18px
            rgba(15, 39, 71, 0.12);
    }

    .dashboard-title {
        color: white;

        font-size: 32px;

        font-weight: 700;

        margin: 0 0 7px 0;

        letter-spacing: -0.4px;
    }

    .dashboard-subtitle {
        color: #DCE8F5;

        font-size: 15px;

        margin: 0;
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

        padding-bottom: 8px;

        border-bottom:
            2px solid #DCE3EB;
    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    div[data-testid="stMetric"] {

        background: white;

        border:
            1px solid #E2E8F0;

        border-radius: 12px;

        padding: 16px 18px;

        box-shadow:
            0 3px 10px
            rgba(15, 39, 71, 0.05);
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

        margin-bottom: 4px;
    }

    .sidebar-caption {

        color: #64748B;

        font-size: 13px;

        margin-bottom: 20px;
    }


    /* ========================================================
       CHART CONTAINERS
       ======================================================== */

    div[data-testid="stPlotlyChart"] {

        background: white;

        border:
            1px solid #E2E8F0;

        border-radius: 12px;

        padding: 8px;

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
       BUTTONS
       ======================================================== */

    .stButton > button {

        border-radius: 8px;

        border: 1px solid #CBD5E1;

        font-weight: 600;
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
       HIDE STREAMLIT CHROME
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
# HELPER FUNCTIONS
# ============================================================

def get_file_path(filename):

    return os.path.join(
        PROCESSED_PATH,
        filename
    )


def clean_column_names(df):

    df = df.copy()

    df.columns = [
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        for column in df.columns
    ]

    return df


def normalize_id(value):

    """
    Normalize IDs before joining datasets.

    Examples:

    SKU001 -> SKU001
    sku001 -> SKU001
    SKU001.0 -> SKU001
    ' SKU001 ' -> SKU001
    """

    if pd.isna(value):
        return ""

    value = str(value).strip().upper()

    if value.endswith(".0"):
        value = value[:-2]

    return value


def find_column(
    df,
    possible_names
):

    """
    Find a column using preferred names.
    """

    if df is None:
        return None

    columns = list(df.columns)

    # Exact match
    for name in possible_names:

        name = name.lower()

        if name in columns:
            return name

    # Partial match
    for column in columns:

        for name in possible_names:

            if name.lower() in column.lower():
                return column

    return None


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_csv(filename):

    path = get_file_path(filename)

    if not os.path.exists(path):

        return None

    try:

        df = pd.read_csv(path)

        df = clean_column_names(df)

        return df

    except Exception as error:

        st.error(
            f"Could not load {filename}: {error}"
        )

        return None


# ============================================================
# LOAD ALL REQUIRED DATASETS
# ============================================================

sales_df = load_csv(
    "sales_transactions_cleaned.csv"
)

sku_master_df = load_csv(
    "sku_master.csv"
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


# ============================================================
# CHECK MAIN SALES DATA
# ============================================================

if sales_df is None:

    st.error(
        "sales_transactions_cleaned.csv "
        "could not be found."
    )

    st.info(
        f"Expected location:\n{PROCESSED_PATH}"
    )

    st.stop()


# ============================================================
# SMART CATEGORY MAPPING
# ============================================================

def find_category_column(master):

    """
    Find the category column inside sku_master.csv.
    """

    preferred_names = [

        "category",

        "product_category",

        "product_category_name",

        "category_name",

        "department",

        "product_type",

        "segment",

        "class"
    ]

    # Exact match
    for column in master.columns:

        if column.lower() in preferred_names:

            return column


    # Partial match
    for column in master.columns:

        column_name = column.lower()

        if (
            "categor" in column_name
            or "department" in column_name
            or "product_type" in column_name
        ):

            return column


    return None


def find_sku_columns(
    sales,
    master
):

    """
    Find the best matching ID columns.

    First we try common SKU/product column names.

    If that fails, we compare actual values.
    """

    sales_candidates = [

        "sku_id",
        "sku",
        "sku_code",
        "product_id",
        "product_code",
        "item_id",
        "item_code",
        "product"
    ]

    master_candidates = [

        "sku_id",
        "sku",
        "sku_code",
        "product_id",
        "product_code",
        "item_id",
        "item_code",
        "product"
    ]


    # --------------------------------------------------------
    # STEP 1: Common column names
    # --------------------------------------------------------

    sales_sku = find_column(
        sales,
        sales_candidates
    )

    master_sku = find_column(
        master,
        master_candidates
    )


    if (
        sales_sku is not None
        and master_sku is not None
    ):

        sales_values = set(
            sales[sales_sku]
            .dropna()
            .map(normalize_id)
        )

        master_values = set(
            master[master_sku]
            .dropna()
            .map(normalize_id)
        )

        overlap = (
            sales_values
            .intersection(master_values)
        )

        if len(overlap) > 0:

            return (
                sales_sku,
                master_sku
            )


    # --------------------------------------------------------
    # STEP 2: Compare actual values
    # --------------------------------------------------------

    best_sales_column = None

    best_master_column = None

    best_percentage = 0


    for sales_column in sales.columns:

        sales_values = set(
            sales[sales_column]
            .dropna()
            .map(normalize_id)
        )

        sales_values = {
            value
            for value in sales_values
            if value != ""
        }


        if len(sales_values) < 2:

            continue


        for master_column in master.columns:

            master_values = set(
                master[master_column]
                .dropna()
                .map(normalize_id)
            )

            master_values = {
                value
                for value in master_values
                if value != ""
            }


            if len(master_values) < 2:

                continue


            overlap = (
                sales_values
                .intersection(master_values)
            )


            if len(overlap) == 0:

                continue


            percentage = (
                len(overlap)
                /
                len(sales_values)
                *
                100
            )


            if percentage > best_percentage:

                best_percentage = percentage

                best_sales_column = sales_column

                best_master_column = master_column


    if (
        best_sales_column is not None
        and best_master_column is not None
    ):

        return (
            best_sales_column,
            best_master_column
        )


    return (
        None,
        None
    )


def add_category_to_sales(
    sales,
    master
):

    """
    Add category to sales dataframe
    using sku_master.csv.
    """

    sales = sales.copy()


    # --------------------------------------------------------
    # Check SKU master
    # --------------------------------------------------------

    if master is None:

        st.warning(
            "sku_master.csv was not found. "
            "Sales by Category cannot be generated."
        )

        sales["category"] = "Uncategorized"

        return sales


    # --------------------------------------------------------
    # Find category column
    # --------------------------------------------------------

    category_column = find_category_column(
        master
    )


    if category_column is None:

        st.error(
            "Category column was not found "
            "inside sku_master.csv."
        )

        st.write(
            "Available sku_master columns:"
        )

        st.write(
            master.columns.tolist()
        )

        sales["category"] = "Uncategorized"

        return sales


    # --------------------------------------------------------
    # Find matching SKU columns
    # --------------------------------------------------------

    (
        sales_sku_column,
        master_sku_column
    ) = find_sku_columns(
        sales,
        master
    )


    if (
        sales_sku_column is None
        or master_sku_column is None
    ):

        st.error(
            "SKU values could not be matched "
            "between the sales and SKU master datasets."
        )

        st.write(
            "Sales columns:"
        )

        st.write(
            sales.columns.tolist()
        )

        st.write(
            "SKU master columns:"
        )

        st.write(
            master.columns.tolist()
        )

        sales["category"] = "Uncategorized"

        return sales


    # --------------------------------------------------------
    # Normalize keys
    # --------------------------------------------------------

    sales["_category_key"] = (
        sales[sales_sku_column]
        .map(normalize_id)
    )

    master = master.copy()

    master["_category_key"] = (
        master[master_sku_column]
        .map(normalize_id)
    )


    # --------------------------------------------------------
    # Create lookup table
    # --------------------------------------------------------

    lookup = master[
        [
            "_category_key",
            category_column
        ]
    ].copy()


    lookup = lookup[
        lookup["_category_key"] != ""
    ]


    lookup = lookup.drop_duplicates(
        subset=["_category_key"]
    )


    lookup = lookup.rename(
        columns={
            category_column:
            "_mapped_category"
        }
    )


    # --------------------------------------------------------
    # Remove old category
    # --------------------------------------------------------

    if "category" in sales.columns:

        sales = sales.drop(
            columns=["category"]
        )


    # --------------------------------------------------------
    # Merge category
    # --------------------------------------------------------

    sales = sales.merge(
        lookup,
        on="_category_key",
        how="left"
    )


    # --------------------------------------------------------
    # Create final category
    # --------------------------------------------------------

    sales["category"] = (
        sales["_mapped_category"]
        .fillna("Uncategorized")
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # Remove invalid category names
    # --------------------------------------------------------

    invalid_categories = [

        "",

        "nan",

        "NaN",

        "None",

        "none",

        "null",

        "NULL",

        "undefined",

        "Undefined"
    ]


    sales.loc[
        sales["category"].isin(
            invalid_categories
        ),
        "category"
    ] = "Uncategorized"


    # --------------------------------------------------------
    # Remove temporary columns
    # --------------------------------------------------------

    sales = sales.drop(
        columns=[
            "_category_key",
            "_mapped_category"
        ],
        errors="ignore"
    )


    # --------------------------------------------------------
    # Mapping statistics
    # --------------------------------------------------------

    matched = (
        sales["category"]
        != "Uncategorized"
    ).sum()


    total = len(sales)


    percentage = (
        matched / total * 100
        if total > 0
        else 0
    )


    # --------------------------------------------------------
    # Success message
    # --------------------------------------------------------

    if matched > 0:

        st.success(
            f"✓ Category mapping connected successfully: "
            f"{sales_sku_column} → "
            f"{master_sku_column} → "
            f"{category_column}"
        )

        st.caption(
            f"Matched {matched:,} of "
            f"{total:,} sales records "
            f"({percentage:.1f}%)."
        )


    else:

        st.warning(
            "SKU columns were found, but no "
            "matching SKU values were found."
        )


    return sales


# ============================================================
# CREATE CATEGORY
# ============================================================

sales_df = add_category_to_sales(
    sales_df,
    sku_master_df
)


# ============================================================
# DATE CONVERSION
# ============================================================

if "date" in sales_df.columns:

    sales_df["date"] = pd.to_datetime(
        sales_df["date"],
        errors="coerce"
    )


if (
    demand_df is not None
    and "date" in demand_df.columns
):

    demand_df["date"] = pd.to_datetime(
        demand_df["date"],
        errors="coerce"
    )


if (
    forecast_df is not None
    and "date" in forecast_df.columns
):

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
# CHART STYLE
# ============================================================

def style_chart(
    fig,
    title=None
):

    fig.update_layout(

        template="plotly_white",

        title=title,

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

        paper_bgcolor="white",

        plot_bgcolor="white",

        margin=dict(
            l=60,
            r=35,
            t=60,
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
        )
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
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        Dashboard Filters
    </div>

    <div class="sidebar-caption">
        Use the controls below to refine the analysis.
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
# APPLY FILTERS
# ============================================================

filtered_sales = sales_df.copy()


if (
    selected_years
    and "year" in filtered_sales.columns
):

    filtered_sales = filtered_sales[
        filtered_sales["year"].isin(
            selected_years
        )
    ]


if (
    selected_channels
    and "channel" in filtered_sales.columns
):

    filtered_sales = filtered_sales[
        filtered_sales["channel"].isin(
            selected_channels
        )
    ]


# ============================================================
# FILTER DEMAND
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
# FILTER FORECAST
# ============================================================

if forecast_df is not None:

    filtered_forecast = forecast_df.copy()

    if (
        selected_years
        and "date" in filtered_forecast.columns
    ):

        filtered_forecast = (
            filtered_forecast[
                filtered_forecast["date"]
                .dt.year
                .isin(selected_years)
            ]
        )

else:

    filtered_forecast = None


# ============================================================
# DATA VALIDATION
# ============================================================

if filtered_sales.empty:

    st.warning(
        "No sales records match the selected filters. "
        "Please select at least one year and channel."
    )

    st.stop()


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.markdown(
    '<div class="section-header">'
    'Executive Summary'
    '</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# KPI CALCULATIONS
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# KPI DISPLAY
# ------------------------------------------------------------

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
        '<div class="section-header">'
        'Sales Trend'
        '</div>',
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
        )


        fig_sales = px.line(

            daily_sales,

            x="date",

            y="total_value",

            title="Daily Sales Trend"
        )


        fig_sales.update_traces(
            line_width=2
        )


        fig_sales.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales (₹)",
            hovermode="x unified"
        )


        style_chart(
            fig_sales
        )


        st.plotly_chart(
            fig_sales,
            use_container_width=True
        )


# ============================================================
# SALES BY CHANNEL
# ============================================================

with right:

    st.markdown(
        '<div class="section-header">'
        'Sales by Channel'
        '</div>',
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

            hole=0.42,

            title="Sales Distribution by Channel"
        )


        fig_channel.update_traces(
            textposition="inside",
            textinfo="percent"
        )


        style_chart(
            fig_channel
        )


        st.plotly_chart(
            fig_channel,
            use_container_width=True
        )


# ============================================================
# SALES BY CATEGORY
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Sales by Category'
    '</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# VERIFY CATEGORY
# ------------------------------------------------------------

if "category" not in filtered_sales.columns:

    st.error(
        "Category could not be created."
    )

else:

    category_data = filtered_sales.copy()


    # --------------------------------------------------------
    # Clean category names
    # --------------------------------------------------------

    category_data["category"] = (
        category_data["category"]
        .fillna("Uncategorized")
        .astype(str)
        .str.strip()
    )


    invalid_categories = [

        "",

        "nan",

        "NaN",

        "None",

        "none",

        "null",

        "NULL",

        "undefined",

        "Undefined"
    ]


    category_data.loc[
        category_data["category"].isin(
            invalid_categories
        ),
        "category"
    ] = "Uncategorized"


    # --------------------------------------------------------
    # Calculate category sales
    # --------------------------------------------------------

    if "total_value" in category_data.columns:

        category_data["total_value"] = (
            pd.to_numeric(
                category_data["total_value"],
                errors="coerce"
            )
            .fillna(0)
        )


        category_sales = (

            category_data
            .groupby("category")["total_value"]
            .sum()
            .sort_values(
                ascending=True
            )
            .reset_index()
        )


        # ----------------------------------------------------
        # Remove Uncategorized ONLY when real categories exist
        # ----------------------------------------------------

        real_categories = (
            category_sales[
                category_sales["category"]
                != "Uncategorized"
            ]
        )


        if (
            len(real_categories) > 0
        ):

            category_sales = (
                real_categories
            )


        # ----------------------------------------------------
        # Chart
        # ----------------------------------------------------

        fig_category = px.bar(

            category_sales,

            x="total_value",

            y="category",

            orientation="h",

            title="Sales by Category",

            text="total_value"
        )


        fig_category.update_traces(

            texttemplate="₹%{x:,.0f}",

            textposition="outside",

            hovertemplate=
            "<b>%{y}</b><br>"
            "Sales: ₹%{x:,.0f}"
            "<extra></extra>"
        )


        fig_category.update_layout(

            xaxis_title="Sales (₹)",

            yaxis_title="Category",

            height=max(
                400,
                100 * len(category_sales)
            )
        )


        style_chart(
            fig_category
        )


        st.plotly_chart(
            fig_category,
            use_container_width=True
        )


        # ----------------------------------------------------
        # Category summary
        # ----------------------------------------------------

        if len(real_categories) > 0:

            st.caption(
                f"{len(real_categories)} product "
                f"categories successfully connected "
                f"from sku_master.csv."
            )

        else:

            st.warning(
                "No valid category values were found "
                "after matching SKU data."
            )


# ============================================================
# STORE-WISE SALES
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Store-wise Sales'
    '</div>',
    unsafe_allow_html=True
)


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

        title="Top Stores by Sales",

        text="total_value"
    )


    fig_store.update_traces(

        texttemplate="₹%{y:,.0f}",

        textposition="outside"
    )


    fig_store.update_layout(

        xaxis_title="Store",

        yaxis_title="Sales (₹)"
    )


    style_chart(
        fig_store
    )


    st.plotly_chart(
        fig_store,
        use_container_width=True
    )


# ============================================================
# DEMAND ANALYSIS
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Demand Analysis'
    '</div>',
    unsafe_allow_html=True
)


demand_left, demand_right = st.columns(
    2
)


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
        )


        fig_demand = px.line(

            daily_demand,

            x="date",

            y="demand",

            title="Daily Demand"
        )


        fig_demand.update_layout(

            xaxis_title="Date",

            yaxis_title="Demand"
        )


        style_chart(
            fig_demand
        )


        st.plotly_chart(
            fig_demand,
            use_container_width=True
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

            xaxis_title="Date",

            yaxis_title="Demand",

            legend_title="Series"
        )


        style_chart(
            fig_forecast
        )


        st.plotly_chart(
            fig_forecast,
            use_container_width=True
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
    '<div class="section-header">'
    'Year-wise Sales'
    '</div>',
    unsafe_allow_html=True
)


if (
    "year" in sales_df.columns
    and "total_value" in sales_df.columns
):

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

        title="Sales by Year",

        text="total_value"
    )


    fig_year.update_traces(

        texttemplate="₹%{y:,.0f}",

        textposition="outside"
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
        use_container_width=True
    )


# ============================================================
# INVENTORY RISK
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Inventory Risk'
    '</div>',
    unsafe_allow_html=True
)


if inventory_df is not None:

    # --------------------------------------------------------
    # Find risk column
    # --------------------------------------------------------

    risk_column = find_column(

        inventory_df,

        [
            "final_risk_level",
            "risk_level",
            "inventory_risk",
            "risk"
        ]
    )


    if risk_column is not None:

        inventory_df[risk_column] = (
            inventory_df[risk_column]
            .astype(str)
            .str.strip()
        )


        risk_counts = (
            inventory_df[risk_column]
            .value_counts()
        )


        # ----------------------------------------------------
        # Risk KPIs
        # ----------------------------------------------------

        critical_inventory = (
            inventory_df[risk_column]
            .str.lower()
            .eq("critical")
            .sum()
        )


        high_risk_inventory = (
            inventory_df[risk_column]
            .str.lower()
            .eq("high risk")
            .sum()
        )


        medium_risk_inventory = (
            inventory_df[risk_column]
            .str.lower()
            .eq("medium risk")
            .sum()
        )


        low_risk_inventory = (
            inventory_df[risk_column]
            .str.lower()
            .eq("low risk")
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


        # ----------------------------------------------------
        # Risk chart
        # ----------------------------------------------------

        risk_chart_data = (
            risk_counts
            .reset_index()
        )


        risk_chart_data.columns = [
            "risk_level",
            "product_count"
        ]


        fig_risk = px.bar(

            risk_chart_data,

            x="risk_level",

            y="product_count",

            title="Inventory Risk Distribution",

            text="product_count"
        )


        fig_risk.update_traces(

            textposition="outside"
        )


        fig_risk.update_layout(

            xaxis_title="Risk Level",

            yaxis_title="Number of Products"
        )


        style_chart(
            fig_risk
        )


        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )


    else:

        st.info(
            "Risk level column was not found "
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


st.markdown(
    '<div class="section-header">'
    'Top Products'
    '</div>',
    unsafe_allow_html=True
)


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


    fig_products = px.bar(

        top_products,

        x="total_value",

        y="sku_id",

        orientation="h",

        title="Top 10 Products by Sales",

        text="total_value"
    )


    fig_products.update_traces(

        texttemplate="₹%{x:,.0f}",

        textposition="outside"
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
        use_container_width=True
    )


# ============================================================
# CATEGORY TABLE
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Category Performance'
    '</div>',
    unsafe_allow_html=True
)


if (
    "category" in filtered_sales.columns
    and "total_value" in filtered_sales.columns
):

    category_summary = (

        filtered_sales
        .groupby("category")
        .agg(

            Sales=(
                "total_value",
                "sum"
            ),

            Quantity=(
                "quantity",
                "sum"
            )
            if "quantity" in filtered_sales.columns
            else (
                "total_value",
                "count"
            )
        )
        .reset_index()
    )


    category_summary = (
        category_summary
        .sort_values(
            "Sales",
            ascending=False
        )
    )


    category_summary["Sales"] = (
        category_summary["Sales"]
        .round(0)
    )


    st.dataframe(

        category_summary,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# PROJECT OVERVIEW
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Project Overview'
    '</div>',
    unsafe_allow_html=True
)


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
# DATASET CONNECTION STATUS
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Data Sources'
    '</div>',
    unsafe_allow_html=True
)


data_status = []


datasets = {

    "Sales Transactions":
        sales_df,

    "SKU Master":
        sku_master_df,

    "Daily Demand Features":
        demand_df,

    "Demand Forecast":
        forecast_df,

    "Inventory Risk":
        inventory_df
}


for name, dataframe in datasets.items():

    if dataframe is not None:

        data_status.append(
            {
                "Dataset": name,
                "Status": "Available",
                "Records": len(dataframe)
            }
        )

    else:

        data_status.append(
            {
                "Dataset": name,
                "Status": "Not Available",
                "Records": 0
            }
        )


status_df = pd.DataFrame(
    data_status
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