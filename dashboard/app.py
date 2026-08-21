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
# CUSTOM CSS
# ============================================================

st.markdown("""
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
        margin-bottom: 0px;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
    }

    .metric-title {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #1f2937;
        margin-top: 20px;
        margin-bottom: 10px;
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
""", unsafe_allow_html=True)


# ============================================================
# DATA PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATHS = [
    os.path.join(BASE_DIR, "data"),
    os.path.join(os.getcwd(), "data"),
    os.path.join(BASE_DIR, "Data"),
    os.path.join(os.getcwd(), "Data"),
]


# ============================================================
# FIND DATA FOLDER
# ============================================================

def find_data_folder():

    for path in DATA_PATHS:
        if os.path.exists(path):
            return path

    return os.path.join(BASE_DIR, "data")


DATA_PATH = find_data_folder()


# ============================================================
# FILE FINDER
# ============================================================

def find_file(possible_names):

    # Search exact names
    for name in possible_names:

        for folder in DATA_PATHS:

            file_path = os.path.join(folder, name)

            if os.path.exists(file_path):
                return file_path

    # Search recursively
    for folder in DATA_PATHS:

        if os.path.exists(folder):

            for name in possible_names:

                matches = glob.glob(
                    os.path.join(folder, "**", name),
                    recursive=True
                )

                if matches:
                    return matches[0]

    return None


# ============================================================
# SALES FILE LOADER
# ============================================================

@st.cache_data
def load_sales_data():

    possible_files = [
        "sales_daily.csv",
        "sales_transactions_cleaned.csv",
        "sales_transactions.csv",
        "sales.csv",
        "daily_sales.csv"
    ]

    sales_file = find_file(possible_files)

    if sales_file is None:
        return None, None

    try:

        df = pd.read_csv(sales_file)

        return df, sales_file

    except Exception as e:

        st.error(f"Unable to read sales file: {e}")
        return None, sales_file


# ============================================================
# OTHER DATA LOADERS
# ============================================================

@st.cache_data
def load_inventory_data():

    possible_files = [
        "inventory_snapshots.csv",
        "inventory.csv",
        "inventory_data.csv"
    ]

    inventory_file = find_file(possible_files)

    if inventory_file is None:
        return None, None

    try:

        df = pd.read_csv(inventory_file)

        return df, inventory_file

    except Exception:
        return None, inventory_file


@st.cache_data
def load_sku_data():

    possible_files = [
        "sku_master.csv",
        "products.csv",
        "product_master.csv",
        "sku.csv"
    ]

    sku_file = find_file(possible_files)

    if sku_file is None:
        return None, None

    try:

        df = pd.read_csv(sku_file)

        return df, sku_file

    except Exception:
        return None, sku_file


@st.cache_data
def load_calendar_data():

    possible_files = [
        "calendar.csv",
        "calender.csv",
        "date.csv"
    ]

    calendar_file = find_file(possible_files)

    if calendar_file is None:
        return None, None

    try:

        df = pd.read_csv(calendar_file)

        return df, calendar_file

    except Exception:
        return None, calendar_file


# ============================================================
# COLUMN DETECTOR
# ============================================================

def find_column(df, candidates):

    if df is None:
        return None

    normalized = {
        str(col).lower().strip().replace(" ", "_"): col
        for col in df.columns
    }

    for candidate in candidates:

        key = candidate.lower().strip().replace(" ", "_")

        if key in normalized:
            return normalized[key]

    # Partial matching
    for col in df.columns:

        col_clean = str(col).lower().strip().replace(" ", "_")

        for candidate in candidates:

            candidate_clean = (
                candidate.lower()
                .strip()
                .replace(" ", "_")
            )

            if candidate_clean in col_clean:
                return col

    return None


# ============================================================
# STANDARDIZE SALES DATA
# ============================================================

def standardize_sales_data(df):

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
            "datetime"
        ]
    )

    if date_col:

        df["Date"] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

    else:

        df["Date"] = pd.NaT

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
            "product_code"
        ]
    )

    if product_col:
        df["Product"] = df[product_col].astype(str)

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
            "department"
        ]
    )

    if category_col:
        df["Category"] = df[category_col].astype(str)

    else:
        df["Category"] = "Unknown"

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
            "demand"
        ]
    )

    if quantity_col:

        df["Quantity"] = pd.to_numeric(
            df[quantity_col],
            errors="coerce"
        ).fillna(0)

    else:

        df["Quantity"] = 0

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
            "price"
        ]
    )

    if sales_col:

        df["Sales"] = pd.to_numeric(
            df[sales_col],
            errors="coerce"
        ).fillna(0)

    else:

        df["Sales"] = 0

    # --------------------------------------------------------
    # PRICE
    # --------------------------------------------------------

    price_col = find_column(
        df,
        [
            "price",
            "unit_price",
            "selling_price"
        ]
    )

    if price_col:

        df["Price"] = pd.to_numeric(
            df[price_col],
            errors="coerce"
        )

    else:

        df["Price"] = np.nan

    # --------------------------------------------------------
    # CLEAN
    # --------------------------------------------------------

    df = df.dropna(
        subset=["Date"]
    )

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Day"] = df["Date"].dt.day
    df["Weekday"] = df["Date"].dt.day_name()

    return df


# ============================================================
# LOAD DATA
# ============================================================

sales_raw, sales_file = load_sales_data()

inventory_raw, inventory_file = load_inventory_data()

sku_raw, sku_file = load_sku_data()

calendar_raw, calendar_file = load_calendar_data()


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
        <b>Expected sales files:</b><br><br>
        sales_daily.csv<br>
        sales_transactions_cleaned.csv<br>
        sales_transactions.csv<br>
        sales.csv<br>
        daily_sales.csv<br><br>

        <b>Current data folder:</b><br>
        {DATA_PATH}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# STANDARDIZE
# ============================================================

sales = standardize_sales_data(sales_raw)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Retail Dashboard")

st.sidebar.markdown("---")

st.sidebar.subheader("Navigation")

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Executive Summary",
        "Sales Analytics",
        "Category Analysis",
        "Product Analysis",
        "Demand Forecast",
        "Inventory Dashboard",
        "Risk Dashboard"
    ]
)


# ============================================================
# DATA INFORMATION
# ============================================================

with st.sidebar.expander("Data Information"):

    st.write(
        f"**Sales file:** {os.path.basename(sales_file)}"
    )

    st.write(
        f"**Rows:** {len(sales):,}"
    )

    st.write(
        f"**Columns:** {len(sales_raw.columns)}"
    )

    if inventory_raw is not None:
        st.write(
            f"**Inventory:** {len(inventory_raw):,} rows"
        )

    if sku_raw is not None:
        st.write(
            f"**SKU Master:** {len(sku_raw):,} rows"
        )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("Filters")


# Date filter
if sales["Date"].notna().any():

    min_date = sales["Date"].min().date()
    max_date = sales["Date"].max().date()

    selected_dates = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(selected_dates) == 2:

        start_date = pd.Timestamp(
            selected_dates[0]
        )

        end_date = pd.Timestamp(
            selected_dates[1]
        )

        filtered_sales = sales[
            (sales["Date"] >= start_date)
            &
            (sales["Date"] <= end_date)
        ]

    else:

        filtered_sales = sales.copy()

else:

    filtered_sales = sales.copy()


# Category filter
categories = sorted(
    filtered_sales["Category"]
    .dropna()
    .unique()
    .tolist()
)

if len(categories) > 0:

    selected_categories = st.sidebar.multiselect(
        "Category",
        categories,
        default=categories
    )

    filtered_sales = filtered_sales[
        filtered_sales["Category"].isin(
            selected_categories
        )
    ]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">Retail Executive Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Sales Performance • Demand Forecasting • Inventory Intelligence'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

if page == "Executive Summary":

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    total_sales = filtered_sales["Sales"].sum()

    total_units = filtered_sales["Quantity"].sum()

    total_products = filtered_sales["Product"].nunique()

    avg_daily_sales = (
        filtered_sales
        .groupby("Date")["Sales"]
        .sum()
        .mean()
    )

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
        f"{total_products:,}"
    )

    col4.metric(
        "Avg Daily Sales",
        f"₹{avg_daily_sales:,.0f}"
    )

    st.markdown("---")

    # Sales Trend
    st.markdown(
        '<div class="section-title">Sales Trend</div>',
        unsafe_allow_html=True
    )

    daily_sales = (
        filtered_sales
        .groupby("Date", as_index=False)["Sales"]
        .sum()
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title="Daily Sales Performance",
        markers=True
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Category performance
    col1, col2 = st.columns(2)

    with col1:

        category_sales = (
            filtered_sales
            .groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            category_sales.head(10),
            x="Sales",
            y="Category",
            orientation="h",
            title="Top Categories by Sales"
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
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

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
# SALES ANALYTICS
# ============================================================

elif page == "Sales Analytics":

    st.markdown(
        '<div class="section-title">Sales Analytics</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Revenue",
        f"₹{filtered_sales['Sales'].sum():,.0f}"
    )

    col2.metric(
        "Quantity",
        f"{filtered_sales['Quantity'].sum():,.0f}"
    )

    col3.metric(
        "Transactions / Records",
        f"{len(filtered_sales):,}"
    )

    st.markdown("---")

    daily = (
        filtered_sales
        .groupby("Date")
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    fig = px.line(
        daily,
        x="Date",
        y="Sales",
        title="Sales Trend"
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

        monthly = (
            filtered_sales
            .groupby(
                ["Year", "Month"]
            )["Sales"]
            .sum()
            .reset_index()
        )

        monthly["Period"] = (
            monthly["Year"].astype(str)
            + "-"
            + monthly["Month"].astype(str).str.zfill(2)
        )

        fig = px.bar(
            monthly,
            x="Period",
            y="Sales",
            title="Monthly Sales"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        weekday = (
            filtered_sales
            .groupby("Weekday")["Sales"]
            .sum()
            .reset_index()
        )

        weekday_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        weekday["Weekday"] = pd.Categorical(
            weekday["Weekday"],
            categories=weekday_order,
            ordered=True
        )

        weekday = weekday.sort_values("Weekday")

        fig = px.bar(
            weekday,
            x="Weekday",
            y="Sales",
            title="Sales by Day of Week"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

elif page == "Category Analysis":

    st.markdown(
        '<div class="section-title">Sales by Category</div>',
        unsafe_allow_html=True
    )

    category_data = (
        filtered_sales
        .groupby("Category")
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum"),
            Products=("Product", "nunique")
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    if category_data.empty:

        st.warning(
            "Category data is not available."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                category_data,
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
                category_data,
                names="Category",
                values="Sales",
                title="Sales Contribution"
            )

            fig.update_layout(
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown(
            '<div class="section-title">Category Performance Table</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            category_data,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

elif page == "Product Analysis":

    st.markdown(
        '<div class="section-title">Product Performance</div>',
        unsafe_allow_html=True
    )

    product_data = (
        filtered_sales
        .groupby(["Product", "Category"])
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    product_data = product_data.sort_values(
        "Sales",
        ascending=False
    )

    col1, col2 = st.columns(2)

    with col1:

        top_products = product_data.head(15)

        fig = px.bar(
            top_products,
            x="Sales",
            y="Product",
            color="Category",
            orientation="h",
            title="Top 15 Products"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        bottom_products = product_data.tail(15)

        fig = px.bar(
            bottom_products,
            x="Sales",
            y="Product",
            color="Category",
            orientation="h",
            title="Lowest Performing Products"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.dataframe(
        product_data.head(100),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DEMAND FORECAST
# ============================================================

elif page == "Demand Forecast":

    st.markdown(
        '<div class="section-title">Demand Forecasting</div>',
        unsafe_allow_html=True
    )

    daily_demand = (
        filtered_sales
        .groupby("Date")["Quantity"]
        .sum()
        .reset_index()
    )

    if len(daily_demand) < 7:

        st.warning(
            "Not enough historical data available for forecasting."
        )

    else:

        forecast_days = st.slider(
            "Forecast Horizon (Days)",
            min_value=7,
            max_value=60,
            value=30
        )

        # Moving average baseline forecast
        window = min(
            14,
            len(daily_demand)
        )

        moving_average = (
            daily_demand["Quantity"]
            .tail(window)
            .mean()
        )

        future_dates = pd.date_range(
            start=daily_demand["Date"].max()
            + pd.Timedelta(days=1),
            periods=forecast_days,
            freq="D"
        )

        forecast = pd.DataFrame({
            "Date": future_dates,
            "Forecast": moving_average
        })

        historical = daily_demand.rename(
            columns={"Quantity": "Demand"}
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=historical["Date"],
                y=historical["Demand"],
                mode="lines",
                name="Historical Demand"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=forecast["Date"],
                y=forecast["Forecast"],
                mode="lines",
                name="Forecast",
                line=dict(dash="dash")
            )
        )

        fig.update_layout(
            title="Demand Forecast",
            template="plotly_white",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Forecast Days",
            forecast_days
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
            "Forecast shown here uses a moving-average baseline. "
            "It can later be replaced with XGBoost, Random Forest, "
            "LightGBM, Prophet, ARIMA or SARIMA."
        )


# ============================================================
# INVENTORY DASHBOARD
# ============================================================

elif page == "Inventory Dashboard":

    st.markdown(
        '<div class="section-title">Inventory Intelligence</div>',
        unsafe_allow_html=True
    )

    if inventory_raw is None:

        st.warning(
            "Inventory dataset was not found. "
            "Make sure inventory_snapshots.csv exists in the data folder."
        )

    else:

        inventory = inventory_raw.copy()

        inventory_product_col = find_column(
            inventory,
            [
                "product_id",
                "product",
                "sku",
                "sku_id",
                "item_id"
            ]
        )

        inventory_qty_col = find_column(
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

        if inventory_qty_col:

            inventory["Stock"] = pd.to_numeric(
                inventory[inventory_qty_col],
                errors="coerce"
            ).fillna(0)

            col1, col2 = st.columns(2)

            col1.metric(
                "Total Inventory",
                f"{inventory['Stock'].sum():,.0f}"
            )

            col2.metric(
                "Inventory Records",
                f"{len(inventory):,}"
            )

            if inventory_product_col:

                stock_by_product = (
                    inventory
                    .groupby(inventory_product_col)["Stock"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(20)
                    .reset_index()
                )

                fig = px.bar(
                    stock_by_product,
                    x="Stock",
                    y=inventory_product_col,
                    orientation="h",
                    title="Top Products by Inventory"
                )

                fig.update_layout(
                    template="plotly_white"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            st.dataframe(
                inventory.head(100),
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# RISK DASHBOARD
# ============================================================

elif page == "Risk Dashboard":

    st.markdown(
        '<div class="section-title">Inventory & Sales Risk</div>',
        unsafe_allow_html=True
    )

    product_summary = (
        filtered_sales
        .groupby(["Product", "Category"])
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum"),
            Active_Days=("Date", "nunique")
        )
        .reset_index()
    )

    if product_summary.empty:

        st.warning(
            "Risk data is not available."
        )

    else:

        # Average daily demand
        product_summary["Avg_Daily_Demand"] = (
            product_summary["Quantity"]
            / product_summary["Active_Days"].replace(0, 1)
        )

        # Risk score
        product_summary["Risk_Score"] = (
            product_summary["Avg_Daily_Demand"]
            .rank(pct=True)
            * 100
        )

        def risk_level(score):

            if score >= 75:
                return "High"

            elif score >= 40:
                return "Medium"

            return "Low"

        product_summary["Risk_Level"] = (
            product_summary["Risk_Score"]
            .apply(risk_level)
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "High Risk Products",
            int(
                (
                    product_summary["Risk_Level"]
                    == "High"
                ).sum()
            )
        )

        col2.metric(
            "Medium Risk Products",
            int(
                (
                    product_summary["Risk_Level"]
                    == "Medium"
                ).sum()
            )
        )

        col3.metric(
            "Low Risk Products",
            int(
                (
                    product_summary["Risk_Level"]
                    == "Low"
                ).sum()
            )
        )

        risk_chart = (
            product_summary
            .groupby("Risk_Level")
            .size()
            .reset_index(name="Products")
        )

        fig = px.bar(
            risk_chart,
            x="Risk_Level",
            y="Products",
            title="Product Risk Distribution"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            '<div class="section-title">High Risk Products</div>',
            unsafe_allow_html=True
        )

        high_risk = (
            product_summary[
                product_summary["Risk_Level"]
                == "High"
            ]
            .sort_values(
                "Risk_Score",
                ascending=False
            )
        )

        st.dataframe(
            high_risk.head(100),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#6b7280;font-size:13px;">
        Retail Executive Dashboard |
        Sales Performance • Demand Forecasting • Inventory Intelligence
    </div>
    """,
    unsafe_allow_html=True
)