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
# PAGE NAVIGATION
# ============================================================

home_page = st.Page(
    "home.py",
    title="Home",
    icon="🏠"
)

sales_page = st.Page(
    "pages/1_Sales_Analytics.py",
    title="Sales Analytics",
    icon="📊"
)


# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation([
    home_page,
    sales_page
])


# ============================================================
# RUN APP
# ============================================================

pg.run()