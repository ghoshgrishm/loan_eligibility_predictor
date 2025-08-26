# Loan Eligibility Predictor

An end-to-end machine learning project that predicts whether a loan application is likely to be approved, and exposes the model via a Streamlit web app.

## Project Structure

```
LOAN_ELIGIBILITY_PREDICTOR/
├── app/
│   └── app.py              # Streamlit UI (run this)
├── data/
│   ├── train.csv           # Training data
│   └── test.csv            # Optional test/inference data
├── models/
│   └── model.pkl           # Saved trained pipeline
├── notebooks/
│   └── EDA.ipynb           # EDA, preprocessing, training, evaluation
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## Setup

1) Create and activate a virtual environment (Windows PowerShell):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

## Train and Save the Model

Open `notebooks/EDA.ipynb` and run the training cells. This will:
- Load and preprocess the data with a `ColumnTransformer` (imputation + one-hot encoding)
- Train a classifier
- Evaluate on a validation split and print metrics
- Save a fitted pipeline to `models/model.pkl`

## Run the App

From the repository root:

```bash
streamlit run app/app.py
```

Then open the provided local URL in your browser. Enter applicant details and click "Check Eligibility". The app will display the prediction and confidence.

## Model Notes

- Target: `Loan_Status` (Y = approved, N = not approved)
- Strongest driver historically: `Credit_History`
- Other important drivers: combined income vs. requested `LoanAmount`, `Property_Area`

## Demo Inputs

Try these examples in the app:

Eligible (likely):
- Gender: Male, Married: Yes, Dependents: 0, Education: Graduate, Self_Employed: No, Property_Area: Semiurban, ApplicantIncome: 6000, CoapplicantIncome: 2000, LoanAmount: 120, Loan_Amount_Term: 360, Credit_History: 1.0

Not Eligible (likely):
- Gender: Female, Married: Yes, Dependents: 2, Education: Graduate, Self_Employed: No, Property_Area: Rural, ApplicantIncome: 5000, CoapplicantIncome: 1500, LoanAmount: 120, Loan_Amount_Term: 360, Credit_History: 0.0

## Publish to GitHub

Initialize and push (replace YOUR_REMOTE_URL with your repo URL):

```bash
git init
git add .
git commit -m "Loan eligibility predictor MVP"
git branch -M main
git remote add origin YOUR_REMOTE_URL
git push -u origin main
```


