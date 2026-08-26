import os
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Product Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL DARK SIDEBAR
# ============================================================

st.markdown(
    """
    <style>

    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }

    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #94A3B8 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #334155 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stAlert"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
    }

    section[data-testid="stSidebar"] label {
        color: #CBD5E1 !important;
    }

    section[data-testid="stSidebar"] input {
        color: #0F172A !important;
    }

    </style>
    """,
    unsafe_allow_html=True
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
# COLORS
# ============================================================

BLUE = "#2563EB"
TEAL = "#0F766E"
GREEN = "#16A34A"
ORANGE = "#F59E0B"
RED = "#DC2626"
PURPLE = "#7C3AED"


# ============================================================
# NUMBER FORMATTING
# ============================================================

def fmt_num(value):

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def fmt_money(value):

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.1f}B"

    if abs(value) >= 1_000_000:
        return f"₹{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"₹{value / 1_000:.1f}K"

    return f"₹{value:,.0f}"


# ============================================================
# LOAD SALES DATA
# ============================================================

@st.cache_data(show_spinner="Loading sales intelligence...") 
def load_sales_data(path):

    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)

    if "date" in df.columns:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

    for column in [
        "total_value",
        "quantity",
        "unit_price"
    ]:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).fillna(0)

    if "sku_id" in df.columns:

        df["sku_id"] = (
            df["sku_id"]
            .astype(str)
        )

    return df


# ============================================================
# LOAD INVENTORY DATA
# ============================================================

@st.cache_data(show_spinner="Loading inventory intelligence...")
def load_inventory_data(path):

    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)

    for column in [
        "stock_on_hand",
        "reorder_point",
        "safety_stock",
        "stock_coverage_days",
        "avg_daily_demand",
        "risk_score"
    ]:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).fillna(0)

    if "sku_id" in df.columns:

        df["sku_id"] = (
            df["sku_id"]
            .astype(str)
        )

    return df


# ============================================================
# LOAD DATA
# ============================================================

sales_df = load_sales_data(
    SALES_PATH
)

inventory_df = load_inventory_data(
    INVENTORY_PATH
)


# ============================================================
# DATA VALIDATION
# ============================================================

if sales_df is None:

    st.error(
        "Sales dataset could not be found."
    )

    st.code(SALES_PATH)

    st.stop()


if "sku_id" not in sales_df.columns:

    st.error(
        "sku_id column is missing from the sales dataset."
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛍️ Retail BI")

    st.caption(
        "PRODUCT INTELLIGENCE"
    )

    st.divider()

    st.subheader("Product Selection")

    products = sorted(
        sales_df["sku_id"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_product = st.selectbox(
        "Select SKU",
        products
    )

    st.divider()

    st.caption(
        "Analysis Modules"
    )

    st.write("📈 Sales Performance")
    st.write("📊 Channel Analysis")
    st.write("🏬 Store Performance")
    st.write("📦 Inventory Intelligence")
    st.write("📋 Transaction History")

    st.divider()

    st.caption(
        f"Available SKUs  •  {len(products):,}"
    )


# ============================================================
# SELECTED PRODUCT
# ============================================================

product_sales = sales_df[
    sales_df["sku_id"] == selected_product
].copy()


if product_sales.empty:

    st.warning(
        "No sales information is available for this SKU."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = (
    product_sales["total_value"].sum()
    if "total_value"
    in product_sales.columns
    else 0
)


total_quantity = (
    product_sales["quantity"].sum()
    if "quantity"
    in product_sales.columns
    else 0
)


transactions = (
    product_sales["receipt_id"].nunique()
    if "receipt_id"
    in product_sales.columns
    else len(product_sales)
)


stores = (
    product_sales["store_id"].nunique()
    if "store_id"
    in product_sales.columns
    else 0
)


channels = (
    product_sales["channel"].nunique()
    if "channel"
    in product_sales.columns
    else 0
)


average_price = (
    total_sales / total_quantity
    if total_quantity > 0
    else 0
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "🛍️ Product Intelligence"
)

st.caption(
    f"Detailed performance, demand and inventory analysis for SKU {selected_product}"
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.subheader(
    "Executive Summary"
)


k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    with st.container(border=True):

        st.metric(
            "Revenue",
            fmt_money(total_sales)
        )

        st.caption(
            "Total product sales"
        )


with k2:

    with st.container(border=True):

        st.metric(
            "Units Sold",
            fmt_num(total_quantity)
        )

        st.caption(
            "Total quantity sold"
        )


with k3:

    with st.container(border=True):

        st.metric(
            "Transactions",
            fmt_num(transactions)
        )

        st.caption(
            "Unique transactions"
        )


with k4:

    with st.container(border=True):

        st.metric(
            "Stores",
            fmt_num(stores)
        )

        st.caption(
            "Selling locations"
        )


with k5:

    with st.container(border=True):

        st.metric(
            "Avg. Unit Price",
            f"₹{average_price:,.2f}"
        )

        st.caption(
            "Revenue per unit"
        )


# ============================================================
# PRODUCT SNAPSHOT
# ============================================================

st.divider()

st.subheader(
    "Product Snapshot"
)


s1, s2, s3, s4 = st.columns(4)


with s1:

    st.info(
        f"**SKU**\n\n{selected_product}"
    )


with s2:

    st.info(
        f"**Sales Channels**\n\n{channels:,}"
    )


with s3:

    if "date" in product_sales.columns:

        first_date = (
            product_sales["date"].min()
        )

        first_text = (
            first_date.strftime("%d %b %Y")
            if pd.notna(first_date)
            else "N/A"
        )

    else:

        first_text = "N/A"

    st.info(
        f"**First Sale**\n\n{first_text}"
    )


with s4:

    if "date" in product_sales.columns:

        last_date = (
            product_sales["date"].max()
        )

        last_text = (
            last_date.strftime("%d %b %Y")
            if pd.notna(last_date)
            else "N/A"
        )

    else:

        last_text = "N/A"

    st.info(
        f"**Latest Sale**\n\n{last_text}"
    )


# ============================================================
# TABS
# ============================================================

tab_sales, tab_channel, tab_store, tab_inventory, tab_data = st.tabs(
    [
        "📈 Sales Performance",
        "📊 Channel Analysis",
        "🏬 Store Performance",
        "📦 Inventory",
        "📋 Transactions"
    ]
)


# ============================================================
# SALES PERFORMANCE
# ============================================================

with tab_sales:

    st.subheader(
        "Revenue Performance"
    )

    st.caption(
        "Historical revenue movement for the selected product"
    )

    if (
        "date" in product_sales.columns
        and "total_value"
        in product_sales.columns
    ):

        daily_sales = (
            product_sales
            .groupby(
                "date",
                as_index=False
            )["total_value"]
            .sum()
            .sort_values("date")
        )

        fig_sales = px.area(
            daily_sales,
            x="date",
            y="total_value"
        )

        fig_sales.update_traces(
            line_color=BLUE,
            fillcolor="rgba(37,99,235,0.15)"
        )

        fig_sales.update_layout(
            template="plotly_white",
            height=430,
            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),
            xaxis_title=None,
            yaxis_title="Revenue (₹)",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_sales,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


    st.subheader(
        "Demand Trend"
    )

    if (
        "date" in product_sales.columns
        and "quantity"
        in product_sales.columns
    ):

        daily_quantity = (
            product_sales
            .groupby(
                "date",
                as_index=False
            )["quantity"]
            .sum()
            .sort_values("date")
        )

        fig_quantity = px.line(
            daily_quantity,
            x="date",
            y="quantity"
        )

        fig_quantity.update_traces(
            line_color=TEAL,
            line_width=3
        )

        fig_quantity.update_layout(
            template="plotly_white",
            height=350,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),
            xaxis_title=None,
            yaxis_title="Units"
        )

        st.plotly_chart(
            fig_quantity,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# CHANNEL ANALYSIS
# ============================================================

with tab_channel:

    st.subheader(
        "Channel Performance"
    )

    if (
        "channel"
        in product_sales.columns
        and "total_value"
        in product_sales.columns
    ):

        channel_sales = (
            product_sales
            .groupby(
                "channel",
                as_index=False
            )["total_value"]
            .sum()
            .sort_values(
                "total_value",
                ascending=False
            )
        )

        left, right = st.columns(
            [1.5, 1]
        )

        with left:

            fig_channel = px.bar(
                channel_sales,
                x="channel",
                y="total_value",
                color="channel",
                text="total_value",
                color_discrete_sequence=[
                    BLUE,
                    TEAL,
                    PURPLE,
                    ORANGE,
                    RED
                ]
            )

            fig_channel.update_traces(
                texttemplate="₹%{y:,.0f}",
                textposition="outside"
            )

            fig_channel.update_layout(
                template="plotly_white",
                height=450,
                showlegend=False,
                xaxis_title=None,
                yaxis_title="Revenue (₹)"
            )

            st.plotly_chart(
                fig_channel,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        with right:

            fig_pie = px.pie(
                channel_sales,
                names="channel",
                values="total_value",
                hole=0.55,
                color_discrete_sequence=[
                    BLUE,
                    TEAL,
                    PURPLE,
                    ORANGE,
                    RED
                ]
            )

            fig_pie.update_traces(
                textinfo="percent+label"
            )

            fig_pie.update_layout(
                template="plotly_white",
                height=450,
                showlegend=False
            )

            st.plotly_chart(
                fig_pie,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )


# ============================================================
# STORE PERFORMANCE
# ============================================================

with tab_store:

    st.subheader(
        "Store Performance"
    )

    st.caption(
        "Top performing stores for the selected SKU"
    )

    if (
        "store_id"
        in product_sales.columns
        and "total_value"
        in product_sales.columns
    ):

        store_sales = (
            product_sales
            .groupby(
                "store_id",
                as_index=False
            )["total_value"]
            .sum()
            .sort_values(
                "total_value",
                ascending=False
            )
            .head(20)
        )

        fig_store = px.bar(
            store_sales,
            x="store_id",
            y="total_value",
            color="total_value",
            color_continuous_scale=[
                "#DBEAFE",
                BLUE
            ],
            text="total_value"
        )

        fig_store.update_traces(
            texttemplate="₹%{y:,.0f}",
            textposition="outside"
        )

        fig_store.update_layout(
            template="plotly_white",
            height=500,
            coloraxis_showscale=False,
            xaxis_title="Store",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(
            fig_store,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# INVENTORY INTELLIGENCE
# ============================================================

with tab_inventory:

    st.subheader(
        "Inventory Intelligence"
    )

    if inventory_df is None:

        st.warning(
            "Inventory dataset is not available."
        )

    else:

        product_inventory = inventory_df[
            inventory_df["sku_id"]
            == selected_product
        ].copy()

        if product_inventory.empty:

            st.info(
                "No inventory information is available for this SKU."
            )

        else:

            stock = (
                product_inventory[
                    "stock_on_hand"
                ].sum()
                if "stock_on_hand"
                in product_inventory.columns
                else 0
            )

            reorder = (
                product_inventory[
                    "reorder_point"
                ].sum()
                if "reorder_point"
                in product_inventory.columns
                else 0
            )

            coverage = (
                product_inventory[
                    "stock_coverage_days"
                ].mean()
                if "stock_coverage_days"
                in product_inventory.columns
                else 0
            )

            risk = (
                str(
                    product_inventory[
                        "final_risk_level"
                    ].iloc[0]
                )
                if "final_risk_level"
                in product_inventory.columns
                else "Not Available"
            )


            i1, i2, i3, i4 = st.columns(4)


            with i1:

                st.metric(
                    "Stock on Hand",
                    fmt_num(stock)
                )


            with i2:

                st.metric(
                    "Reorder Point",
                    fmt_num(reorder)
                )


            with i3:

                st.metric(
                    "Stock Coverage",
                    f"{coverage:.1f} days"
                )


            with i4:

                risk_lower = risk.lower()

                if "critical" in risk_lower:

                    st.error(
                        f"🔴 {risk}"
                    )

                elif "high" in risk_lower:

                    st.warning(
                        f"🟠 {risk}"
                    )

                elif "medium" in risk_lower:

                    st.warning(
                        f"🟡 {risk}"
                    )

                else:

                    st.success(
                        f"🟢 {risk}"
                    )


            st.divider()

            st.subheader(
                "Stock Position"
            )


            inventory_chart = pd.DataFrame(
                {
                    "Metric": [
                        "Stock on Hand",
                        "Reorder Point"
                    ],
                    "Units": [
                        stock,
                        reorder
                    ]
                }
            )


            fig_inventory = px.bar(
                inventory_chart,
                x="Metric",
                y="Units",
                color="Metric",
                text="Units",
                color_discrete_sequence=[
                    TEAL,
                    ORANGE
                ]
            )


            fig_inventory.update_traces(
                texttemplate="%{y:,.0f}",
                textposition="outside"
            )


            fig_inventory.update_layout(
                template="plotly_white",
                height=380,
                showlegend=False,
                xaxis_title=None,
                yaxis_title="Units"
            )


            st.plotly_chart(
                fig_inventory,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )


# ============================================================
# TRANSACTION HISTORY
# ============================================================

with tab_data:

    st.subheader(
        "Transaction History"
    )

    st.caption(
        "Latest 100 transactions for the selected product"
    )


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


    transactions_df = (
        product_sales[
            display_columns
        ]
        .sort_values(
            "date",
            ascending=False
        )
        .head(100)
        .copy()
    )


    st.dataframe(
        transactions_df,
        use_container_width=True,
        hide_index=True,
        height=520
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

footer_left, footer_right = st.columns(2)


with footer_left:

    st.caption(
        "Retail Demand Forecasting • Product Intelligence"
    )


with footer_right:

    st.caption(
        f"Active SKU: {selected_product}"
    )
