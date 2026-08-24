import os
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Product Details",
    page_icon="🛍️",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

SALES_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "sales_transactions_cleaned.csv"
)

INVENTORY_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "inventory_risk_scoring.csv"
)


# ============================================================
# LOAD SALES DATA
# ============================================================

@st.cache_data
def load_sales_data():

    if not os.path.exists(SALES_PATH):
        return None

    return pd.read_csv(SALES_PATH)


# ============================================================
# LOAD INVENTORY DATA
# ============================================================

@st.cache_data
def load_inventory_data():

    if not os.path.exists(INVENTORY_PATH):
        return None

    return pd.read_csv(INVENTORY_PATH)


sales_df = load_sales_data()
inventory_df = load_inventory_data()


# ============================================================
# DATA CHECK
# ============================================================

if sales_df is None:

    st.error(
        "Sales dataset could not be found."
    )

    st.code(SALES_PATH)

    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🛍️ Product Details")

st.caption(
    "Analyze individual product performance, sales activity "
    "and inventory position."
)

st.divider()


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


# ============================================================
# PRODUCT SELECTION
# ============================================================

st.header("Select Product")


if "sku_id" not in sales_df.columns:

    st.error(
        "sku_id column is not available in the sales dataset."
    )

    st.stop()


products = sorted(
    sales_df["sku_id"]
    .dropna()
    .astype(str)
    .unique()
)


selected_product = st.selectbox(
    "Choose a SKU",
    products
)


# ============================================================
# FILTER SELECTED PRODUCT
# ============================================================

product_sales = sales_df[
    sales_df["sku_id"].astype(str)
    == selected_product
].copy()


if product_sales.empty:

    st.warning(
        "No sales data available for this product."
    )

    st.stop()


# ============================================================
# PRODUCT KPIs
# ============================================================

total_sales = (
    product_sales["total_value"].sum()
    if "total_value" in product_sales.columns
    else 0
)


total_quantity = (
    product_sales["quantity"].sum()
    if "quantity" in product_sales.columns
    else 0
)


transactions = (
    product_sales["receipt_id"].nunique()
    if "receipt_id" in product_sales.columns
    else len(product_sales)
)


stores = (
    product_sales["store_id"].nunique()
    if "store_id" in product_sales.columns
    else 0
)


average_price = (
    total_sales / total_quantity
    if total_quantity > 0
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
    "Quantity Sold",
    f"{total_quantity:,.0f}"
)


kpi3.metric(
    "Transactions",
    f"{transactions:,}"
)


kpi4.metric(
    "Stores",
    f"{stores:,}"
)


kpi5.metric(
    "Average Price",
    f"₹{average_price:,.2f}"
)


# ============================================================
# PRODUCT INFORMATION
# ============================================================

st.divider()

st.header("Product Information")


info1, info2, info3 = st.columns(3)


info1.metric(
    "SKU",
    selected_product
)


if "channel" in product_sales.columns:

    channel_count = (
        product_sales["channel"]
        .nunique()
    )

else:

    channel_count = 0


info2.metric(
    "Sales Channels",
    f"{channel_count:,}"
)


if "date" in product_sales.columns:

    first_date = product_sales["date"].min()
    last_date = product_sales["date"].max()

    date_range = (
        f"{first_date:%d %b %Y}"
        if pd.notna(first_date)
        else "N/A"
    )

else:

    date_range = "N/A"


info3.metric(
    "First Sales Date",
    date_range
)


# ============================================================
# SALES TREND
# ============================================================

st.divider()

st.header("Product Sales Trend")


if (
    "date" in product_sales.columns
    and "total_value" in product_sales.columns
):

    daily_sales = (
        product_sales
        .groupby("date")["total_value"]
        .sum()
        .reset_index()
        .sort_values("date")
    )


    fig_sales = px.line(
        daily_sales,
        x="date",
        y="total_value",
        title=f"Daily Sales — {selected_product}"
    )


    fig_sales.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Sales (₹)",
        height=450
    )


    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )


# ============================================================
# QUANTITY TREND
# ============================================================

st.header("Product Quantity Trend")


if (
    "date" in product_sales.columns
    and "quantity" in product_sales.columns
):

    daily_quantity = (
        product_sales
        .groupby("date")["quantity"]
        .sum()
        .reset_index()
        .sort_values("date")
    )


    fig_quantity = px.line(
        daily_quantity,
        x="date",
        y="quantity",
        title=f"Daily Quantity Sold — {selected_product}"
    )


    fig_quantity.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Quantity",
        height=450
    )


    st.plotly_chart(
        fig_quantity,
        use_container_width=True
    )


# ============================================================
# SALES BY CHANNEL
# ============================================================

if (
    "channel" in product_sales.columns
    and "total_value" in product_sales.columns
):

    st.divider()

    st.header("Sales by Channel")


    channel_sales = (
        product_sales
        .groupby("channel")["total_value"]
        .sum()
        .reset_index()
        .sort_values(
            "total_value",
            ascending=False
        )
    )


    channel_left, channel_right = st.columns(2)


    with channel_left:

        fig_channel = px.bar(
            channel_sales,
            x="channel",
            y="total_value",
            text="total_value",
            title="Sales by Channel"
        )


        fig_channel.update_traces(
            texttemplate="₹%{y:,.0f}",
            textposition="outside"
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


    with channel_right:

        fig_channel_pie = px.pie(
            channel_sales,
            names="channel",
            values="total_value",
            hole=0.45,
            title="Channel Sales Distribution"
        )


        fig_channel_pie.update_layout(
            template="plotly_white",
            height=430
        )


        st.plotly_chart(
            fig_channel_pie,
            use_container_width=True
        )


# ============================================================
# SALES BY STORE
# ============================================================

if (
    "store_id" in product_sales.columns
    and "total_value" in product_sales.columns
):

    st.divider()

    st.header("Sales by Store")


    store_sales = (
        product_sales
        .groupby("store_id")["total_value"]
        .sum()
        .reset_index()
        .sort_values(
            "total_value",
            ascending=False
        )
    )


    fig_store = px.bar(
        store_sales,
        x="store_id",
        y="total_value",
        text="total_value",
        title=f"Store Performance — {selected_product}"
    )


    fig_store.update_traces(
        texttemplate="₹%{y:,.0f}",
        textposition="outside"
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


# ============================================================
# INVENTORY INFORMATION
# ============================================================

if inventory_df is not None:

    if "sku_id" in inventory_df.columns:

        product_inventory = inventory_df[
            inventory_df["sku_id"].astype(str)
            == selected_product
        ].copy()


        if not product_inventory.empty:

            st.divider()

            st.header("Inventory Position")


            if "stock_on_hand" in product_inventory.columns:

                stock = pd.to_numeric(
                    product_inventory["stock_on_hand"],
                    errors="coerce"
                ).fillna(0).sum()

            else:

                stock = 0


            if "reorder_point" in product_inventory.columns:

                reorder_point = pd.to_numeric(
                    product_inventory["reorder_point"],
                    errors="coerce"
                ).fillna(0).sum()

            else:

                reorder_point = 0


            if "stock_coverage_days" in product_inventory.columns:

                coverage = pd.to_numeric(
                    product_inventory["stock_coverage_days"],
                    errors="coerce"
                ).fillna(0).mean()

            else:

                coverage = 0


            if "final_risk_level" in product_inventory.columns:

                risk_level = (
                    product_inventory["final_risk_level"]
                    .astype(str)
                    .iloc[0]
                )

            else:

                risk_level = "Not Available"


            inv1, inv2, inv3, inv4 = st.columns(4)


            inv1.metric(
                "Stock on Hand",
                f"{stock:,.0f}"
            )


            inv2.metric(
                "Reorder Point",
                f"{reorder_point:,.0f}"
            )


            inv3.metric(
                "Stock Coverage",
                f"{coverage:.1f} days"
            )


            inv4.metric(
                "Risk Level",
                risk_level
            )


# ============================================================
# PRODUCT DATA TABLE
# ============================================================

st.divider()

st.header("Product Transaction Details")


display_columns = [
    "date",
    "receipt_id",
    "store_id",
    "sku_id",
    "quantity",
    "unit_price",
    "total_value",
    "channel"
]


display_columns = [
    column
    for column in display_columns
    if column in product_sales.columns
]


st.dataframe(
    product_sales[display_columns]
    .sort_values(
        "date",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting | Product Details"
)
