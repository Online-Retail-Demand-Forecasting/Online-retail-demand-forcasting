# 🛍️ Online Retail Demand Forecasting & Inventory Intelligence

An end-to-end **retail analytics, demand forecasting, and inventory intelligence project** that transforms large-scale retail transaction data into actionable business insights.

The project covers **data cleaning, exploratory data analysis, feature engineering, machine learning, time-series forecasting, inventory risk analysis, and interactive dashboard development** using Python and Streamlit.

---

## 🚀 Live Dashboard

🔗 **Streamlit Dashboard:**
https://online-retail-demand-forecasting-cvuv5o6feercgpvcpmkdog.streamlit.app/

The deployed dashboard provides interactive views of sales performance, demand forecasts, inventory intelligence, product-level insights, and business KPIs.

---

## 📌 Project Overview

Retail businesses need accurate demand estimates to maintain the right inventory levels, reduce stockouts, avoid overstocking, and improve sales planning.

This project develops an end-to-end **Retail Demand Forecasting & Inventory Intelligence System** using historical retail transaction data.

The system:

* Analyzes historical sales performance
* Identifies sales trends and seasonality
* Performs customer, product, and channel analysis
* Engineers time-series forecasting features
* Forecasts future demand using multiple models
* Compares machine learning and statistical forecasting approaches
* Calculates inventory risk
* Provides product-level insights
* Presents results through an interactive Streamlit dashboard

---

# 🎯 Project Objectives

The main objectives of this project are:

1. Analyze historical retail sales data.
2. Understand product, customer, store, and channel-level performance.
3. Identify trends, seasonality, and demand patterns.
4. Build meaningful features for demand forecasting.
5. Develop and compare multiple forecasting models.
6. Implement statistical time-series models such as **ARIMA and SARIMA**.
7. Identify inventory risk and potential stock-related issues.
8. Build an interactive business intelligence dashboard.
9. Deploy the dashboard online for easy access.
10. Provide actionable insights for retail decision-making.

---

# 🗂️ Project Structure

```text
Online-retail-demand-forecasting/
│
├── dashboard/
│   ├── app.py
│   └── pages/
│       ├── 1_Sales_Analytics.py
│       ├── 2_Forecast.py
│       ├── 3_Inventory.py
│       ├── 4_Risk_Dashboard.py
│       └── 5_Product_Details.py
│
├── data/
│   ├── raw/
│   │   └── retail_clean_dataset/
│   │       ├── customer_master.csv
│   │       ├── inventory_snapshot.csv
│   │       ├── promotions.csv
│   │       └── sales_transactions.csv
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
├── requirements.txt
├── README.md
├── .gitignore
└── .gitattributes
```

> File names may vary slightly depending on the final repository version.

---

# 📊 Dataset

The project uses a large-scale retail transaction dataset covering **2022–2025**.

### Dataset Summary

| Attribute                   |         Value |
| --------------------------- | ------------: |
| Original Transactions       | ~9.97 Million |
| Transactions After Cleaning | ~9.96 Million |
| Date Range                  |     2022–2025 |
| Stores                      |            30 |
| Products / SKUs             |         5,000 |
| Customers                   |        10,000 |
| Receipts                    | ~5.17 Million |
| Sales Channels              |             3 |

### Sales Channels

* 🏪 In-Store
* 🌐 Online
* 📱 Mobile App

---

# 🧹 Data Cleaning

The raw transaction data was cleaned before analysis and modeling.

Major preprocessing steps included:

* Duplicate record detection and removal
* Missing-value analysis
* Data type correction
* Date conversion
* Numerical column validation
* Quantity validation
* Price validation
* Total sales validation
* Consistency checks across transaction fields

After cleaning, the dataset contained approximately **9.96 million valid transaction records**.

---

# 🔍 Exploratory Data Analysis

EDA was performed to understand retail sales behavior and identify important patterns.

### Analysis Areas

* Overall sales performance
* Daily and monthly sales trends
* Yearly sales comparison
* Product performance
* Store performance
* Customer behavior
* Sales by channel
* Quantity trends
* Revenue trends
* Promotional impact
* Seasonal patterns
* Demand fluctuations

### Key Business Questions

The analysis helps answer questions such as:

* Which products generate the highest demand?
* Which stores perform best?
* Which sales channel contributes the most?
* How does demand change over time?
* Are there seasonal demand patterns?
* Which products may require inventory attention?
* What future demand can be expected?

---

# ⚙️ Feature Engineering

Time-series and forecasting features were created from the cleaned sales data.

### Temporal Features

* `year`
* `month`
* `quarter`
* `day`
* `day_of_week`
* `week_of_year`
* `is_weekend`

### Lag Features

* `lag_1`
* `lag_7`
* `lag_14`
* `lag_30`

These capture previous demand values and help models learn temporal dependencies.

### Rolling Features

* `rolling_7`
* `rolling_14`
* `rolling_30`

Rolling averages help smooth short-term fluctuations and capture demand trends.

### Target Variable

The primary forecasting target is:

```text
demand
```

---

# 🤖 Demand Forecasting

Multiple forecasting approaches were explored to determine which models provide reliable demand predictions.

The project combines:

### Machine Learning Models

* Random Forest
* XGBoost

### Statistical Time-Series Models

* ARIMA
* SARIMA

This combination allows the project to compare traditional statistical forecasting with machine-learning-based approaches.

---

# 📈 Random Forest

Random Forest was implemented as a machine-learning forecasting model using engineered temporal, lag, and rolling features.

### Performance

| Metric | Random Forest |
| ------ | ------------: |
| MAE    |        414.75 |
| RMSE   |        524.62 |
| MAPE   |         2.86% |

The model captures nonlinear relationships between historical demand and engineered forecasting features.

---

# ⚡ XGBoost

XGBoost was also implemented for demand prediction.

### Performance

| Metric | XGBoost |
| ------ | ------: |
| MAE    |  417.45 |
| RMSE   |  521.34 |
| MAPE   |   2.87% |

XGBoost provided competitive forecasting performance and successfully captured complex relationships within the engineered features.

---

# 📉 ARIMA

**ARIMA (AutoRegressive Integrated Moving Average)** was implemented as a statistical time-series forecasting approach.

ARIMA models demand based on:

* Autoregression
* Differencing
* Moving averages

It is useful for understanding temporal patterns in historical demand without relying on a large set of external predictors.

---

# 📊 SARIMA

**SARIMA (Seasonal ARIMA)** extends ARIMA by incorporating seasonal behavior.

SARIMA is particularly useful for retail demand because sales can exhibit recurring patterns related to:

* Months
* Weeks
* Seasons
* Holidays
* Repeated purchasing cycles

The project therefore includes both **ARIMA and SARIMA** to evaluate traditional statistical forecasting approaches alongside machine-learning models.

---

# 🧪 Train-Test Strategy

The forecasting dataset was divided chronologically rather than randomly.

This is important for time-series forecasting because future information must not leak into the training data.

The general approach was:

```text
Historical Data
       │
       ▼
Training Period
       │
       ▼
Forecasting Models
       │
       ▼
Testing Period
       │
       ▼
Model Evaluation
```

The model predictions were evaluated using:

### MAE

Mean Absolute Error measures the average absolute difference between actual and predicted demand.

### RMSE

Root Mean Squared Error penalizes larger prediction errors more heavily.

### MAPE

Mean Absolute Percentage Error measures prediction error relative to actual demand.

---

# 📦 Inventory Intelligence

The project also incorporates inventory analysis to identify products that may require management attention.

Inventory intelligence helps identify potential:

* Stockout risk
* Overstock risk
* High-demand products
* Low-demand products
* Inventory imbalance
* Products requiring replenishment attention

An inventory risk scoring dataset is generated and used within the dashboard.

---

# ⚠️ Inventory Risk Analysis

Products can be evaluated based on demand and inventory-related indicators.

The risk dashboard helps businesses identify:

### 🔴 High Risk

Products requiring immediate attention due to potentially unfavorable inventory-demand conditions.

### 🟡 Medium Risk

Products that should be monitored.

### 🟢 Low Risk

Products with comparatively stable inventory-demand conditions.

This helps support better inventory planning and prioritization.

---

# 📊 Interactive Streamlit Dashboard

The final solution is presented through an interactive **Streamlit Executive Dashboard**.

The dashboard contains multiple pages designed for different business analysis requirements.

## 🏠 Home

Provides an overview of the retail intelligence system and key business metrics.

---

## 📈 Sales Analytics

Provides interactive analysis of:

* Sales trends
* Revenue
* Quantity
* Yearly performance
* Monthly performance
* Channel performance
* Product performance
* Store-level insights

---

## 🔮 Demand Forecast

Displays:

* Historical demand
* Forecasted demand
* Model predictions
* Forecast trends
* Forecast comparisons
* Demand insights

The forecasting section incorporates the project's statistical and machine-learning approaches.

---

## 📦 Inventory Dashboard

Provides inventory-focused insights including:

* Inventory levels
* Product demand
* Inventory status
* Stock-related indicators
* Inventory monitoring

---

## ⚠️ Risk Dashboard

Highlights products with different levels of inventory risk.

Users can identify:

* High-risk products
* Medium-risk products
* Low-risk products
* Products requiring attention

---

## 🛍️ Product Details

Provides detailed product-level analysis.

Users can explore individual products and understand:

* Demand
* Sales
* Performance
* Historical trends
* Forecast information
* Inventory-related insights

---

# 🛠️ Technologies Used

### Programming

* Python

### Data Analysis

* Pandas
* NumPy

### Visualization

* Matplotlib
* Plotly

### Machine Learning

* Scikit-learn
* Random Forest
* XGBoost

### Time-Series Forecasting

* ARIMA
* SARIMA
* Statsmodels

### Dashboard

* Streamlit

### Development & Version Control

* Jupyter Notebook
* Git
* GitHub

### Deployment

* Streamlit Community Cloud

---

# 📚 Project Workflow

```text
Raw Retail Data
       │
       ▼
Data Cleaning
       │
       ▼
Exploratory Data Analysis
       │
       ▼
Feature Engineering
       │
       ▼
Demand Aggregation
       │
       ▼
Train-Test Split
       │
       ├───────────────┐
       ▼               ▼
Machine Learning   Time-Series
Models             Models
       │               │
       ├───────┬───────┤
       │       │       │
       ▼       ▼       ▼
 Random     ARIMA    SARIMA
 Forest
       │
       ▼
   XGBoost
       │
       ▼
Model Evaluation
       │
       ▼
Inventory Risk Analysis
       │
       ▼
Streamlit Dashboard
       │
       ▼
Streamlit Cloud Deployment
```

---

# 📌 Key Insights

The project demonstrates several important retail analytics concepts:

* Retail demand changes over time and contains strong temporal patterns.
* Monthly and historical demand information can be highly useful for forecasting.
* Lag-based features capture recent demand behavior.
* Rolling features help capture short-term and medium-term trends.
* Machine-learning models can capture nonlinear relationships in demand.
* ARIMA and SARIMA provide traditional statistical approaches for time-series forecasting.
* Inventory risk analysis can help prioritize products requiring attention.
* Interactive dashboards make complex forecasting results easier for business users to understand.

---

# 💡 Business Value

The solution can help retail organizations:

### 📦 Improve Inventory Planning

Use demand forecasts to make better replenishment decisions.

### 🚨 Reduce Stockout Risk

Identify products where inventory may not adequately support expected demand.

### 📉 Reduce Overstock

Identify products with comparatively lower demand and potential excess inventory.

### 📈 Improve Sales Planning

Use historical trends and forecasts to support future planning.

### 🎯 Identify High-Performing Products

Understand which products, stores, and channels contribute most to sales.

### 📊 Support Data-Driven Decisions

Provide decision-makers with interactive dashboards rather than relying only on static reports.

---

# ▶️ How to Run the Project Locally

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Online-retail-demand-forecasting
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit dashboard

```bash
python -m streamlit run dashboard/app.py
```

The application will open in your browser.

---

# ☁️ Deployment

The dashboard has been deployed using **Streamlit Community Cloud**.

### Deployment Flow

```text
GitHub Repository
       │
       ▼
Streamlit Community Cloud
       │
       ▼
Install requirements
       │
       ▼
Run dashboard/app.py
       │
       ▼
Live Web Application
```

### Live Application

https://online-retail-demand-forecasting-cvuv5o6feercgpvcpmkdog.streamlit.app/

---

# 🔐 Data & Repository Notes

Large raw datasets may not always be included directly in the GitHub repository due to storage and deployment limitations.

The dashboard uses the required processed datasets available within the project structure.

Sensitive credentials, environment files, temporary files, and unnecessary generated files should not be committed to the repository.

---

# 🔮 Future Enhancements

Potential future improvements include:

* Real-time inventory updates
* Automated model retraining
* Advanced hyperparameter tuning
* Prophet forecasting
* LightGBM forecasting
* Deep-learning forecasting using LSTM/GRU
* Automated stock replenishment recommendations
* Supplier lead-time integration
* Holiday and festival effects
* Price elasticity analysis
* Promotion optimization
* Customer-level demand forecasting
* Automated forecasting reports
* Cloud database integration

---

# 👥 Project Team

This project was developed as part of the **Zidio Development Internship**.

The project combines contributions across:

* Data preprocessing
* Exploratory data analysis
* Feature engineering
* Demand forecasting
* Inventory intelligence
* Dashboard development
* Documentation
* Deployment

---

# 🏆 Project Outcome

The completed project provides an end-to-end retail analytics solution that combines:

**Data → Analysis → Forecasting → Inventory Intelligence → Visualization → Deployment**

The final Streamlit application transforms complex retail transaction data into an interactive decision-support system for understanding sales performance, forecasting demand, and monitoring inventory risk.

---

## ⭐ Final Deliverables

* ✅ Cleaned retail dataset
* ✅ Exploratory data analysis
* ✅ Feature engineering
* ✅ Demand forecasting
* ✅ Random Forest model
* ✅ XGBoost model
* ✅ ARIMA model
* ✅ SARIMA model
* ✅ Inventory risk analysis
* ✅ Interactive Streamlit dashboard
* ✅ Multiple dashboard pages
* ✅ Project documentation
* ✅ GitHub repository
* ✅ Live Streamlit deployment

---

## 📎 Project Links

**GitHub Repository:**
Add your final GitHub repository URL here.

**Live Dashboard:**
https://online-retail-demand-forecasting-cvuv5o6feercgpvcpmkdog.streamlit.app/

---

# ⭐ Thank You

Thank you for exploring the **Online Retail Demand Forecasting & Inventory Intelligence** project.

This project demonstrates how **data analytics, machine learning, time-series forecasting, and business intelligence** can be combined to build a practical retail decision-support system.
