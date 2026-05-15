# Home-Credit-Default-Risk

## Project Overview

This project focuses on building a machine learning model to predict whether a loan applicant is likely to default on a loan. The goal is to support more accurate credit risk assessment by using customer application data, credit history, and financial behavior indicators.

The project is based on the Home Credit Default Risk dataset, which contains information about loan applicants, including demographic characteristics, income, employment status, previous loan records, credit bureau history, and payment behavior.

By applying data cleaning, feature engineering, exploratory data analysis, and machine learning models, this project aims to identify key factors associated with loan default risk and improve prediction performance.

---

## Business Problem

Home Credit provides loans to customers who may have limited or no traditional credit history. For financial institutions, accurately predicting default risk is important because it helps:

- Reduce financial loss from high-risk loans
- Improve loan approval decisions
- Support fairer and more data-driven credit evaluation
- Identify important risk factors among applicants

The main prediction task is:

> Given an applicant's financial and personal information, predict whether the applicant will have difficulty repaying the loan.

---

## Dataset

The dataset includes multiple tables related to loan applications and customer credit history.

Main data sources include:

- `application_train.csv`: Main training dataset with applicant information and target label
- `application_test.csv`: Test dataset for prediction
- `bureau.csv`: Applicant's previous credit records reported to the credit bureau
- `bureau_balance.csv`: Monthly balance information for previous bureau credits
- `previous_application.csv`: Previous loan applications with Home Credit
- `installments_payments.csv`: Payment history for previous loans
- `credit_card_balance.csv`: Credit card balance records
- `POS_CASH_balance.csv`: Point-of-sale and cash loan balance records

The target variable is:

- `TARGET = 1`: Applicant had payment difficulties
- `TARGET = 0`: Applicant did not have payment difficulties

---

## Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- XGBoost / LightGBM
- Jupyter Notebook

---

## Project Workflow

### 1. Data Understanding

First, I reviewed the structure of the dataset, including the number of rows, columns, missing values, data types, and target distribution.

Key checks included:

- Dataset shape
- Column data types
- Missing value percentage
- Target class imbalance
- Duplicate records
- Numeric and categorical feature distributions

---

### 2. Exploratory Data Analysis

Exploratory data analysis was performed to understand applicant characteristics and default patterns.

Main analysis areas included:

- Distribution of default vs. non-default applicants
- Income and credit amount patterns
- Age and employment length distribution
- Education and family status analysis
- Correlation between numeric features and default risk
- Missing value patterns
- Outlier detection

Important business questions explored:

- Do applicants with lower income have higher default risk?
- Does employment length affect repayment behavior?
- Are certain education or family status groups associated with higher risk?
- How does credit amount compare with income?
- Which financial indicators are most related to default?

---

### 3. Data Cleaning

Data cleaning steps included:

- Handling missing values
- Removing or capping extreme outliers
- Converting abnormal values into missing values
- Encoding categorical variables
- Checking duplicated records
- Standardizing feature formats

Examples:

- Replaced abnormal employment values with missing values
- Filled missing categorical values with `"Unknown"`
- Filled missing numerical values using median values
- Applied one-hot encoding for categorical variables

---

### 4. Feature Engineering

Feature engineering was used to create more meaningful risk indicators.

Examples of engineered features:

- `CREDIT_INCOME_RATIO`: Credit amount divided by applicant income
- `ANNUITY_INCOME_RATIO`: Loan annuity divided by applicant income
- `EMPLOYED_AGE_RATIO`: Employment length compared with applicant age
- `DAYS_EMPLOYED_PERCENT`: Employment duration relative to age
- Aggregated credit bureau features
- Aggregated previous application statistics
- Payment delay indicators
- Number of previous loans
- Average credit amount from previous applications

These features help capture financial pressure, repayment ability, and historical credit behavior.

---

## Modeling Approach

Several machine learning models were trained and compared.

Models used:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- LightGBM

Because the dataset is imbalanced, model evaluation focused on metrics beyond accuracy.

Evaluation metrics included:

- ROC-AUC
- Precision
- Recall
- F1-score
- Confusion matrix

ROC-AUC was used as the main metric because the goal is to rank applicants by default risk.

---

## Model Evaluation

The models were evaluated on a validation set using a train-validation split.

General findings:

- Logistic Regression provided a simple and interpretable baseline.
- Tree-based models captured non-linear relationships better.
- Random Forest improved performance but was slower on larger feature sets.
- Gradient boosting models such as XGBoost and LightGBM achieved stronger predictive performance.
- Feature engineering improved model performance compared with using raw features only.

---

## Feature Importance

Feature importance analysis was used to understand which variables contributed most to default prediction.

Important features often included:

- External credit scores
- Credit-to-income ratio
- Annuity-to-income ratio
- Applicant age
- Employment length
- Previous loan behavior
- Credit bureau history
- Payment delay indicators

This helps make the model more interpretable and useful for business decision-making.

---

## Key Insights

Some important insights from the project include:

- Applicants with higher credit-to-income ratios tend to show higher default risk.
- External credit score variables are strong predictors of repayment difficulty.
- Employment history and income stability are important risk indicators.
- Previous loan behavior provides useful signals for predicting future default.
- Class imbalance is a major challenge in credit risk modeling.

---

## Challenges

The main challenges in this project were:

- Large number of missing values
- Multiple related data tables
- Class imbalance in the target variable
- High-dimensional categorical features
- Outliers and abnormal values
- Need for both predictive performance and interpretability

---

## Project Structure

```text
Home-Credit-Default-Risk-Modeling/
│
├── data/
│   ├── application_train.csv
│   ├── application_test.csv
│   ├── bureau.csv
│   ├── bureau_balance.csv
│   ├── previous_application.csv
│   ├── installments_payments.csv
│   ├── credit_card_balance.csv
│   └── POS_CASH_balance.csv
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_modeling.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   └── evaluation.py
│
├── outputs/
│   ├── figures/
│   ├── model_results.csv
│   └── feature_importance.csv
│
├── README.md
└── requirements.txt
