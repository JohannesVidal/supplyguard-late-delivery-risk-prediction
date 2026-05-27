# SupplyGuard — Delivery Delay Risk Prediction for E-Commerce Operations

End-to-end analytics and machine learning project that helps e-commerce operations teams identify high-risk orders, monitor delivery performance, and prioritize late-delivery prevention actions.

SupplyGuard simulates a real consulting-style data project for an e-commerce marketplace. The project combines data understanding, data cleaning, SQL modeling, exploratory analysis, feature engineering, machine learning, Tableau dashboards, and a Streamlit scoring app.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Project Objective](#project-objective)
- [Dataset](#dataset)
- [Target Definition](#target-definition)
- [Project Architecture](#project-architecture)
- [Workflow](#workflow)
- [Key Insights](#key-insights)
- [Machine Learning Results](#machine-learning-results)
- [Risk Segmentation](#risk-segmentation)
- [Tableau Dashboards](#tableau-dashboards)
- [Streamlit App](#streamlit-app)
- [Repository Structure](#repository-structure)
- [How to Run Locally](#how-to-run-locally)
- [Important Files](#important-files)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Portfolio Positioning](#portfolio-positioning)
- [Author](#author)

---

## Project Overview

SupplyGuard is an end-to-end Data Analytics and Machine Learning project focused on late delivery risk in e-commerce operations.

The project uses the Olist Brazilian E-Commerce dataset to analyze delivery performance, identify operational risk patterns, build a leakage-safe prediction model, and translate the results into practical business tools.

The final project includes:

- Data understanding and quality assessment
- Data cleaning and processed data creation
- SQL and relational modeling
- MySQL Workbench schema documentation
- Business-focused delivery performance EDA
- Leakage-safe feature engineering
- Machine learning classification pipeline
- Model interpretation and business impact analysis
- Tableau Public dashboards
- Streamlit operational scoring app

---

## Business Problem

Late deliveries create operational pressure and damage customer satisfaction in e-commerce.

Operations teams need to understand where delivery delays are more likely to happen and prioritize the orders that deserve closer monitoring before the customer is affected.

The core business question is:

> How can an e-commerce company identify orders with higher late-delivery risk before delivery happens and use that information to improve operational decision-making?

---

## Project Objective

The objective of SupplyGuard is to build a practical decision-support workflow that helps an e-commerce company:

- Monitor historical delivery performance
- Identify geographic, product, freight, and timing patterns behind late deliveries
- Predict late-delivery risk using information available before the delivery outcome
- Rank orders by risk
- Flag high-risk orders for operational follow-up
- Communicate insights through dashboards and an operational scoring app

The model is not positioned as a fully production-ready automated decision system. It is designed as a risk-prioritization layer.

---

## Dataset

The project uses the Olist Brazilian E-Commerce Public Dataset, a relational e-commerce dataset containing marketplace order information.

Main raw tables include:

- Orders
- Customers
- Sellers
- Products
- Order items
- Payments
- Reviews
- Geolocation
- Product category translations

The dataset is relational, so a major part of the project involved validating safe joins and avoiding row multiplication across orders, items, payments, reviews, and geolocation.

---

## Target Definition

The official target is defined at calendar-date level:

```text
is_late = delivered_date > estimated_delivery_date
```

SQL implementation:

```sql
DATE(order_delivered_customer_date) > DATE(order_estimated_delivery_date)
```

Pandas implementation:

```python
order_delivered_customer_date.dt.normalize() > order_estimated_delivery_date.dt.normalize()
```

Orders delivered on the estimated delivery date are not considered late, regardless of timestamp.

This date-only definition was adopted because `order_estimated_delivery_date` represents a promised delivery date, not an exact timestamp deadline.

Official target results:

| Metric | Value |
|---|---:|
| Delivered orders analyzed | 96,470 |
| On-time orders | 89,936 |
| Late orders | 6,534 |
| Late delivery rate | 6.77% |

---

## Project Architecture

SupplyGuard is structured as a complete analytics-to-action workflow:

```text
Raw Olist CSV files
        │
        ▼
01 Data Understanding
        │
        ▼
02 Data Cleaning
        │
        ▼
03 SQL & Relational Modeling
        │
        ▼
04 Delivery Performance EDA
        │
        ▼
05 Feature Engineering
        │
        ▼
06 Machine Learning Modeling
        │
        ▼
07 Business Impact & Model Interpretation
        │
        ├── Tableau Dashboards
        │
        └── Streamlit Scoring App
```

The project separates responsibilities clearly:

- SQL / relational layer: validates structure and safe joins
- EDA: explains historical delivery performance
- ML: predicts and ranks late-delivery risk
- Tableau: monitors business performance and model behavior at aggregate level
- Streamlit: scores individual or batch orders for operational action

---

## Workflow

### 01 — Data Understanding

The first notebook establishes the raw data baseline.

It covers:

- Raw CSV validation
- Table shapes and column inventory
- Data types and missing values
- Duplicate checks
- Preliminary primary and foreign key checks
- Relational structure overview
- Initial leakage considerations

No cleaning, target creation, feature engineering, or modeling is performed in this stage.

---

### 02 — Data Cleaning

The second notebook creates clean and consistent processed tables.

Main decisions:

- Conservative cleaning strategy
- Date and timestamp conversion
- Exact duplicate removal from geolocation
- Product category translation enrichment
- Aggregated geolocation table by zip code prefix
- Missing values preserved where analytically meaningful
- Post-delivery fields kept for target creation and diagnostic analysis, but documented as leakage-sensitive

Important output:

```text
data/processed/
```

---

### 03 — SQL & Relational Modeling

The third notebook builds the relational foundation of the project.

Main goals:

- Validate primary and compound keys
- Validate relationships between cleaned tables
- Quantify row multiplication risks
- Define safe join strategy
- Create reusable order-level aggregate tables
- Build SQL scripts and MySQL layer
- Document the relational schema with an EER diagram

Safe join strategy:

- Use `orders` as base for order-level analysis
- Aggregate order items, payments, and reviews before joining to orders
- Use aggregated geolocation by zip prefix for geographic joins

---

### 04 — Delivery Performance EDA

This notebook analyzes historical delivery performance from a business perspective.

Main questions:

- What is the overall late delivery rate?
- How severe are late deliveries?
- Which geographies have higher risk?
- How do seller-customer routes affect late delivery?
- How do freight, product category, order value, and timing relate to delay risk?
- How do late deliveries affect customer review scores?

Important result:

```text
Official late delivery rate: 6.77%
```

---

### 05 — Feature Engineering

This notebook creates the official modeling dataset.

Main principles:

- One row per delivered order
- Official date-only target
- Features available at or shortly after payment approval
- No post-delivery leakage variables
- No encoding, scaling, imputation, or modeling yet

Output:

```text
data/processed/modeling_dataset.csv
data/processed/feature_dictionary.csv
data/processed/feature_engineering_summary.csv
```

The final modeling dataset contains:

| Metric | Value |
|---|---:|
| Rows | 96,470 |
| Columns | 35 |
| Late orders | 6,534 |
| Late delivery rate | 6.77% |
| Duplicate order IDs | 0 |

---

### 06 — Machine Learning Modeling

This notebook builds the leakage-safe machine learning workflow.

The modeling process uses:

- Train / validation / test split
- Sklearn pipelines
- ColumnTransformer preprocessing
- Train-only fitting of imputers, scalers, and encoders
- Consistent model comparison
- Validation-based threshold selection
- Untouched test set final evaluation

Compared models:

- DummyClassifier baseline
- Logistic Regression
- Decision Tree
- Random Forest
- Extra Trees

Final selected model:

```text
Random Forest classifier
```

Selected threshold:

```text
0.16
```

---

### 07 — Business Impact & Model Interpretation

This notebook translates the final model into business value.

It does not retrain models or change the threshold.

It focuses on:

- Risk bands
- Lift vs baseline
- Top-risk order concentration
- Feature importance by business area
- Prediction outcome interpretation
- Operational recommendations
- Dashboard and Streamlit implications
- Limitations and future improvements

---

## Key Insights

### Delivery Performance

Late delivery is a focused but meaningful operational issue:

```text
6.77% of delivered orders arrived after the estimated delivery date.
```

Late deliveries are also a severity problem:

- Median late delay: 7 days
- P95 late delay: 31 days

---

### Geography and Route Risk

Geography is one of the strongest operational signals.

Cross-state orders are riskier than same-state orders:

| Route type | Late delivery rate |
|---|---:|
| Same-state | 4.52% |
| Cross-state | 8.04% |

The `SP → RJ` route is especially relevant:

| Metric | Value |
|---|---:|
| Orders | 8,131 |
| Late orders | 1,152 |
| Late delivery rate | 14.17% |

---

### Customer Experience Impact

Late delivery strongly affects customer review scores:

| Delivery status | Average review score |
|---|---:|
| On-time | 4.29 |
| Late | 2.27 |

Review data is used only as post-delivery diagnostic information, not as a predictive model feature.

---

### Peak Months

Delivery risk varies significantly over time.

Peak months showed much higher late delivery rates:

| Period | Late delivery rate |
|---|---:|
| Other months | 4.46% |
| Peak months | 15.15% |

---

## Machine Learning Results

The final model is interpreted as a risk-prioritization tool, not as a complete detector of all late deliveries.

Final model:

```text
Random Forest classifier
```

Final threshold:

```text
0.16
```

Final test performance:

| Metric | Value |
|---|---:|
| Accuracy | 89.91% |
| Precision | 29.14% |
| Recall | 34.20% |
| F1-score | 31.47% |
| ROC-AUC | 76.20% |
| PR-AUC | 23.84% |

Confusion matrix:

| Actual / Predicted | Predicted On Time | Predicted Late |
|---|---:|---:|
| Actual On Time | 16,900 | 1,087 |
| Actual Late | 860 | 447 |

Business interpretation:

- Baseline late delivery rate: 6.77%
- Flagged orders late delivery rate: 29.14%
- Lift vs baseline: 4.3x
- Flagged order share: 7.95%

This means the model identifies a smaller group of orders with a much higher concentration of late deliveries than the overall dataset.

---

## Risk Segmentation

Risk bands were created to translate model scores into operational categories.

| Risk band | Late rate |
|---|---:|
| Low Risk | 3.44% |
| Medium Risk | 10.06% |
| High Risk | 23.57% |
| Very High Risk | 40.00% |

Top-risk concentration:

| Segment | Late rate | Late deliveries captured |
|---|---:|---:|
| Top 5% highest-risk orders | 32.99% | 24.33% |
| Top 10% highest-risk orders | 25.92% | 38.26% |
| Top 20% highest-risk orders | 18.61% | 54.93% |

This supports the use of the model as an operational prioritization layer.

---

## Tableau Dashboards

The Tableau dashboard phase was completed directly in Tableau Public.

Tableau is used as the monitoring and reporting layer of the project.

The workbook contains two dashboards:

### 1. Delivery Operations Overview

Purpose:

> Monitor historical delivery performance and identify operational late-delivery patterns.

Main sections:

- Delivered orders
- Late delivery rate
- Late orders
- Median late delay
- Monthly late delivery trend
- Route type late rate
- Top customer states by late orders
- Top customer states by late delivery rate
- Top seller-customer routes
- Review score by delivery status
- Brazil late delivery rate map

Main message:

> Late delivery is not random. It varies over time, is higher for cross-state deliveries, concentrates in specific states and routes, and is strongly associated with lower review scores.

### 2. Predictive Risk Monitoring

Purpose:

> Show how the machine learning model supports operations by prioritizing orders with higher-than-average late delivery risk.

Main sections:

- Baseline late rate
- Flagged late rate
- Lift vs baseline
- Flagged order share
- Late rate by risk band
- Orders by risk band
- Top-risk concentration
- Feature area importance
- Prediction outcome matrix

Main message:

> The model does not capture every late delivery, but it identifies groups of orders with substantially higher risk than the baseline.

Tableau Public link:

```text
TABLEAU_PUBLIC_LINK_HERE
```

Dashboard screenshots:

```text
reports/figures/tableau_dashboard_1_delivery_operations.png
reports/figures/tableau_dashboard_2_predictive_risk_monitoring.png
```

---

## Streamlit App

The Streamlit app is the operational scoring and action layer of the project.

It does not duplicate Tableau.

### Tableau vs Streamlit

| Tool | Role | Business use |
|---|---|---|
| Tableau | Monitoring and reporting layer | Track delivery performance and model risk at aggregate level |
| Streamlit | Operational scoring layer | Score individual or batch orders and recommend action |

### Streamlit Features

The app includes four sections:

1. Home / Overview
   - Explains SupplyGuard
   - Shows model context
   - Explains risk bands and business use

2. Single Order Scoring
   - Manual order input form
   - Predicts late-delivery probability
   - Assigns risk band
   - Flags orders above threshold
   - Returns recommended operational action

3. Batch Scoring
   - Upload CSV file
   - Validate required columns
   - Score all orders
   - Assign risk band
   - Flag high-risk orders
   - Download scored CSV

4. Model Information / Limitations
   - Explains model design
   - Explains leakage-safe workflow
   - Lists limitations and intended use

### Risk Band Logic

| Risk band | Score range | Recommended action |
|---|---:|---|
| Low Risk | `< 0.08` | Standard handling |
| Medium Risk | `0.08 – 0.16` | Monitor normally |
| High Risk | `0.16 – 0.25` | Prioritize logistics follow-up |
| Very High Risk | `>= 0.25` | Escalate and consider proactive customer communication |

Flagging rule:

```python
flagged_order = predicted_late_probability >= 0.16
```

Streamlit app link:

```text
STREAMLIT_APP_LINK_HERE
```

---

## Repository Structure

```text
supplyguard-delivery-risk/
│
├── data/
│   ├── raw/                         # Raw data not committed
│   └── processed/                   # Selected processed files used by app/dashboard
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_sql_modeling.ipynb
│   ├── 04_eda_delivery_performance.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_modeling.ipynb
│   └── 07_business_impact_and_model_interpretation.ipynb
│
├── sql/
│   ├── 00_create_database.sql
│   ├── 01_create_tables.sql
│   ├── 02_import_notes.sql
│   ├── 03_quality_checks.sql
│   ├── 04_relationship_checks.sql
│   ├── 05_create_views.sql
│   ├── 06_business_queries.sql
│   └── schema/
│       ├── supplyguard_schema.mwb
│       └── supplyguard_schema.png
│
├── scripts/
│   └── load_processed_to_mysql.py
│
├── outputs/
│   ├── best_model_compressed.pkl
│   ├── model_comparison_results.csv
│   ├── test_predictions.csv
│   ├── test_predictions_with_risk_segments.csv
│   ├── risk_band_summary.csv
│   ├── top_risk_summary.csv
│   ├── feature_importance_summary.csv
│   ├── feature_area_summary.csv
│   └── prediction_outcome_summary.csv
│
├── reports/
│   └── figures/
│       ├── tableau_dashboard_1_delivery_operations.png
│       └── tableau_dashboard_2_predictive_risk_monitoring.png
│
├── streamlit_app/
│   ├── app.py
│   └── assets/
│       ├── SupplyGuard_Logo.png
│       └── SupplyGuard_Logo_Cropped.png
│
├── .streamlit/
│   └── config.toml
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/supplyguard-delivery-risk.git
cd supplyguard-delivery-risk
```

### 2. Create environment

Using Conda:

```bash
conda create -n supplyguard python=3.11 -y
conda activate supplyguard
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit app

```bash
streamlit run streamlit_app/app.py
```

The app expects the following files to exist:

```text
outputs/best_model_compressed.pkl
data/processed/modeling_dataset.csv
data/processed/feature_dictionary.csv
outputs/test_predictions_with_risk_segments.csv
streamlit_app/assets/SupplyGuard_Logo.png
streamlit_app/assets/SupplyGuard_Logo_Cropped.png
```

---

## Important Files

### Core notebooks

```text
notebooks/01_data_understanding.ipynb
notebooks/02_data_cleaning.ipynb
notebooks/03_sql_modeling.ipynb
notebooks/04_eda_delivery_performance.ipynb
notebooks/05_feature_engineering.ipynb
notebooks/06_modeling.ipynb
notebooks/07_business_impact_and_model_interpretation.ipynb
```

### SQL layer

```text
sql/
scripts/load_processed_to_mysql.py
```

### Streamlit app

```text
streamlit_app/app.py
.streamlit/config.toml
```

### Model artifact

```text
outputs/best_model_compressed.pkl
```

The original uncompressed model artifact was not included because it was too large for normal GitHub usage.

---

## Limitations

This project is intentionally leakage-safe, which makes the prediction task harder but more realistic.

Main limitations:

- No carrier or logistics provider data
- No warehouse capacity data
- No inventory availability data
- No weather, strike, or holiday disruption data
- No real-time tracking events
- No production monitoring infrastructure
- The model was trained on historical Olist data and should not be treated as production-ready
- Model probabilities should be interpreted as risk scores for prioritization, not guaranteed delivery outcomes

The model is useful for identifying higher-risk groups of orders, but it does not capture every late delivery.

---

## Future Improvements

Potential next steps:

- Add carrier and logistics event data
- Add weather and holiday features
- Use chronological validation as a robustness check
- Create train-safe historical seller/category/state risk features
- Calibrate predicted probabilities
- Use cost-based threshold optimization
- Deploy Streamlit app online
- Add model monitoring over time
- Extend Tableau dashboard with refreshed data simulation
- Build an operational workflow around high-risk order escalation

---

## Portfolio Positioning

SupplyGuard demonstrates:

- End-to-end project structure
- Relational data understanding
- Data cleaning and processed data creation
- SQL and MySQL Workbench workflow
- Business-focused EDA
- Leakage-safe target definition
- Feature engineering
- Machine learning pipelines
- Model interpretation
- Dashboarding in Tableau
- Streamlit app development
- Business storytelling and decision support

The project is designed to show both Data Analytics and Data Science skills in a realistic business context.

---

## Author

Johannes Vidal

Data Analyst / Data Science portfolio project.