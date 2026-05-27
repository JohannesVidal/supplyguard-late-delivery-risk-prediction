# SupplyGuard — Delivery Delay Risk Prediction for E-Commerce Operations

SupplyGuard is an end-to-end analytics and machine learning project focused on late delivery risk in e-commerce operations.

The project uses the Olist Brazilian E-Commerce dataset to understand delivery performance, identify operational risk patterns, build a leakage-safe prediction model, and translate the results into business tools through Tableau and Streamlit.

The goal is not only to train a model, but to build a realistic workflow around a business problem: helping an e-commerce operations team identify orders with higher late-delivery risk before the customer is affected.

---

## Live Project Links

- [Tableau Dashboard](https://public.tableau.com/app/profile/johannes.vidal.blickle/viz/supplyguard_tableau_dashboard/Dashboard1-DeliveryOperationsOverview)
- [Streamlit App](https://supplyguard-late-delivery-risk-prediction-app.streamlit.app/)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Project Objective](#project-objective)
- [Dataset](#dataset)
- [Target Definition](#target-definition)
- [Project Workflow](#project-workflow)
- [Repository Structure](#repository-structure)
- [Key Insights](#key-insights)
- [Machine Learning Results](#machine-learning-results)
- [Tableau Dashboard](#tableau-dashboard)
- [Streamlit App](#streamlit-app)
- [How to Run Locally](#how-to-run-locally)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Project Context](#project-context)
- [Author](#author)

---

## Project Overview

SupplyGuard simulates a consulting-style project for an e-commerce marketplace.

It combines:

- data understanding;
- data cleaning;
- SQL and relational modeling;
- exploratory data analysis;
- feature engineering;
- machine learning classification;
- model interpretation;
- Tableau dashboards;
- Streamlit operational scoring.

The project follows a full workflow from raw relational data to business-facing outputs.

---

## Business Problem

Late deliveries create operational pressure and reduce customer satisfaction.

For an e-commerce company, the problem is not only knowing that some orders arrived late. The more valuable question is:

> Can we identify which orders are more likely to arrive late before the delivery happens?

If operations teams can identify higher-risk orders earlier, they can prioritize monitoring, logistics follow-up, escalation, or proactive customer communication.

---

## Project Objective

The objective of SupplyGuard is to build a decision-support workflow that helps an e-commerce company:

- monitor delivery performance;
- understand where late deliveries are concentrated;
- identify operational patterns behind delays;
- predict late-delivery risk using pre-delivery information;
- rank orders by risk;
- flag high-risk orders for follow-up;
- communicate results through dashboards and an app.

The model is not presented as a fully automated production system. It is used as a **risk-prioritization layer**.

---

## Dataset

The project uses the **Olist Brazilian E-Commerce Public Dataset**.

The dataset contains relational e-commerce data, including:

- orders;
- customers;
- sellers;
- products;
- order items;
- payments;
- reviews;
- geolocation;
- product category translations.

Because the data is relational, a significant part of the project focuses on validating table relationships and avoiding row multiplication when joining orders with items, payments, reviews, or geolocation.

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

Orders delivered on the estimated delivery date are **not** considered late, even if the timestamp is later than midnight.

This definition was chosen because `order_estimated_delivery_date` represents a promised delivery date, not an exact timestamp deadline.

Official target distribution:

| Metric | Value |
|---|---:|
| Delivered orders analyzed | 96,470 |
| On-time orders | 89,936 |
| Late orders | 6,534 |
| Late delivery rate | 6.77% |

---

## Project Workflow

### 01 — Data Understanding

The first notebook establishes the raw data baseline.

It validates the raw CSV files, reviews table shapes, columns, data types, missing values, duplicate rows, preliminary keys, table relationships, and initial leakage risks.

No cleaning, target creation, feature engineering, or modeling is performed in this stage.

---

### 02 — Data Cleaning

The second notebook creates clean processed versions of the raw Olist tables.

Main work completed:

- converted date and timestamp columns;
- removed exact duplicate geolocation rows;
- created an aggregated geolocation table by zip code prefix;
- enriched product categories with English translations;
- handled text fields conservatively;
- documented missing values without aggressive imputation;
- kept post-delivery fields for target creation and diagnostic analysis, while marking them as leakage-sensitive.

---

### 03 — SQL & Relational Modeling

The third notebook builds the relational and SQL layer.

Main work completed:

- validated primary and compound keys;
- checked relationships between cleaned tables;
- quantified row multiplication risks;
- defined safe join rules;
- created order-level aggregate tables;
- built SQL scripts for MySQL;
- created a MySQL Workbench EER schema diagram.

Safe join strategy:

- use `orders` as the base table for order-level analysis;
- aggregate order items, payments, and reviews before joining to orders;
- use the aggregated zip-prefix geolocation table for geographic joins.

---

### 04 — Delivery Performance EDA

This notebook analyzes historical delivery performance from a business perspective.

It focuses on:

- overall late delivery rate;
- delay severity;
- customer and seller geography;
- same-state vs cross-state deliveries;
- customer-seller route patterns;
- freight and order value;
- product categories;
- payment profile;
- review score impact;
- monthly and peak-period risk.

---

### 05 — Feature Engineering

This notebook creates the official modeling dataset.

Main principles:

- one row per delivered order;
- official date-only target;
- features available at or shortly after payment approval;
- no post-delivery leakage variables;
- no encoding, scaling, imputation, or model training.

Final modeling dataset:

| Metric | Value |
|---|---:|
| Rows | 96,470 |
| Columns | 35 |
| Late orders | 6,534 |
| Late delivery rate | 6.77% |
| Duplicate order IDs | 0 |

---

### 06 — Machine Learning Modeling

This notebook builds the leakage-safe modeling workflow.

The workflow uses:

- train / validation / test split;
- sklearn pipelines;
- ColumnTransformer preprocessing;
- train-only fitting of imputers, scalers, and encoders;
- consistent model comparison;
- validation-based threshold selection;
- final evaluation on an untouched test set.

Compared models:

- DummyClassifier baseline;
- Logistic Regression;
- Decision Tree;
- Random Forest;
- Extra Trees.

Final selected model:

```text
Random Forest classifier
```

Final selected threshold:

```text
0.16
```

---

### 07 — Business Impact & Model Interpretation

This notebook translates the model into business terms.

It does not retrain the model or change the threshold.

It focuses on:

- risk bands;
- lift vs baseline;
- top-risk order concentration;
- feature importance by business area;
- prediction outcome interpretation;
- operational recommendations;
- dashboard and Streamlit implications;
- limitations and future improvements.

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

## Key Insights

### Late delivery is focused but meaningful

Late deliveries represent a minority of delivered orders, but they are operationally important:

```text
Late delivery rate: 6.77%
```

Late delays are also severe when they happen:

- median late delay: 7 days;
- P95 late delay: 31 days.

---

### Geography matters

Cross-state deliveries are riskier than same-state deliveries:

| Route type | Late delivery rate |
|---|---:|
| Same-state | 4.52% |
| Cross-state | 8.04% |

The route `SP → RJ` is especially important:

| Metric | Value |
|---|---:|
| Orders | 8,131 |
| Late orders | 1,152 |
| Late delivery rate | 14.17% |

---

### Late deliveries damage customer experience

Late delivery is strongly associated with lower review scores:

| Delivery status | Average review score |
|---|---:|
| On-time | 4.29 |
| Late | 2.27 |

Review data is used only as post-delivery diagnostic context. It is not used as a predictive model feature.

---

### Peak periods are operationally risky

Delivery risk varies significantly by month.

| Period | Late delivery rate |
|---|---:|
| Other months | 4.46% |
| Peak months | 15.15% |

---

## Machine Learning Results

The final model should be interpreted as a risk-prioritization tool, not as a complete detector of all late deliveries.

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

| Metric | Value |
|---|---:|
| Baseline late delivery rate | 6.77% |
| Flagged orders late delivery rate | 29.14% |
| Lift vs baseline | 4.3x |
| Flagged order share | 7.95% |

The model does not capture every late delivery. Its value is that the flagged group has a much higher late-delivery rate than the dataset baseline.

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

This is the main practical value of the model: it helps operations focus attention on a smaller group of orders that contains a disproportionate share of actual late deliveries.

---

## Tableau Dashboard

The Tableau dashboard was built as the monitoring and reporting layer of the project.

It contains two dashboards:

### 1. Delivery Operations Overview

Purpose:

> Monitor historical delivery performance and identify operational late-delivery patterns.

Main sections:

- delivered orders;
- late delivery rate;
- late orders;
- median late delay;
- monthly late delivery trend;
- route type late rate;
- top customer states by late orders;
- top customer states by late delivery rate;
- top seller-customer routes;
- review score by delivery status;
- Brazil late delivery rate map.

Main message:

> Late delivery is not random. It varies over time, is higher for cross-state deliveries, concentrates in specific states and routes, and is strongly associated with lower review scores.

### 2. Predictive Risk Monitoring

Purpose:

> Show how the machine learning model supports operations by prioritizing orders with higher-than-average late delivery risk.

Main sections:

- baseline late rate;
- flagged late rate;
- lift vs baseline;
- flagged order share;
- late rate by risk band;
- orders by risk band;
- top-risk concentration;
- feature area importance;
- prediction outcome matrix.

Main message:

> The model does not capture every late delivery, but it identifies groups of orders with substantially higher risk than the baseline.

[View the SupplyGuard Tableau Dashboard](https://public.tableau.com/app/profile/johannes.vidal.blickle/viz/supplyguard_tableau_dashboard/Dashboard1-DeliveryOperationsOverview)

Dashboard screenshots:

```text
reports/figures/tableau_dashboard_1_delivery_operations.png
reports/figures/tableau_dashboard_2_predictive_risk_monitoring.png
```

---

## Streamlit App

The Streamlit app is the operational scoring and action layer of the project.

It does not duplicate Tableau.

| Tool | Role | Business use |
|---|---|---|
| Tableau | Monitoring and reporting layer | Track delivery performance and model risk at aggregate level |
| Streamlit | Operational scoring layer | Score individual or batch orders and recommend action |

The app includes four sections:

1. **Home / Overview**
   - explains SupplyGuard;
   - shows model context;
   - explains risk bands and business use.

2. **Single Order Scoring**
   - manual order input form;
   - predicts late-delivery probability;
   - assigns risk band;
   - flags orders above threshold;
   - returns recommended operational action.

3. **Batch Scoring**
   - upload CSV file;
   - validate required columns;
   - score all orders;
   - assign risk band;
   - flag high-risk orders;
   - download scored CSV.

4. **Model Information / Limitations**
   - explains model design;
   - explains leakage-safe workflow;
   - lists limitations and intended use.

Risk band logic:

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

[Open the SupplyGuard Streamlit App](https://supplyguard-late-delivery-risk-prediction-app.streamlit.app/)

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone <repository-url>
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

### 4. Run the Streamlit app

```bash
streamlit run streamlit_app/app.py
```

The app expects these files to exist:

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

Core notebooks:

```text
notebooks/01_data_understanding.ipynb
notebooks/02_data_cleaning.ipynb
notebooks/03_sql_modeling.ipynb
notebooks/04_eda_delivery_performance.ipynb
notebooks/05_feature_engineering.ipynb
notebooks/06_modeling.ipynb
notebooks/07_business_impact_and_model_interpretation.ipynb
```

SQL layer:

```text
sql/
scripts/load_processed_to_mysql.py
```

Streamlit app:

```text
streamlit_app/app.py
.streamlit/config.toml
```

Model artifact:

```text
outputs/best_model_compressed.pkl
```

The original uncompressed model artifact is not included because it is too large for normal GitHub usage.

---

## Limitations

This project was designed to be realistic, so the model only uses information that would be available before the delivery outcome is known. That makes the prediction task harder, but also more honest.

The main limitation is that the dataset does not include several operational variables that would likely be very important in a real e-commerce environment, such as:

- carrier or logistics provider;
- warehouse capacity;
- inventory availability;
- real-time tracking events;
- route disruptions;
- weather conditions;
- holidays, strikes or regional incidents;
- seller handling performance over time.

Because of this, the model should not be interpreted as a complete late-delivery detection system. Its value is in ranking orders by risk and helping operations teams focus on a smaller group of orders with a much higher late-delivery rate than the overall baseline.

The model is useful for prioritization, but it is not production-ready.

---

## Future Improvements

If this project were continued in a real business context, the next improvements would be:

- add carrier and logistics event data;
- include weather, holidays and regional disruption data;
- test chronological validation to better simulate future prediction;
- create train-safe historical features, such as seller or route delay history;
- calibrate predicted probabilities;
- define cost-based thresholds depending on operational capacity;
- monitor model performance over time;
- connect the Streamlit app to a live order database;
- automate daily batch scoring for new orders.

These additions would make the model more operationally useful and closer to a real deployment scenario.

---

## Project Context

This project was developed as my final portfolio project during the Ironhack Data Analytics bootcamp.

The goal was not only to train a machine learning model, but to build a complete analytical workflow around a realistic business problem. For that reason, the project includes data cleaning, relational modeling, SQL, EDA, machine learning, Tableau dashboards and a Streamlit app.

The main focus was to show how data analysis and machine learning can support operational decision-making in an e-commerce environment.

In practical terms:

- Tableau works as the monitoring and reporting layer.
- Streamlit works as the operational scoring layer.
- The machine learning model works as a risk-prioritization tool.

This separation was intentional. The dashboard explains what is happening at business level, while the app helps score individual or batch orders for action.

---

## Author

Johannes Vidal

Data Analytics / Data Science portfolio project  
Ironhack Data Analytics Bootcamp

[Tableau Dashboard](https://public.tableau.com/app/profile/johannes.vidal.blickle/viz/supplyguard_tableau_dashboard/Dashboard1-DeliveryOperationsOverview)  
[Streamlit App](https://supplyguard-late-delivery-risk-prediction-app.streamlit.app/)