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
# PROFESSIONAL STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 90% 0%,
                rgba(37, 99, 235, 0.08),
                transparent 25%
            ),
            #F4F7FB;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* ========================================================
       TYPOGRAPHY
       ======================================================== */

    h1 {
        color: #0B1F3A !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #102A43 !important;
        font-size: 1.45rem !important;
        font-weight: 750 !important;
        margin-top: 1.5rem !important;
    }

    h3 {
        color: #183B56 !important;
        font-weight: 700 !important;
    }

    p {
        color: #52667A;
        line-height: 1.6;
    }

    /* ========================================================
       HEADER
       ======================================================== */

    div[data-testid="stTitle"] {
        background:
            linear-gradient(
                135deg,
                #0B1F3A 0%,
                #123E67 60%,
                #1565A3 100%
            );

        padding: 1.8rem 2rem;
        border-radius: 18px;

        box-shadow:
            0 12px 35px rgba(11, 31, 58, 0.16);

        margin-bottom: 0.7rem;
    }

    div[data-testid="stTitle"] h1 {
        color: white !important;
        margin-bottom: 0 !important;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0B1F3A 0%,
                #102A43 55%,
                #0A1D35 100%
            );

        border-right: none;
    }

    section[data-testid="stSidebar"] h1 {
        color: white !important;
        font-size: 1.3rem !important;
    }

    section[data-testid="stSidebar"] p {
        color: #B7C8D9 !important;
    }

    section[data-testid="stSidebar"] label {
        color: #DCE8F3 !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.12) !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 9px !important;
    }

    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #FFFFFF,
                #F8FAFD
            );

        border: 1px solid #E0E7EF;
        border-radius: 15px;

        padding: 1.1rem 1.2rem;
        min-height: 115px;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.05);

        position: relative;
        overflow: hidden;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]::before {
        content: "";

        position: absolute;
        top: 0;
        left: 0;

        width: 100%;
        height: 4px;

        background:
            linear-gradient(
                90deg,
                #2563EB,
                #06B6D4
            );
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);

        box-shadow:
            0 12px 28px rgba(15,39,71,0.09);
    }

    div[data-testid="stMetricLabel"] {
        color: #718398 !important;
        font-size: 0.78rem !important;
        font-weight: 650 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #102A43 !important;
        font-size: 1.45rem !important;
        font-weight: 800 !important;
    }

    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .section-title {
        font-size: 1.15rem;
        font-weight: 750;
        color: #102A43;

        padding-left: 12px;

        border-left: 4px solid #2563EB;

        margin-top: 1.4rem;
        margin-bottom: 0.7rem;
    }

    /* ========================================================
       CHARTS
       ======================================================== */

    div[data-testid="stPlotlyChart"] {
        background: white;

        border: 1px solid #E1E8F0;
        border-radius: 15px;

        padding: 7px;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.045);
    }

    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border: none !important;
        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                #D5DEE8,
                transparent
            ) !important;

        margin: 1.4rem 0 !important;
    }

    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar {
        width: 7px;
        height: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #EEF2F6;
    }

    ::-webkit-scrollbar-thumb {
        background: #94A3B8;
        border-radius: 10px;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {
        text-align: center;
        color: #8191A1;

        font-size: 0.75rem;

        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT PATH
# ============================================================

from pathlib import Path

# This file is:
# dashboard/pages/1_Sales_Analytics.py
#
# Therefore:
# parents[0] = pages
# parents[1] = dashboard
# parents[2] = project root
#
# Project root:
# Online-retail-demand-forcasting/

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEPLOYMENT_PATH = PROJECT_ROOT / "data" / "deployment"

DAILY_PATH = DEPLOYMENT_PATH / "daily_sales_dashboard.csv"
STORE_PATH = DEPLOYMENT_PATH / "store_sales_dashboard.csv"
CHANNEL_PATH = DEPLOYMENT_PATH / "channel_sales_dashboard.csv"
YEARLY_PATH = DEPLOYMENT_PATH / "yearly_sales_dashboard.csv"
# ============================================================
# LOAD DEPLOYMENT DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_deployment_data():

    daily = pd.read_csv(DAILY_PATH)
    store = pd.read_csv(STORE_PATH)
    channel = pd.read_csv(CHANNEL_PATH)
    yearly = pd.read_csv(YEARLY_PATH)

    # --------------------------------------------------------
    # DAILY DATA
    # --------------------------------------------------------

    if "date" in daily.columns:
        daily["date"] = pd.to_datetime(
            daily["date"],
            errors="coerce"
        )

    daily_numeric_columns = [
        "year",
        "total_value",
        "quantity",
        "transactions",
        "active_stores",
        "active_products"
    ]

    for col in daily_numeric_columns:
        if col in daily.columns:
            daily[col] = pd.to_numeric(
                daily[col],
                errors="coerce"
            ).fillna(0)

    # --------------------------------------------------------
    # STORE DATA
    # --------------------------------------------------------

    store_numeric_columns = [
        "year",
        "total_value",
        "quantity",
        "transactions"
    ]

    for col in store_numeric_columns:
        if col in store.columns:
            store[col] = pd.to_numeric(
                store[col],
                errors="coerce"
            ).fillna(0)

    # --------------------------------------------------------
    # CHANNEL DATA
    # --------------------------------------------------------

    channel_numeric_columns = [
        "year",
        "total_value",
        "quantity",
        "transactions"
    ]

    for col in channel_numeric_columns:
        if col in channel.columns:
            channel[col] = pd.to_numeric(
                channel[col],
                errors="coerce"
            ).fillna(0)

    # --------------------------------------------------------
    # YEARLY DATA
    # --------------------------------------------------------

    yearly_numeric_columns = [
        "year",
        "total_value",
        "quantity",
        "transactions"
    ]

    for col in yearly_numeric_columns:
        if col in yearly.columns:
            yearly[col] = pd.to_numeric(
                yearly[col],
                errors="coerce"
            ).fillna(0)

    return daily, store, channel, yearly


# ============================================================
# LOAD DATA SAFELY
# ============================================================

try:

    daily_df, store_df, channel_df, yearly_df = (
        load_deployment_data()
    )

except Exception as e:

    st.error(
        "Unable to load the Sales Analytics deployment data."
    )

    st.write("Expected deployment folder:")

    st.code(
        "data/deployment/"
    )

    st.write("Error:")

    st.code(str(e))

    st.stop()


# ============================================================
# BASIC COLUMN VALIDATION
# ============================================================

required_daily_columns = [
    "date",
    "year",
    "channel",
    "total_value",
    "quantity",
    "transactions",
    "active_stores",
    "active_products"
]

missing_daily_columns = [
    col
    for col in required_daily_columns
    if col not in daily_df.columns
]

if missing_daily_columns:

    st.error(
        "The daily deployment dataset is missing required columns."
    )

    st.write(
        "Missing columns:"
    )

    st.code(
        ", ".join(missing_daily_columns)
    )

    st.stop()


# ============================================================
# NUMBER FORMATTERS
# ============================================================

def format_number(value):

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    elif abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def format_currency(value):

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.2f}B"

    elif abs(value) >= 1_000_000:
        return f"₹{value / 1_000_000:.2f}M"

    elif abs(value) >= 1_000:
        return f"₹{value / 1_000:.1f}K"

    return f"₹{value:,.0f}"


# ============================================================
# HEADER
# ============================================================

st.title("📊 Sales Analytics")

st.caption(
    "Retail sales performance, transaction behaviour, "
    "channels, stores and revenue trends."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Sales Filters")

st.sidebar.caption(
    "Filter the dashboard to analyze specific periods "
    "and sales channels."
)

st.sidebar.divider()


# ============================================================
# YEAR FILTER
# ============================================================

years = sorted(
    daily_df["year"]
    .dropna()
    .unique()
    .tolist()
)

years = [
    int(year)
    for year in years
]

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)


# ============================================================
# CHANNEL FILTER
# ============================================================

channels = sorted(
    daily_df["channel"]
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


# ============================================================
# FILTER DAILY DATA
# ============================================================

filtered_daily = daily_df.copy()

if selected_years:

    filtered_daily = filtered_daily[
        filtered_daily["year"].isin(selected_years)
    ]

if selected_channels:

    filtered_daily = filtered_daily[
        filtered_daily["channel"].isin(
            selected_channels
        )
    ]


# ============================================================
# FILTER STORE DATA
# ============================================================

filtered_store = store_df.copy()

if "year" in filtered_store.columns:

    if selected_years:

        filtered_store = filtered_store[
            filtered_store["year"].isin(selected_years)
        ]

if "channel" in filtered_store.columns:

    if selected_channels:

        filtered_store = filtered_store[
            filtered_store["channel"].isin(
                selected_channels
            )
        ]


# ============================================================
# FILTER CHANNEL DATA
# ============================================================

filtered_channel = channel_df.copy()

if "year" in filtered_channel.columns:

    if selected_years:

        filtered_channel = filtered_channel[
            filtered_channel["year"].isin(selected_years)
        ]

if "channel" in filtered_channel.columns:

    if selected_channels:

        filtered_channel = filtered_channel[
            filtered_channel["channel"].isin(
                selected_channels
            )
        ]


# ============================================================
# FILTER YEARLY DATA
# ============================================================

filtered_yearly = yearly_df.copy()

if "year" in filtered_yearly.columns:

    if selected_years:

        filtered_yearly = filtered_yearly[
            filtered_yearly["year"].isin(selected_years)
        ]

# IMPORTANT:
# yearly_sales_dashboard.csv may NOT contain a channel column.
# Therefore we only filter it by channel when that column exists.

if "channel" in filtered_yearly.columns:

    if selected_channels:

        filtered_yearly = filtered_yearly[
            filtered_yearly["channel"].isin(
                selected_channels
            )
        ]


# ============================================================
# EMPTY CHECK
# ============================================================

if filtered_daily.empty:

    st.warning(
        "No sales records match the selected filters."
    )

    st.stop()


# ============================================================
# ACTIVE FILTER STATUS
# ============================================================

filter_year_text = (
    "All Years"
    if not selected_years
    else ", ".join(
        str(int(year))
        for year in selected_years
    )
)

filter_channel_text = (
    "All Channels"
    if not selected_channels
    else ", ".join(selected_channels)
)

st.info(
    f"Showing data for: {filter_year_text}  |  "
    f"Channels: {filter_channel_text}"
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = (
    filtered_daily["total_value"].sum()
)

transactions = (
    filtered_daily["transactions"].sum()
)

total_quantity = (
    filtered_daily["quantity"].sum()
)

stores = (
    filtered_daily["active_stores"].max()
)

products = (
    filtered_daily["active_products"].max()
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


with k1:

    st.metric(
        "💰 Total Sales",
        format_currency(total_sales)
    )


with k2:

    st.metric(
        "🧾 Transactions",
        format_number(transactions)
    )


with k3:

    st.metric(
        "📦 Quantity Sold",
        format_number(total_quantity)
    )


with k4:

    st.metric(
        "🏬 Active Stores",
        format_number(stores)
    )


with k5:

    st.metric(
        "🛒 Avg. Order Value",
        format_currency(average_order_value)
    )


# ============================================================
# SALES TREND
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📈 Sales Trend</div>',
    unsafe_allow_html=True
)

st.caption(
    "Daily sales movement across the selected period."
)


daily_sales = (
    filtered_daily
    .groupby("date", sort=True)["total_value"]
    .sum()
    .reset_index()
)


fig_sales = px.line(
    daily_sales,
    x="date",
    y="total_value"
)


fig_sales.update_traces(

    line=dict(
        color="#2563EB",
        width=3
    ),

    fill="tozeroy",

    fillcolor="rgba(37,99,235,0.08)",

    hovertemplate=
    "<b>%{x|%d %b %Y}</b>"
    "<br>Sales: ₹%{y:,.0f}"
    "<extra></extra>"
)


fig_sales.update_layout(

    height=430,

    template="plotly_white",

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="",
        showgrid=False
    ),

    yaxis=dict(
        title="Sales (₹)",
        gridcolor="#EEF2F6"
    ),

    hovermode="x unified",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white"
)


st.plotly_chart(

    fig_sales,

    use_container_width=True,

    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# CHANNEL ANALYSIS
# ============================================================

st.divider()

left, right = st.columns(2)


# ============================================================
# CHANNEL SALES
# ============================================================

with left:

    st.markdown(
        '<div class="section-title">📊 Sales by Channel</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Revenue contribution by sales channel."
    )

    if (
        "channel" in filtered_channel.columns
        and "total_value" in filtered_channel.columns
    ):

        channel_sales = (
            filtered_channel
            .groupby("channel")["total_value"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

    else:

        channel_sales = pd.DataFrame(
            columns=[
                "channel",
                "total_value"
            ]
        )

    if not channel_sales.empty:

        fig_channel = px.bar(
            channel_sales,
            x="channel",
            y="total_value"
        )


        fig_channel.update_traces(

            marker_color="#2563EB",

            hovertemplate=
            "<b>%{x}</b>"
            "<br>Sales: ₹%{y:,.0f}"
            "<extra></extra>"
        )


        fig_channel.update_layout(

            height=400,

            template="plotly_white",

            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),

            xaxis=dict(
                title="",
                showgrid=False
            ),

            yaxis=dict(
                title="Sales (₹)",
                gridcolor="#EEF2F6"
            ),

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="white"
        )


        st.plotly_chart(

            fig_channel,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "Channel sales data is not available."
        )


# ============================================================
# CHANNEL DISTRIBUTION
# ============================================================

with right:

    st.markdown(
        '<div class="section-title">◉ Channel Distribution</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Share of total sales by channel."
    )

    if not channel_sales.empty:

        fig_channel_pie = px.pie(

            channel_sales,

            names="channel",

            values="total_value",

            hole=0.55
        )


        fig_channel_pie.update_traces(

            textposition="inside",

            textinfo="percent",

            marker=dict(
                colors=[
                    "#2563EB",
                    "#06B6D4",
                    "#14B8A6",
                    "#8B5CF6",
                    "#F59E0B"
                ]
            ),

            hovertemplate=
            "<b>%{label}</b>"
            "<br>Sales: ₹%{value:,.0f}"
            "<br>Share: %{percent}"
            "<extra></extra>"
        )


        fig_channel_pie.update_layout(

            height=400,

            template="plotly_white",

            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="white",

            showlegend=True
        )


        st.plotly_chart(

            fig_channel_pie,

            use_container_width=True,

            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "Channel distribution data is not available."
        )


# ============================================================
# STORE PERFORMANCE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🏬 Store Performance</div>',
    unsafe_allow_html=True
)

st.caption(
    "Top-performing stores ranked by total sales."
)


if (
    "store_id" in filtered_store.columns
    and "total_value" in filtered_store.columns
):

    store_sales = (
        filtered_store
        .groupby("store_id")["total_value"]
        .sum()
        .sort_values(ascending=True)
        .tail(15)
        .reset_index()
    )

else:

    store_sales = pd.DataFrame(
        columns=[
            "store_id",
            "total_value"
        ]
    )


if not store_sales.empty:

    fig_store = px.bar(

        store_sales,

        x="total_value",

        y="store_id",

        orientation="h"
    )


    fig_store.update_traces(

        marker_color="#0EA5E9",

        hovertemplate=
        "<b>Store %{y}</b>"
        "<br>Sales: ₹%{x:,.0f}"
        "<extra></extra>"
    )


    fig_store.update_layout(

        height=500,

        template="plotly_white",

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        xaxis=dict(
            title="Sales (₹)",
            gridcolor="#EEF2F6"
        ),

        yaxis=dict(
            title="Store",
            showgrid=False
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="white"
    )


    st.plotly_chart(

        fig_store,

        use_container_width=True,

        config={
            "displayModeBar": False
        }
    )

else:

    st.info(
        "Store performance data is not available."
    )


# ============================================================
# YEAR-WISE SALES
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📅 Year-wise Sales</div>',
    unsafe_allow_html=True
)

st.caption(
    "Annual revenue comparison."
)


if (
    "year" in filtered_yearly.columns
    and "total_value" in filtered_yearly.columns
):

    yearly_sales = (
        filtered_yearly
        .groupby("year")["total_value"]
        .sum()
        .reset_index()
        .sort_values("year")
    )

else:

    yearly_sales = pd.DataFrame(
        columns=[
            "year",
            "total_value"
        ]
    )


if not yearly_sales.empty:

    fig_year = px.bar(

        yearly_sales,

        x="year",

        y="total_value"
    )


    fig_year.update_traces(

        marker_color="#14B8A6",

        hovertemplate=
        "<b>%{x}</b>"
        "<br>Sales: ₹%{y:,.0f}"
        "<extra></extra>"
    )


    fig_year.update_layout(

        height=400,

        template="plotly_white",

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        xaxis=dict(
            title="Year",
            showgrid=False
        ),

        yaxis=dict(
            title="Sales (₹)",
            gridcolor="#EEF2F6"
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="white"
    )


    st.plotly_chart(

        fig_year,

        use_container_width=True,

        config={
            "displayModeBar": False
        }
    )

else:

    st.info(
        "Year-wise sales data is not available."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer-text">'
    'Retail Demand Forecasting | Sales Analytics'
    '</div>',
    unsafe_allow_html=True
)