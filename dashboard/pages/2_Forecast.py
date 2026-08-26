import os
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Demand Forecast",
    page_icon="🔮",
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
       PAGE TITLE
       ======================================================== */

    div[data-testid="stTitle"] {
        background:
            linear-gradient(
                135deg,
                #0B1F3A 0%,
                #123E67 55%,
                #2563A6 100%
            );

        padding: 1.8rem 2rem;

        border-radius: 18px;

        box-shadow:
            0 12px 35px rgba(11, 31, 58, 0.16);

        margin-bottom: 0.7rem;
    }

    div[data-testid="stTitle"] h1 {
        color: #FFFFFF !important;
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

        box-shadow:
            8px 0 30px rgba(15, 23, 42, 0.12);
    }

    section[data-testid="stSidebar"] h1 {
        color: #FFFFFF !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] p {
        color: #B7C8D9 !important;
        font-size: 0.8rem !important;
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
       KPI CARDS
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

        padding: 1.15rem 1.2rem;

        min-height: 120px;

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
       SECTION TITLES
       ======================================================== */

    .section-title {
        font-size: 1.15rem;
        font-weight: 750;
        color: #102A43;
        padding-left: 12px;
        border-left: 4px solid #2563EB;
        margin-top: 1.4rem;
        margin-bottom: 0.5rem;
    }


    /* ========================================================
       PLOTLY CHART CONTAINERS
       ======================================================== */

    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;

        border: 1px solid #E1E8F0;

        border-radius: 15px;

        padding: 7px;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.045);
    }


    /* ========================================================
       DATA TABLE
       ======================================================== */

    div[data-testid="stDataFrame"] {
        background: #FFFFFF;

        border: 1px solid #E1E8F0;

        border-radius: 14px;

        overflow: hidden;

        box-shadow:
            0 5px 18px rgba(15,39,71,0.045);
    }


    /* ========================================================
       INFO / WARNING / ERROR
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px !important;
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
       FOOTER
       ======================================================== */

    .footer-text {
        text-align: center;
        color: #8191A1;
        font-size: 0.75rem;
        padding-top: 1rem;
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

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA PATH
# ============================================================

DATA_PATH = (
    r"C:\Users\Pawan\OneDrive\Desktop\Online-Retail-II"
    r"\Online-retail-demand-forcasting\data\processed"
    r"\demand_forecast_results.csv"
)


# ============================================================
# LOAD FORECAST DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_forecast_data(path):

    if not os.path.exists(path):
        return None

    try:

        df = pd.read_csv(path)

        return df

    except Exception:

        return None


forecast_df = load_forecast_data(DATA_PATH)


# ============================================================
# DATA VALIDATION
# ============================================================

if forecast_df is None:

    st.error(
        "Forecast dataset could not be found or loaded."
    )

    st.write("Expected location:")

    st.code(DATA_PATH)

    st.stop()


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "date",
    "actual_demand",
    "predicted_demand"
]


missing_columns = [
    column
    for column in required_columns
    if column not in forecast_df.columns
]


if missing_columns:

    st.error(
        "The forecast dataset is missing required columns."
    )

    st.write(missing_columns)

    st.write("Available columns:")

    st.write(
        forecast_df.columns.tolist()
    )

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

@st.cache_data(show_spinner=False)
def prepare_forecast_data(df):

    df = df.copy()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["actual_demand"] = pd.to_numeric(
        df["actual_demand"],
        errors="coerce"
    )

    df["predicted_demand"] = pd.to_numeric(
        df["predicted_demand"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "date",
            "actual_demand",
            "predicted_demand"
        ]
    )

    df = df.sort_values(
        "date"
    )

    df["year"] = df["date"].dt.year

    return df


forecast_df = prepare_forecast_data(
    forecast_df
)


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


def format_difference(value):

    value = float(value)

    if value > 0:

        return f"+{format_number(value)}"

    return format_number(value)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🔮 Demand Forecast")

st.caption(
    "Machine-learning powered demand analysis, "
    "forecast accuracy and future demand patterns."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔮 Forecast Controls")

st.sidebar.caption(
    "Select the analysis period for the forecast dashboard."
)

st.sidebar.divider()


# ============================================================
# YEAR FILTER
# ============================================================

years = sorted(
    forecast_df["year"]
    .dropna()
    .unique()
    .tolist()
)


selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_forecast = forecast_df


if selected_years:

    filtered_forecast = filtered_forecast[
        filtered_forecast["year"].isin(
            selected_years
        )
    ]


if filtered_forecast.empty:

    st.warning(
        "No forecast records match the selected year."
    )

    st.stop()


# ============================================================
# FILTER STATUS
# ============================================================

if selected_years:

    year_text = ", ".join(
        str(int(year))
        for year in selected_years
    )

else:

    year_text = "All Years"


st.info(
    f"Showing forecast analysis for: {year_text}"
)


# ============================================================
# FORECAST SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">Forecast Overview</div>',
    unsafe_allow_html=True
)

st.caption(
    "High-level demand and model performance indicators."
)


actual_demand = (
    filtered_forecast["actual_demand"].sum()
)


predicted_demand = (
    filtered_forecast["predicted_demand"].sum()
)


forecast_difference = (
    predicted_demand - actual_demand
)


if actual_demand != 0:

    forecast_accuracy = (
        100
        -
        (
            abs(forecast_difference)
            /
            actual_demand
            *
            100
        )
    )

    forecast_accuracy = max(
        0,
        forecast_accuracy
    )

else:

    forecast_accuracy = 0


# ============================================================
# ADDITIONAL METRICS
# ============================================================

forecast_records = len(
    filtered_forecast
)

mean_actual = (
    filtered_forecast["actual_demand"].mean()
)

mean_predicted = (
    filtered_forecast["predicted_demand"].mean()
)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "📦 Actual Demand",
        format_number(actual_demand)
    )


with kpi2:

    st.metric(
        "🔮 Predicted Demand",
        format_number(predicted_demand)
    )


with kpi3:

    st.metric(
        "📐 Forecast Difference",
        format_difference(forecast_difference)
    )


with kpi4:

    st.metric(
        "🎯 Forecast Accuracy",
        f"{forecast_accuracy:.2f}%"
    )


# ============================================================
# ACTUAL VS PREDICTED DEMAND
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📈 Actual vs Predicted Demand</div>',
    unsafe_allow_html=True
)

st.caption(
    "Comparison between observed demand and machine-learning predictions."
)


fig_forecast = px.line(
    filtered_forecast,
    x="date",
    y=[
        "actual_demand",
        "predicted_demand"
    ]
)


fig_forecast.update_traces(
    selector=dict(
        name="actual_demand"
    ),
    line=dict(
        color="#2563EB",
        width=3
    ),
    hovertemplate=
    "<b>%{x|%d %b %Y}</b>"
    "<br>Actual Demand: %{y:,.0f}"
    "<extra></extra>"
)


fig_forecast.update_traces(
    selector=dict(
        name="predicted_demand"
    ),
    line=dict(
        color="#F59E0B",
        width=3,
        dash="dash"
    ),
    hovertemplate=
    "<b>%{x|%d %b %Y}</b>"
    "<br>Predicted Demand: %{y:,.0f}"
    "<extra></extra>"
)


fig_forecast.update_layout(
    template="plotly_white",

    height=500,

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
        title="Demand",
        gridcolor="#EEF2F6",
        zeroline=False
    ),

    hovermode="x unified",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white",

    legend=dict(
        orientation="h",
        y=1.08,
        x=0
    )
)


st.plotly_chart(
    fig_forecast,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# FORECAST ERROR ANALYSIS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📉 Forecast Error Analysis</div>',
    unsafe_allow_html=True
)

st.caption(
    "Positive values indicate over-prediction; negative values indicate under-prediction."
)


forecast_difference_df = (
    filtered_forecast[
        [
            "date",
            "actual_demand",
            "predicted_demand"
        ]
    ]
    .copy()
)


forecast_difference_df["difference"] = (
    forecast_difference_df["predicted_demand"]
    -
    forecast_difference_df["actual_demand"]
)


fig_difference = px.line(
    forecast_difference_df,
    x="date",
    y="difference"
)


fig_difference.update_traces(
    line=dict(
        color="#8B5CF6",
        width=2.5
    ),

    fill="tozeroy",

    fillcolor="rgba(139,92,246,0.08)",

    hovertemplate=
    "<b>%{x|%d %b %Y}</b>"
    "<br>Forecast Error: %{y:,.0f}"
    "<extra></extra>"
)


fig_difference.add_hline(
    y=0,
    line_dash="dash",
    line_color="#94A3B8",
    line_width=1
)


fig_difference.update_layout(
    template="plotly_white",

    height=400,

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
        title="Prediction Error",
        gridcolor="#EEF2F6",
        zeroline=False
    ),

    hovermode="x unified",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white"
)


st.plotly_chart(
    fig_difference,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# MONTHLY FORECAST
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📅 Monthly Demand Forecast</div>',
    unsafe_allow_html=True
)

st.caption(
    "Monthly comparison of actual and predicted demand."
)


monthly_forecast = (
    filtered_forecast
    .assign(
        month=filtered_forecast["date"].dt.to_period("M")
    )
    .groupby("month")
    .agg(
        Actual_Demand=(
            "actual_demand",
            "sum"
        ),

        Predicted_Demand=(
            "predicted_demand",
            "sum"
        )
    )
    .reset_index()
)


monthly_forecast["month"] = (
    monthly_forecast["month"]
    .astype(str)
)


monthly_long = monthly_forecast.melt(
    id_vars=["month"],
    value_vars=[
        "Actual_Demand",
        "Predicted_Demand"
    ],
    var_name="Demand Type",
    value_name="Demand"
)


fig_monthly = px.bar(
    monthly_long,
    x="month",
    y="Demand",
    color="Demand Type",
    barmode="group",
    color_discrete_map={
        "Actual_Demand": "#2563EB",
        "Predicted_Demand": "#F59E0B"
    }
)


fig_monthly.update_traces(
    hovertemplate=
    "<b>%{x}</b>"
    "<br>%{fullData.name}: %{y:,.0f}"
    "<extra></extra>"
)


fig_monthly.update_layout(
    template="plotly_white",

    height=450,

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis=dict(
        title="Month",
        showgrid=False
    ),

    yaxis=dict(
        title="Demand",
        gridcolor="#EEF2F6"
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="white",

    legend=dict(
        orientation="h",
        y=1.08,
        x=0
    )
)


st.plotly_chart(
    fig_monthly,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# MODEL SUMMARY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🎯 Forecast Performance</div>',
    unsafe_allow_html=True
)

st.caption(
    "Additional indicators describing the selected forecast period."
)


performance1, performance2, performance3 = st.columns(3)


with performance1:

    st.metric(
        "Forecast Records",
        format_number(forecast_records)
    )


with performance2:

    st.metric(
        "Avg. Actual Demand",
        format_number(mean_actual)
    )


with performance3:

    st.metric(
        "Avg. Predicted Demand",
        format_number(mean_predicted)
    )


# ============================================================
# FORECAST DATA
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📋 Forecast Data</div>',
    unsafe_allow_html=True
)

st.caption(
    "Detailed forecast records for the selected period."
)


display_columns = [
    column
    for column in [
        "date",
        "actual_demand",
        "predicted_demand"
    ]
    if column in filtered_forecast.columns
]


display_df = filtered_forecast[
    display_columns
].copy()


display_df = display_df.rename(
    columns={
        "date": "Date",
        "actual_demand": "Actual Demand",
        "predicted_demand": "Predicted Demand"
    }
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=400
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer-text">Retail Demand Forecasting | Machine Learning Demand Analytics</div>',
    unsafe_allow_html=True
)
