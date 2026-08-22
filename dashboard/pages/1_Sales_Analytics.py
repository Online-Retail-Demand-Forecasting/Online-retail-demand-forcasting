import os
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "sales_transactions_cleaned.csv"
)


# ============================================================
# LOAD SALES DATA
# ============================================================

@st.cache_data
def load_sales_data():

    if not os.path.exists(DATA_PATH):
        return None

    return pd.read_csv(DATA_PATH)


sales_df = load_sales_data()


# ============================================================
# DATA VALIDATION
# ============================================================

if sales_df is None:

    st.error("Sales dataset could not be found.")

    st.info(
        f"Expected location: {DATA_PATH}"
    )

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

if "date" in sales_df.columns:

    sales_df["date"] = pd.to_datetime(
        sales_df["date"],
        errors="coerce"
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


if "date" in sales_df.columns:

    sales_df["year"] = sales_df["date"].dt.year


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📊 Sales Analytics")

st.caption(
    "Analyze retail sales performance, transactions, "
    "channels, stores and yearly trends."
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("Sales Filters")


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
    options=years,
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
    options=channels,
    default=channels
)


st.sidebar.divider()

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
        filtered_sales["year"].isin(selected_years)
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
# SALES OVERVIEW
# ============================================================

st.header("Sales Overview")


# ============================================================
# KPI CALCULATIONS
# ============================================================

if "total_value" in filtered_sales.columns:

    total_sales = (
        filtered_sales["total_value"].sum()
    )

else:

    total_sales = 0


if "receipt_id" in filtered_sales.columns:

    total_transactions = (
        filtered_sales["receipt_id"].nunique()
    )

else:

    total_transactions = len(
        filtered_sales
    )


if "quantity" in filtered_sales.columns:

    total_quantity = (
        filtered_sales["quantity"].sum()
    )

else:

    total_quantity = 0


if "store_id" in filtered_sales.columns:

    total_stores = (
        filtered_sales["store_id"].nunique()
    )

else:

    total_stores = 0


if "sku_id" in filtered_sales.columns:

    total_products = (
        filtered_sales["sku_id"].nunique()
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

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


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
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)


# ============================================================
# DAILY SALES TREND
# ============================================================

st.divider()

st.header("Sales Trend")


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
        line_width=2,
        hovertemplate=
        "<b>%{x|%d %b %Y}</b>"
        "<br>Sales: ₹%{y:,.0f}"
        "<extra></extra>"
    )

    fig_sales.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Sales (₹)",
        hovermode="x unified",
        height=450
    )

    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )

else:

    st.info(
        "Date or total_value column is not available."
    )


# ============================================================
# CHANNEL ANALYSIS
# ============================================================

st.divider()

st.header("Channel Analysis")


channel_left, channel_right = st.columns(2)


# ============================================================
# SALES BY CHANNEL
# ============================================================

with channel_left:

    if (
        "channel" in filtered_sales.columns
        and "total_value" in filtered_sales.columns
    ):

        channel_sales = (
            filtered_sales
            .groupby("channel")["total_value"]
            .sum()
            .reset_index()
            .sort_values(
                "total_value",
                ascending=False
            )
        )

        fig_channel = px.bar(
            channel_sales,
            x="channel",
            y="total_value",
            title="Sales by Channel",
            text="total_value"
        )

        fig_channel.update_traces(
            texttemplate="₹%{y:,.0f}",
            textposition="outside",
            hovertemplate=
            "<b>%{x}</b>"
            "<br>Sales: ₹%{y:,.0f}"
            "<extra></extra>"
        )

        fig_channel.update_layout(
            template="plotly_white",
            xaxis_title="Channel",
            yaxis_title="Sales (₹)",
            height=430
        )

        st.plotly_chart(
            fig_channel,
            use_container_width=True
        )

    else:

        st.info(
            "Channel data is not available."
        )


# ============================================================
# CHANNEL DISTRIBUTION
# ============================================================

with channel_right:

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

        fig_channel_pie = px.pie(
            channel_sales,
            names="channel",
            values="total_value",
            hole=0.45,
            title="Sales Distribution by Channel"
        )

        fig_channel_pie.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=
            "<b>%{label}</b>"
            "<br>Sales: ₹%{value:,.0f}"
            "<br>Share: %{percent}"
            "<extra></extra>"
        )

        fig_channel_pie.update_layout(
            template="plotly_white",
            height=430
        )

        st.plotly_chart(
            fig_channel_pie,
            use_container_width=True
        )

    else:

        st.info(
            "Channel data is not available."
        )


# ============================================================
# STORE PERFORMANCE
# ============================================================

st.divider()

st.header("Store Performance")


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
        text="total_value"
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
        template="plotly_white",
        xaxis_title="Store",
        yaxis_title="Sales (₹)",
        height=450
    )

    st.plotly_chart(
        fig_store,
        use_container_width=True
    )

else:

    st.info(
        "Store or sales data is not available."
    )


# ============================================================
# YEAR-WISE SALES
# ============================================================

st.divider()

st.header("Year-wise Sales")


if (
    "year" in filtered_sales.columns
    and "total_value" in filtered_sales.columns
):

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
        text="total_value"
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
        template="plotly_white",
        xaxis_title="Year",
        yaxis_title="Sales (₹)",
        height=430
    )

    st.plotly_chart(
        fig_year,
        use_container_width=True
    )

else:

    st.info(
        "Year or sales data is not available."
    )


# ============================================================
# TOP PRODUCTS
# ============================================================

st.divider()

st.header("Top Products")


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
        textposition="outside",
        hovertemplate=
        "<b>Product %{y}</b>"
        "<br>Sales: ₹%{x:,.0f}"
        "<extra></extra>"
    )

    fig_products.update_layout(
        template="plotly_white",
        xaxis_title="Sales (₹)",
        yaxis_title="Product",
        yaxis={
            "categoryorder": "total ascending"
        },
        height=450
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

else:

    st.info(
        "Product or sales data is not available."
    )


# ============================================================
# SALES DATA TABLE
# ============================================================

st.divider()

st.header("Sales Data")


display_columns = [
    column
    for column in [
        "date",
        "receipt_id",
        "store_id",
        "sku_id",
        "customer_id",
        "quantity",
        "unit_price",
        "total_value",
        "channel",
        "discount_pct",
        "promo_id"
    ]
    if column in filtered_sales.columns
]


if display_columns:

    st.dataframe(
        filtered_sales[display_columns].head(100),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Sales columns are not available."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting | Sales Analytics"
)