# 🛍️ Online Retail Demand Forecasting & Inventory Intelligence

An end-to-end **retail analytics, demand forecasting, and inventory intelligence project** that analyzes historical retail transactions, identifies sales trends, forecasts demand, evaluates inventory risk, and presents business insights through an interactive **Streamlit Executive Dashboard**.

---

## 📌 Project Overview

Retail businesses need accurate demand insights to maintain appropriate inventory levels, reduce stockouts, avoid overstocking, and improve sales planning.

This project uses historical retail transaction data to:

* Analyze historical sales performance
* Identify sales trends and patterns
* Perform exploratory data analysis
* Engineer demand-related features
* Forecast retail demand
* Compare forecasting models against baseline methods
* Calculate inventory risk
* Identify critical and high-risk inventory
* Analyze product and category performance
* Build an interactive Streamlit dashboard
* Generate management-oriented business insights

The final solution combines **Data Analytics, Machine Learning, Demand Forecasting, Inventory Risk Scoring, and Interactive Visualization** into a single retail intelligence workflow.

---

## 🎯 Business Objectives

The project focuses on the following objectives:

* Understand historical retail sales patterns
* Analyze sales across different channels and stores
* Identify high-performing products and categories
* Understand daily demand behavior
* Forecast future retail demand
* Evaluate forecasting model performance
* Compare machine learning models with simple forecasting baselines
* Identify inventory items requiring attention
* Analyze stock coverage and inventory risk
* Support data-driven inventory and sales decisions

---

## 📊 Dataset

The project uses synthetic retail transaction and inventory data covering:

* **Time Period:** 2022–2025
* **Transactions:** Approximately 10 million records
* **Stores:** 30
* **Products/SKUs:** 5,000
* **Customers:** 10,000
* **Channels:** In-Store, Online, Mobile App

### Main Transaction Columns

| Column         | Description                    |
| -------------- | ------------------------------ |
| `date`         | Transaction date               |
| `receipt_id`   | Transaction/receipt identifier |
| `store_id`     | Store identifier               |
| `sku_id`       | Product/SKU identifier         |
| `customer_id`  | Customer identifier            |
| `quantity`     | Quantity purchased             |
| `unit_price`   | Unit price                     |
| `total_value`  | Total transaction value        |
| `channel`      | Sales channel                  |
| `discount_pct` | Discount percentage            |
| `promo_id`     | Promotion identifier           |

---

## 🔄 Project Workflow

```text
Data Collection
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Feature Engineering
      ↓
Demand Forecasting
      ↓
Model Evaluation
      ↓
Inventory Risk Scoring
      ↓
Streamlit Dashboard
      ↓
Business Insights
```

---

## 🧹 Data Cleaning

The raw transaction data was processed to improve data quality and consistency.

Major data-cleaning steps included:

* Duplicate removal
* Missing-value checking and handling
* Data type conversion
* Date standardization
* Numerical column validation
* Sales and quantity validation
* Daily demand aggregation

After duplicate removal, the cleaned transaction dataset contained approximately **9.96 million records**.

---

## 🔎 Exploratory Data Analysis

The EDA stage was used to understand the underlying sales and demand patterns.

Key analyses included:

* Daily sales trends
* Daily demand trends
* Monthly sales patterns
* Year-wise sales performance
* Sales by channel
* Customer-level sales
* Store-level performance
* Product-level performance
* Transaction patterns
* Demand behavior over time

The analysis helped identify important temporal patterns and provided the foundation for demand forecasting.

---

## ⚙️ Feature Engineering

The demand forecasting dataset contains time-based, lag-based, and rolling statistical features.

### Features Used

* `year`
* `month`
* `quarter`
* `day_of_week`
* `day`
* `week_of_year`
* `is_weekend`
* `lag_1`
* `lag_7`
* `lag_14`
* `lag_30`
* `rolling_7`
* `rolling_14`
* `rolling_30`

### Target Variable

```text
demand
```

These features help the forecasting models capture:

* Seasonality
* Weekly patterns
* Recent demand behavior
* Short-term demand changes
* Longer-term demand trends

---

## 🤖 Demand Forecasting

Several forecasting approaches were evaluated using a time-based train/test split.

### Train/Test Split

```text
Training Data: 1144 rows
Testing Data: 287 rows

Training Period:
2022-01-31 → 2025-03-19

Testing Period:
2025-03-20 → 2025-12-31
```

The models were evaluated using:

* **MAE — Mean Absolute Error**
* **RMSE — Root Mean Squared Error**
* **MAPE — Mean Absolute Percentage Error**

---

## 📈 Model Comparison

| Model                  |        MAE |       RMSE |      MAPE |
| ---------------------- | ---------: | ---------: | --------: |
| **Naive Baseline**     | **366.53** | **486.85** | **2.56%** |
| Random Forest          |     414.75 |     524.62 |     2.86% |
| XGBoost                |     417.45 | **521.34** |     2.87% |
| Improved Random Forest |     429.45 |     540.88 |     2.95% |
| Seasonal Naive (7-day) |     488.05 |     733.76 |     3.34% |

### Model Evaluation Insights

The **Naive Baseline** achieved the lowest MAE and MAPE in this experiment, demonstrating the importance of benchmarking machine learning models against simple forecasting approaches.

Among the machine learning models:

* **Random Forest** achieved a lower MAE and MAPE than XGBoost.
* **XGBoost** achieved the lowest RMSE among the machine learning models.
* The improved Random Forest feature set did not improve performance over the original Random Forest model.
* The 7-day Seasonal Naive approach performed worse than the other evaluated methods.

This comparison provides a realistic evaluation of forecasting performance rather than relying only on machine learning models.

---

## 📦 Inventory Risk Scoring

An inventory risk scoring component was developed to identify products that may require inventory attention.

The analysis considers inventory-related factors such as:

* Stock on hand
* Reorder point
* Safety stock
* Average daily demand
* Stock coverage days
* Risk score

### Risk Categories

The final inventory classification contains:

* 🔴 **Critical**
* 🟠 **High Risk**
* 🟡 **Medium Risk**
* 🟢 **Low Risk**

### Final Risk Distribution

| Risk Level     |      Count |
| -------------- | ---------: |
| 🟢 Low Risk    |     18,375 |
| 🔴 Critical    |      2,815 |
| 🟡 Medium Risk |         30 |
| 🟠 High Risk   |          8 |
| **Total**      | **21,228** |

The risk analysis helps identify inventory items that may require:

* Immediate replenishment
* Inventory monitoring
* Demand review
* Stock optimization
* Reorder planning

---

## 📊 Processed Datasets

The major processed datasets generated during the project include:

### `sales_transactions_cleaned.csv`

Cleaned transaction-level retail data used for sales analysis and dashboard visualizations.

### `daily_demand_features.csv`

Daily aggregated demand data containing time-based, lag, and rolling features used for forecasting.

### `demand_forecast_results.csv`

Forecasting results containing actual and predicted demand values used for model evaluation and dashboard visualization.

### `inventory_risk_scoring.csv`

Inventory-level risk scoring dataset containing stock information, demand estimates, coverage metrics, risk scores, and final risk categories.

---

## 📈 Executive Dashboard

The project includes an interactive **Streamlit Executive Dashboard** designed to provide management-oriented retail insights.

### Dashboard Capabilities

The dashboard brings together:

* Sales performance
* Demand trends
* Forecast results
* Inventory intelligence
* Product performance
* Risk analysis
* Key business KPIs

### Executive Summary

Key performance indicators include:

* Total Sales
* Total Transactions
* Quantity Sold
* Number of Stores
* Number of Products
* Average Order Value

### Sales Analysis

The sales section provides insights into:

* Daily Sales Trend
* Sales by Channel
* Store-wise Sales
* Year-wise Sales
* Product performance

### Demand Analysis

The demand section provides:

* Daily Demand Trend
* Actual vs Predicted Demand
* Forecast performance
* Demand patterns over time

### Product Analysis

The product section provides:

* Top Products by Sales
* Product-level performance
* Category performance
* Sales by Category
* Quantity Sold by Category

### Inventory Intelligence

The inventory section provides:

* Critical Inventory
* High Risk Inventory
* Medium Risk Inventory
* Low Risk Inventory
* Inventory Risk Distribution
* Stock Coverage Analysis
* Store-level Risk Analysis

---

## 🎛️ Dashboard Filters

The dashboard provides interactive filters to allow users to explore the data dynamically.

Depending on the dashboard section, filters include:

* **Year**
* **Sales Channel**
* **Store**
* **Product/SKU**
* **Risk Level**

The charts, tables, and KPIs update based on the selected filters where applicable.

---

## 🖥️ Technology Stack

### Programming & Data Analysis

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* Random Forest
* XGBoost

### Visualization & Dashboard

* Plotly
* Streamlit

### Development Tools

* Jupyter Notebook
* VS Code
* Git
* GitHub

---

## 📁 Project Structure

```text
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
```

---

## 🚀 How to Run the Dashboard

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Navigate to the Project

```bash
cd Online-retail-demand-forecasting
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit

```bash
python -m streamlit run dashboard/app.py
```

The dashboard will open in your default web browser.

---

## 📌 Key Business Insights

The project enables management to:

* Monitor overall retail sales performance
* Compare sales across different channels
* Identify high-performing stores
* Identify top-selling products
* Analyze category performance
* Understand historical demand patterns
* Compare actual and predicted demand
* Evaluate forecasting model performance
* Identify critical inventory
* Identify products with low stock coverage
* Monitor inventory risk across stores and SKUs
* Support more informed replenishment decisions

---

## 💡 Future Improvements

Potential future enhancements include:

* Product-level demand forecasting
* Automated future-demand forecasting pipelines
* Real-time inventory monitoring
* Automated alerts for critical inventory
* Advanced forecasting models such as LightGBM, Prophet, ARIMA, and SARIMA
* Automated model retraining
* Real-time dashboard data refresh
* Cloud deployment
* Automated data pipelines
* Improved inventory optimization and replenishment recommendations

---

## 👩‍💻 Project

**Online Retail Demand Forecasting & Inventory Intelligence**

Developed as part of a **Data Science & Analytics Internship Project at Zidio Development**.

The project demonstrates an end-to-end workflow covering:

**Data Analytics → Machine Learning → Demand Forecasting → Inventory Risk Analysis → Business Intelligence Dashboard**

---

## ⭐ Conclusion-

This project combines **data analytics, exploratory data analysis, machine learning, demand forecasting, inventory risk scoring, and interactive visualization** into an end-to-end retail intelligence solution.

The resulting dashboard provides a management-friendly view of:

* **Sales**
* **Demand**
* **Forecasting**
* **Products**
* **Categories**
* **Inventory**
* **Risk**

The project also demonstrates the importance of comparing machine learning forecasting models against simple baseline methods and using analytical results to support practical retail inventory decisions.

