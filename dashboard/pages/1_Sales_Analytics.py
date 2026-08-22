import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PROFESSIONAL STYLE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F6F8FB;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 3px 10px rgba(15,39,71,0.05);
    }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    .section-title {
        font-size: 21px;
        font-weight: 700;
        color: #17324D;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SALES DATA PATH
# ============================================================

DATA_PATH = (
    r"C:\Users\Pawan\OneDrive\Desktop\Online-Retail-II"
    r"\Online-retail-demand-forcasting\data\processed"
    r"\sales_transactions_cleaned.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_sales_data():

    return pd.read_csv(DATA_PATH)


try:

    sales_df = load_sales_data()

except Exception as e:

    st.error("Unable to load the sales dataset.")

    st.write("Expected location:")

    st.code(DATA_PATH)

    st.write("Error:")

    st.code(str(e))

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
# HEADER
# ============================================================

st.title("📊 Sales Analytics")

st.caption(
    "Analyze retail sales performance, transactions, channels and stores."
)
unsafe_allow_html=True



# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Sales Filters")

years = sorted(
    sales_df["year"]
    .dropna()
    .unique()
    .tolist()
)

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)


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
# FILTER DATA
# ============================================================

filtered_sales = sales_df.copy()


if selected_years:

    filtered_sales = filtered_sales[
        filtered_sales["year"].isin(selected_years)
    ]


if selected_channels and "channel" in filtered_sales.columns:

    filtered_sales = filtered_sales[
        filtered_sales["channel"].isin(selected_channels)
    ]


if filtered_sales.empty:

    st.warning(
        "No sales records match the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = (
    filtered_sales["total_value"].sum()
    if "total_value" in filtered_sales.columns
    else 0
)


if "receipt_id" in filtered_sales.columns:

    transactions = filtered_sales["receipt_id"].nunique()

else:

    transactions = len(filtered_sales)


total_quantity = (
    filtered_sales["quantity"].sum()
    if "quantity" in filtered_sales.columns
    else 0
)


stores = (
    filtered_sales["store_id"].nunique()
    if "store_id" in filtered_sales.columns
    else 0
)


products = (
    filtered_sales["sku_id"].nunique()
    if "sku_id" in filtered_sales.columns
    else 0
)


average_order_value = (
    total_sales / transactions
    if transactions > 0
    else 0
)


# ============================================================
# SALES OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">Sales Overview</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4, k5 = st.columns(5)


k1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)

k2.metric(
    "Transactions",
    f"{transactions:,}"
)

k3.metric(
    "Quantity Sold",
    f"{total_quantity:,.0f}"
)

k4.metric(
    "Stores",
    f"{stores:,}"
)

k5.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)


# ============================================================
# SALES TREND
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Sales Trend</div>',
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


# ============================================================
# CHANNEL ANALYSIS
# ============================================================

st.divider()

left, right = st.columns(2)


with left:

    st.markdown(
        '<div class="section-title">Sales by Channel</div>',
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

        fig_channel = px.bar(
            channel_sales,
            x="channel",
            y="total_value",
            title="Sales by Channel",
            text="total_value"
        )

        fig_channel.update_traces(
            texttemplate="₹%{y:,.0f}",
            textposition="outside"
        )

        fig_channel.update_layout(
            template="plotly_white",
            xaxis_title="Channel",
            yaxis_title="Sales (₹)",
            height=420
        )

        st.plotly_chart(
            fig_channel,
            use_container_width=True
        )


with right:

    st.markdown(
        '<div class="section-title">Channel Distribution</div>',
        unsafe_allow_html=True
    )

    if (
        "channel" in filtered_sales.columns
        and "total_value" in filtered_sales.columns
    ):

        fig_channel_pie = px.pie(
            channel_sales,
            names="channel",
            values="total_value",
            hole=0.45,
            title="Sales Distribution by Channel"
        )

        fig_channel_pie.update_traces(
            textposition="inside",
            textinfo="percent"
        )

        fig_channel_pie.update_layout(
            template="plotly_white",
            height=420
        )

        st.plotly_chart(
            fig_channel_pie,
            use_container_width=True
        )


# ============================================================
# STORE PERFORMANCE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Store Performance</div>',
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
        .sort_values(ascending=False)
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
# YEAR-WISE SALES
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">Year-wise Sales</div>',
    unsafe_allow_html=True
)


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
    textposition="outside"
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


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting | Sales Analytics"
)