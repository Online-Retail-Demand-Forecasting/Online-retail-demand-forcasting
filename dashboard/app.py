import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Retail Executive Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PROFESSIONAL DESIGN
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F6F8FB;
    }

    .main .block-container {
        max-width: 1500px;
        padding: 2rem 2.5rem;
    }

    /* HEADER */
    .dashboard-header {
        background: linear-gradient(
            135deg,
            #102A43 0%,
            #1F4E79 100%
        );
        padding: 30px 34px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0 6px 18px rgba(16, 42, 67, 0.12);
    }

    .dashboard-title {
        color: white;
        font-size: 32px;
        font-weight: 700;
        margin: 0;
    }

    .dashboard-subtitle {
        color: #D9E8F5;
        font-size: 15px;
        margin-top: 7px;
    }

    /* SECTION HEADERS */
    .section-header {
        color: #17324D;
        font-size: 21px;
        font-weight: 700;
        padding-bottom: 8px;
        margin-top: 8px;
        margin-bottom: 15px;
        border-bottom: 2px solid #DCE3EB;
    }

    /* METRIC CARDS */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 3px 10px rgba(15, 39, 71, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #17324D !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #E2E8F0;
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

    /* CHART CONTAINER */
    div[data-testid="stPlotlyChart"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 8px;
        box-shadow: 0 3px 10px rgba(15, 39, 71, 0.04);
    }

    /* INFO CARD */
    .info-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 22px;
        line-height: 1.7;
        color: #475569;
        box-shadow: 0 3px 10px rgba(15, 39, 71, 0.04);
    }

    /* FOOTER */
    .footer {
        text-align: center;
        color: #718096;
        font-size: 12px;
        border-top: 1px solid #DCE3EB;
        padding-top: 18px;
        margin-top: 30px;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FIND DATA FILES
# =========================================================

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

SEARCH_ROOTS = [
    APP_DIR,
    PROJECT_DIR,
]


def find_file(filename):
    """
    Search common project folders for a dataset.
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

            possible_paths.extend(
                data_folder.rglob(filename)
            )

    for path in possible_paths:

        if path.exists() and path.is_file():
            return path

    return None


@st.cache_data
def load_csv(filename):

    path = find_file(filename)

    if path is None:
        return None

    return pd.read_csv(path)


# =========================================================
# LOAD DATASETS
# =========================================================

sales_df = load_csv(
    "sales_transactions_cleaned.csv"
)

# Fallback if cleaned file is unavailable
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

demand_df = load_csv(
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


if sales_df is None:

    st.error(
        """
        Sales dataset was not found.

        Please make sure that either:

        sales_transactions_cleaned.csv

        or

        sales_transactions.csv

        exists inside your project/data folder.
        """
    )

    st.stop()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

def clean_columns(df):

    if df is None:
        return None

    df = df.copy()

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df


sales_df = clean_columns(sales_df)
sku_master_df = clean_columns(sku_master_df)
customer_df = clean_columns(customer_df)
inventory_snapshot_df = clean_columns(inventory_snapshot_df)
promotions_df = clean_columns(promotions_df)
store_master_df = clean_columns(store_master_df)
demand_df = clean_columns(demand_df)
forecast_df = clean_columns(forecast_df)
inventory_risk_df = clean_columns(inventory_risk_df)
inventory_flags_df = clean_columns(inventory_flags_df)


# =========================================================
# FIND COLUMN
# =========================================================

def find_column(df, possible_names):

    if df is None:
        return None

    column_lookup = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for name in possible_names:

        if name.lower() in column_lookup:

            return column_lookup[
                name.lower()
            ]

    return None


# =========================================================
# NORMALIZE SKU IDs
# =========================================================

def normalize_id(series):

    return (
        series
        .astype(str)
        .str.strip()
        .str.replace(
            r"\.0$",
            "",
            regex=True
        )
    )


# =========================================================
# IMPORTANT FIX
# ADD CATEGORY FROM SKU MASTER
# =========================================================

def add_category_to_sales(
    sales,
    sku_master
):

    sales = sales.copy()

    if sku_master is None:
        return sales

    sales_sku_column = find_column(
        sales,
        ["sku_id"]
    )

    master_sku_column = find_column(
        sku_master,
        ["sku_id"]
    )

    category_column = find_column(
        sku_master,
        ["category"]
    )

    if (
        sales_sku_column is None
        or master_sku_column is None
        or category_column is None
    ):

        return sales

    # Create temporary normalized SKU ID
    sales["_sku_key"] = normalize_id(
        sales[sales_sku_column]
    )

    master = sku_master.copy()

    master["_sku_key"] = normalize_id(
        master[master_sku_column]
    )

    # Only keep the fields needed
    master_category = master[
        [
            "_sku_key",
            category_column
        ]
    ].copy()

    master_category = (
        master_category
        .drop_duplicates(
            subset="_sku_key"
        )
    )

    master_category = (
        master_category
        .rename(
            columns={
                category_column: "category"
            }
        )
    )

    # Remove category if sales already has one.
    if "category" in sales.columns:

        sales = sales.drop(
            columns=["category"]
        )

    # Merge category
    sales = sales.merge(
        master_category,
        on="_sku_key",
        how="left"
    )

    sales = sales.drop(
        columns=["_sku_key"]
    )

    return sales


# APPLY THE FIX
sales_df = add_category_to_sales(
    sales_df,
    sku_master_df
)


# =========================================================
# DATE PREPARATION
# =========================================================

date_column = find_column(
    sales_df,
    ["date"]
)

if date_column:

    sales_df["date"] = pd.to_datetime(
        sales_df[date_column],
        errors="coerce"
    )

else:

    sales_df["date"] = pd.NaT


sales_df["year"] = (
    sales_df["date"]
    .dt.year
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="dashboard-header">

        <div class="dashboard-title">
            Retail Executive Dashboard
        </div>

        <div class="dashboard-subtitle">
            Sales Performance • Demand Forecasting •
            Inventory Intelligence
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    '<div class="sidebar-title">Dashboard Filters</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="sidebar-text">'
    'Use the filters below to refine your analysis.'
    '</div>',
    unsafe_allow_html=True
)


# YEAR FILTER
years = sorted(
    sales_df["year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)


selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)


# CHANNEL FILTER
channel_column = find_column(
    sales_df,
    ["channel"]
)


if channel_column:

    channels = sorted(
        sales_df[channel_column]
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

else:

    selected_channels = []


# =========================================================
# FILTER SALES
# =========================================================

filtered_sales = sales_df.copy()


if selected_years:

    filtered_sales = filtered_sales[
        filtered_sales["year"].isin(
            selected_years
        )
    ]


if (
    channel_column
    and selected_channels
):

    filtered_sales = filtered_sales[
        filtered_sales[channel_column].isin(
            selected_channels
        )
    ]


if filtered_sales.empty:

    st.warning(
        "No records match the selected filters."
    )

    st.stop()


# =========================================================
# FIND IMPORTANT SALES COLUMNS
# =========================================================

sales_value_column = find_column(
    filtered_sales,
    [
        "total_value",
        "sales",
        "revenue",
        "amount"
    ]
)

quantity_column = find_column(
    filtered_sales,
    [
        "quantity",
        "qty",
        "units"
    ]
)

transaction_column = find_column(
    filtered_sales,
    [
        "receipt_id",
        "transaction_id",
        "order_id"
    ]
)

store_column = find_column(
    filtered_sales,
    [
        "store_id",
        "store"
    ]
)

sku_column = find_column(
    filtered_sales,
    [
        "sku_id",
        "product_id"
    ]
)


# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

st.markdown(
    '<div class="section-header">'
    'Executive Summary'
    '</div>',
    unsafe_allow_html=True
)


if sales_value_column:

    total_sales = pd.to_numeric(
        filtered_sales[
            sales_value_column
        ],
        errors="coerce"
    ).fillna(0).sum()

else:

    total_sales = 0


if quantity_column:

    total_quantity = pd.to_numeric(
        filtered_sales[
            quantity_column
        ],
        errors="coerce"
    ).fillna(0).sum()

else:

    total_quantity = 0


if transaction_column:

    total_transactions = (
        filtered_sales[
            transaction_column
        ].nunique()
    )

else:

    total_transactions = len(
        filtered_sales
    )


if store_column:

    total_stores = (
        filtered_sales[
            store_column
        ].nunique()
    )

else:

    total_stores = 0


if sku_column:

    total_products = (
        filtered_sales[
            sku_column
        ].nunique()
    )

else:

    total_products = 0


average_order_value = (
    total_sales / total_transactions
    if total_transactions > 0
    else 0
)


m1, m2, m3, m4, m5, m6 = st.columns(6)


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


# =========================================================
# PROFESSIONAL CHART STYLING
# =========================================================

def style_chart(
    fig,
    title
):

    fig.update_layout(

        template="plotly_white",

        font=dict(
            family="Arial",
            size=12,
            color="#334155"
        ),

        paper_bgcolor="white",

        plot_bgcolor="white",

        margin=dict(
            l=55,
            r=30,
            t=70,
            b=50
        ),

        hoverlabel=dict(
            bgcolor="white",
            font_family="Arial"
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


    # =====================================================
    # IMPORTANT:
    # SET TITLE AFTER ALL OTHER STYLING
    # THIS FIXES "undefined"
    # =====================================================

    fig.update_layout(
        title=dict(
            text=str(title),
            x=0.02,
            xanchor="left",
            y=0.97,
            yanchor="top",
            font=dict(
                family="Arial",
                size=17,
                color="#17324D"
            )
        )
    )

    return fig


# =========================================================
# DAILY SALES TREND
# =========================================================

st.divider()

left_column, right_column = st.columns(
    [2, 1]
)


with left_column:

    st.markdown(
        '<div class="section-header">'
        'Sales Trend'
        '</div>',
        unsafe_allow_html=True
    )


    if (
        sales_value_column
        and "date" in filtered_sales.columns
    ):

        daily_sales = (
            filtered_sales
            .dropna(subset=["date"])
            .copy()
        )


        daily_sales["_sales"] = pd.to_numeric(
            daily_sales[
                sales_value_column
            ],
            errors="coerce"
        ).fillna(0)


        daily_sales = (
            daily_sales
            .groupby("date")["_sales"]
            .sum()
            .reset_index()
        )


        fig_sales = px.line(
            daily_sales,
            x="date",
            y="_sales"
        )


        fig_sales.update_traces(
            hovertemplate=
            "Date: %{x|%d %b %Y}<br>"
            "Sales: ₹%{y:,.0f}"
            "<extra></extra>"
        )


        fig_sales.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales (₹)"
        )


        style_chart(
            fig_sales,
            "Daily Sales Trend"
        )


        st.plotly_chart(
            fig_sales,
            use_container_width=True
        )


# =========================================================
# SALES BY CHANNEL
# =========================================================

with right_column:

    st.markdown(
        '<div class="section-header">'
        'Sales by Channel'
        '</div>',
        unsafe_allow_html=True
    )


    if (
        channel_column
        and sales_value_column
    ):

        channel_sales = (
            filtered_sales
            .copy()
        )


        channel_sales["_sales"] = pd.to_numeric(
            channel_sales[
                sales_value_column
            ],
            errors="coerce"
        ).fillna(0)


        channel_sales = (
            channel_sales
            .groupby(
                channel_column
            )["_sales"]
            .sum()
            .reset_index()
        )


        fig_channel = px.pie(
            channel_sales,
            names=channel_column,
            values="_sales",
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
            use_container_width=True
        )


# =========================================================
# SALES BY CATEGORY
# =========================================================

st.divider()

st.markdown(
    '<div class="section-header">'
    'Sales by Category'
    '</div>',
    unsafe_allow_html=True
)


category_column = find_column(
    filtered_sales,
    ["category"]
)


if (
    category_column
    and sales_value_column
):

    category_data = (
        filtered_sales[
            [
                category_column,
                sales_value_column
            ]
        ]
        .copy()
    )


    category_data["_sales"] = pd.to_numeric(
        category_data[
            sales_value_column
        ],
        errors="coerce"
    ).fillna(0)


    # -----------------------------------------------------
    # FIX EMPTY / UNDEFINED CATEGORY
    # -----------------------------------------------------

    category_data["_category"] = (
        category_data[
            category_column
        ]
        .fillna("Uncategorized")
        .astype(str)
        .str.strip()
    )


    category_data.loc[
        category_data["_category"].isin(
            [
                "",
                "nan",
                "NaN",
                "None",
                "undefined",
                "Undefined"
            ]
        ),
        "_category"
    ] = "Uncategorized"


    category_sales = (
        category_data
        .groupby(
            "_category"
        )["_sales"]
        .sum()
        .sort_values()
        .reset_index()
    )


    if not category_sales.empty:

        fig_category = px.bar(
            category_sales,
            x="_sales",
            y="_category",
            orientation="h"
        )


        fig_category.update_traces(
            texttemplate="₹%{x:,.0f}",
            textposition="outside",
            cliponaxis=False,

            hovertemplate=
            "<b>%{y}</b><br>"
            "Sales: ₹%{x:,.0f}"
            "<extra></extra>"
        )


        fig_category.update_layout(
            xaxis_title="Sales (₹)",
            yaxis_title="Category"
        )


        # IMPORTANT:
        # Explicit title after all chart configuration.
        style_chart(
            fig_category,
            "Sales by Category"
        )


        st.plotly_chart(
            fig_category,
            use_container_width=True,
            key="sales_by_category"
        )


    else:

        st.info(
            "No category sales are available."
        )


else:

    st.warning(
        """
        Category data could not be connected.

        The dashboard expects:

        sales_transactions_cleaned.csv
        ↓ sku_id
        sku_master.csv
        ↓ category

        Make sure the sku_id values match.
        """
    )


# =========================================================
# STORE-WISE SALES
# =========================================================

st.divider()

st.markdown(
    '<div class="section-header">'
    'Store-wise Sales'
    '</div>',
    unsafe_allow_html=True
)


if (
    store_column
    and sales_value_column
):

    store_sales = (
        filtered_sales
        .copy()
    )


    store_sales["_sales"] = pd.to_numeric(
        store_sales[
            sales_value_column
        ],
        errors="coerce"
    ).fillna(0)


    store_sales = (
        store_sales
        .groupby(
            store_column
        )["_sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(20)
        .sort_values()
        .reset_index()
    )


    fig_store = px.bar(
        store_sales,
        x="_sales",
        y=store_column,
        orientation="h"
    )


    fig_store.update_traces(
        hovertemplate=
        "Store: %{y}<br>"
        "Sales: ₹%{x:,.0f}"
        "<extra></extra>"
    )


    fig_store.update_layout(
        xaxis_title="Sales (₹)",
        yaxis_title="Store"
    )


    style_chart(
        fig_store,
        "Top Stores by Sales"
    )


    st.plotly_chart(
        fig_store,
        use_container_width=True
    )


# =========================================================
# DEMAND ANALYSIS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-header">'
    'Demand Analysis'
    '</div>',
    unsafe_allow_html=True
)


if (
    demand_df is not None
    and not demand_df.empty
):

    demand_date_column = find_column(
        demand_df,
        ["date"]
    )

    demand_value_column = find_column(
        demand_df,
        ["demand"]
    )


    if (
        demand_date_column
        and demand_value_column
    ):

        demand_left, demand_right = st.columns(
            2
        )


        with demand_left:

            demand_plot = (
                demand_df
                .groupby(
                    demand_date_column
                )[demand_value_column]
                .sum()
                .reset_index()
            )


            fig_demand = px.line(
                demand_plot,
                x=demand_date_column,
                y=demand_value_column
            )


            style_chart(
                fig_demand,
                "Daily Demand"
            )


            st.plotly_chart(
                fig_demand,
                use_container_width=True
            )


        with demand_right:

            if (
                forecast_df is not None
                and not forecast_df.empty
            ):

                forecast_date_column = find_column(
                    forecast_df,
                    ["date"]
                )

                actual_column = find_column(
                    forecast_df,
                    ["actual_demand"]
                )

                predicted_column = find_column(
                    forecast_df,
                    [
                        "predicted_demand",
                        "forecast",
                        "forecast_demand"
                    ]
                )


                if (
                    forecast_date_column
                    and actual_column
                    and predicted_column
                ):

                    forecast_plot = (
                        forecast_df[
                            [
                                forecast_date_column,
                                actual_column,
                                predicted_column
                            ]
                        ]
                        .set_index(
                            forecast_date_column
                        )
                    )


                    st.line_chart(
                        forecast_plot,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "Forecast columns were not found."
                    )

            else:

                st.info(
                    "Forecast data is not available."
                )


    else:

        st.info(
            "Demand data does not contain the expected columns."
        )

else:

    st.info(
        "daily_demand_features.csv is not available."
    )


# =========================================================
# YEAR-WISE SALES
# =========================================================

st.divider()

st.markdown(
    '<div class="section-header">'
    'Year-wise Sales'
    '</div>',
    unsafe_allow_html=True
)


if sales_value_column:

    yearly_sales = (
        filtered_sales
        .copy()
    )


    yearly_sales["_sales"] = pd.to_numeric(
        yearly_sales[
            sales_value_column
        ],
        errors="coerce"
    ).fillna(0)


    yearly_sales = (
        yearly_sales
        .groupby(
            "year"
        )["_sales"]
        .sum()
        .reset_index()
    )


    fig_year = px.bar(
        yearly_sales,
        x="year",
        y="_sales"
    )


    fig_year.update_traces(
        hovertemplate=
        "Year: %{x}<br>"
        "Sales: ₹%{y:,.0f}"
        "<extra></extra>"
    )


    fig_year.update_layout(
        xaxis_title="Year",
        yaxis_title="Sales (₹)"
    )


    style_chart(
        fig_year,
        "Sales by Year"
    )


    st.plotly_chart(
        fig_year,
        use_container_width=True
    )


# =========================================================
# INVENTORY RISK
# =========================================================

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

    risk_column = find_column(
        inventory_risk_df,
        [
            "final_risk_level",
            "risk_level",
            "risk",
            "risk_category"
        ]
    )


    if risk_column:

        risk_data = (
            inventory_risk_df[
                risk_column
            ]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )


        risk_counts = (
            risk_data
            .value_counts()
            .reset_index()
        )


        risk_counts.columns = [
            "risk_level",
            "count"
        ]


        # -------------------------------------------------
        # RISK SUMMARY CARDS
        # -------------------------------------------------

        r1, r2, r3, r4 = st.columns(4)


        critical_count = int(
            risk_data[
                risk_data.str.lower()
                .str.contains("critical")
            ].count()
        )


        high_count = int(
            risk_data[
                risk_data.str.lower()
                .str.contains("high")
            ].count()
        )


        medium_count = int(
            risk_data[
                risk_data.str.lower()
                .str.contains("medium")
            ].count()
        )


        low_count = int(
            risk_data[
                risk_data.str.lower()
                .str.contains("low")
            ].count()
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


        # -------------------------------------------------
        # RISK CHART
        # -------------------------------------------------

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


        fig_risk.update_layout(
            xaxis_title="Risk Level",
            yaxis_title="Number of Products"
        )


        # -------------------------------------------------
        # IMPORTANT FIX:
        # THIS TITLE IS EXPLICITLY SET.
        # IT CANNOT BECOME "undefined".
        # -------------------------------------------------

        style_chart(
            fig_risk,
            "Inventory Risk Distribution"
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
            but a risk-level column could not be identified.
            """
        )


elif (
    inventory_flags_df is not None
    and not inventory_flags_df.empty
):

    st.info(
        "Using sku_inventory_flags.csv because "
        "inventory_risk_scoring.csv is unavailable."
    )


    flag_column = find_column(
        inventory_flags_df,
        ["flag"]
    )


    if flag_column:

        flag_counts = (
            inventory_flags_df[
                flag_column
            ]
            .fillna("No Flag")
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


        style_chart(
            fig_flags,
            "Inventory Risk Flags"
        )


        st.plotly_chart(
            fig_flags,
            use_container_width=True
        )


else:

    st.info(
        "No inventory risk dataset is available."
    )


# =========================================================
# TOP PRODUCTS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-header">'
    'Top 10 Products'
    '</div>',
    unsafe_allow_html=True
)


if (
    sku_column
    and sales_value_column
):

    top_products = (
        filtered_sales
        .copy()
    )


    top_products["_sales"] = pd.to_numeric(
        top_products[
            sales_value_column
        ],
        errors="coerce"
    ).fillna(0)


    top_products = (
        top_products
        .groupby(
            sku_column
        )["_sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .sort_values()
        .reset_index()
    )


    fig_products = px.bar(
        top_products,
        x="_sales",
        y=sku_column,
        orientation="h"
    )


    fig_products.update_traces(
        hovertemplate=
        "SKU: %{y}<br>"
        "Sales: ₹%{x:,.0f}"
        "<extra></extra>"
    )


    fig_products.update_layout(
        xaxis_title="Sales (₹)",
        yaxis_title="SKU"
    )


    style_chart(
        fig_products,
        "Top 10 Products by Sales"
    )


    st.plotly_chart(
        fig_products,
        use_container_width=True
    )


# =========================================================
# PROJECT OVERVIEW
# =========================================================

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

    This Retail Executive Dashboard provides a consolidated
    view of sales performance, product categories, demand
    trends, forecasting results and inventory risk.

    <br><br>

    The dashboard helps management identify sales patterns,
    compare channels and stores, understand product performance,
    monitor demand and support inventory decisions.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        Retail Executive Dashboard
        &nbsp;|&nbsp;
        Online Retail Demand Forecasting Project

    </div>
    """,
    unsafe_allow_html=True
)