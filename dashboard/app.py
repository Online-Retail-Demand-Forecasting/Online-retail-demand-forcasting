# ============================================================
# RETAIL EXECUTIVE DASHBOARD
# ============================================================
# Sales Performance | Demand Forecasting | Inventory Risk
# ============================================================

import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Executive Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
<style>

/* ----------------------------------------------------------
   GLOBAL
---------------------------------------------------------- */

.stApp {
    background-color: #F5F7FA;
}

.main .block-container {
    max-width: 1500px;
    padding: 1.5rem 2.5rem 3rem 2.5rem;
}


/* ----------------------------------------------------------
   HEADER
---------------------------------------------------------- */

.dashboard-header {
    background: linear-gradient(
        135deg,
        #102A43 0%,
        #1F4E79 100%
    );

    padding: 30px 34px;

    border-radius: 14px;

    margin-bottom: 25px;

    box-shadow:
        0 6px 18px rgba(16, 42, 67, 0.12);
}

.dashboard-title {
    color: #FFFFFF;
    font-size: 32px;
    font-weight: 700;
    margin: 0;
}

.dashboard-subtitle {
    color: #D9E8F5;
    font-size: 15px;
    margin-top: 8px;
}


/* ----------------------------------------------------------
   SECTION HEADERS
---------------------------------------------------------- */

.section-header {
    color: #17324D;

    font-size: 21px;

    font-weight: 700;

    padding-bottom: 8px;

    margin-top: 8px;

    margin-bottom: 15px;

    border-bottom:
        2px solid #DCE3EB;
}


/* ----------------------------------------------------------
   METRIC CARDS
---------------------------------------------------------- */

div[data-testid="stMetric"] {
    background-color: #FFFFFF;

    border:
        1px solid #E2E8F0;

    border-radius: 12px;

    padding: 15px 17px;

    box-shadow:
        0 3px 10px rgba(15, 39, 71, 0.05);
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


/* ----------------------------------------------------------
   SIDEBAR
---------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background-color: #FFFFFF;

    border-right:
        1px solid #E2E8F0;
}

.sidebar-title {
    color: #17324D;

    font-size: 20px;

    font-weight: 700;
}

.sidebar-text {
    color: #64748B;

    font-size: 13px;

    margin-bottom: 18px;
}


/* ----------------------------------------------------------
   CHARTS
---------------------------------------------------------- */

div[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;

    border:
        1px solid #E2E8F0;

    border-radius: 12px;

    padding: 6px;

    box-shadow:
        0 3px 10px rgba(15, 39, 71, 0.04);
}


/* ----------------------------------------------------------
   INFO CARD
---------------------------------------------------------- */

.info-card {
    background-color: #FFFFFF;

    border:
        1px solid #E2E8F0;

    border-radius: 12px;

    padding: 20px 22px;

    line-height: 1.7;

    color: #475569;

    box-shadow:
        0 3px 10px rgba(15, 39, 71, 0.04);
}


/* ----------------------------------------------------------
   FOOTER
---------------------------------------------------------- */

.dashboard-footer {
    text-align: center;

    color: #718096;

    font-size: 12px;

    border-top:
        1px solid #DCE3EB;

    padding-top: 18px;

    margin-top: 35px;
}


/* ----------------------------------------------------------
   STREAMLIT UI CLEANUP
---------------------------------------------------------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# PROJECT PATHS
# ============================================================

APP_DIR = Path(__file__).resolve().parent

PROJECT_DIR = APP_DIR.parent

SEARCH_ROOTS = [
    APP_DIR,
    PROJECT_DIR,
]


# ============================================================
# FILE FINDER
# ============================================================

def find_file(filename):
    """
    Search for a CSV file in common project locations.
    """

    possible_paths = []

    for root in SEARCH_ROOTS:

        possible_paths.extend(
            [
                root / filename,
                root / "data" / filename,
                root / "data" / "raw" / filename,
                root / "data" / "processed" / filename,
            ]
        )

    for root in SEARCH_ROOTS:

        data_folder = root / "data"

        if data_folder.exists():

            try:

                possible_paths.extend(
                    data_folder.rglob(filename)
                )

            except Exception:
                pass

    for path in possible_paths:

        if path.exists() and path.is_file():

            return path

    return None


# ============================================================
# LOAD CSV
# ============================================================

@st.cache_data
def load_csv(filename):

    path = find_file(filename)

    if path is None:

        return None

    try:

        return pd.read_csv(path)

    except Exception as error:

        st.error(
            f"Unable to read {filename}: {error}"
        )

        return None


# ============================================================
# LOAD ALL DATASETS
# ============================================================

sales_df = load_csv(
    "sales_transactions_cleaned.csv"
)

# Fallback to original sales file
if sales_df is None:

    sales_df = load_csv(
        "sales_transactions.csv"
    )


sku_master_df = load_csv(
    "sku_master.csv"
)

customer_df = load_csv(
    "customer_master.csv"
)

inventory_snapshot_df = load_csv(
    "inventory_snapshot.csv"
)

promotions_df = load_csv(
    "promotions.csv"
)

store_master_df = load_csv(
    "store_master.csv"
)

daily_demand_df = load_csv(
    "daily_demand_features.csv"
)

forecast_df = load_csv(
    "demand_forecast_results.csv"
)

inventory_risk_df = load_csv(
    "inventory_risk_scoring.csv"
)

inventory_flags_df = load_csv(
    "sku_inventory_flags.csv"
)


# ============================================================
# CHECK SALES DATA
# ============================================================

if sales_df is None:

    st.error(
        """
        Sales dataset was not found.

        Please make sure one of these files exists:

        sales_transactions_cleaned.csv

        OR

        sales_transactions.csv

        Recommended location:

        project/
        ├── app.py
        └── data/
            ├── sales_transactions_cleaned.csv
            └── ...
        """
    )

    st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

def clean_columns(df):

    if df is None:
        return None

    df = df.copy()

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df


sales_df = clean_columns(
    sales_df
)

sku_master_df = clean_columns(
    sku_master_df
)

customer_df = clean_columns(
    customer_df
)

inventory_snapshot_df = clean_columns(
    inventory_snapshot_df
)

promotions_df = clean_columns(
    promotions_df
)

store_master_df = clean_columns(
    store_master_df
)

daily_demand_df = clean_columns(
    daily_demand_df
)

forecast_df = clean_columns(
    forecast_df
)

inventory_risk_df = clean_columns(
    inventory_risk_df
)

inventory_flags_df = clean_columns(
    inventory_flags_df
)


# ============================================================
# COLUMN DETECTOR
# ============================================================

def find_column(
    df,
    candidates
):
    """
    Finds a column even if the dataset uses
    slightly different naming.
    """

    if df is None:

        return None

    columns = list(df.columns)

    normalized = {}

    for column in columns:

        clean = (
            str(column)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        normalized[clean] = column

    # Exact match
    for candidate in candidates:

        candidate_clean = (
            str(candidate)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        if candidate_clean in normalized:

            return normalized[
                candidate_clean
            ]

    # Partial match
    for normalized_name, original_name in normalized.items():

        for candidate in candidates:

            candidate_clean = (
                str(candidate)
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            if (
                candidate_clean in normalized_name
                or normalized_name in candidate_clean
            ):

                return original_name

    return None


# ============================================================
# NORMALIZE SKU
# ============================================================

def normalize_sku(value):

    if pd.isna(value):

        return ""

    value = str(value).strip()

    # Handle IDs such as 1001.0
    if value.endswith(".0"):

        value = value[:-2]

    return value.upper()


# ============================================================
# CATEGORY MAPPING
# ============================================================

def create_category_mapping(
    sales,
    sku_master
):

    sales = sales.copy()

    # --------------------------------------------------------
    # IF SKU MASTER DOES NOT EXIST
    # --------------------------------------------------------

    if sku_master is None:

        sales["category"] = "Uncategorized"

        return sales


    # --------------------------------------------------------
    # FIND SALES SKU COLUMN
    # --------------------------------------------------------

    sales_sku_column = find_column(
        sales,
        [
            "sku_id",
            "sku",
            "product_id",
            "product_code",
            "productid",
            "item_id",
            "item_code",
            "item"
        ]
    )


    # --------------------------------------------------------
    # FIND MASTER SKU COLUMN
    # --------------------------------------------------------

    master_sku_column = find_column(
        sku_master,
        [
            "sku_id",
            "sku",
            "product_id",
            "product_code",
            "productid",
            "item_id",
            "item_code",
            "item"
        ]
    )


    # --------------------------------------------------------
    # FIND CATEGORY COLUMN
    # --------------------------------------------------------

    category_column = find_column(
        sku_master,
        [
            "category",
            "product_category",
            "product_category_name",
            "category_name",
            "department",
            "product_type",
            "segment"
        ]
    )


    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if sales_sku_column is None:

        st.warning(
            "SKU column could not be identified "
            "in the sales dataset."
        )

        sales["category"] = "Uncategorized"

        return sales


    if master_sku_column is None:

        st.warning(
            "SKU column could not be identified "
            "in sku_master.csv."
        )

        sales["category"] = "Uncategorized"

        return sales


    if category_column is None:

        st.warning(
            "Category column could not be identified "
            "in sku_master.csv."
        )

        sales["category"] = "Uncategorized"

        return sales


    # --------------------------------------------------------
    # NORMALIZED JOIN KEY
    # --------------------------------------------------------

    sales["_category_join_key"] = (
        sales[
            sales_sku_column
        ]
        .apply(normalize_sku)
    )


    master = sku_master.copy()


    master["_category_join_key"] = (
        master[
            master_sku_column
        ]
        .apply(normalize_sku)
    )


    # --------------------------------------------------------
    # CREATE LOOKUP TABLE
    # --------------------------------------------------------

    category_lookup = master[
        [
            "_category_join_key",
            category_column
        ]
    ].copy()


    category_lookup = (
        category_lookup
        .dropna(
            subset=[
                "_category_join_key"
            ]
        )
        .drop_duplicates(
            subset=[
                "_category_join_key"
            ]
        )
    )


    category_lookup = category_lookup.rename(
        columns={
            category_column:
            "_mapped_category"
        }
    )


    # --------------------------------------------------------
    # REMOVE OLD CATEGORY
    # --------------------------------------------------------

    if "category" in sales.columns:

        sales = sales.drop(
            columns=[
                "category"
            ]
        )


    # --------------------------------------------------------
    # MERGE
    # --------------------------------------------------------

    sales = sales.merge(
        category_lookup,
        on="_category_join_key",
        how="left"
    )


    # --------------------------------------------------------
    # FINAL CATEGORY COLUMN
    # --------------------------------------------------------

    sales["category"] = (
        sales[
            "_mapped_category"
        ]
        .fillna("Uncategorized")
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # CLEAN BAD VALUES
    # --------------------------------------------------------

    invalid_values = [
        "",
        "nan",
        "NaN",
        "None",
        "none",
        "undefined",
        "Undefined",
        "null",
        "NULL"
    ]


    sales.loc[
        sales["category"].isin(
            invalid_values
        ),
        "category"
    ] = "Uncategorized"


    # --------------------------------------------------------
    # REMOVE TEMPORARY COLUMNS
    # --------------------------------------------------------

    sales = sales.drop(
        columns=[
            "_category_join_key",
            "_mapped_category"
        ],
        errors="ignore"
    )


    return sales


# ============================================================
# APPLY CATEGORY MAPPING
# ============================================================

sales_df = create_category_mapping(
    sales_df,
    sku_master_df
)


# ============================================================
# DATE COLUMN
# ============================================================

date_column = find_column(
    sales_df,
    [
        "date",
        "sales_date",
        "transaction_date",
        "order_date"
    ]
)


if date_column is not None:

    sales_df["date"] = pd.to_datetime(
        sales_df[
            date_column
        ],
        errors="coerce"
    )

else:

    sales_df["date"] = pd.NaT


sales_df["year"] = (
    sales_df[
        "date"
    ].dt.year
)


# ============================================================
# HEADER
# ============================================================
# IMPORTANT:
# HTML starts at the beginning of the line.
# This prevents Streamlit from displaying HTML as text.
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
    '<div class="sidebar-title">Dashboard Filters</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-text">'
    'Use the controls below to refine the analysis.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# YEAR FILTER
# ============================================================

years = (
    sales_df[
        "year"
    ]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

years = sorted(
    years
)


selected_years = st.sidebar.multiselect(
    "Select Year",
    options=years,
    default=years
)


# ============================================================
# CHANNEL FILTER
# ============================================================

channel_column = find_column(
    sales_df,
    [
        "channel",
        "sales_channel",
        "sales_channel_name"
    ]
)


if channel_column is not None:

    channels = (
        sales_df[
            channel_column
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    channels = sorted(
        channels
    )


    selected_channels = (
        st.sidebar.multiselect(
            "Select Channel",
            options=channels,
            default=channels
        )
    )

else:

    selected_channels = []


# ============================================================
# FILTER SALES DATA
# ============================================================

filtered_sales = sales_df.copy()


if selected_years:

    filtered_sales = filtered_sales[
        filtered_sales[
            "year"
        ].isin(
            selected_years
        )
    ]


if (
    channel_column is not None
    and selected_channels
):

    filtered_sales = filtered_sales[
        filtered_sales[
            channel_column
        ].isin(
            selected_channels
        )
    ]


if filtered_sales.empty:

    st.warning(
        "No records match the selected filters."
    )

    st.stop()


# ============================================================
# FIND SALES COLUMNS
# ============================================================

sales_value_column = find_column(
    filtered_sales,
    [
        "total_value",
        "total_sales",
        "sales",
        "revenue",
        "amount",
        "sales_amount",
        "net_sales",
        "total_amount"
    ]
)


quantity_column = find_column(
    filtered_sales,
    [
        "quantity",
        "qty",
        "units",
        "units_sold"
    ]
)


transaction_column = find_column(
    filtered_sales,
    [
        "receipt_id",
        "transaction_id",
        "order_id",
        "invoice_id",
        "bill_id"
    ]
)


store_column = find_column(
    filtered_sales,
    [
        "store_id",
        "store",
        "store_code",
        "store_name"
    ]
)


sku_column = find_column(
    filtered_sales,
    [
        "sku_id",
        "sku",
        "product_id",
        "product_code",
        "item_id"
    ]
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.markdown(
    '<div class="section-header">'
    'Executive Summary'
    '</div>',
    unsafe_allow_html=True
)


# Total sales

if sales_value_column is not None:

    total_sales = pd.to_numeric(
        filtered_sales[
            sales_value_column
        ],
        errors="coerce"
    ).fillna(0).sum()

else:

    total_sales = 0


# Quantity

if quantity_column is not None:

    total_quantity = pd.to_numeric(
        filtered_sales[
            quantity_column
        ],
        errors="coerce"
    ).fillna(0).sum()

else:

    total_quantity = 0


# Transactions

if transaction_column is not None:

    total_transactions = (
        filtered_sales[
            transaction_column
        ]
        .nunique()
    )

else:

    total_transactions = len(
        filtered_sales
    )


# Stores

if store_column is not None:

    total_stores = (
        filtered_sales[
            store_column
        ]
        .nunique()
    )

else:

    total_stores = 0


# Products

if sku_column is not None:

    total_products = (
        filtered_sales[
            sku_column
        ]
        .nunique()
    )

else:

    total_products = 0


# Average order value

if total_transactions > 0:

    average_order_value = (
        total_sales
        / total_transactions
    )

else:

    average_order_value = 0


# ============================================================
# METRIC CARDS
# ============================================================

m1, m2, m3, m4, m5, m6 = st.columns(
    6
)


m1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)


m2.metric(
    "Transactions",
    f"{total_transactions:,}"
)


m3.metric(
    "Quantity Sold",
    f"{total_quantity:,.0f}"
)


m4.metric(
    "Stores",
    f"{total_stores:,}"
)


m5.metric(
    "Products",
    f"{total_products:,}"
)


m6.metric(
    "Avg Order Value",
    f"₹{average_order_value:,.0f}"
)


# ============================================================
# CHART STYLE FUNCTION
# ============================================================

def style_chart(
    fig,
    title,
    x_title=None,
    y_title=None
):
    """
    Apply a professional style to Plotly charts.
    """

    fig.update_layout(
        template="plotly_white",

        font=dict(
            family="Arial",
            size=12,
            color="#334155"
        ),

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        margin=dict(
            l=60,
            r=40,
            t=75,
            b=55
        ),

        # Explicit title.
        # This prevents undefined titles.
        title=dict(
            text=str(title),
            x=0.02,
            xanchor="left",
            y=0.96,
            yanchor="top",
            font=dict(
                family="Arial",
                size=18,
                color="#17324D"
            )
        )
    )


    if x_title is not None:

        fig.update_xaxes(
            title_text=x_title
        )


    if y_title is not None:

        fig.update_yaxes(
            title_text=y_title
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
# SALES TREND + CHANNEL
# ============================================================

st.divider()


left_column, right_column = st.columns(
    [2, 1]
)


# ============================================================
# DAILY SALES TREND
# ============================================================

with left_column:

    st.markdown(
        '<div class="section-header">'
        'Sales Trend'
        '</div>',
        unsafe_allow_html=True
    )


    if (
        sales_value_column is not None
        and filtered_sales["date"].notna().any()
    ):

        daily_sales = filtered_sales.copy()


        daily_sales = daily_sales.dropna(
            subset=["date"]
        )


        daily_sales["_sales_value"] = pd.to_numeric(
            daily_sales[
                sales_value_column
            ],
            errors="coerce"
        ).fillna(0)


        daily_sales = (
            daily_sales
            .groupby(
                "date",
                as_index=False
            )["_sales_value"]
            .sum()
        )


        fig_sales = px.line(
            daily_sales,
            x="date",
            y="_sales_value"
        )


        fig_sales.update_traces(
            hovertemplate=
            "Date: %{x|%d %b %Y}<br>"
            "Sales: ₹%{y:,.0f}"
            "<extra></extra>"
        )


        style_chart(
            fig_sales,
            "Daily Sales Trend",
            "Date",
            "Sales (₹)"
        )


        st.plotly_chart(
            fig_sales,
            use_container_width=True,
            key="daily_sales_chart"
        )


    else:

        st.info(
            "Sales trend data is not available."
        )


# ============================================================
# SALES BY CHANNEL
# ============================================================

with right_column:

    st.markdown(
        '<div class="section-header">'
        'Sales by Channel'
        '</div>',
        unsafe_allow_html=True
    )


    if (
        channel_column is not None
        and sales_value_column is not None
    ):

        channel_data = filtered_sales.copy()


        channel_data["_sales_value"] = pd.to_numeric(
            channel_data[
                sales_value_column
            ],
            errors="coerce"
        ).fillna(0)


        channel_sales = (
            channel_data
            .groupby(
                channel_column,
                as_index=False
            )["_sales_value"]
            .sum()
        )


        fig_channel = px.pie(
            channel_sales,
            names=channel_column,
            values="_sales_value",
            hole=0.48
        )


        fig_channel.update_traces(
            hovertemplate=
            "<b>%{label}</b><br>"
            "Sales: ₹%{value:,.0f}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )


        style_chart(
            fig_channel,
            "Sales Distribution by Channel"
        )


        st.plotly_chart(
            fig_channel,
            use_container_width=True,
            key="channel_sales_chart"
        )


    else:

        st.info(
            "Channel data is not available."
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
# Check category column
# ------------------------------------------------------------

if "category" not in filtered_sales.columns:

    st.error(
        "Category column was not created."
    )

else:

    category_data = filtered_sales.copy()


    # --------------------------------------------------------
    # Clean category values
    # --------------------------------------------------------

    category_data["category"] = (
        category_data[
            "category"
        ]
        .fillna("Uncategorized")
        .astype(str)
        .str.strip()
    )


    category_data.loc[
        category_data[
            "category"
        ].isin(
            [
                "",
                "nan",
                "NaN",
                "None",
                "none",
                "undefined",
                "Undefined",
                "null",
                "NULL"
            ]
        ),
        "category"
    ] = "Uncategorized"


    # --------------------------------------------------------
    # Check sales value
    # --------------------------------------------------------

    if sales_value_column is None:

        st.error(
            "Sales value column could not be identified."
        )

    else:

        category_data["_sales_value"] = pd.to_numeric(
            category_data[
                sales_value_column
            ],
            errors="coerce"
        ).fillna(0)


        # ----------------------------------------------------
        # GROUP BY CATEGORY
        # ----------------------------------------------------

        category_sales = (
            category_data
            .groupby(
                "category",
                as_index=False
            )["_sales_value"]
            .sum()
        )


        category_sales = (
            category_sales
            .sort_values(
                "_sales_value",
                ascending=True
            )
        )


        # ----------------------------------------------------
        # REMOVE COMPLETELY EMPTY CATEGORIES
        # ----------------------------------------------------

        category_sales = category_sales[
            category_sales[
                "_sales_value"
            ] > 0
        ]


        # ----------------------------------------------------
        # DRAW CATEGORY CHART
        # ----------------------------------------------------

        if not category_sales.empty:

            fig_category = px.bar(
                category_sales,
                x="_sales_value",
                y="category",
                orientation="h"
            )


            fig_category.update_traces(

                texttemplate=
                "₹%{x:,.0f}",

                textposition="outside",

                cliponaxis=False,

                hovertemplate=
                "<b>%{y}</b><br>"
                "Sales: ₹%{x:,.0f}"
                "<extra></extra>"
            )


            style_chart(
                fig_category,
                "Sales by Category",
                "Sales (₹)",
                "Category"
            )


            st.plotly_chart(
                fig_category,
                use_container_width=True,
                key="sales_category_chart"
            )


        else:

            st.info(
                "No category sales are available."
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
    store_column is not None
    and sales_value_column is not None
):

    store_data = filtered_sales.copy()


    store_data["_sales_value"] = pd.to_numeric(
        store_data[
            sales_value_column
        ],
        errors="coerce"
    ).fillna(0)


    store_sales = (
        store_data
        .groupby(
            store_column,
            as_index=False
        )["_sales_value"]
        .sum()
    )


    store_sales = (
        store_sales
        .sort_values(
            "_sales_value",
            ascending=False
        )
        .head(20)
        .sort_values(
            "_sales_value",
            ascending=True
        )
    )


    fig_store = px.bar(
        store_sales,
        x="_sales_value",
        y=store_column,
        orientation="h"
    )


    fig_store.update_traces(
        hovertemplate=
        "<b>Store: %{y}</b><br>"
        "Sales: ₹%{x:,.0f}"
        "<extra></extra>"
    )


    style_chart(
        fig_store,
        "Top Stores by Sales",
        "Sales (₹)",
        "Store"
    )


    st.plotly_chart(
        fig_store,
        use_container_width=True,
        key="store_sales_chart"
    )


else:

    st.info(
        "Store sales data is not available."
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


if sales_value_column is not None:

    yearly_data = filtered_sales.copy()


    yearly_data["_sales_value"] = pd.to_numeric(
        yearly_data[
            sales_value_column
        ],
        errors="coerce"
    ).fillna(0)


    yearly_sales = (
        yearly_data
        .groupby(
            "year",
            as_index=False
        )["_sales_value"]
        .sum()
    )


    fig_year = px.bar(
        yearly_sales,
        x="year",
        y="_sales_value"
    )


    fig_year.update_traces(
        hovertemplate=
        "Year: %{x}<br>"
        "Sales: ₹%{y:,.0f}"
        "<extra></extra>"
    )


    style_chart(
        fig_year,
        "Sales by Year",
        "Year",
        "Sales (₹)"
    )


    st.plotly_chart(
        fig_year,
        use_container_width=True,
        key="year_sales_chart"
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


if (
    daily_demand_df is not None
    and not daily_demand_df.empty
):

    demand_date_column = find_column(
        daily_demand_df,
        [
            "date",
            "demand_date",
            "forecast_date"
        ]
    )


    demand_value_column = find_column(
        daily_demand_df,
        [
            "demand",
            "daily_demand",
            "demand_qty",
            "quantity"
        ]
    )


    if (
        demand_date_column is not None
        and demand_value_column is not None
    ):

        demand_data = daily_demand_df.copy()


        demand_data[demand_date_column] = pd.to_datetime(
            demand_data[
                demand_date_column
            ],
            errors="coerce"
        )


        demand_data[demand_value_column] = pd.to_numeric(
            demand_data[
                demand_value_column
            ],
            errors="coerce"
        ).fillna(0)


        demand_plot = (
            demand_data
            .groupby(
                demand_date_column,
                as_index=False
            )[demand_value_column]
            .sum()
        )


        fig_demand = px.line(
            demand_plot,
            x=demand_date_column,
            y=demand_value_column
        )


        fig_demand.update_traces(
            hovertemplate=
            "Date: %{x|%d %b %Y}<br>"
            "Demand: %{y:,.0f}"
            "<extra></extra>"
        )


        style_chart(
            fig_demand,
            "Daily Demand Trend",
            "Date",
            "Demand"
        )


        st.plotly_chart(
            fig_demand,
            use_container_width=True,
            key="demand_chart"
        )


    else:

        st.info(
            "Demand columns could not be identified."
        )


else:

    st.info(
        "daily_demand_features.csv is not available."
    )


# ============================================================
# FORECAST ANALYSIS
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Demand Forecast'
    '</div>',
    unsafe_allow_html=True
)


if (
    forecast_df is not None
    and not forecast_df.empty
):

    forecast_date_column = find_column(
        forecast_df,
        [
            "date",
            "forecast_date",
            "ds"
        ]
    )


    actual_column = find_column(
        forecast_df,
        [
            "actual_demand",
            "actual",
            "actual_quantity"
        ]
    )


    predicted_column = find_column(
        forecast_df,
        [
            "predicted_demand",
            "forecast",
            "forecast_demand",
            "predicted",
            "prediction"
        ]
    )


    if (
        forecast_date_column is not None
        and predicted_column is not None
    ):

        forecast_data = forecast_df.copy()


        forecast_data[
            forecast_date_column
        ] = pd.to_datetime(
            forecast_data[
                forecast_date_column
            ],
            errors="coerce"
        )


        forecast_data[
            predicted_column
        ] = pd.to_numeric(
            forecast_data[
                predicted_column
            ],
            errors="coerce"
        )


        fig_forecast = px.line(
            forecast_data,
            x=forecast_date_column,
            y=predicted_column
        )


        fig_forecast.update_traces(
            hovertemplate=
            "Date: %{x|%d %b %Y}<br>"
            "Forecast: %{y:,.0f}"
            "<extra></extra>"
        )


        style_chart(
            fig_forecast,
            "Demand Forecast",
            "Date",
            "Forecasted Demand"
        )


        st.plotly_chart(
            fig_forecast,
            use_container_width=True,
            key="forecast_chart"
        )


    else:

        st.info(
            "Forecast columns could not be identified."
        )


else:

    st.info(
        "demand_forecast_results.csv is not available."
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


if (
    inventory_risk_df is not None
    and not inventory_risk_df.empty
):

    # --------------------------------------------------------
    # FIND RISK COLUMN
    # --------------------------------------------------------

    risk_column = find_column(
        inventory_risk_df,
        [
            "final_risk_level",
            "risk_level",
            "risk",
            "risk_category",
            "risk_class",
            "inventory_risk"
        ]
    )


    if risk_column is not None:

        risk_data = (
            inventory_risk_df[
                risk_column
            ]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )


        # ----------------------------------------------------
        # CLEAN RISK VALUES
        # ----------------------------------------------------

        risk_data.loc[
            risk_data.isin(
                [
                    "",
                    "nan",
                    "NaN",
                    "None",
                    "undefined",
                    "Undefined"
                ]
            )
        ] = "Unknown"


        # ----------------------------------------------------
        # COUNTS
        # ----------------------------------------------------

        critical_count = int(
            risk_data[
                risk_data.str.lower()
                .str.contains(
                    "critical",
                    na=False
                )
            ].count()
        )


        high_count = int(
            risk_data[
                risk_data.str.lower()
                .str.contains(
                    "high",
                    na=False
                )
                &
                ~risk_data.str.lower()
                .str.contains(
                    "critical",
                    na=False
                )
            ].count()
        )


        medium_count = int(
            risk_data[
                risk_data.str.lower()
                .str.contains(
                    "medium",
                    na=False
                )
            ].count()
        )


        low_count = int(
            risk_data[
                risk_data.str.lower()
                .str.contains(
                    "low",
                    na=False
                )
            ].count()
        )


        # ----------------------------------------------------
        # RISK CARDS
        # ----------------------------------------------------

        r1, r2, r3, r4 = st.columns(
            4
        )


        r1.metric(
            "Critical Risk",
            f"{critical_count:,}"
        )


        r2.metric(
            "High Risk",
            f"{high_count:,}"
        )


        r3.metric(
            "Medium Risk",
            f"{medium_count:,}"
        )


        r4.metric(
            "Low Risk",
            f"{low_count:,}"
        )


        # ----------------------------------------------------
        # RISK DISTRIBUTION
        # ----------------------------------------------------

        risk_counts = (
            risk_data
            .value_counts()
            .reset_index()
        )


        risk_counts.columns = [
            "risk_level",
            "count"
        ]


        fig_risk = px.bar(
            risk_counts,
            x="risk_level",
            y="count"
        )


        fig_risk.update_traces(
            hovertemplate=
            "<b>%{x}</b><br>"
            "Products: %{y:,}"
            "<extra></extra>"
        )


        # IMPORTANT:
        # EXPLICIT TITLE.
        # NO "undefined".
        style_chart(
            fig_risk,
            "Inventory Risk Distribution",
            "Risk Level",
            "Number of Products"
        )


        st.plotly_chart(
            fig_risk,
            use_container_width=True,
            key="inventory_risk_chart"
        )


    else:

        st.warning(
            """
            inventory_risk_scoring.csv was found,
            but the risk-level column could not be identified.
            """
        )


# ============================================================
# INVENTORY FLAGS FALLBACK
# ============================================================

elif (
    inventory_flags_df is not None
    and not inventory_flags_df.empty
):

    st.info(
        "inventory_risk_scoring.csv was not available. "
        "Showing inventory flags instead."
    )


    flag_column = find_column(
        inventory_flags_df,
        [
            "flag",
            "risk_flag",
            "inventory_flag",
            "status"
        ]
    )


    if flag_column is not None:

        flag_data = (
            inventory_flags_df[
                flag_column
            ]
            .fillna("No Flag")
            .astype(str)
            .str.strip()
        )


        flag_counts = (
            flag_data
            .value_counts()
            .reset_index()
        )


        flag_counts.columns = [
            "flag",
            "count"
        ]


        fig_flags = px.bar(
            flag_counts,
            x="flag",
            y="count"
        )


        fig_flags.update_traces(
            hovertemplate=
            "<b>%{x}</b><br>"
            "Products: %{y:,}"
            "<extra></extra>"
        )


        style_chart(
            fig_flags,
            "Inventory Flags",
            "Flag",
            "Number of Products"
        )


        st.plotly_chart(
            fig_flags,
            use_container_width=True,
            key="inventory_flags_chart"
        )


    else:

        st.info(
            "Inventory flag column could not be identified."
        )


else:

    st.info(
        "No inventory risk data is available."
    )


# ============================================================
# TOP PRODUCTS
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Top 10 Products'
    '</div>',
    unsafe_allow_html=True
)


if (
    sku_column is not None
    and sales_value_column is not None
):

    product_data = filtered_sales.copy()


    product_data["_sales_value"] = pd.to_numeric(
        product_data[
            sales_value_column
        ],
        errors="coerce"
    ).fillna(0)


    top_products = (
        product_data
        .groupby(
            sku_column,
            as_index=False
        )["_sales_value"]
        .sum()
    )


    top_products = (
        top_products
        .sort_values(
            "_sales_value",
            ascending=False
        )
        .head(10)
        .sort_values(
            "_sales_value",
            ascending=True
        )
    )


    fig_products = px.bar(
        top_products,
        x="_sales_value",
        y=sku_column,
        orientation="h"
    )


    fig_products.update_traces(
        hovertemplate=
        "<b>SKU: %{y}</b><br>"
        "Sales: ₹%{x:,.0f}"
        "<extra></extra>"
    )


    style_chart(
        fig_products,
        "Top 10 Products by Sales",
        "Sales (₹)",
        "SKU"
    )


    st.plotly_chart(
        fig_products,
        use_container_width=True,
        key="top_products_chart"
    )


else:

    st.info(
        "Product sales data is not available."
    )


# ============================================================
# DATASET STATUS
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Dataset Status'
    '</div>',
    unsafe_allow_html=True
)


dataset_status = []


datasets = {
    "Sales Transactions": sales_df,
    "SKU Master": sku_master_df,
    "Customer Master": customer_df,
    "Inventory Snapshot": inventory_snapshot_df,
    "Promotions": promotions_df,
    "Store Master": store_master_df,
    "Daily Demand Features": daily_demand_df,
    "Demand Forecast Results": forecast_df,
    "Inventory Risk Scoring": inventory_risk_df,
    "SKU Inventory Flags": inventory_flags_df,
}


for name, dataframe in datasets.items():

    if (
        dataframe is not None
        and not dataframe.empty
    ):

        status = "Available"

        rows = len(dataframe)

    else:

        status = "Not Available"

        rows = 0


    dataset_status.append(
        {
            "Dataset": name,
            "Status": status,
            "Rows": rows
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
# PROJECT OVERVIEW
# ============================================================

st.divider()


st.markdown(
    '<div class="section-header">'
    'Project Overview'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
<div class="info-card">

<b>Retail Executive Dashboard</b>

<br><br>

This dashboard provides an integrated view of retail
sales performance, product categories, demand patterns,
forecasting results and inventory risk.

<br><br>

<b>Key analytical areas:</b>

<br>

• Sales Performance

<br>
• Sales by Channel

<br>
• Sales by Category

<br>
• Store-wise Sales

<br>
• Product Performance

<br>
• Demand Analysis

<br>
• Demand Forecasting

<br>
• Inventory Risk

<br>
• Inventory Flags

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="dashboard-footer">
    Retail Executive Dashboard
    &nbsp; | &nbsp;
    Online Retail Demand Forecasting Project
</div>
""",
    unsafe_allow_html=True
)