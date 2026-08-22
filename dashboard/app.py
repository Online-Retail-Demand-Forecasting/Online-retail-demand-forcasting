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

forecast_page = st.Page(
    "pages/2_Forecast.py",
    title="Forecast",
    icon="🔮"
)

inventory_page = st.Page(
    "pages/3_Inventory.py",
    title="Inventory",
    icon="📦"
)

risk_page = st.Page(
    "pages/4_Risk.py",
    title="Risk",
    icon="⚠️"
)

product_page = st.Page(
    "pages/5_Product_Details.py",
    title="Product Details",
    icon="🛍️"
)

executive_page = st.Page(
    "pages/6_Executive_Summary.py",
    title="Executive Summary",
    icon="📈"
)


# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation([
    home_page,
    sales_page,
    forecast_page,
    inventory_page,
    risk_page,
    product_page,
    executive_page
])


# ============================================================
# RUN APP
# ============================================================

pg.run()