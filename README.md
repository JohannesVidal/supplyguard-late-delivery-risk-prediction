# SupplyGuard — Delivery Delay Risk Prediction for E-Commerce Operations

## Project Overview

SupplyGuard is an end-to-end Data Analytics and Data Science project that simulates a real consulting engagement for an e-commerce marketplace.

The objective is to help operations teams anticipate late delivery risk before it happens, identify operational inefficiencies, and support decision-making through analytics, machine learning, dashboarding, and a possible Streamlit application.

## Business Problem

E-commerce companies depend heavily on reliable delivery performance. Late deliveries can damage customer satisfaction, reduce trust, and create operational pressure.

This project aims to answer:

How can an e-commerce company predict delivery delay risk before it happens and use that information to improve logistics operations and customer satisfaction?

## Dataset

The project uses the Olist Brazilian E-Commerce Public Dataset.

The dataset contains relational marketplace data, including:

- Orders
- Customers
- Sellers
- Products
- Order items
- Payments
- Reviews
- Geolocation
- Product category translations

## Main Target

The main predictive target is:

is_late = order_delivered_customer_date > order_estimated_delivery_date

## Critical Modeling Rule

To avoid data leakage, the model must not use information that would only be known after delivery, such as:

- Actual delivery date
- Final delay days
- Review score
- Final delivery status
- Any post-delivery information

## Project Components

- Data understanding
- Data cleaning
- SQL / relational analysis
- Exploratory Data Analysis
- Feature engineering
- Machine Learning classification
- Model evaluation and interpretation
- Dashboard
- Optional Streamlit app
- Business recommendations

## Repository Structure

supplyguard-delivery-risk/
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── database/
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_sql_analysis.ipynb
│   ├── 04_eda_business_insights.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_modeling.ipynb
│   └── 07_model_interpretation.ipynb
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_quality_checks.sql
│   └── 03_business_queries.sql
│
├── src/
│   ├── cleaning.py
│   ├── features.py
│   ├── database.py
│   ├── preprocessing.py
│   ├── train.py
│   ├── evaluate.py
│   └── utils.py
│
├── dashboard/
├── streamlit_app/
├── models/
├── visuals/
├── presentation/
├── README.md
├── requirements.txt
└── .gitignore

## Author

Johannes Vidal

