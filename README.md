🛍️ Online Retail Demand Forecasting & Inventory Intelligence

An end-to-end retail analytics, demand forecasting, inventory risk analysis, and business intelligence project built using Python, Machine Learning, Statistical Forecasting, and Streamlit.

The project analyzes approximately 10 million retail transactions from 2022–2025 to identify sales patterns, understand demand behavior, forecast future demand, evaluate inventory risk, and provide management-oriented insights through an interactive Streamlit Executive Dashboard.

--

📌 Project Overview

Retail businesses need reliable demand insights to maintain the right inventory levels, reduce stockouts, avoid overstocking, and improve sales planning.

This project provides an end-to-end retail intelligence workflow covering:

- Historical sales analysis
- Exploratory Data Analysis (EDA)
- Demand aggregation and feature engineering
- Statistical time-series forecasting
- Machine Learning forecasting
- Forecast model evaluation
- Inventory risk scoring
- Product and category analysis
- Store and channel analysis
- Interactive business dashboards
- Management-oriented insights

The solution combines:

Data Analytics → Machine Learning → Time-Series Forecasting → Inventory Intelligence → Business Dashboard

---

🎯 Business Objectives

The primary objectives of the project are to:

- Understand historical retail sales patterns
- Analyze sales across stores and channels
- Identify high-performing products
- Analyze category-level performance
- Understand daily demand behavior
- Forecast future retail demand
- Compare statistical and machine learning forecasting methods
- Evaluate forecasting performance using standard metrics
- Identify inventory items requiring attention
- Analyze stock coverage and inventory risk
- Support data-driven replenishment decisions
- Present insights through an interactive dashboard

---

📊 Dataset

The project uses synthetic retail transaction and inventory data covering the period from 2022 to 2025.

Dataset Overview

Attribute| Value
Time Period| 2022–2025
Original Transactions| ~10 million
Cleaned Transactions| ~9.96 million
Stores| 30
Products / SKUs| 5,000
Customers| 10,000
Channels| 3

Sales Channels

- In-Store
- Online
- Mobile App

---

🧾 Main Transaction Columns

Column| Description
"date"| Transaction date
"receipt_id"| Transaction / receipt identifier
"store_id"| Store identifier
"sku_id"| Product / SKU identifier
"customer_id"| Customer identifier
"quantity"| Quantity purchased
"unit_price"| Unit price
"total_value"| Total transaction value
"channel"| Sales channel
"discount_pct"| Discount percentage
"promo_id"| Promotion identifier

---

🔄 Project Workflow

Raw Retail Data
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Demand Aggregation
      ↓
Feature Engineering
      ↓
Forecasting
      ↓
Model Evaluation
      ↓
Inventory Risk Scoring
      ↓
Streamlit Dashboard
      ↓
Business Insights

---

🧹 Data Cleaning

The raw transaction data was processed to improve data quality, consistency, and usability.

Major Data Cleaning Steps

- Duplicate removal
- Missing-value checking
- Data type conversion
- Date standardization
- Numerical column validation
- Quantity validation
- Price validation
- Transaction consistency checks
- Daily demand aggregation

After duplicate removal, the cleaned transaction dataset contained approximately:

9.96 million records

---

🔎 Exploratory Data Analysis

Exploratory Data Analysis was performed to understand historical sales and demand behavior.

Key Analyses

- Daily sales trends
- Daily demand trends
- Monthly sales patterns
- Year-wise sales performance
- Sales by channel
- Store-level performance
- Product-level performance
- Customer-level sales
- Transaction patterns
- Demand behavior over time
- Category performance

The EDA stage helped identify temporal patterns and provided the foundation for the forecasting workflow.

---

⚙️ Feature Engineering

A dedicated demand dataset was created using daily aggregated demand and time-series features.

Time-Based Features

- "year"
- "month"
- "quarter"
- "day_of_week"
- "day"
- "week_of_year"
- "is_weekend"

Lag Features

- "lag_1"
- "lag_7"
- "lag_14"
- "lag_30"

Rolling Features

- "rolling_7"
- "rolling_14"
- "rolling_30"

Target Variable

demand

These features help forecasting models capture:

- Recent demand behavior
- Weekly patterns
- Seasonal effects
- Short-term demand changes
- Longer-term demand trends

---

🤖 Demand Forecasting

Multiple forecasting approaches were evaluated to determine how effectively future demand could be predicted.

The project uses both statistical time-series methods and machine learning models.

Forecasting Methods

Statistical Forecasting

- Naive Baseline
- Seasonal Naive Forecast
- ARIMA
- SARIMA

Machine Learning

- Random Forest
- XGBoost
- Improved Random Forest

---

📅 Train/Test Split

A chronological time-based split was used to avoid data leakage.

Training Data: 1144 rows
Testing Data: 287 rows

Training Period:
2022-01-31 → 2025-03-19

Testing Period:
2025-03-20 → 2025-12-31

The chronological split ensures that future observations are not used to train the models.

---

📏 Forecasting Evaluation Metrics

The forecasting models were evaluated using:

MAE — Mean Absolute Error

Measures the average absolute difference between actual and predicted demand.

Lower values indicate better performance.

RMSE — Root Mean Squared Error

Penalizes larger prediction errors more heavily than MAE.

Lower values indicate better performance.

MAPE — Mean Absolute Percentage Error

Measures prediction error as a percentage of actual demand.

Lower values indicate better performance.

---

📈 Forecasting Model Evaluation

The evaluated models produced the following results:

Model| MAE| RMSE| MAPE
Naive Baseline| 366.53| 486.85| 2.56%
Random Forest| 414.75| 524.62| 2.86%
XGBoost| 417.45| 521.34| 2.87%
Improved Random Forest| 429.45| 540.88| 2.95%
Seasonal Naive (7-day)| 488.05| 733.76| 3.34%

---

📌 Forecasting Insights

The model evaluation produced several important observations:

- The Naive Baseline achieved the lowest MAE and MAPE in this experiment.
- The baseline therefore outperformed the tested machine learning models for these evaluation metrics.
- Random Forest achieved lower MAE and MAPE than XGBoost.
- XGBoost achieved the lowest RMSE among the machine learning models.
- The Improved Random Forest feature set did not improve performance over the original Random Forest.
- The 7-day Seasonal Naive approach performed worse than the other evaluated approaches.
- ARIMA and SARIMA were also incorporated as statistical time-series forecasting approaches.

Key Takeaway

The results demonstrate why forecasting systems should be compared against simple baseline methods rather than assuming that a more complex machine learning model will always perform better.

---

📦 Inventory Risk Scoring

An inventory risk scoring component was developed to identify products that may require inventory attention.

The analysis considers inventory-related indicators such as:

- Stock on hand
- Reorder point
- Safety stock
- Average daily demand
- Stock coverage days
- Risk score
- Risk category

---

🚦 Inventory Risk Categories

Inventory items are classified into four risk levels:

Risk Level| Meaning
🔴 Critical| Immediate inventory attention required
🟠 High Risk| High probability of inventory shortage
🟡 Medium Risk| Requires monitoring
🟢 Low Risk| Relatively healthy inventory position

---

📊 Inventory Risk Distribution

The final inventory risk dataset contains 21,228 inventory records.

Risk Level| Count
🟢 Low Risk| 18,375
🔴 Critical| 2,815
🟡 Medium Risk| 30
🟠 High Risk| 8
Total| 21,228

The risk analysis helps identify inventory items that may require:

- Immediate replenishment
- Inventory monitoring
- Demand review
- Stock optimization
- Reorder planning

---

📁 Processed Datasets

The major processed datasets generated during the project are:

"sales_transactions_cleaned.csv"

Contains cleaned transaction-level retail data used for sales analysis and dashboard visualizations.

"daily_demand_features.csv"

Contains daily aggregated demand along with time-based, lag, and rolling features used for forecasting.

"demand_forecast_results.csv"

Contains actual and predicted demand values generated during the forecasting process.

"inventory_risk_scoring.csv"

Contains inventory-level information including stock, demand estimates, coverage metrics, risk scores, and final risk categories.

---

📊 Executive Dashboard

The project includes an interactive Streamlit Executive Dashboard designed to convert analytical results into management-friendly business insights.

The dashboard brings together:

- Sales Analytics
- Demand Analysis
- Forecasting
- Product Analysis
- Inventory Intelligence
- Risk Analysis
- Key Performance Indicators

---

🏠 Dashboard Sections

📌 Executive Summary

Provides a high-level overview of retail performance through KPIs such as:

- Total Sales
- Total Transactions
- Quantity Sold
- Number of Stores
- Number of Products
- Average Order Value

---

💰 Sales Analytics

Provides insights into:

- Daily Sales Trend
- Sales by Channel
- Store-wise Sales
- Year-wise Sales
- Product performance
- Sales patterns

---

📈 Demand & Forecasting

Provides:

- Daily Demand Trend
- Actual vs Predicted Demand
- Forecast results
- Forecast performance
- Demand patterns over time
- Model comparison

---

🛍️ Product Analysis

Provides:

- Top Products by Sales
- Product-level performance
- Category performance
- Sales by Category
- Quantity Sold by Category

---

📦 Inventory Intelligence

Provides:

- Critical inventory
- High-risk inventory
- Medium-risk inventory
- Low-risk inventory
- Inventory risk distribution
- Stock coverage analysis
- Store-level risk analysis

---

🎛️ Dashboard Filters

Interactive filters allow users to explore the data dynamically.

Depending on the dashboard section, filters include:

- Year
- Sales Channel
- Store
- Product / SKU
- Risk Level

Charts, tables, and KPIs update based on the selected filters where applicable.

---

🖥️ Technology Stack

Programming & Data Analysis

- Python
- Pandas
- NumPy

Machine Learning

- Scikit-learn
- Random Forest
- XGBoost

Statistical Forecasting

- ARIMA
- SARIMA
- Naive Forecasting
- Seasonal Naive Forecasting

Visualization & Dashboard

- Plotly
- Streamlit

Development Tools

- Jupyter Notebook
- VS Code
- Git
- GitHub

---

📁 Project Structure

Online-retail-demand-forecasting/
│
├── data/
│   ├── raw/
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
│   ├── 04_demand_forecasting.ipynb
│   └── 05_risk_scoring.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   └── forecasting.py
│
├── dashboard/
│   └── app.py
│
├── README.md
└── requirements.txt

«Note: Update the project structure above if your final GitHub repository contains additional files or folders.»

---

🚀 How to Run the Project

1. Clone the Repository

git clone <your-github-repository-url>

2. Navigate to the Project Directory

cd Online-retail-demand-forecasting

3. Install Dependencies

pip install -r requirements.txt

4. Run the Streamlit Dashboard

python -m streamlit run dashboard/app.py

The dashboard will open in your default web browser.

---

📸 Dashboard Preview

Screenshots of the completed dashboard can be added here to provide a visual overview of the project.

Executive Dashboard

![Executive Dashboard](docs/images/executive-dashboard.png)

Sales Analytics

![Sales Analytics](docs/images/sales-analytics.png)

Demand Forecasting

![Demand Forecasting](docs/images/demand-forecasting.png)

Inventory Risk Dashboard

![Inventory Risk](docs/images/inventory-risk.png)

«Replace the image paths with the actual screenshot locations in your repository.»

---

💡 Key Business Insights

The project enables management to:

- Monitor overall retail sales performance
- Compare sales across different channels
- Identify high-performing stores
- Identify top-selling products
- Analyze category performance
- Understand historical demand patterns
- Compare actual and predicted demand
- Evaluate forecasting model performance
- Identify critical inventory
- Identify products with low stock coverage
- Monitor inventory risk across stores and SKUs
- Support informed replenishment decisions

---

📌 Key Project Outcomes

The project successfully demonstrates an end-to-end retail analytics workflow involving:

📊 Data Analytics

Historical transaction analysis and business performance measurement.

🔎 Exploratory Data Analysis

Identification of sales, demand, store, product, and channel patterns.

⚙️ Feature Engineering

Creation of temporal, lag, and rolling demand features.

🤖 Machine Learning

Application of Random Forest and XGBoost for demand prediction.

📈 Time-Series Forecasting

Evaluation of Naive, Seasonal Naive, ARIMA, and SARIMA approaches.

📦 Inventory Intelligence

Identification and classification of inventory risk.

📊 Business Intelligence

Development of an interactive Streamlit dashboard for management-oriented decision support.

---

🔮 Future Improvements

Potential future enhancements include:

- Product-level demand forecasting
- Store-level demand forecasting
- Automated future-demand forecasting pipelines
- Automated model retraining
- Advanced hyperparameter optimization
- LightGBM forecasting
- Prophet-based forecasting
- Real-time inventory monitoring
- Automated alerts for critical inventory
- Real-time dashboard data refresh
- Cloud deployment
- Automated ETL/data pipelines
- Advanced inventory optimization
- Automated replenishment recommendations
- Integration with live retail systems

---

👩‍💻 Project

Online Retail Demand Forecasting & Inventory Intelligence

Developed as part of a Data Science & Analytics Internship Project at Zidio Development.

The project demonstrates practical application of:

Data Analytics → Machine Learning → Time-Series Forecasting → Inventory Risk Analysis → Business Intelligence

---

⭐ Conclusion

The Online Retail Demand Forecasting & Inventory Intelligence project combines data analytics, exploratory data analysis, machine learning, statistical forecasting, inventory risk scoring, and interactive visualization into a single end-to-end retail intelligence solution.

The project analyzes approximately 10 million retail transactions and transforms raw transactional data into actionable business insights.

The resulting dashboard provides a management-friendly view of:

- 💰 Sales
- 📈 Demand
- 🔮 Forecasting
- 🛍️ Products
- 🏷️ Categories
- 📦 Inventory
- 🚦 Risk

A key finding from the forecasting experiment was that the Naive Baseline outperformed the tested machine learning models on MAE and MAPE, highlighting the importance of benchmarking complex models against simple forecasting approaches.

Overall, the project demonstrates how data-driven analytics and forecasting can support sales analysis, demand planning, inventory monitoring, and retail decision-making.

---

⭐ Project Highlights

10M+        Retail Transactions
30          Stores
5,000       Products / SKUs
10,000      Customers
2022–2025   Historical Data
6+          Forecasting Approaches
21K+        Inventory Risk Records
Streamlit   Interactive Dashboard

---

🏆 Technologies

Python • Pandas • NumPy • Scikit-learn • XGBoost • ARIMA • SARIMA • Plotly • Streamlit • Jupyter • Git • GitHub