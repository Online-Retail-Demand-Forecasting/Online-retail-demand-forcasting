# ============================================================
# RETAIL DEMAND FORECASTING DASHBOARD
# HOME PAGE
# ============================================================

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
# PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background-color: #F6F8FB;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .hero-section {

        background: linear-gradient(
            135deg,
            #0F2747 0%,
            #183B63 100%
        );

        padding: 42px 45px;

        border-radius: 16px;

        margin-bottom: 30px;

        box-shadow:
            0 8px 25px
            rgba(15, 39, 71, 0.12);
    }


    .hero-title {

        color: #FFFFFF;

        font-size: 36px;

        font-weight: 700;

        margin-bottom: 10px;

        letter-spacing: -0.5px;
    }


    .hero-subtitle {

        color: #DCE8F5;

        font-size: 16px;

        line-height: 1.6;

        max-width: 850px;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {

        color: #17324D;

        font-size: 22px;

        font-weight: 700;

        margin-top: 20px;

        margin-bottom: 18px;
    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    .kpi-card {

        background: #FFFFFF;

        border: 1px solid #E2E8F0;

        border-radius: 14px;

        padding: 22px;

        min-height: 125px;

        box-shadow:
            0 4px 12px
            rgba(15, 39, 71, 0.05);
    }


    .kpi-label {

        color: #64748B;

        font-size: 13px;

        font-weight: 600;

        margin-bottom: 10px;
    }


    .kpi-value {

        color: #17324D;

        font-size: 27px;

        font-weight: 700;

        margin-bottom: 5px;
    }


    .kpi-description {

        color: #94A3B8;

        font-size: 12px;
    }


    /* ========================================================
       INFORMATION CARD
       ======================================================== */

    .info-card {

        background: #FFFFFF;

        border: 1px solid #E2E8F0;

        border-radius: 14px;

        padding: 25px;

        margin-top: 10px;

        box-shadow:
            0 4px 12px
            rgba(15, 39, 71, 0.04);
    }


    .info-title {

        color: #17324D;

        font-size: 18px;

        font-weight: 700;

        margin-bottom: 10px;
    }


    .info-text {

        color: #64748B;

        font-size: 14px;

        line-height: 1.7;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        background-color: #FFFFFF;

        border-right:
            1px solid #E2E8F0;
    }


    .sidebar-title {

        color: #17324D;

        font-size: 21px;

        font-weight: 700;

        margin-bottom: 5px;
    }


    .sidebar-text {

        color: #64748B;

        font-size: 13px;

        line-height: 1.5;

        margin-bottom: 20px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {

        text-align: center;

        color: #718096;

        font-size: 12px;

        padding-top: 20px;

        margin-top: 35px;

        border-top:
            1px solid #DCE3EB;
    }


    /* ========================================================
       HIDE DEFAULT STREAMLIT ELEMENTS
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        🛍️ Retail Dashboard
    </div>

    <div class="sidebar-text">
        Retail Demand Forecasting and
        Business Intelligence System
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown("---")

st.sidebar.markdown(
    "### Navigation"
)


st.sidebar.info(
    "🏠 You are currently on the Home page."
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero-section">

        <div class="hero-title">
            Retail Demand Forecasting
        </div>

        <div class="hero-subtitle">
            A centralized business intelligence dashboard
            for understanding retail sales performance,
            demand patterns, forecasting and inventory
            decision-making.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WELCOME SECTION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Executive Overview
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-card">

        <div class="info-title">
            Welcome to the Retail Analytics Dashboard
        </div>

        <div class="info-text">
            This dashboard is designed to provide a clear
            and professional view of retail business
            performance. It combines sales analysis,
            demand forecasting and inventory intelligence
            into a single analytics platform.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Project Highlights
    </div>
    """,
    unsafe_allow_html=True
)


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.markdown(
        """
        <div class="kpi-card">

            <div class="kpi-label">
                📊 SALES ANALYTICS
            </div>

            <div class="kpi-value">
                Real-Time
            </div>

            <div class="kpi-description">
                Monitor sales performance
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        """
        <div class="kpi-card">

            <div class="kpi-label">
                🔮 DEMAND FORECAST
            </div>

            <div class="kpi-value">
                ML Powered
            </div>

            <div class="kpi-description">
                Predict future demand
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        """
        <div class="kpi-card">

            <div class="kpi-label">
                📦 INVENTORY
            </div>

            <div class="kpi-value">
                Intelligent
            </div>

            <div class="kpi-description">
                Monitor inventory position
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        """
        <div class="kpi-card">

            <div class="kpi-label">
                ⚠️ RISK ANALYSIS
            </div>

            <div class="kpi-value">
                Automated
            </div>

            <div class="kpi-description">
                Identify inventory risks
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BUSINESS OBJECTIVE
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Business Objective
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-card">

        <div class="info-title">
            Turning Retail Data into Business Decisions
        </div>

        <div class="info-text">

            The objective of this project is to transform
            large-scale retail transaction data into
            meaningful business insights.

            <br><br>

            The system helps decision-makers understand
            historical sales behaviour, identify demand
            patterns, forecast future demand and detect
            potential inventory risks.

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DASHBOARD MODULES
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Dashboard Modules
    </div>
    """,
    unsafe_allow_html=True
)


module1, module2, module3 = st.columns(3)


with module1:

    st.markdown(
        """
        <div class="info-card">

            <div class="info-title">
                📊 Sales Analytics
            </div>

            <div class="info-text">
                Explore sales trends, channels,
                stores and business performance.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with module2:

    st.markdown(
        """
        <div class="info-card">

            <div class="info-title">
                🔮 Demand Forecasting
            </div>

            <div class="info-text">
                Analyze historical demand and
                machine-learning based forecasts.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with module3:

    st.markdown(
        """
        <div class="info-card">

            <div class="info-title">
                📦 Inventory Intelligence
            </div>

            <div class="info-text">
                Understand inventory conditions
                and identify potential risks.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        Retail Demand Forecasting Dashboard
        &nbsp; | &nbsp;
        Data Science Project

    </div>
    """,
    unsafe_allow_html=True
)