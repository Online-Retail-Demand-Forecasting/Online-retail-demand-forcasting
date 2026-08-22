import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
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
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 3px 10px rgba(15,39,71,0.05);
    }

    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #E2E8F0;
    }

    .dashboard-footer {
        text-align: center;
        color: #718096;
        font-size: 12px;
        padding: 20px 0 5px 0;
        border-top: 1px solid #DCE3EB;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛍️ Retail Dashboard")

st.sidebar.caption(
    "Retail Demand Forecasting & Business Intelligence"
)

st.sidebar.divider()

st.sidebar.info(
    "🏠 You are currently on the Home page."
)


# ============================================================
# HERO SECTION
# ============================================================

st.title("Retail Demand Forecasting")

st.subheader(
    "A centralized business intelligence dashboard "
    "for understanding retail sales performance, "
    "demand patterns, forecasting and inventory "
    "decision-making."
)

st.divider()


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.header("Executive Overview")

with st.container(border=True):

    st.subheader(
        "Welcome to the Retail Analytics Dashboard"
    )

    st.write(
        "This dashboard is designed to provide a clear "
        "and professional view of retail business "
        "performance. It combines sales analysis, "
        "demand forecasting and inventory intelligence "
        "into a single analytics platform."
    )


# ============================================================
# PROJECT HIGHLIGHTS
# ============================================================

st.header("Project Highlights")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📊 Sales Analytics",
        "Real-Time"
    )

    st.caption(
        "Monitor sales performance"
    )


with col2:

    st.metric(
        "🔮 Demand Forecast",
        "ML Powered"
    )

    st.caption(
        "Predict future demand"
    )


with col3:

    st.metric(
        "📦 Inventory",
        "Intelligent"
    )

    st.caption(
        "Monitor inventory position"
    )


with col4:

    st.metric(
        "⚠️ Risk Analysis",
        "Automated"
    )

    st.caption(
        "Identify inventory risks"
    )


# ============================================================
# BUSINESS OBJECTIVE
# ============================================================

st.header("Business Objective")

with st.container(border=True):

    st.subheader(
        "Turning Retail Data into Business Decisions"
    )

    st.write(
        "The objective of this project is to transform "
        "large-scale retail transaction data into "
        "meaningful business insights."
    )

    st.write(
        "The system helps decision-makers understand "
        "historical sales behaviour, identify demand "
        "patterns, forecast future demand and detect "
        "potential inventory risks."
    )


# ============================================================
# DASHBOARD MODULES
# ============================================================

st.header("Dashboard Modules")

module1, module2, module3 = st.columns(3)


with module1:

    with st.container(border=True):

        st.subheader("📊 Sales Analytics")

        st.write(
            "Explore sales trends, channels, "
            "stores and overall business performance."
        )


with module2:

    with st.container(border=True):

        st.subheader("🔮 Demand Forecasting")

        st.write(
            "Analyze historical demand and "
            "machine-learning based forecasts."
        )


with module3:

    with st.container(border=True):

        st.subheader("📦 Inventory Intelligence")

        st.write(
            "Understand inventory conditions "
            "and identify potential risks."
        )


# ============================================================
# ANALYTICS FLOW
# ============================================================

st.header("Analytics Flow")

with st.container(border=True):

    st.write(
        "Sales Data → Sales Analytics → Demand Patterns "
        "→ Forecasting → Inventory Intelligence "
        "→ Business Decisions"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting Dashboard | "
    "Data Science Project"
)