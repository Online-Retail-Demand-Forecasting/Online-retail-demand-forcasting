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
    layout="wide"
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

@st.cache_data
def load_forecast_data():

    if not os.path.exists(DATA_PATH):
        return None

    try:
        return pd.read_csv(DATA_PATH)

    except Exception as e:
        st.error(f"Unable to load forecast dataset: {e}")
        return None


forecast_df = load_forecast_data()


# ============================================================
# DATA VALIDATION
# ============================================================

if forecast_df is None:

    st.error("Forecast dataset could not be found.")

    st.write("Expected location:")

    st.code(DATA_PATH)

    st.stop()


# ============================================================
# DATE CONVERSION
# ============================================================

if "date" in forecast_df.columns:

    forecast_df["date"] = pd.to_datetime(
        forecast_df["date"],
        errors="coerce"
    )


# ============================================================
# NUMERIC CONVERSION
# ============================================================

for column in [
    "actual_demand",
    "predicted_demand"
]:

    if column in forecast_df.columns:

        forecast_df[column] = pd.to_numeric(
            forecast_df[column],
            errors="coerce"
        )


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🔮 Demand Forecast")

st.caption(
    "Analyze historical demand and machine-learning based demand forecasts."
)

st.divider()


# ============================================================
# CHECK REQUIRED COLUMNS
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
        "The forecast dataset is missing required columns:"
    )

    st.write(missing_columns)

    st.write("Available columns:")

    st.write(
        forecast_df.columns.tolist()
    )

    st.stop()


# ============================================================
# REMOVE INVALID RECORDS
# ============================================================

forecast_df = forecast_df.dropna(
    subset=[
        "date",
        "actual_demand",
        "predicted_demand"
    ]
).copy()


forecast_df = forecast_df.sort_values(
    "date"
)


# ============================================================
# YEAR FILTER
# ============================================================

forecast_df["year"] = (
    forecast_df["date"].dt.year
)


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
# APPLY FILTER
# ============================================================

filtered_forecast = forecast_df.copy()


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
# FORECAST SUMMARY
# ============================================================

st.header("Forecast Overview")


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
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


kpi1.metric(
    "Actual Demand",
    f"{actual_demand:,.0f}"
)


kpi2.metric(
    "Predicted Demand",
    f"{predicted_demand:,.0f}"
)


kpi3.metric(
    "Forecast Difference",
    f"{forecast_difference:,.0f}"
)


kpi4.metric(
    "Forecast Accuracy",
    f"{forecast_accuracy:.2f}%"
)


# ============================================================
# ACTUAL VS FORECAST
# ============================================================

st.divider()

st.header("Actual vs Predicted Demand")


fig_forecast = px.line(
    filtered_forecast,
    x="date",
    y=[
        "actual_demand",
        "predicted_demand"
    ],
    title="Actual vs Predicted Demand"
)


fig_forecast.update_layout(
    template="plotly_white",
    xaxis_title="Date",
    yaxis_title="Demand",
    hovermode="x unified",
    height=500
)


st.plotly_chart(
    fig_forecast,
    use_container_width=True
)


# ============================================================
# DAILY FORECAST DIFFERENCE
# ============================================================

st.divider()

st.header("Forecast Difference")


forecast_difference_df = filtered_forecast.copy()


forecast_difference_df["difference"] = (
    forecast_difference_df["predicted_demand"]
    -
    forecast_difference_df["actual_demand"]
)


fig_difference = px.line(
    forecast_difference_df,
    x="date",
    y="difference",
    title="Predicted Demand - Actual Demand"
)


fig_difference.update_layout(
    template="plotly_white",
    xaxis_title="Date",
    yaxis_title="Demand Difference",
    height=400
)


st.plotly_chart(
    fig_difference,
    use_container_width=True
)


# ============================================================
# MONTHLY FORECAST
# ============================================================

st.divider()

st.header("Monthly Demand Forecast")


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


fig_monthly = px.bar(
    monthly_forecast,
    x="month",
    y=[
        "Actual_Demand",
        "Predicted_Demand"
    ],
    barmode="group",
    title="Monthly Actual vs Predicted Demand"
)


fig_monthly.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="Demand",
    height=450
)


st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# ============================================================
# FORECAST DATA
# ============================================================

st.divider()

st.header("Forecast Data")


display_columns = [
    column
    for column in [
        "date",
        "actual_demand",
        "predicted_demand"
    ]
    if column in filtered_forecast.columns
]


st.dataframe(
    filtered_forecast[display_columns],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting | Demand Forecast"
)
