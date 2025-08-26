import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Enhanced page configuration
st.set_page_config(
    page_title="Loan Eligibility Predictor", 
    page_icon="💸", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for SAMSI-inspired dark theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(26, 26, 26, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        padding: 3rem 2rem;
        margin-top: 2rem;
        backdrop-filter: blur(10px);
    }
    
    /* Header styling - SAMSI inspired */
    h1 {
        color: #ffffff !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 500 !important;
        text-align: center !important;
        font-size: 3rem !important;
        letter-spacing: 3px !important;
        margin-bottom: 0.5rem !important;
        text-transform: uppercase;
    }
    
    .main h1 + .caption {
        color: #cccccc !important;
        text-align: center !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 300 !important;
        letter-spacing: 1px !important;
        margin-bottom: 3rem !important;
        text-transform: uppercase;
    }
    
    /* Subheader styling */
    h2, h3 {
        color: #ffffff !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 500 !important;
        text-align: center !important;
        letter-spacing: 2px !important;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 1rem;
        margin: 2rem 0 !important;
    }
    
    h4 {
        color: #e74c3c !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem !important;
        margin: 1.5rem 0 1rem 0 !important;
    }
    
    /* Form container - dark elegant styling */
    .stForm {
        background: rgba(45, 45, 45, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2.5rem;
        border-radius: 0;
        backdrop-filter: blur(5px);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Input field styling - minimalist dark */
    .stSelectbox > div > div {
        background: rgba(26, 26, 26, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 0 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 300;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #e74c3c !important;
        box-shadow: 0 0 0 1px #e74c3c !important;
    }
    
    .stSelectbox label {
        color: #cccccc !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(26, 26, 26, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 0 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        padding: 0.75rem;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #e74c3c !important;
        box-shadow: 0 0 0 1px #e74c3c !important;
    }
    
    .stNumberInput label {
        color: #cccccc !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button styling - SAMSI red accent */
    .stButton > button {
        background: #e74c3c !important;
        color: white !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 1rem 3rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 2rem !important;
    }
    
    .stButton > button:hover {
        background: #c0392b !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: rgba(46, 125, 50, 0.2) !important;
        border: 1px solid #2e7d32 !important;
        color: #4caf50 !important;
        border-radius: 0 !important;
        padding: 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        text-align: center;
        backdrop-filter: blur(5px);
    }
    
    .stError {
        background: rgba(211, 47, 47, 0.2) !important;
        border: 1px solid #d32f2f !important;
        color: #f44336 !important;
        border-radius: 0 !important;
        padding: 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        text-align: center;
        backdrop-filter: blur(5px);
    }
    
    /* Sidebar styling - dark elegant */
    .css-1d391kg {
        background: rgba(26, 26, 26, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar .sidebar-content {
        background: rgba(45, 45, 45, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(5px);
    }
    
    .sidebar h3 {
        color: #ffffff !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 500 !important;
        text-align: left !important;
        font-size: 1.2rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 0.5rem;
    }
    
    .sidebar h4 {
        color: #e74c3c !important;
        font-family: 'Inter', sans-serif !important;
        text-align: left !important;
    }
    
    .sidebar p, .sidebar li {
        color: #cccccc !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 300 !important;
        line-height: 1.6;
    }
    
    /* Divider styling */
    hr {
        border: none !important;
        height: 1px !important;
        background: rgba(255, 255, 255, 0.2) !important;
        margin: 3rem 0 !important;
    }
    
    /* Column spacing */
    .row-widget.stHorizontal > div {
        padding: 0 0.75rem;
    }
    
    /* Help text styling */
    .stTooltipHoverTarget {
        color: #e74c3c !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(45, 45, 45, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0 !important;
        padding: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .streamlit-expanderContent {
        background: rgba(26, 26, 26, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-top: none !important;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        border-radius: 0 !important;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Confidence display */
    .confidence-display {
        background: rgba(45, 45, 45, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        text-align: center;
        backdrop-filter: blur(5px);
        margin: 2rem 0;
    }
    
    .confidence-title {
        color: #ffffff;
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    
    .confidence-value {
        color: #e74c3c;
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #e74c3c transparent transparent transparent !important;
    }
    
    /* Remove default Streamlit branding colors */
    .css-1v0mbdj.etr89bj1 {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Main title with SAMSI-inspired styling
st.title("FINANCIAL")
st.caption("Loan Eligibility Assessment")

# Enhanced sidebar with dark elegant theme
with st.sidebar:
    st.markdown("### About This Assessment")
    st.markdown("""
    <div style='background: rgba(231, 76, 60, 0.1); padding: 1.5rem; border: 1px solid rgba(231, 76, 60, 0.3); margin: 1rem 0;'>
        <p style='margin: 0; color: #cccccc; font-size: 0.9rem; line-height: 1.6;'>
            Advanced machine learning algorithms evaluate your financial profile to determine loan eligibility with precision and reliability.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Key Assessment Factors")
    st.markdown("""
    • **Credit History** — Primary determinant  
    • **Income Stability** — Monthly earnings evaluation  
    • **Debt-to-Income** — Financial obligation ratio  
    • **Property Location** — Geographic risk assessment  
    """)
    
    st.divider()
    
    st.markdown("### Guidelines")
    st.markdown("""
    <div style='background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.1); margin: 1rem 0;'>
        <p style='margin: 0; color: #cccccc; font-size: 0.85rem; line-height: 1.6;'>
            Provide accurate financial information. All income figures should reflect monthly earnings. Loan amounts are specified in thousands.
        </p>
    </div>
    """, unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_model():
    model_path = Path(__file__).resolve().parent.parent / "models" / "model.pkl"
    if not model_path.exists():
        # Fallback for running from repo root (e.g., `streamlit run app/app.py`)
        model_path = Path.cwd() / "models" / "model.pkl"
    return joblib.load(model_path)

def build_input_form():
    st.markdown("### Application Details")
    with st.form("loan_form"):
        # Personal Information Section
        st.markdown("#### Personal Information")
        c1, c2, c3 = st.columns(3)
        with c1:
            gender = st.selectbox("Gender", options=["Male", "Female"], index=0, help="Applicant gender")
        with c2:
            married = st.selectbox("Marital Status", options=["Yes", "No"], index=0, help="Current marital status")
        with c3:
            dependents = st.selectbox("Dependents", options=["0", "1", "2", "3+"], index=0, help="Number of financial dependents")

        c4, c5, c6 = st.columns(3)
        with c4:
            education = st.selectbox("Education Level", options=["Graduate", "Not Graduate"], index=0)
        with c5:
            self_employed = st.selectbox("Employment Type", options=["No", "Yes"], index=0, help="Self-employment status")
        with c6:
            property_area = st.selectbox("Property Area", options=["Urban", "Semiurban", "Rural"], index=0)

        # Financial Information Section
        st.markdown("#### Financial Profile")
        n1, n2 = st.columns(2)
        with n1:
            applicant_income = st.number_input("Primary Income", min_value=0, value=5000, step=100, help="Monthly income of primary applicant")
            loan_amount = st.number_input("Loan Amount", min_value=0, value=150, step=1, help="Requested amount in thousands")
            credit_history = st.selectbox("Credit History", options=[1.0, 0.0], index=0, format_func=lambda x: "Excellent" if x == 1.0 else "Needs Improvement")
        with n2:
            coapplicant_income = st.number_input("Secondary Income", min_value=0, value=0, step=100, help="Monthly income of co-applicant")
            loan_amount_term = st.number_input("Repayment Term", min_value=0, value=360, step=12, help="Loan duration in months")

        # Enhanced submit button
        submitted = st.form_submit_button("Submit Application")

    # Build a single-row dataframe with expected column names
    data = {
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_amount_term,
        "Credit_History": float(credit_history),
        "Property_Area": property_area,
    }
    return submitted, pd.DataFrame([data])

# Load model with enhanced error handling
model = None
try:
    model = load_model()
except Exception as e:
    st.error("⚠️ Assessment system temporarily unavailable. Please try again later.")
    st.stop()

# Build and handle form submission
submitted, input_df = build_input_form()

if submitted:
    with st.spinner("Processing your application..."):
        try:
            pred = model.predict(input_df)[0]
            proba = None
            if hasattr(model, "predict_proba"):
                # Probability for class 'Y' if present
                classes = getattr(model, "classes_", None)
                if classes is not None and "Y" in list(classes):
                    y_index = list(classes).index("Y")
                    proba = model.predict_proba(input_df)[0][y_index]
                else:
                    # Fall back to max probability
                    proba = float(max(model.predict_proba(input_df)[0]))

            eligible = (pred == "Y") or (pred == 1) or (str(pred).upper() == "Y")

            # Enhanced result display
            st.markdown("---")
            st.markdown("### Assessment Results")
            
            if eligible:
                st.success("✓ APPLICATION APPROVED — You are eligible for loan processing.")
            else:
                st.error("✗ APPLICATION DECLINED — Current profile does not meet eligibility criteria.")

            if proba is not None:
                # Enhanced confidence display with SAMSI styling
                st.markdown(f"""
                <div class='confidence-display'>
                    <div class='confidence-title'>Confidence Level</div>
                    <div class='confidence-value'>{proba * 100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

            # Enhanced input display
            with st.expander("View Application Summary"):
                st.dataframe(input_df, use_container_width=True)

        except Exception as e:
            st.exception(e)