🛍️ Online Retail Demand Forecasting & Inventory Intelligence

An end-to-end retail analytics, demand forecasting, and inventory intelligence project that analyzes historical retail transactions, identifies sales trends, forecasts future demand, evaluates inventory risk, and presents actionable business insights through an interactive Streamlit Executive Dashboard.

---

📌 Project Overview

Retail businesses need accurate demand insights to maintain the right inventory levels, reduce stockouts, avoid overstocking, and improve sales planning.

This project transforms large-scale retail transaction data into meaningful business insights using:

- 📊 Exploratory Data Analysis
- 🧹 Data Cleaning & Preprocessing
- ⚙️ Feature Engineering
- 📈 Sales & Revenue Analytics
- 🤖 Machine Learning Forecasting
- 📉 Time-Series Forecasting
- 📦 Inventory Intelligence
- ⚠️ Inventory Risk Scoring
- 📋 Product-Level Analysis
- 🎯 Interactive Streamlit Dashboards

The final solution provides a centralized dashboard for monitoring sales performance, understanding demand patterns, forecasting future demand, and identifying inventory risks.

---

🎯 Project Objectives

The main objectives of this project are to:

1. Analyze historical retail transaction data.
2. Identify sales and demand trends.
3. Understand product, store, customer, and channel performance.
4. Engineer meaningful time-series and demand-related features.
5. Forecast future demand using multiple forecasting techniques.
6. Compare forecasting model performance.
7. Identify potential inventory risks.
8. Provide actionable business insights.
9. Present results through an interactive Streamlit dashboard.
10. Create a deployment-ready retail analytics solution.

---

🗂️ Project Structure

Online-retail-demand-forecasting/
│
├── data/
│   ├── raw/
│   │   └── Original datasets
│   │
│   └── processed/
│       ├── sales_transactions_cleaned.csv
│       ├── daily_demand_features.csv
│       ├── demand_forecast_results.csv
│       └── inventory_risk_scoring.csv
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   └── 04_demand_forecasting.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   └── forecasting.py
│
├── dashboard/
│   └── app.py
│
├── .gitattributes
├── .gitignore
├── README.md
└── requirements.txt

---

📊 Dataset

The project uses large-scale retail transaction data covering 2022–2025.

Dataset Statistics

Attribute| Value
Original Transactions| 9,972,038
Transactions after Duplicate Removal| 9,959,019
Date Range| 2022–2025
Stores| 30
Products / SKUs| 5,000
Customers| 10,000
Receipts| 5,174,631
Sales Channels| 3

Sales Channels

- 🏪 In-Store
- 🌐 Online
- 📱 Mobile App

Main Dataset Columns

date
receipt_id
store_id
sku_id
customer_id
quantity
unit_price
total_value
channel
discount_pct
promo_id

---

🧹 Data Cleaning

The raw transaction data was processed to improve data quality and reliability.

Cleaning steps included:

- Duplicate detection and removal
- Missing-value analysis
- Data-type validation
- Numerical conversion
- Date conversion
- Validation of quantity and price values
- Preparation of clean transaction data

The cleaned dataset is stored in:

data/processed/sales_transactions_cleaned.csv

---

📈 Exploratory Data Analysis

The EDA phase analyzes the major sales and demand patterns in the dataset.

Key analysis areas

- Daily sales trends
- Monthly sales trends
- Yearly sales performance
- Product performance
- Store performance
- Customer activity
- Channel performance
- Revenue distribution
- Demand patterns
- Seasonal behavior

These analyses help identify business trends and provide the foundation for forecasting and inventory decisions.

---

⚙️ Feature Engineering

Time-series and demand-related features were created to improve forecasting performance.

Features Used

year
month
quarter
day_of_week
day
week_of_year
is_weekend
lag_1
lag_7
lag_14
lag_30
rolling_7
rolling_14
rolling_30

Lag Features

Lag features capture previous demand values.

Examples:

- "lag_1" → Previous day's demand
- "lag_7" → Demand from the previous week
- "lag_14" → Demand from 14 days earlier
- "lag_30" → Demand from 30 days earlier

Rolling Features

Rolling statistics help capture recent demand behavior.

rolling_7
rolling_14
rolling_30

These represent rolling demand patterns over 7, 14, and 30-day windows.

---

🤖 Demand Forecasting

Multiple forecasting approaches were explored to predict future retail demand.

1. Random Forest

Random Forest was used as a machine-learning forecasting model using engineered time-series features.

Performance

Metric| Score
MAE| 414.75
RMSE| 524.62
MAPE| 2.86%

---

2. XGBoost

XGBoost was also evaluated for demand prediction.

Performance

Metric| Score
MAE| 417.45
RMSE| 521.34
MAPE| 2.87%

XGBoost provides strong predictive performance and captures nonlinear relationships between demand and engineered features.

---

📉 Time-Series Forecasting

Traditional time-series forecasting techniques were also implemented to analyze temporal demand patterns.

ARIMA

ARIMA (AutoRegressive Integrated Moving Average) was used for univariate time-series demand forecasting.

It models demand based on:

- Previous observations
- Differences in the series
- Previous forecast errors

ARIMA is useful for understanding demand trends and temporal dependencies.

---

SARIMA

SARIMA (Seasonal ARIMA) extends ARIMA by incorporating seasonal patterns.

SARIMA is particularly useful for retail demand because sales can exhibit recurring patterns across:

- Weeks
- Months
- Seasons
- Other periodic intervals

Both ARIMA and SARIMA were implemented and evaluated as part of the forecasting analysis.

---

🔬 Forecasting Model Comparison

Different forecasting approaches were explored to understand their strengths and suitability for retail demand prediction.

Model| Type| Purpose
Random Forest| Machine Learning| Demand prediction
XGBoost| Machine Learning| Demand prediction
ARIMA| Time Series| Temporal forecasting
SARIMA| Time Series| Seasonal forecasting

The project combines machine-learning and statistical forecasting techniques to provide a broader view of future demand.

---

📦 Inventory Intelligence

Forecasting demand alone is not sufficient for retail decision-making.

The project therefore incorporates inventory intelligence to identify products that may require attention.

Inventory analysis focuses on:

- Demand levels
- Stock availability
- Potential stockout risk
- Overstock risk
- Product-level demand
- Inventory risk scoring

---

⚠️ Inventory Risk Analysis

An inventory risk scoring approach is used to classify products according to their potential inventory risk.

The analysis helps identify:

🔴 High Risk

Products that may require immediate inventory attention.

🟡 Medium Risk

Products that should be monitored regularly.

🟢 Low Risk

Products with relatively lower inventory concerns.

This allows businesses to prioritize inventory management activities.

---

📊 Streamlit Executive Dashboard

The project includes an interactive Streamlit dashboard that brings together the major analytical components.

Dashboard Sections

🏠 Home Dashboard

Provides a high-level overview of the retail business.

Includes:

- Key performance indicators
- Sales overview
- Demand overview
- Business highlights

---

📈 Sales Analytics

Provides detailed sales analysis through:

- Sales trends
- Revenue analysis
- Channel analysis
- Product performance
- Store performance
- Time-based analysis

---

🔮 Demand Forecast

Displays future demand predictions generated using forecasting models.

Users can explore:

- Historical demand
- Forecasted demand
- Forecast trends
- Model results
- Forecast performance

---

📦 Inventory Dashboard

Provides an overview of inventory-related metrics and demand patterns.

---

⚠️ Risk Dashboard

Highlights inventory risk categories and helps identify products that require attention.

---

🛍️ Product Details

Provides product-level insights including demand and sales-related information.

---

📋 Executive Summary

Provides a concise business-level overview of important findings and KPIs.

---

🛠️ Technologies Used

Programming & Analysis

- 🐍 Python
- 🐼 Pandas
- 🔢 NumPy

Visualization

- 📊 Matplotlib
- 📈 Plotly
- 📉 Streamlit

Machine Learning

- 🌲 Scikit-learn
- 🚀 XGBoost

Time-Series Forecasting

- 📉 ARIMA
- 📊 SARIMA
- Statsmodels

Development & Deployment

- Git
- GitHub
- Streamlit Community Cloud
- Jupyter Notebook

---

🔄 Project Workflow

Raw Retail Data
       ↓
Data Cleaning
       ↓
Exploratory Data Analysis
       ↓
Feature Engineering
       ↓
Demand Aggregation
       ↓
Forecasting
       ↓
Model Evaluation
       ↓
Inventory Risk Analysis
       ↓
Business Insights
       ↓
Streamlit Dashboard
       ↓
Deployment

---

📏 Model Evaluation Metrics

The forecasting models were evaluated using standard regression metrics.

MAE — Mean Absolute Error

Measures the average absolute difference between actual and predicted demand.

Lower MAE indicates better performance.

RMSE — Root Mean Squared Error

Penalizes larger prediction errors more strongly.

Lower RMSE indicates better performance.

MAPE — Mean Absolute Percentage Error

Measures prediction error as a percentage of actual demand.

Lower MAPE generally indicates better forecasting accuracy.

---

💡 Key Business Insights

The project enables businesses to:

- Identify sales trends and seasonal patterns.
- Understand the contribution of different sales channels.
- Identify high-demand products.
- Forecast future demand.
- Compare forecasting approaches.
- Detect potential inventory risks.
- Reduce the possibility of stockouts.
- Reduce unnecessary overstocking.
- Improve inventory planning.
- Support data-driven business decisions.

---

🚀 Installation

Clone the repository:

git clone https://github.com/Online-Retail-Demand-Forecasting/Online-retail-demand-forcasting.git

Navigate to the project directory:

cd Online-retail-demand-forcasting

Create a virtual environment:

python -m venv venv

Activate the environment.

Windows

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

---

▶️ Running the Dashboard Locally

From the project root directory, run:

python -m streamlit run dashboard/app.py

The Streamlit application will open in your browser.

---

☁️ Deployment

The Streamlit dashboard is designed to be deployed using Streamlit Community Cloud.

Deployment configuration

Repository: Your GitHub repository
Branch: main
Main file path: dashboard/app.py

The required Python dependencies should be listed in:

requirements.txt

---

📁 Important Files

File| Purpose
"dashboard/app.py"| Streamlit dashboard
"01_data_exploration.ipynb"| Initial data exploration
"02_data_cleaning.ipynb"| Data cleaning
"03_eda.ipynb"| Exploratory Data Analysis
"04_demand_forecasting.ipynb"| Forecasting models
"data_cleaning.py"| Data cleaning functions
"feature_engineering.py"| Feature creation
"forecasting.py"| Forecasting utilities
"requirements.txt"| Python dependencies
"README.md"| Project documentation

---

🔮 Future Enhancements

Possible future improvements include:

- Real-time inventory monitoring
- Automated inventory alerts
- Advanced hyperparameter tuning
- Deep-learning forecasting models
- LSTM/GRU-based demand forecasting
- Automated model selection
- Product recommendation systems
- Real-time data integration
- Cloud database integration
- Automated forecast retraining
- Advanced anomaly detection
- Role-based dashboard access

---

👥 Project Team

This project was developed as part of the Zidio Development Internship.

Project Area

Data Science & Analytics

Focus Areas

- Retail Analytics
- Demand Forecasting
- Machine Learning
- Time-Series Analysis
- Inventory Intelligence
- Business Intelligence
- Data Visualization

---

📌 Conclusion

The Online Retail Demand Forecasting & Inventory Intelligence project provides an end-to-end solution for transforming retail transaction data into actionable business intelligence.

By combining data analytics, machine learning, ARIMA/SARIMA time-series forecasting, inventory risk analysis, and interactive Streamlit dashboards, the project helps businesses better understand demand, anticipate future sales, and make more informed inventory decisions.

---

⭐ Project Highlights

✔ 9.9M+ cleaned retail transactions
✔ 5,000 products
✔ 30 stores
✔ 10,000 customers
✔ 2022–2025 historical data
✔ Machine Learning Forecasting
✔ ARIMA & SARIMA Forecasting
✔ Inventory Risk Analysis
✔ Interactive Streamlit Dashboard
✔ GitHub-based project structure
✔ Deployment-ready application

---

📜 License

This project is developed for educational and internship purposes as part of the Zidio Development Internship.