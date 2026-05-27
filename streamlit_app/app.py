from pathlib import Path
import base64
import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SupplyGuard Risk Scoring", page_icon=None, layout="wide")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "outputs" / "best_model_compressed.pkl"
MODELING_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "modeling_dataset.csv"
FEATURE_DICTIONARY_PATH = PROJECT_ROOT / "data" / "processed" / "feature_dictionary.csv"
RISK_SEGMENTS_PATH = PROJECT_ROOT / "outputs" / "test_predictions_with_risk_segments.csv"
LOGO_PATH = PROJECT_ROOT / "streamlit_app" / "assets" / "SupplyGuard_Logo_Cropped.png"

MODEL_THRESHOLD = 0.16
BASELINE_LATE_RATE = 0.0677
FLAGGED_LATE_RATE = 0.2914
LIFT_VS_BASELINE = 4.3

def assign_risk_band(score):
    if score < 0.08:
        return "Low Risk"
    elif score < 0.16:
        return "Medium Risk"
    elif score < 0.25:
        return "High Risk"
    return "Very High Risk"

def recommend_action(risk_band):
    actions = {
        "Low Risk": "Standard handling.",
        "Medium Risk": "Monitor normally.",
        "High Risk": "Prioritize logistics follow-up.",
        "Very High Risk": "Escalate and consider proactive customer communication."
    }
    return actions[risk_band]

def style_risk_output(df):
    def risk_band_style(value):
        colors = {
            "Low Risk": "background-color: #E8F0E6; color: #1F3D35;",
            "Medium Risk": "background-color: #DDE8D2; color: #2F5D50;",
            "High Risk": "background-color: #F3E2C3; color: #7A4A12;",
            "Very High Risk": "background-color: #E9C7BA; color: #7A2E1D;"
        }
        return colors.get(value, "")

    def flagged_style(value):
        if value is True:
            return "background-color: #E9C7BA; color: #7A2E1D;"
        if value is False:
            return "background-color: #E8F0E6; color: #1F3D35;"
        return ""

    styled = df.style
    if "risk_band" in df.columns:
        styled = styled.map(risk_band_style, subset=["risk_band"])
    if "flagged_order" in df.columns:
        styled = styled.map(flagged_style, subset=["flagged_order"])
    return styled


def image_to_base64(path):
    if not path.exists():
        return None
    return base64.b64encode(path.read_bytes()).decode()

def apply_custom_style():
    st.markdown(
        """
        <style>
        html, body, [class*="css"], .stApp {
            font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background-color: #F7F8F5;
        }

        h1, h2, h3 {
            color: #1D2D44;
            letter-spacing: -0.02em;
        }

        p, li, div {
            color: #2F2F2F;
        }

        section[data-testid="stSidebar"] {
            background-color: #1D2D44;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div {
            color: #F7F8F5;
        }

        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #D8C3A5;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 2px 10px rgba(29, 45, 68, 0.08);
        }

        div[data-testid="stMetric"] label {
            color: #3E5C76;
        }

        div[data-testid="stMetricValue"] {
            color: #1D2D44;
        }

        .supplyguard-hero {
            background: linear-gradient(135deg, #1D2D44 0%, #3E5C76 100%);
            border-radius: 22px;
            padding: 28px 32px;
            margin-bottom: 28px;
            box-shadow: 0 6px 22px rgba(29, 45, 68, 0.18);
            display: flex;
            align-items: center;
            gap: 34px;
        }

        .supplyguard-hero img {
            background-color: #F7F8F5;
            border-radius: 18px;
            padding: 12px;
            object-fit: contain;
        }

        .supplyguard-hero-title {
            color: #F7F8F5;
            font-size: 2.15rem;
            font-weight: 700;
            line-height: 1.15;
            margin: 0 0 8px 0;
        }

        .supplyguard-hero-subtitle {
            color: #D8C3A5;
            font-size: 1.05rem;
            margin: 0;
        }

        .supplyguard-section-card {
            background-color: #FFFFFF;
            border: 1px solid #E5D8C4;
            border-radius: 16px;
            padding: 18px 20px;
            margin: 12px 0 18px 0;
            box-shadow: 0 2px 10px rgba(29, 45, 68, 0.05);
        }

        .stButton button, .stDownloadButton button {
            background-color: #1D2D44;
            color: #F7F8F5;
            border-radius: 10px;
            border: 1px solid #1D2D44;
            font-weight: 600;
        }

        .stButton button:hover, .stDownloadButton button:hover {
            background-color: #3E5C76;
            color: #F7F8F5;
            border: 1px solid #3E5C76;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_page_header(title, subtitle="", compact=False):
    logo_b64 = image_to_base64(LOGO_PATH)
    logo_width = 320 if not compact else 150

    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" width="{logo_width}">'
    else:
        logo_html = '<div style="background:#F7F8F5;color:#1D2D44;border-radius:16px;padding:20px;font-weight:700;">SG</div>'

    st.markdown(
        f"""
        <div class="supplyguard-hero">
            <div>{logo_html}</div>
            <div>
                <div class="supplyguard-hero-title">{title}</div>
                <p class="supplyguard-hero-subtitle">{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_reference_data():
    modeling_df = pd.read_csv(MODELING_DATA_PATH)
    feature_dictionary = pd.read_csv(FEATURE_DICTIONARY_PATH)
    risk_segments = pd.read_csv(RISK_SEGMENTS_PATH)
    return modeling_df, feature_dictionary, risk_segments

model = load_model()
modeling_df, feature_dictionary, risk_segments = load_reference_data()
model_features = list(model.feature_names_in_)

if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), width=165)

st.sidebar.title("SupplyGuard")
page = st.sidebar.radio(
    "Navigation",
    ["Home / Overview", "Single Order Scoring", "Batch Scoring", "Model Information / Limitations"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Operational late-delivery risk scoring tool.")

if page == "Home / Overview":
    render_page_header(
        "SupplyGuard — Late Delivery Risk Scoring",
        "Operational late-delivery risk scoring for e-commerce orders."
    )

    st.write(
        "This is an operational scoring tool designed to help SupplyGuard's e-commerce teams identify orders with elevated late-delivery risk before the delay happens."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Baseline late rate", f"{BASELINE_LATE_RATE:.2%}")
    col2.metric("Model threshold", f"{MODEL_THRESHOLD:.2f}")
    col3.metric("Flagged late rate", f"{FLAGGED_LATE_RATE:.2%}")
    col4.metric("Lift vs baseline", f"{LIFT_VS_BASELINE:.1f}x")

    st.subheader("Risk band catalog")
    risk_band_catalog = pd.DataFrame([
        {"risk_band": "Low Risk", "score_range": "0.00% to 7.50%", "flagged": "No", "recommended_action": "Standard handling."},
        {"risk_band": "Medium Risk", "score_range": "8.00% to 15.50%", "flagged": "No", "recommended_action": "Monitor normally."},
        {"risk_band": "High Risk", "score_range": "16.00% to 24.50%", "flagged": "Yes", "recommended_action": "Prioritize logistics follow-up."},
        {"risk_band": "Very High Risk", "score_range": "25.00%+", "flagged": "Yes", "recommended_action": "Escalate and consider proactive customer communication."}
    ])
    st.dataframe(risk_band_catalog, width='stretch', hide_index=True)
    st.caption("Orders are flagged when predicted late-delivery probability is greater than or equal to 16.00%.")

    st.subheader("Purpose")
    st.write(
        "The app converts the final machine learning model into a practical order-level decision support tool. "
        "It helps operations teams prioritize follow-up, escalation and proactive customer communication for orders that deserve attention."
    )

    st.subheader("How to use this app")
    st.markdown(
        """
        - Use **Single Order Scoring** to manually score one order.
        - Use **Batch Scoring** to upload and score multiple orders from a CSV file.
        - Use **Model Information / Limitations** to understand what the model uses, what it excludes and where it should not be overtrusted.
        """
    )

    st.subheader("Positioning")
    st.write(
        "Tableau acts as the historical monitoring and executive reporting layer. "
        "This Streamlit app acts as the operational scoring and action layer for individual orders."
    )

    st.info(
        "The model is designed for risk prioritization, not full automation. "
        "A flagged order should be reviewed by an operations team before action is taken."
    )

elif page == "Single Order Scoring":
    render_page_header("Single Order Scoring", "Score one order and receive a risk band, flag and recommended action.", compact=True)
    st.write(
        "Enter the characteristics of a new order to estimate its late-delivery risk. "
        "The app translates user-friendly inputs into the exact feature format expected by the model."
    )

    reference_df = modeling_df[model_features].copy()
    feature_descriptions = feature_dictionary.set_index("column")["description"].to_dict()
    input_values = {}

    feature_labels = {
        "purchase_month": "Purchase month",
        "purchase_day_of_week": "Purchase day of week",
        "purchase_hour": "Purchase hour",
        "is_weekend_purchase": "Weekend purchase",
        "estimated_delivery_days": "Estimated delivery days",
        "approval_delay_hours": "Payment approval delay hours",
        "customer_state": "Customer state",
        "main_seller_state": "Main seller state",
        "same_state_order": "Customer and seller in same state",
        "customer_seller_state_pair": "Customer-seller state pair",
        "customer_seller_distance_km": "Customer-seller distance km",
        "order_item_count": "Order item count",
        "product_count": "Unique product count",
        "seller_count": "Seller count",
        "total_item_price": "Total item price",
        "total_freight_value": "Total freight value",
        "avg_item_price": "Average item price",
        "max_item_price": "Maximum item price",
        "total_order_item_value": "Total order item value",
        "freight_ratio": "Freight ratio",
        "product_category_count": "Product category count",
        "dominant_product_category": "Dominant product category",
        "total_product_weight_g": "Total product weight g",
        "max_product_weight_g": "Maximum product weight g",
        "total_product_volume_cm3": "Total product volume cm3",
        "max_product_volume_cm3": "Maximum product volume cm3",
        "payment_count": "Payment count",
        "payment_method_count": "Payment method count",
        "total_payment_value": "Total payment value",
        "avg_payment_value": "Average payment value",
        "max_payment_installments": "Maximum payment installments",
        "main_payment_type": "Main payment type"
    }

    month_options = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    day_options = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    yes_no_options = {"No": 0, "Yes": 1}

    timing_features = ["purchase_month", "purchase_day_of_week", "purchase_hour", "is_weekend_purchase", "estimated_delivery_days", "approval_delay_hours"]
    order_product_features = [
        "order_item_count", "product_count", "seller_count", "total_item_price", "total_freight_value", "avg_item_price",
        "max_item_price", "total_order_item_value", "freight_ratio", "product_category_count", "dominant_product_category",
        "total_product_weight_g", "max_product_weight_g", "total_product_volume_cm3", "max_product_volume_cm3"
    ]
    payment_features = ["payment_count", "payment_method_count", "total_payment_value", "avg_payment_value", "max_payment_installments", "main_payment_type"]

    integer_features = {
        "purchase_month", "purchase_day_of_week", "purchase_hour", "is_weekend_purchase", "estimated_delivery_days",
        "order_item_count", "product_count", "seller_count", "product_category_count", "payment_count",
        "payment_method_count", "max_payment_installments"
    }

    def numeric_input_from_reference(col, min_floor=0):
        label = feature_labels.get(col, col.replace("_", " ").title())
        help_text = feature_descriptions.get(col, "")
        series = pd.to_numeric(reference_df[col], errors="coerce").dropna()

        if series.empty:
            st.selectbox(label, ["Missing / not available"], help=f"{help_text} The model pipeline will handle this as missing.")
            input_values[col] = np.nan
            return

        train_min, train_max, default_value = float(series.min()), float(series.max()), float(series.median())
        min_value = int(max(min_floor, train_min)) if col in integer_features else float(round(max(min_floor, train_min), 2))

        if col in integer_features:
            value = st.number_input(label, min_value=min_value, value=int(round(default_value)), step=1, help=help_text)
        else:
            step = 0.01 if "ratio" in col else 1.00
            value = st.number_input(label, min_value=min_value, value=float(round(default_value, 2)), step=step, format="%.2f", help=help_text)

        input_values[col] = value

        if value < train_min or value > train_max:
            st.caption(f"Outside training range: historical range was {train_min:.2f} to {train_max:.2f}. Prediction may be less reliable.")

    def categorical_input_from_reference(col):
        label = feature_labels.get(col, col.replace("_", " ").title())
        help_text = feature_descriptions.get(col, "")
        options = sorted(reference_df[col].dropna().astype(str).unique())

        if not options:
            st.selectbox(label, ["Missing / not available"], help=help_text)
            input_values[col] = np.nan
            return

        default = str(reference_df[col].mode(dropna=True).iloc[0])
        input_values[col] = st.selectbox(label, options, index=options.index(default) if default in options else 0, help=help_text)

    def render_feature(col):
        label = feature_labels.get(col, col.replace("_", " ").title())
        help_text = feature_descriptions.get(col, "")

        if col == "purchase_month":
            default_value = int(reference_df[col].dropna().mode().iloc[0])
            default_label = next(k for k, v in month_options.items() if v == default_value)
            selected = st.selectbox(label, list(month_options.keys()), index=list(month_options.keys()).index(default_label), help=help_text)
            input_values[col] = month_options[selected]
            return

        if col == "purchase_day_of_week":
            default_value = int(reference_df[col].dropna().mode().iloc[0])
            default_label = next(k for k, v in day_options.items() if v == default_value)
            selected = st.selectbox(label, list(day_options.keys()), index=list(day_options.keys()).index(default_label), help=help_text)
            input_values[col] = day_options[selected]
            return

        if col == "purchase_hour":
            options = list(range(24))
            default_value = int(reference_df[col].dropna().mode().iloc[0])
            input_values[col] = st.selectbox(label, options, index=options.index(default_value), help=help_text)
            return

        if col == "is_weekend_purchase":
            default_value = int(reference_df[col].dropna().mode().iloc[0])
            default_label = "Yes" if default_value == 1 else "No"
            selected = st.selectbox(label, list(yes_no_options.keys()), index=list(yes_no_options.keys()).index(default_label), help=help_text)
            input_values[col] = yes_no_options[selected]
            return

        if pd.api.types.is_string_dtype(reference_df[col]):
            categorical_input_from_reference(col)
            return

        numeric_input_from_reference(col)

    with st.form("single_order_form"):
        st.subheader("Order inputs")

        with st.expander("Timing features", expanded=True):
            col1, col2 = st.columns(2)
            for i, feature in enumerate(timing_features):
                with col1 if i % 2 == 0 else col2:
                    render_feature(feature)

        with st.expander("Geography features", expanded=True):
            customer_states = sorted(reference_df["customer_state"].dropna().astype(str).unique())
            seller_states = sorted(reference_df["main_seller_state"].dropna().astype(str).unique())
            known_state_pairs = set(reference_df["customer_seller_state_pair"].dropna().astype(str).unique())

            default_customer_state = str(reference_df["customer_state"].mode(dropna=True).iloc[0])
            default_seller_state = str(reference_df["main_seller_state"].mode(dropna=True).iloc[0])

            col1, col2 = st.columns(2)
            with col1:
                customer_state = st.selectbox(
                    "Customer state", customer_states,
                    index=customer_states.index(default_customer_state) if default_customer_state in customer_states else 0,
                    help=feature_descriptions.get("customer_state", "")
                )
            with col2:
                main_seller_state = st.selectbox(
                    "Main seller state", seller_states,
                    index=seller_states.index(default_seller_state) if default_seller_state in seller_states else 0,
                    help=feature_descriptions.get("main_seller_state", "")
                )

            state_pair = f"{customer_state}_{main_seller_state}"
            same_state = int(customer_state == main_seller_state)

            input_values["customer_state"] = customer_state
            input_values["main_seller_state"] = main_seller_state
            input_values["same_state_order"] = same_state
            input_values["customer_seller_state_pair"] = state_pair

            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Derived same-state order", value="Yes" if same_state else "No", disabled=True)
            with col2:
                st.text_input("Derived state pair", value=state_pair, disabled=True)

            if state_pair not in known_state_pairs:
                st.caption("This state pair was not present in the training data. The model can still score it, but the prediction may be less reliable.")

            numeric_input_from_reference("customer_seller_distance_km")

        with st.expander("Order and product features", expanded=False):
            col1, col2 = st.columns(2)
            for i, feature in enumerate(order_product_features):
                with col1 if i % 2 == 0 else col2:
                    render_feature(feature)

        with st.expander("Payment features", expanded=False):
            col1, col2 = st.columns(2)
            for i, feature in enumerate(payment_features):
                with col1 if i % 2 == 0 else col2:
                    render_feature(feature)

        submitted = st.form_submit_button("Score order", type="primary")

    if submitted:
        input_df = pd.DataFrame([input_values])[model_features]
        late_risk_score = float(model.predict_proba(input_df)[:, 1][0])
        risk_band = assign_risk_band(late_risk_score)
        flagged_order = late_risk_score >= MODEL_THRESHOLD
        recommended_action = recommend_action(risk_band)

        st.subheader("Scoring result")

        col1, col2, col3 = st.columns(3)
        col1.metric("Late-delivery risk score", f"{late_risk_score:.2%}")
        col2.metric("Risk band", risk_band)
        col3.metric("Flagged order", "Yes" if flagged_order else "No")

        if flagged_order:
            st.warning("This order is above the operational risk threshold and should be reviewed.")
        else:
            st.success("This order is below the operational risk threshold.")

        result = pd.DataFrame([{
            "predicted_late_probability": round(late_risk_score, 4),
            "risk_band": risk_band,
            "flagged_order": flagged_order,
            "recommended_action": recommended_action
        }])

        st.dataframe(style_risk_output(result), width='stretch')

        with st.expander("View model input row", expanded=False):
            st.dataframe(input_df, width='stretch')

elif page == "Batch Scoring":
    render_page_header("Batch Scoring", "Upload a CSV file and score multiple orders at once.", compact=True)
    st.write(
        "Upload a CSV file with multiple orders. The app validates the required fields, applies light formatting cleanup, "
        "scores each order with the saved model Pipeline and returns an operational risk output."
    )

    reference_df = modeling_df[model_features].copy()
    categorical_features = [col for col in model_features if pd.api.types.is_string_dtype(reference_df[col])]
    numeric_features = [col for col in model_features if col not in categorical_features]

    def parse_number(value):
        if pd.isna(value):
            return np.nan

        if isinstance(value, (int, float, np.integer, np.floating)):
            return float(value)

        value = str(value).strip()
        if value == "" or value.lower() in {"nan", "none", "null", "missing", "not available"}:
            return np.nan

        value = value.replace("R$", "").replace("€", "").replace("$", "").replace(" ", "")

        if "," in value and "." in value:
            if value.rfind(",") > value.rfind("."):
                value = value.replace(".", "").replace(",", ".")
            else:
                value = value.replace(",", "")
        elif "," in value:
            parts = value.split(",")
            if len(parts) == 2 and len(parts[1]) <= 2:
                value = value.replace(",", ".")
            elif len(parts) == 2 and len(parts[1]) == 3:
                value = value.replace(",", "")
            else:
                value = value.replace(",", ".")

        try:
            return float(value)
        except ValueError:
            return np.nan

    def prepare_batch_input(df):
        df = df.copy()
        df.columns = df.columns.str.strip()

        for col in ["customer_state", "main_seller_state", "main_payment_type", "dominant_product_category"]:
            if col in df.columns:
                df[col] = df[col].astype(object)
                df[col] = df[col].where(df[col].notna(), np.nan)
                df[col] = df[col].apply(lambda x: str(x).strip() if pd.notna(x) else np.nan)

        if "same_state_order" not in df.columns and {"customer_state", "main_seller_state"}.issubset(df.columns):
            df["same_state_order"] = (df["customer_state"].astype(str) == df["main_seller_state"].astype(str)).astype(int)

        if "customer_seller_state_pair" not in df.columns and {"customer_state", "main_seller_state"}.issubset(df.columns):
            df["customer_seller_state_pair"] = df["customer_state"].astype(str).str.strip() + "_" + df["main_seller_state"].astype(str).str.strip()

        if "is_weekend_purchase" not in df.columns and "purchase_day_of_week" in df.columns:
            day_values = df["purchase_day_of_week"].apply(parse_number)
            df["is_weekend_purchase"] = day_values.isin([5, 6]).astype(int)

        if "total_order_item_value" not in df.columns and {"total_item_price", "total_freight_value"}.issubset(df.columns):
            df["total_order_item_value"] = df["total_item_price"].apply(parse_number) + df["total_freight_value"].apply(parse_number)

        if "freight_ratio" not in df.columns and {"total_freight_value", "total_order_item_value"}.issubset(df.columns):
            freight = df["total_freight_value"].apply(parse_number)
            total = df["total_order_item_value"].apply(parse_number)
            df["freight_ratio"] = np.where(total > 0, freight / total, np.nan)

        if "avg_payment_value" not in df.columns and {"total_payment_value", "payment_count"}.issubset(df.columns):
            total_payment = df["total_payment_value"].apply(parse_number)
            payment_count = df["payment_count"].apply(parse_number)
            df["avg_payment_value"] = np.where(payment_count > 0, total_payment / payment_count, np.nan)

        missing_columns = [col for col in model_features if col not in df.columns]
        if missing_columns:
            return None, missing_columns

        batch_input = df[model_features].copy()

        for col in numeric_features:
            batch_input[col] = batch_input[col].apply(parse_number)

        for col in categorical_features:
            batch_input[col] = batch_input[col].astype(object)
            batch_input[col] = batch_input[col].where(batch_input[col].notna(), np.nan)
            batch_input[col] = batch_input[col].apply(lambda x: str(x).strip() if pd.notna(x) else np.nan)

        return batch_input, []

    st.subheader("Expected CSV structure")
    st.write(
        "The CSV can include all model features directly. Some operational fields can also be derived automatically "
        "when the necessary source columns are present."
    )

    with st.expander("Required model columns", expanded=False):
        st.dataframe(pd.DataFrame({"required_column": model_features}), width='stretch')

    with st.expander("Columns that can be derived automatically", expanded=False):
        derived_columns = pd.DataFrame([
            {"derived_column": "same_state_order", "needed_columns": "customer_state, main_seller_state"},
            {"derived_column": "customer_seller_state_pair", "needed_columns": "customer_state, main_seller_state"},
            {"derived_column": "is_weekend_purchase", "needed_columns": "purchase_day_of_week"},
            {"derived_column": "total_order_item_value", "needed_columns": "total_item_price, total_freight_value"},
            {"derived_column": "freight_ratio", "needed_columns": "total_freight_value, total_order_item_value"},
            {"derived_column": "avg_payment_value", "needed_columns": "total_payment_value, payment_count"}
        ])
        st.dataframe(derived_columns, width='stretch')

    st.caption(
        "Recommended numeric format for CSV uploads: use dot as decimal separator and no thousands separator, e.g. 1500.75. "
        "The app attempts to clean common comma/dot formats, but ambiguous values such as 1,500 can be interpreted differently depending on locale."
    )

    risk_segments_for_template = risk_segments.copy()

    if "risk_band" not in risk_segments_for_template.columns and "late_risk_score" in risk_segments_for_template.columns:
        risk_segments_for_template["risk_band"] = risk_segments_for_template["late_risk_score"].apply(assign_risk_band)

    template_parts = []
    for band in ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"]:
        band_orders = risk_segments_for_template.loc[
            risk_segments_for_template["risk_band"] == band,
            ["order_id", "risk_band", "late_risk_score"]
        ]

        if not band_orders.empty:
            template_parts.append(band_orders.sample(min(len(band_orders), 3), random_state=42))

    if template_parts:
        template_orders = pd.concat(template_parts, ignore_index=True)

        sample_template = (
            modeling_df.merge(template_orders, on="order_id", how="inner")
            .sample(frac=1, random_state=17)
            .reset_index(drop=True)
        )

        sample_template = sample_template[["order_id"] + model_features]
    else:
        sample_template = reference_df.sample(10, random_state=42).reset_index(drop=True)
        sample_template.insert(0, "order_id", [f"sample_order_{i+1}" for i in range(len(sample_template))])

    st.download_button(
        "Download sample input template",
        data=sample_template.to_csv(index=False).encode("utf-8"),
        file_name="supplyguard_batch_scoring_template.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader("Upload batch scoring CSV", type=["csv"])

    if uploaded_file is not None:
        raw_batch = pd.read_csv(uploaded_file)
        st.subheader("Uploaded data preview")
        st.dataframe(raw_batch.head(20), width='stretch')

        batch_input, missing_columns = prepare_batch_input(raw_batch)

        if missing_columns:
            st.error("The uploaded file is missing required columns that could not be derived.")
            st.dataframe(pd.DataFrame({"missing_column": missing_columns}), width='stretch')
        else:
            invalid_numeric = []
            for col in numeric_features:
                missing_after_parse = batch_input[col].isna().sum()
                if missing_after_parse > 0:
                    invalid_numeric.append({"column": col, "missing_or_unparsed_values": int(missing_after_parse)})

            if invalid_numeric:
                st.warning(
                    "Some numeric values are missing or could not be parsed. The model Pipeline may handle missing values if the preprocessing step includes imputation."
                )
                st.dataframe(pd.DataFrame(invalid_numeric), width='stretch')

            scores = model.predict_proba(batch_input)[:, 1]
            scored_batch = raw_batch.copy()

            if "order_id" not in scored_batch.columns:
                scored_batch.insert(0, "order_id", [f"uploaded_order_{i+1}" for i in range(len(scored_batch))])

            scored_batch["predicted_late_probability"] = scores.round(4)
            scored_batch["risk_band"] = scored_batch["predicted_late_probability"].apply(assign_risk_band)
            scored_batch["flagged_order"] = scored_batch["predicted_late_probability"] >= MODEL_THRESHOLD
            scored_batch["recommended_action"] = scored_batch["risk_band"].apply(recommend_action)

            output_columns = ["order_id", "predicted_late_probability", "risk_band", "flagged_order", "recommended_action"]
            output = scored_batch[output_columns].copy()

            st.subheader("Batch scoring summary")

            col1, col2, col3 = st.columns(3)
            col1.metric("Orders scored", f"{len(output):,}")
            col2.metric("Flagged orders", f"{int(output['flagged_order'].sum()):,}")
            col3.metric("Flagged share", f"{output['flagged_order'].mean():.2%}")

            st.subheader("Scored orders")
            st.dataframe(style_risk_output(output), width='stretch')

            st.download_button(
                "Download scored CSV",
                data=output.to_csv(index=False).encode("utf-8"),
                file_name="supplyguard_scored_orders.csv",
                mime="text/csv"
            )

elif page == "Model Information / Limitations":
    render_page_header("Model Information and Limitations", "Understand model inputs, risk bands, leakage controls and practical limitations.", compact=True)

    st.subheader("Model artifact")
    st.write(
        "The app loads the saved sklearn Pipeline from `outputs/best_model.pkl`. "
        "This Pipeline includes both preprocessing and the final Random Forest classifier, so the app does not retrain the model."
    )

    st.subheader("Prediction target")
    st.write(
        "The model estimates the probability that an order will be delivered late based on the official date-only late delivery definition used in the project."
    )

    st.subheader("Input areas")
    st.markdown(
        """
        The model uses leakage-safe order-level features from four main areas:

        - **Timing:** purchase month, day of week, purchase hour, weekend flag, estimated delivery window and approval delay.
        - **Geography:** customer state, seller state, same-state flag, customer-seller state pair and approximate distance.
        - **Order and product profile:** item counts, sellers, product categories, freight, order value, product weight and product volume.
        - **Payment profile:** payment count, payment method count, payment value, installments and main payment type.
        """
    )

    st.subheader("Leakage-safe design")
    st.write(
        "The app does not use actual delivery date, delivery delay, review score, review comments, final delivery outcome variables or order status as model inputs. "
        "Those variables are excluded because they would only be known after the delivery process or after the customer experience has already happened."
    )

    st.subheader("Operational interpretation")
    st.write(
        "The final threshold is 0.16. Orders with predicted late-delivery probability greater than or equal to this threshold are flagged for operational review."
    )

    threshold_table = pd.DataFrame([
        {"risk_band": "Low Risk", "score_range": "0.00 to 0.075", "recommended_action": "Standard handling."},
        {"risk_band": "Medium Risk", "score_range": "0.08 to 0.155", "recommended_action": "Monitor normally."},
        {"risk_band": "High Risk", "score_range": "0.16 to 0.245", "recommended_action": "Prioritize logistics follow-up."},
        {"risk_band": "Very High Risk", "score_range": "0.25+", "recommended_action": "Escalate and consider proactive customer communication."}
    ])
    st.dataframe(threshold_table, width='stretch')

    st.subheader("Known limitations")
    st.markdown(
        """
        This model should not be treated as production-ready. Important real-world signals are missing, including:

        - carrier-level performance;
        - warehouse capacity;
        - inventory availability;
        - real-time tracking events;
        - weather disruptions;
        - holidays, strikes or regional logistics incidents;
        - live seller operational constraints.

        Because of these limitations, the model is best used as a prioritization layer rather than an automated decision system.
        """
    )

    st.subheader("Feature dictionary")
    st.dataframe(feature_dictionary, width='stretch')
