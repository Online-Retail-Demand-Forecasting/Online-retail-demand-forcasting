# ============================================================
# RETAIL EXECUTIVE DASHBOARD
# ============================================================
# Sections:
# 1. Executive Summary
# 2. Sales Trend
# 3. Sales by Channel
# 4. Sales by Category
# 5. Store-wise Sales
# 6. Demand Analysis
# 7. Actual vs Forecast
# 8. Year-wise Sales
# 9. Inventory Risk
# 10. Top Products
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
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Retail Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f8fc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .dashboard-title {
        font-size: 36px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 3px;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #1f2937;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #eef2ff;
        border-left: 5px solid #6366f1;
        margin-bottom: 15px;
    }

    .warning-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #fff7ed;
        border-left: 5px solid #f97316;
        margin-bottom: 15px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FIND PROJECT DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# POSSIBLE DATA FOLDERS
# ============================================================

DATA_PATHS = [
    os.path.join(BASE_DIR, "data"),
    os.path.join(BASE_DIR, "Data"),
    os.path.join(os.getcwd(), "data"),
    os.path.join(os.getcwd(), "Data"),
]


def find_data_folder():

    for folder in DATA_PATHS:

        if os.path.exists(folder):
            return folder

    return os.path.join(BASE_DIR, "data")


DATA_PATH = find_data_folder()


# ============================================================
# FIND FILE
# ============================================================

def find_file(file_names):

    # Exact search
    for folder in DATA_PATHS:

        if not os.path.exists(folder):
            continue

        for file_name in file_names:

            path = os.path.join(folder, file_name)

            if os.path.exists(path):
                return path

    # Recursive search
    for folder in DATA_PATHS:

        if not os.path.exists(folder):
            continue

        for file_name in file_names:

            matches = glob.glob(
                os.path.join(folder, "**", file_name),
                recursive=True
            )

            if matches:
                return matches[0]

    return None


# ============================================================
# LOAD CSV SAFELY
# ============================================================

def safe_read_csv(file_path):

    if file_path is None:
        return None

    try:

        return pd.read_csv(file_path)

    except Exception as e:

        st.error(
            f"Unable to read {os.path.basename(file_path)}: {e}"
        )

        return None


# ============================================================
# LOAD SALES DATA
# ============================================================

@st.cache_data
def load_sales():

    file_names = [
        "sales_daily.csv",
        "sales_transactions_cleaned.csv",
        "sales_transactions.csv",
        "sales.csv",
        "daily_sales.csv"
    ]

    file_path = find_file(file_names)

    if file_path is None:
        return None, None

    return safe_read_csv(file_path), file_path


# ============================================================
# LOAD INVENTORY
# ============================================================

@st.cache_data
def load_inventory():

    file_names = [
        "inventory_snapshots.csv",
        "inventory.csv",
        "inventory_data.csv"
    ]

    file_path = find_file(file_names)

    if file_path is None:
        return None, None

    return safe_read_csv(file_path), file_path


# ============================================================
# LOAD SKU MASTER
# ============================================================

@st.cache_data
def load_sku_master():

    file_names = [
        "sku_master.csv",
        "product_master.csv",
        "products.csv",
        "sku.csv"
    ]

    file_path = find_file(file_names)

    if file_path is None:
        return None, None

    return safe_read_csv(file_path), file_path


# ============================================================
# LOAD DATA
# ============================================================

sales_raw, sales_file = load_sales()

inventory_raw, inventory_file = load_inventory()

sku_raw, sku_file = load_sku_master()


# ============================================================
# SALES FILE ERROR
# ============================================================

if sales_raw is None:

    st.error(
        "Sales data could not be loaded."
    )

    st.markdown(
        f"""
        <div class="warning-box">

        <b>Sales file was not found.</b>

        <br><br>

        The dashboard searches for:

        <br><br>

        sales_daily.csv<br>
        sales_transactions_cleaned.csv<br>
        sales_transactions.csv<br>
        sales.csv<br>
        daily_sales.csv

        <br><br>

        <b>Data folder being searched:</b>

        <br>

        {DATA_PATH}

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# COLUMN FINDER
# ============================================================

def find_column(df, candidates):

    if df is None:
        return None

    columns = list(df.columns)

    # Exact normalized match
    normalized_columns = {}

    for col in columns:

        normalized = (
            str(col)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        normalized_columns[normalized] = col

    for candidate in candidates:

        normalized_candidate = (
            str(candidate)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        if normalized_candidate in normalized_columns:

            return normalized_columns[
                normalized_candidate
            ]

    # Partial match
    for col in columns:

        clean_col = (
            str(col)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        for candidate in candidates:

            clean_candidate = (
                str(candidate)
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            if clean_candidate in clean_col:

                return col

    return None


# ============================================================
# STANDARDIZE SALES DATA
# ============================================================

def standardize_sales(df):

    df = df.copy()

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    date_col = find_column(
        df,
        [
            "date",
            "sales_date",
            "transaction_date",
            "order_date",
            "day",
            "datetime",
            "timestamp"
        ]
    )

    if date_col is not None:

        df["Date"] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

    else:

        df["Date"] = pd.NaT


    # --------------------------------------------------------
    # SALES / REVENUE
    # --------------------------------------------------------

    sales_col = find_column(
        df,
        [
            "sales",
            "revenue",
            "sales_amount",
            "total_sales",
            "total_revenue",
            "amount",
            "net_sales",
            "gmv"
        ]
    )

    if sales_col is not None:

        df["Sales"] = pd.to_numeric(
            df[sales_col],
            errors="coerce"
        ).fillna(0)

    else:

        # If sales is not present, try quantity × price
        quantity_temp = find_column(
            df,
            [
                "quantity",
                "qty",
                "units",
                "units_sold",
                "demand"
            ]
        )

        price_temp = find_column(
            df,
            [
                "price",
                "unit_price",
                "selling_price"
            ]
        )

        if quantity_temp and price_temp:

            df["Sales"] = (
                pd.to_numeric(
                    df[quantity_temp],
                    errors="coerce"
                ).fillna(0)
                *
                pd.to_numeric(
                    df[price_temp],
                    errors="coerce"
                ).fillna(0)
            )

        else:

            df["Sales"] = 0


    # --------------------------------------------------------
    # QUANTITY
    # --------------------------------------------------------

    quantity_col = find_column(
        df,
        [
            "quantity",
            "qty",
            "units",
            "units_sold",
            "sales_quantity",
            "demand",
            "volume"
        ]
    )

    if quantity_col is not None:

        df["Quantity"] = pd.to_numeric(
            df[quantity_col],
            errors="coerce"
        ).fillna(0)

    else:

        df["Quantity"] = 0


    # --------------------------------------------------------
    # PRODUCT
    # --------------------------------------------------------

    product_col = find_column(
        df,
        [
            "product_id",
            "product",
            "sku",
            "sku_id",
            "item_id",
            "product_code",
            "item"
        ]
    )

    if product_col is not None:

        df["Product"] = (
            df[product_col]
            .astype(str)
            .replace("nan", "Unknown")
        )

    else:

        df["Product"] = "Unknown"


    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    category_col = find_column(
        df,
        [
            "category",
            "product_category",
            "category_name",
            "department",
            "product_type"
        ]
    )

    if category_col is not None:

        df["Category"] = (
            df[category_col]
            .astype(str)
            .replace("nan", "Unknown")
        )

    else:

        df["Category"] = "Unknown"


    # --------------------------------------------------------
    # CHANNEL
    # --------------------------------------------------------

    channel_col = find_column(
        df,
        [
            "channel",
            "sales_channel",
            "order_channel",
            "sales_type",
            "platform",
            "source"
        ]
    )

    if channel_col is not None:

        df["Channel"] = (
            df[channel_col]
            .astype(str)
            .replace("nan", "Unknown")
        )

    else:

        df["Channel"] = "Unknown"


    # --------------------------------------------------------
    # STORE
    # --------------------------------------------------------

    store_col = find_column(
        df,
        [
            "store",
            "store_id",
            "store_name",
            "location",
            "branch",
            "shop",
            "outlet"
        ]
    )

    if store_col is not None:

        df["Store"] = (
            df[store_col]
            .astype(str)
            .replace("nan", "Unknown")
        )

    else:

        df["Store"] = "Unknown"


    # --------------------------------------------------------
    # CLEAN DATE
    # --------------------------------------------------------

    df = df.dropna(
        subset=["Date"]
    )

    # --------------------------------------------------------
    # TIME FEATURES
    # --------------------------------------------------------

    if not df.empty:

        df["Year"] = df["Date"].dt.year

        df["Month"] = df["Date"].dt.month

        df["Month_Name"] = (
            df["Date"]
            .dt.strftime("%b")
        )

        df["Week"] = (
            df["Date"]
            .dt.isocalendar()
            .week
            .astype(int)
        )

        df["Day"] = df["Date"].dt.day

        df["Weekday"] = (
            df["Date"]
            .dt.day_name()
        )

    return df


# ============================================================
# STANDARDIZE
# ============================================================

sales = standardize_sales(sales_raw)


# ============================================================
# HANDLE EMPTY DATA
# ============================================================

if sales.empty:

    st.error(
        "The sales file was found, but no valid sales records were available."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    'Retail Executive Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Sales Performance • Demand Forecasting • Inventory Intelligence'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Dashboard")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Summary",
        "Sales Trend",
        "Sales by Channel",
        "Sales by Category",
        "Store-wise Sales",
        "Demand Analysis",
        "Actual vs Forecast",
        "Year-wise Sales",
        "Inventory Risk",
        "Top Products"
    ]
)


# ============================================================
# SIDEBAR DATA INFO
# ============================================================

with st.sidebar.expander("Dataset Information"):

    st.write(
        "**Sales File:**"
    )

    st.write(
        os.path.basename(sales_file)
    )

    st.write(
        f"**Rows:** {len(sales_raw):,}"
    )

    st.write(
        f"**Columns:** {len(sales_raw.columns)}"
    )

    if inventory_raw is not None:

        st.write(
            f"**Inventory Rows:** {len(inventory_raw):,}"
        )

    if sku_raw is not None:

        st.write(
            f"**SKU Rows:** {len(sku_raw):,}"
        )


# ============================================================
# FILTERS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("Filters")


# ------------------------------------------------------------
# DATE FILTER
# ------------------------------------------------------------

minimum_date = sales["Date"].min().date()

maximum_date = sales["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(
        minimum_date,
        maximum_date
    ),
    min_value=minimum_date,
    max_value=maximum_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = (
        pd.Timestamp(date_range[1])
        + pd.Timedelta(days=1)
        - pd.Timedelta(seconds=1)
    )

    filtered_sales = sales[
        (sales["Date"] >= start_date)
        &
        (sales["Date"] <= end_date)
    ].copy()

else:

    filtered_sales = sales.copy()


# ------------------------------------------------------------
# CATEGORY FILTER
# ------------------------------------------------------------

category_values = sorted(
    filtered_sales["Category"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "Category",
    category_values,
    default=category_values
)

if selected_categories:

    filtered_sales = filtered_sales[
        filtered_sales["Category"]
        .isin(selected_categories)
    ]


# ============================================================
# COMMON FUNCTION
# ============================================================

def show_no_data(message):

    st.info(message)


# ============================================================
# 1. EXECUTIVE SUMMARY
# ============================================================

if page == "Executive Summary":

    st.markdown(
        '<div class="section-title">'
        'Executive Summary'
        '</div>',
        unsafe_allow_html=True
    )

    total_sales = filtered_sales["Sales"].sum()

    total_units = filtered_sales["Quantity"].sum()

    products = filtered_sales["Product"].nunique()

    stores = filtered_sales["Store"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Sales",
        f"₹{total_sales:,.0f}"
    )

    col2.metric(
        "Units Sold",
        f"{total_units:,.0f}"
    )

    col3.metric(
        "Products",
        f"{products:,}"
    )

    col4.metric(
        "Stores",
        f"{stores:,}"
    )

    st.markdown("---")

    # Sales trend
    daily_sales = (
        filtered_sales
        .groupby("Date", as_index=False)["Sales"]
        .sum()
    )

    if not daily_sales.empty:

        fig = px.line(
            daily_sales,
            x="Date",
            y="Sales",
            title="Sales Trend",
            markers=True
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:

        category_sales = (
            filtered_sales
            .groupby("Category")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .reset_index()
        )

        if not category_sales.empty:

            fig = px.bar(
                category_sales.head(10),
                x="Category",
                y="Sales",
                title="Sales by Category"
            )

            fig.update_layout(
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with col2:

        top_products = (
            filtered_sales
            .groupby("Product")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        if not top_products.empty:

            fig = px.bar(
                top_products,
                x="Sales",
                y="Product",
                orientation="h",
                title="Top Products"
            )

            fig.update_layout(
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# 2. SALES TREND
# ============================================================

elif page == "Sales Trend":

    st.markdown(
        '<div class="section-title">'
        'Sales Trend'
        '</div>',
        unsafe_allow_html=True
    )

    daily_sales = (
        filtered_sales
        .groupby("Date")
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    if daily_sales.empty:

        show_no_data(
            "No sales trend data is available for the selected filters."
        )

    else:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=daily_sales["Date"],
                y=daily_sales["Sales"],
                mode="lines",
                name="Sales"
            )
        )

        fig.update_layout(
            title="Daily Sales Trend",
            xaxis_title="Date",
            yaxis_title="Sales",
            template="plotly_white",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            daily_sales,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 3. SALES BY CHANNEL
# ============================================================

elif page == "Sales by Channel":

    st.markdown(
        '<div class="section-title">'
        'Sales by Channel'
        '</div>',
        unsafe_allow_html=True
    )

    channel_sales = (
        filtered_sales
        .groupby("Channel")
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    # Even if channel does not exist, the standardized
    # column contains "Unknown", so the section never crashes.

    if channel_sales.empty:

        show_no_data(
            "Channel sales data is not available."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                channel_sales,
                x="Channel",
                y="Sales",
                title="Sales by Channel"
            )

            fig.update_layout(
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            fig = px.pie(
                channel_sales,
                names="Channel",
                values="Sales",
                title="Channel Contribution"
            )

            fig.update_layout(
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.dataframe(
            channel_sales,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 4. SALES BY CATEGORY
# ============================================================

elif page == "Sales by Category":

    st.markdown(
        '<div class="section-title">'
        'Sales by Category'
        '</div>',
        unsafe_allow_html=True
    )

    category_sales = (
        filtered_sales
        .groupby("Category")
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum"),
            Products=("Product", "nunique")
        )
        .reset_index()
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    if category_sales.empty:

        show_no_data(
            "Category sales data is not available."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                category_sales,
                x="Category",
                y="Sales",
                title="Sales by Category"
            )

            fig.update_layout(
                template="plotly_white",
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            fig = px.pie(
                category_sales,
                names="Category",
                values="Sales",
                title="Category Contribution"
            )

            fig.update_layout(
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.dataframe(
            category_sales,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 5. STORE-WISE SALES
# ============================================================

elif page == "Store-wise Sales":

    st.markdown(
        '<div class="section-title">'
        'Store-wise Sales'
        '</div>',
        unsafe_allow_html=True
    )

    store_sales = (
        filtered_sales
        .groupby("Store")
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum"),
            Products=("Product", "nunique")
        )
        .reset_index()
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    if store_sales.empty:

        show_no_data(
            "Store-wise sales data is not available."
        )

    else:

        # Remove Unknown if real stores exist
        chart_data = store_sales.copy()

        if (
            len(chart_data) > 1
            and "Unknown" in chart_data["Store"].values
        ):

            chart_data = chart_data[
                chart_data["Store"] != "Unknown"
            ]

        if chart_data.empty:

            chart_data = store_sales

        fig = px.bar(
            chart_data.head(20),
            x="Sales",
            y="Store",
            orientation="h",
            title="Top Stores by Sales"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            store_sales,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 6. DEMAND ANALYSIS
# ============================================================

elif page == "Demand Analysis":

    st.markdown(
        '<div class="section-title">'
        'Demand Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    demand = (
        filtered_sales
        .groupby("Date")
        .agg(
            Demand=("Quantity", "sum"),
            Sales=("Sales", "sum")
        )
        .reset_index()
    )

    if demand.empty:

        show_no_data(
            "Demand data is not available."
        )

    else:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Demand",
            f"{demand['Demand'].sum():,.0f}"
        )

        col2.metric(
            "Average Daily Demand",
            f"{demand['Demand'].mean():,.0f}"
        )

        col3.metric(
            "Peak Daily Demand",
            f"{demand['Demand'].max():,.0f}"
        )

        fig = px.line(
            demand,
            x="Date",
            y="Demand",
            title="Daily Demand"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Demand by weekday
        weekday_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        weekday_demand = (
            filtered_sales
            .groupby("Weekday")["Quantity"]
            .sum()
            .reindex(weekday_order)
            .reset_index()
        )

        fig = px.bar(
            weekday_demand,
            x="Weekday",
            y="Quantity",
            title="Demand by Day of Week"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# 7. ACTUAL VS FORECAST
# ============================================================

elif page == "Actual vs Forecast":

    st.markdown(
        '<div class="section-title">'
        'Actual vs Forecast'
        '</div>',
        unsafe_allow_html=True
    )

    actual = (
        filtered_sales
        .groupby("Date")["Quantity"]
        .sum()
        .reset_index()
    )

    actual = actual.sort_values("Date")

    if len(actual) < 7:

        show_no_data(
            "At least 7 days of data are required for the forecast."
        )

    else:

        forecast_days = st.slider(
            "Forecast Horizon",
            min_value=7,
            max_value=60,
            value=30
        )

        window = min(
            14,
            len(actual)
        )

        moving_average = (
            actual["Quantity"]
            .tail(window)
            .mean()
        )

        future_dates = pd.date_range(
            start=actual["Date"].max()
            + pd.Timedelta(days=1),
            periods=forecast_days,
            freq="D"
        )

        forecast = pd.DataFrame(
            {
                "Date": future_dates,
                "Forecast": moving_average
            }
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=actual["Date"],
                y=actual["Quantity"],
                mode="lines",
                name="Actual Demand"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=forecast["Date"],
                y=forecast["Forecast"],
                mode="lines",
                name="Forecast",
                line=dict(
                    dash="dash"
                )
            )
        )

        fig.add_vline(
            x=actual["Date"].max(),
            line_dash="dot"
        )

        fig.update_layout(
            title="Actual Demand vs Forecast",
            xaxis_title="Date",
            yaxis_title="Demand",
            template="plotly_white",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Forecast Horizon",
            f"{forecast_days} Days"
        )

        col2.metric(
            "Average Forecast",
            f"{moving_average:,.0f}"
        )

        col3.metric(
            "Expected Demand",
            f"{forecast['Forecast'].sum():,.0f}"
        )

        st.info(
            "The current forecast uses a moving-average baseline "
            "so the dashboard remains functional without requiring "
            "an external forecasting model."
        )


# ============================================================
# 8. YEAR-WISE SALES
# ============================================================

elif page == "Year-wise Sales":

    st.markdown(
        '<div class="section-title">'
        'Year-wise Sales'
        '</div>',
        unsafe_allow_html=True
    )

    yearly_sales = (
        filtered_sales
        .groupby("Year")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Year")
    )

    if yearly_sales.empty:

        show_no_data(
            "Year-wise sales data is not available."
        )

    else:

        fig = px.bar(
            yearly_sales,
            x="Year",
            y="Sales",
            text_auto=".2s",
            title="Sales by Year"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Growth calculation
        yearly_sales["Growth %"] = (
            yearly_sales["Sales"]
            .pct_change()
            .mul(100)
            .round(2)
        )

        st.dataframe(
            yearly_sales,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 9. INVENTORY RISK
# ============================================================

elif page == "Inventory Risk":

    st.markdown(
        '<div class="section-title">'
        'Inventory Risk'
        '</div>',
        unsafe_allow_html=True
    )

    if inventory_raw is None:

        # Fallback risk calculation using sales demand
        st.info(
            "Inventory snapshot data was not found. "
            "Showing demand-based inventory risk instead."
        )

        product_risk = (
            filtered_sales
            .groupby(["Product", "Category"])
            .agg(
                Demand=("Quantity", "sum"),
                Sales=("Sales", "sum"),
                Active_Days=("Date", "nunique")
            )
            .reset_index()
        )

        if product_risk.empty:

            show_no_data(
                "Inventory risk cannot be calculated."
            )

        else:

            product_risk["Avg_Daily_Demand"] = (
                product_risk["Demand"]
                /
                product_risk["Active_Days"]
                .replace(0, 1)
            )

            # Demand percentile risk
            product_risk["Risk_Score"] = (
                product_risk[
                    "Avg_Daily_Demand"
                ]
                .rank(pct=True)
                * 100
            )

            def assign_risk(score):

                if score >= 75:
                    return "High"

                if score >= 40:
                    return "Medium"

                return "Low"

            product_risk["Risk_Level"] = (
                product_risk["Risk_Score"]
                .apply(assign_risk)
            )

            high_risk = product_risk[
                product_risk["Risk_Level"]
                == "High"
            ]

            medium_risk = product_risk[
                product_risk["Risk_Level"]
                == "Medium"
            ]

            low_risk = product_risk[
                product_risk["Risk_Level"]
                == "Low"
            ]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "High Risk",
                len(high_risk)
            )

            col2.metric(
                "Medium Risk",
                len(medium_risk)
            )

            col3.metric(
                "Low Risk",
                len(low_risk)
            )

            risk_distribution = (
                product_risk
                .groupby("Risk_Level")
                .size()
                .reset_index(
                    name="Products"
                )
            )

            fig = px.bar(
                risk_distribution,
                x="Risk_Level",
                y="Products",
                title="Inventory Risk Distribution"
            )

            fig.update_layout(
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown(
                "### High-Risk Products"
            )

            st.dataframe(
                high_risk.sort_values(
                    "Risk_Score",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

    else:

        inventory = inventory_raw.copy()

        inventory_product = find_column(
            inventory,
            [
                "product_id",
                "product",
                "sku",
                "sku_id",
                "item_id"
            ]
        )

        inventory_quantity = find_column(
            inventory,
            [
                "inventory",
                "stock",
                "stock_quantity",
                "quantity",
                "on_hand",
                "units"
            ]
        )

        if inventory_quantity is None:

            st.warning(
                "Inventory file exists, but a stock quantity column "
                "could not be identified."
            )

            st.dataframe(
                inventory.head(100),
                use_container_width=True,
                hide_index=True
            )

        else:

            inventory["Stock"] = pd.to_numeric(
                inventory[inventory_quantity],
                errors="coerce"
            ).fillna(0)

            if inventory_product is not None:

                inventory_summary = (
                    inventory
                    .groupby(inventory_product)["Stock"]
                    .sum()
                    .reset_index()
                )

                # Calculate demand
                product_demand = (
                    filtered_sales
                    .groupby("Product")["Quantity"]
                    .mean()
                    .reset_index()
                )

                product_demand.columns = [
                    "Product",
                    "Avg_Daily_Demand"
                ]

                inventory_summary = (
                    inventory_summary
                    .rename(
                        columns={
                            inventory_product:
                            "Product"
                        }
                    )
                    .merge(
                        product_demand,
                        on="Product",
                        how="left"
                    )
                )

                inventory_summary[
                    "Avg_Daily_Demand"
                ] = inventory_summary[
                    "Avg_Daily_Demand"
                ].fillna(0)

                inventory_summary[
                    "Days_of_Cover"
                ] = np.where(
                    inventory_summary[
                        "Avg_Daily_Demand"
                    ] > 0,
                    inventory_summary["Stock"]
                    /
                    inventory_summary[
                        "Avg_Daily_Demand"
                    ],
                    np.inf
                )

                def inventory_risk(days):

                    if days < 7:
                        return "High"

                    elif days < 21:
                        return "Medium"

                    return "Low"

                inventory_summary[
                    "Risk_Level"
                ] = (
                    inventory_summary[
                        "Days_of_Cover"
                    ]
                    .apply(inventory_risk)
                )

                high = (
                    inventory_summary[
                        "Risk_Level"
                    ] == "High"
                ).sum()

                medium = (
                    inventory_summary[
                        "Risk_Level"
                    ] == "Medium"
                ).sum()

                low = (
                    inventory_summary[
                        "Risk_Level"
                    ] == "Low"
                ).sum()

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "High Risk",
                    int(high)
                )

                col2.metric(
                    "Medium Risk",
                    int(medium)
                )

                col3.metric(
                    "Low Risk",
                    int(low)
                )

                risk_distribution = pd.DataFrame(
                    {
                        "Risk Level": [
                            "High",
                            "Medium",
                            "Low"
                        ],
                        "Products": [
                            high,
                            medium,
                            low
                        ]
                    }
                )

                fig = px.bar(
                    risk_distribution,
                    x="Risk Level",
                    y="Products",
                    title="Inventory Risk Distribution"
                )

                fig.update_layout(
                    template="plotly_white"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.markdown(
                    "### Inventory Risk Details"
                )

                st.dataframe(
                    inventory_summary.sort_values(
                        "Days_of_Cover"
                    ),
                    use_container_width=True,
                    hide_index=True
                )


# ============================================================
# 10. TOP PRODUCTS
# ============================================================

elif page == "Top Products":

    st.markdown(
        '<div class="section-title">'
        'Top Products'
        '</div>',
        unsafe_allow_html=True
    )

    number_of_products = st.slider(
        "Number of Products",
        min_value=5,
        max_value=30,
        value=10
    )

    top_products = (
        filtered_sales
        .groupby(
            ["Product", "Category"]
        )
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(number_of_products)
    )

    if top_products.empty:

        show_no_data(
            "Top product data is not available."
        )

    else:

        fig = px.bar(
            top_products.sort_values(
                "Sales"
            ),
            x="Sales",
            y="Product",
            color="Category",
            orientation="h",
            title=f"Top {number_of_products} Products by Sales"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            top_products,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#6b7280;
        font-size:13px;
        padding:10px;
    ">
        Retail Executive Dashboard
        <br>
        Sales Performance • Demand Forecasting • Inventory Intelligence
    </div>
    """,
    unsafe_allow_html=True
)