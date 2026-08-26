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
# PROFESSIONAL DASHBOARD STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       IMPORT / GLOBAL
       ======================================================== */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(37, 99, 235, 0.08),
                transparent 25%
            ),
            radial-gradient(
                circle at 10% 30%,
                rgba(14, 165, 233, 0.06),
                transparent 25%
            ),
            #F5F7FB;

        font-family: 'Inter', sans-serif;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Hide Streamlit default decoration */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0B1F3A 0%,
                #102A43 45%,
                #0B2039 100%
            );

        border-right: none;

        box-shadow:
            8px 0 30px rgba(15, 23, 42, 0.10);
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1.2rem;
    }

    section[data-testid="stSidebar"] h1 {
        color: #FFFFFF !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.4px;
    }

    section[data-testid="stSidebar"] p {
        color: #AFC1D5 !important;
        font-size: 0.82rem !important;
        line-height: 1.6 !important;
    }

    section[data-testid="stSidebar"] hr {
        border: none !important;
        border-top: 1px solid rgba(255,255,255,0.12) !important;
        margin: 1.4rem 0 !important;
    }

    /* Sidebar info */

    section[data-testid="stSidebar"]
    div[data-testid="stAlert"] {
        background:
            rgba(255,255,255,0.07) !important;

        border:
            1px solid rgba(255,255,255,0.12) !important;

        border-radius: 14px !important;

        color: #D9E7F5 !important;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.12);
    }

    section[data-testid="stSidebar"]
    div[data-testid="stAlert"] p {
        color: #D9E7F5 !important;
    }


    /* ========================================================
       MAIN TITLE
       ======================================================== */

    h1 {
        color: #0B1F3A !important;

        font-size: 2.65rem !important;

        font-weight: 800 !important;

        letter-spacing: -1.5px;

        line-height: 1.15 !important;

        margin-bottom: 0.35rem !important;
    }

    h2 {
        color: #102A43 !important;

        font-size: 1.45rem !important;

        font-weight: 750 !important;

        letter-spacing: -0.5px;

        margin-top: 2rem !important;

        margin-bottom: 1rem !important;
    }

    h3 {
        color: #183B56 !important;

        font-weight: 700 !important;

        letter-spacing: -0.2px;
    }

    p {
        color: #52667A;

        line-height: 1.7;
    }

    .stSubheader {
        color: #60758A !important;
    }


    /* ========================================================
       HERO SECTION
       ======================================================== */

    div[data-testid="stTitle"] {
        background:
            linear-gradient(
                135deg,
                #0B1F3A 0%,
                #123E67 55%,
                #155E91 100%
            );

        padding:
            2.4rem 2.5rem 2.2rem 2.5rem;

        border-radius: 22px;

        box-shadow:
            0 18px 45px rgba(15, 39, 71, 0.18);

        position: relative;

        overflow: hidden;

        margin-bottom: 1rem;
    }

    div[data-testid="stTitle"]::before {
        content: "";

        position: absolute;

        width: 240px;
        height: 240px;

        border-radius: 50%;

        background:
            rgba(56, 189, 248, 0.14);

        right: -70px;
        top: -100px;
    }

    div[data-testid="stTitle"]::after {
        content: "";

        position: absolute;

        width: 140px;
        height: 140px;

        border-radius: 50%;

        background:
            rgba(255,255,255,0.06);

        right: 160px;
        bottom: -100px;
    }

    div[data-testid="stTitle"] h1 {
        color: #FFFFFF !important;

        position: relative;

        z-index: 2;
    }

    div[data-testid="stSubheader"] {
        background: #FFFFFF;

        border:
            1px solid #E5EAF1;

        border-left:
            5px solid #2196F3;

        padding:
            1.15rem 1.5rem;

        border-radius:
            0 13px 13px 0;

        box-shadow:
            0 6px 18px rgba(15, 39, 71, 0.05);

        max-width: 1100px;
    }

    div[data-testid="stSubheader"] p {
        color: #536B82 !important;

        font-size: 0.98rem !important;

        line-height: 1.7 !important;

        margin: 0 !important;
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
                #D8E0E9,
                transparent
            ) !important;

        margin:
            1.8rem 0 !important;
    }


    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    h2::before {
        content: "";

        display: inline-block;

        width: 5px;

        height: 22px;

        background:
            linear-gradient(
                180deg,
                #2196F3,
                #0EA5E9
            );

        border-radius: 5px;

        margin-right: 10px;

        vertical-align: -3px;
    }


    /* ========================================================
       GENERAL BORDERED CONTAINERS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            rgba(255,255,255,0.96);

        border:
            1px solid #E1E8F0 !important;

        border-radius:
            18px !important;

        box-shadow:
            0 7px 25px rgba(15, 39, 71, 0.055);

        transition:
            all 0.25s ease;

        overflow: hidden;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color:
            #C9D8E8 !important;

        box-shadow:
            0 14px 35px rgba(15, 39, 71, 0.09);

        transform:
            translateY(-2px);
    }


    /* ========================================================
       EXECUTIVE OVERVIEW CARD
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"]
    h3 {
        color: #123E67 !important;

        font-size: 1.15rem !important;

        margin-bottom: 0.4rem !important;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #FFFFFF 0%,
                #F9FBFD 100%
            );

        border:
            1px solid #E2E8F0;

        border-radius:
            18px;

        padding:
            1.25rem 1.35rem;

        min-height:
            130px;

        position:
            relative;

        overflow:
            hidden;

        box-shadow:
            0 8px 22px rgba(15,39,71,0.055);

        transition:
            all 0.25s ease;
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

    div[data-testid="stMetric"]::after {
        content: "";

        position: absolute;

        width: 90px;
        height: 90px;

        border-radius: 50%;

        background:
            rgba(37,99,235,0.045);

        right: -35px;
        bottom: -40px;
    }

    div[data-testid="stMetric"]:hover {
        transform:
            translateY(-5px);

        box-shadow:
            0 15px 35px rgba(15,39,71,0.10);

        border-color:
            #BFD2E5;
    }

    div[data-testid="stMetricLabel"] {
        color:
            #63788C !important;

        font-size:
            0.82rem !important;

        font-weight:
            650 !important;
    }

    div[data-testid="stMetricValue"] {
        color:
            #102A43 !important;

        font-size:
            1.55rem !important;

        font-weight:
            800 !important;

        letter-spacing:
            -0.5px;
    }


    /* ========================================================
       PROJECT HIGHLIGHT CAPTIONS
       ======================================================== */

    div[data-testid="stMetric"] + div[data-testid="stCaptionContainer"] {
        padding-left: 5px;
        padding-top: 4px;
    }

    div[data-testid="stCaptionContainer"] p {
        color:
            #71869A !important;

        font-size:
            0.78rem !important;

        font-weight:
            500 !important;
    }


    /* ========================================================
       DASHBOARD MODULE CARDS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"]
    div[data-testid="stVerticalBlock"] {
        min-height: 145px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]
    h3 {
        position: relative;
    }


    /* ========================================================
       ANALYTICS FLOW
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] p {
        color:
            #52667A;
    }

    /* Specifically emphasize flow container */

    div[data-testid="stVerticalBlockBorderWrapper"]
    p {
        font-size:
            0.94rem;
    }


    /* ========================================================
       INFO / ALERT COMPONENTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius:
            14px !important;

        border-width:
            1px !important;

        box-shadow:
            0 5px 15px rgba(15,39,71,0.04);
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #2563EB,
                #0EA5E9
            );

        color:
            #FFFFFF;

        border:
            none;

        border-radius:
            10px;

        font-weight:
            650;

        padding:
            0.65rem 1.1rem;

        box-shadow:
            0 6px 15px rgba(37,99,235,0.20);

        transition:
            all 0.2s ease;
    }

    .stButton > button:hover {
        transform:
            translateY(-2px);

        box-shadow:
            0 10px 22px rgba(37,99,235,0.28);

        color:
            #FFFFFF;

        border:
            none;
    }


    /* ========================================================
       DATAFRAMES
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border:
            1px solid #DDE5EE;

        border-radius:
            14px;

        overflow:
            hidden;

        box-shadow:
            0 7px 20px rgba(15,39,71,0.05);
    }


    /* ========================================================
       INPUT ELEMENTS
       ======================================================== */

    div[data-baseweb="select"] > div {
        background:
            #FFFFFF !important;

        border:
            1px solid #D7E0EA !important;

        border-radius:
            10px !important;

        box-shadow:
            0 2px 7px rgba(15,39,71,0.03);
    }

    input,
    textarea {
        border-radius:
            10px !important;

        border-color:
            #D7E0EA !important;
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
        background:
            linear-gradient(
                180deg,
                #94A3B8,
                #64748B
            );

        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .dashboard-footer {
        text-align: center;

        color: #7A8A9A;

        font-size: 0.75rem;

        padding:
            1.4rem 0 0.3rem 0;

        border-top:
            1px solid #DCE3EB;

        margin-top:
            2.5rem;

        letter-spacing:
            0.3px;
    }


    /* ========================================================
       RESPONSIVE DESIGN
       ======================================================== */

    @media (max-width: 1100px) {

        .main .block-container {
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        h1 {
            font-size: 2.25rem !important;
        }
    }


    @media (max-width: 700px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 1.9rem !important;
        }

        h2 {
            font-size: 1.25rem !important;
        }

        div[data-testid="stTitle"] {
            padding:
                1.6rem 1.4rem;
        }
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
