# 🛍️ Online Retail Demand Forecasting & Inventory Intelligence

An end-to-end **retail analytics and demand forecasting project** that analyzes historical sales data, forecasts future demand, evaluates inventory risk, and presents business insights through an interactive **Streamlit Executive Dashboard**.

---

## 📌 Project Overview

Retail businesses need accurate demand forecasts to maintain the right inventory levels, reduce stockouts, avoid overstocking, and improve sales planning.

This project uses historical retail transaction data to:

* Analyze sales performance
* Identify sales trends and patterns
* Engineer demand-related features
* Forecast retail demand
* Compare machine learning models
* Calculate inventory risk
* Analyze product and category performance
* Build an interactive executive dashboard

The final dashboard provides management-oriented insights into **Sales Performance, Demand Forecasting, and Inventory Intelligence**.

---

## 🎯 Business Objectives

The project focuses on the following objectives:

* Understand historical retail sales patterns
* Analyze sales across different channels and stores
* Identify high-performing products and categories
* Forecast future product demand
* Evaluate forecasting model performance
* Identify products with higher inventory risk
* Support better inventory planning and business decisions

---

## 📊 Dataset

The project uses retail transaction data covering:

* **Time Period:** 2022–2025
* **Transactions:** ~10 million records
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

Major steps included:

* Duplicate removal
* Missing-value handling
* Data type conversion
* Date standardization
* Numerical column validation
* Sales and quantity validation
* Daily demand aggregation

After removing duplicate records, the cleaned dataset contained approximately **9.96 million records**.

---

## ⚙️ Feature Engineering

The demand forecasting dataset includes time-based and lag-based features.

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

These features help the models capture:

* Seasonality
* Weekly patterns
* Recent demand
* Short-term demand changes
* Longer-term demand trends

---

## 🤖 Demand Forecasting Models

The project evaluates machine learning models for demand forecasting.

### Random Forest

| Metric | Result |
| ------ | -----: |
| MAE    | 414.75 |
| RMSE   | 524.62 |
| MAPE   |  2.86% |

### XGBoost

| Metric | Result |
| ------ | -----: |
| MAE    | 417.45 |
| RMSE   | 521.34 |
| MAPE   |  2.87% |

The models provide low forecasting error, with MAPE values of approximately **2.9%**.

---

## 📦 Inventory Risk Scoring

An inventory risk scoring component is included to help identify products requiring attention.

The dashboard categorizes inventory into:

* 🔴 Critical
* 🟠 High Risk
* 🟡 Medium Risk
* 🟢 Low Risk

This allows management to identify products that may require:

* Replenishment
* Inventory monitoring
* Demand review
* Stock optimization

---

## 📈 Executive Dashboard

The project includes an interactive **Streamlit Executive Dashboard**.

### Dashboard Sections

#### Executive Summary

Key performance indicators including:

* Total Sales
* Transactions
* Quantity Sold
* Stores
* Products
* Average Order Value

#### Sales Analysis

* Daily Sales Trend
* Sales by Channel
* Store-wise Sales
* Year-wise Sales

#### Demand Analysis

* Daily Demand Trend
* Actual vs Predicted Demand

#### Product Analysis

* Top 10 Products by Sales
* Category Performance Table
* Sales by Category
* Category Sales Distribution
* Quantity Sold by Category

#### Inventory Intelligence

* Critical Inventory
* High Risk Inventory
* Medium Risk Inventory
* Low Risk Inventory
* Inventory Risk Distribution

---

## 🎛️ Dashboard Filters

The dashboard provides interactive filters for:

* **Year**
* **Sales Channel**

The charts and KPIs update according to the selected filters.

---

## 🖥️ Technology Stack

### Programming & Analysis

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* Random Forest
* XGBoost

### Visualization

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
├── README.md
└── requirements.txt
```

---

## 🚀 How to Run the Dashboard

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

### 2. Navigate to the project

```bash
cd Online-retail-demand-forecasting
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit

```bash
python -m streamlit run dashboard/app.py
```

The dashboard will open in your browser.

---

## 📌 Key Business Insights

The project enables management to:

* Monitor overall retail sales performance
* Compare different sales channels
* Identify high-performing stores
* Identify top-selling products
* Compare category-level performance
* Understand demand trends
* Compare actual and predicted demand
* Identify high-risk inventory
* Make data-driven inventory decisions

---

## 💡 Future Improvements

Potential future enhancements include:

* Automated future-demand forecasting
* Product-level forecasting
* Real-time inventory monitoring
* Automated alerts for critical inventory
* Advanced forecasting models such as LightGBM, Prophet, ARIMA/SARIMA
* Dashboard deployment using Streamlit Cloud or another cloud platform
* Automated data pipelines

---

## 👩‍💻 Project

**Online Retail Demand Forecasting & Inventory Intelligence**

Developed as part of a **Data Science & Analytics Internship project at Zidio Development**.

---

## ⭐ Conclusion

This project combines **data analytics, machine learning, demand forecasting, inventory risk analysis, and interactive visualization** into a single end-to-end retail intelligence solution.

The resulting dashboard provides a management-friendly view of retail performance and helps support more informed decisions around **sales, demand, products, categories, and inventory**.

