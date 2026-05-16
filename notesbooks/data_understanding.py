# ============================================================
# Home Credit Default Risk — Data Understanding
# ============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Plotting style ──────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#F8F9FA',
    'axes.facecolor':   '#F8F9FA',
    'axes.edgecolor':   '#CCCCCC',
    'axes.grid':        True,
    'grid.alpha':       0.4,
    'font.size':        11,
})
PALETTE = ['#4C72B0', '#DD8452']

# ============================================================
# 1. LOAD DATA
# ============================================================
BASE = "/Users/elina/Downloads/home-credit-default-risk (1)/"

application_train     = pd.read_csv(BASE + "application_train.csv")
application_test      = pd.read_csv(BASE + "application_test.csv")
bureau                = pd.read_csv(BASE + "bureau.csv")
bureau_balance        = pd.read_csv(BASE + "bureau_balance.csv")
credit_card_balance   = pd.read_csv(BASE + "credit_card_balance.csv")
installments_payments = pd.read_csv(BASE + "installments_payments.csv")
POS_CASH_balance      = pd.read_csv(BASE + "POS_CASH_balance.csv")
previous_application  = pd.read_csv(BASE + "previous_application.csv")

datasets = {
    "application_train":     application_train,
    "application_test":      application_test,
    "bureau":                bureau,
    "bureau_balance":        bureau_balance,
    "credit_card_balance":   credit_card_balance,
    "installments_payments": installments_payments,
    "POS_CASH_balance":      POS_CASH_balance,
    "previous_application":  previous_application,
}

# ============================================================
# 2. DATASET OVERVIEW  — shape, dtypes, memory
# ============================================================
print("=" * 65)
print("  SECTION 1: DATASET OVERVIEW")
print("=" * 65)

overview_rows = []
for name, df in datasets.items():
    n_num = df.select_dtypes(include=np.number).shape[1]
    n_cat = df.select_dtypes(include='object').shape[1]
    mem   = df.memory_usage(deep=True).sum() / 1024**2
    overview_rows.append({
        "Dataset":    name,
        "Rows":       df.shape[0],
        "Columns":    df.shape[1],
        "Numeric":    n_num,
        "Categorical":n_cat,
        "Memory (MB)":round(mem, 2),
    })

overview_df = pd.DataFrame(overview_rows).set_index("Dataset")
print(overview_df.to_string())

# ── Bar chart: rows per dataset ─────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Dataset Overview", fontsize=14, fontweight='bold')

overview_df["Rows"].sort_values().plot(
    kind="barh", ax=axes[0], color='#4C72B0', edgecolor='white')
axes[0].set_title("Number of Rows")
axes[0].set_xlabel("Rows")

overview_df["Columns"].sort_values().plot(
    kind="barh", ax=axes[1], color='#DD8452', edgecolor='white')
axes[1].set_title("Number of Columns")
axes[1].set_xlabel("Columns")
plt.tight_layout()
plt.savefig("01_dataset_overview.png", dpi=150)
plt.show()

# ============================================================
# 3. TARGET VARIABLE ANALYSIS
# ============================================================
print("\n" + "=" * 65)
print("  SECTION 2: TARGET VARIABLE (application_train)")
print("=" * 65)

target_counts = application_train['TARGET'].value_counts()
target_pct    = application_train['TARGET'].value_counts(normalize=True) * 100
print(pd.DataFrame({'Count': target_counts, 'Percentage (%)': target_pct.round(2)}))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Target Variable Distribution", fontsize=14, fontweight='bold')

axes[0].bar(['No Default (0)', 'Default (1)'], target_counts.values,
            color=PALETTE, edgecolor='white', width=0.5)
for i, v in enumerate(target_counts.values):
    axes[0].text(i, v + 500, f'{v:,}', ha='center', fontweight='bold')
axes[0].set_title("Count")
axes[0].set_ylabel("Number of Applications")

axes[1].pie(target_counts.values,
            labels=['No Default (0)', 'Default (1)'],
            autopct='%1.2f%%', colors=PALETTE,
            startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
axes[1].set_title("Proportion")
plt.tight_layout()
plt.savefig("02_target_distribution.png", dpi=150)
plt.show()

# ============================================================
# 4. MISSING VALUES ANALYSIS
# ============================================================
print("\n" + "=" * 65)
print("  SECTION 3: MISSING VALUES")
print("=" * 65)

def missing_summary(df, name):
    miss = df.isnull().sum()
    miss = miss[miss > 0].sort_values(ascending=False)
    pct  = (miss / len(df) * 100).round(2)
    result = pd.DataFrame({'Missing Count': miss, 'Missing %': pct})
    print(f"\n── {name}: {len(miss)} columns with missing values ──")
    print(result.head(15).to_string())
    return result

for name, df in datasets.items():
    missing_summary(df, name)

# ── Heatmap: top-20 missing columns in application_train ───
miss_train = application_train.isnull().mean().sort_values(ascending=False).head(20)

fig, ax = plt.subplots(figsize=(10, 6))
miss_train.plot(kind='bar', color='#4C72B0', edgecolor='white', ax=ax)
ax.set_title("Top-20 Missing Value Columns — application_train", fontweight='bold')
ax.set_ylabel("Missing Rate")
ax.set_ylim(0, 1)
ax.axhline(0.5, color='red', linestyle='--', alpha=0.6, label='50% threshold')
ax.legend()
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.tight_layout()
plt.savefig("03_missing_values.png", dpi=150)
plt.show()

# ============================================================
# 5. DATA TYPES & UNIQUE VALUES
# ============================================================
print("\n" + "=" * 65)
print("  SECTION 4: DATA TYPES & UNIQUE VALUES (application_train)")
print("=" * 65)

dtype_df = pd.DataFrame({
    'dtype':   application_train.dtypes,
    'nunique': application_train.nunique(),
    'sample':  [application_train[c].dropna().iloc[0]
                if application_train[c].dropna().shape[0] > 0 else np.nan
                for c in application_train.columns]
})
print(dtype_df.to_string())

# ── dtype breakdown ─────────────────────────────────────────
dtype_counts = application_train.dtypes.astype(str).value_counts()
fig, ax = plt.subplots(figsize=(7, 5))
dtype_counts.plot(kind='bar', color='#4C72B0', edgecolor='white', ax=ax)
ax.set_title("Column Data Types — application_train", fontweight='bold')
ax.set_ylabel("Count")
ax.set_xlabel("dtype")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("04_dtypes.png", dpi=150)
plt.show()

# ============================================================
# 6. NUMERICAL FEATURE DISTRIBUTIONS
# ============================================================
print("\n" + "=" * 65)
print("  SECTION 5: NUMERICAL FEATURE DISTRIBUTIONS")
print("=" * 65)

# Key numerical columns
key_num = [
    'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY',
    'AMT_GOODS_PRICE', 'DAYS_BIRTH', 'DAYS_EMPLOYED',
    'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3'
]
key_num = [c for c in key_num if c in application_train.columns]

print(application_train[key_num].describe().T.round(2).to_string())

fig, axes = plt.subplots(3, 3, figsize=(16, 12))
fig.suptitle("Key Numerical Feature Distributions by TARGET", fontsize=14, fontweight='bold')

for i, col in enumerate(key_num):
    ax = axes[i // 3][i % 3]
    for target_val, color in zip([0, 1], PALETTE):
        subset = application_train.loc[application_train['TARGET'] == target_val, col].dropna()
        subset.plot(kind='hist', bins=50, ax=ax, alpha=0.55,
                    color=color, label=f'TARGET={target_val}', density=True)
    ax.set_title(col, fontsize=10)
    ax.set_xlabel("")
    ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("05_numerical_distributions.png", dpi=150)
plt.show()

# ── DAYS_BIRTH: convert to age in years ─────────────────────
application_train['AGE_YEARS'] = application_train['DAYS_BIRTH'].abs() / 365
print("\nAge Statistics:")
print(application_train['AGE_YEARS'].describe().round(2))

# ── DAYS_EMPLOYED anomaly (365243 = data entry error) ───────
anomaly_count = (application_train['DAYS_EMPLOYED'] == 365243).sum()
print(f"\nDAYS_EMPLOYED anomaly count (365243): {anomaly_count:,}")

# ============================================================
# 7. CATEGORICAL FEATURE ANALYSIS
# ============================================================
print("\n" + "=" * 65)
print("  SECTION 6: CATEGORICAL FEATURE ANALYSIS")
print("=" * 65)

key_cat = [
    'NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR',
    'FLAG_OWN_REALTY', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE',
    'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'OCCUPATION_TYPE'
]
key_cat = [c for c in key_cat if c in application_train.columns]

for col in key_cat:
    counts = application_train[col].value_counts()
    print(f"\n{col}:\n{counts.to_string()}")

# ── Default rate by category ─────────────────────────────────
fig, axes = plt.subplots(3, 3, figsize=(18, 14))
fig.suptitle("Default Rate by Categorical Features", fontsize=14, fontweight='bold')

for i, col in enumerate(key_cat):
    ax = axes[i // 3][i % 3]
    dr = (application_train.groupby(col)['TARGET']
          .mean()
          .sort_values(ascending=False))
    dr.plot(kind='bar', ax=ax, color='#4C72B0', edgecolor='white')
    ax.set_title(f"Default Rate — {col}", fontsize=9)
    ax.set_ylabel("Default Rate")
    ax.axhline(application_train['TARGET'].mean(), color='red',
               linestyle='--', alpha=0.7, linewidth=1.2)
    plt.setp(ax.get_xticklabels(), rotation=35, ha='right', fontsize=8)

plt.tight_layout()
plt.savefig("06_categorical_default_rates.png", dpi=150)
plt.show()

# ============================================================
# 8. CORRELATION ANALYSIS
# ============================================================
print("\n" + "=" * 65)
print("  SECTION 7: CORRELATION WITH TARGET")
print("=" * 65)

num_cols = application_train.select_dtypes(include=np.number).columns.tolist()
corr_target = (application_train[num_cols]
               .corr()['TARGET']
               .drop('TARGET')
               .sort_values(key=abs, ascending=False))

print("Top 20 features most correlated with TARGET:")
print(corr_target.head(20).round(4).to_string())

fig, ax = plt.subplots(figsize=(10, 8))
top_corr = corr_target.head(20)
colors = ['#DD8452' if v > 0 else '#4C72B0' for v in top_corr.values]
top_corr.sort_values().plot(kind='barh', ax=ax, color=colors[::-1], edgecolor='white')
ax.set_title("Top 20 Features Correlated with TARGET", fontweight='bold')
ax.set_xlabel("Pearson Correlation")
ax.axvline(0, color='black', linewidth=0.8)
plt.tight_layout()
plt.savefig("07_correlation_target.png", dpi=150)
plt.show()

# ── Correlation matrix: EXT_SOURCE & AMT fields ─────────────
corr_cols = [c for c in ['EXT_SOURCE_1','EXT_SOURCE_2','EXT_SOURCE_3',
                          'AMT_CREDIT','AMT_ANNUITY','AMT_INCOME_TOTAL',
                          'DAYS_BIRTH','DAYS_EMPLOYED','TARGET']
             if c in application_train.columns]

fig, ax = plt.subplots(figsize=(10, 8))
corr_matrix = application_train[corr_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
            cmap='RdYlBu_r', center=0, linewidths=0.5,
            square=True, ax=ax, annot_kws={"size": 9})
ax.set_title("Correlation Matrix — Key Features", fontweight='bold')
plt.tight_layout()
plt.savefig("08_correlation_matrix.png", dpi=150)
plt.show()

# ============================================================
# 9. BUREAU & SUPPLEMENTARY TABLE SUMMARIES
# ============================================================
print("\n" + "=" * 65)
print("  SECTION 8: SUPPLEMENTARY TABLE SUMMARIES")
print("=" * 65)

# Bureau: credits per applicant
credits_per_app = bureau.groupby('SK_ID_CURR').size()
print(f"\nBureau — Credits per applicant:\n{credits_per_app.describe().round(2)}")

fig, ax = plt.subplots(figsize=(9, 4))
credits_per_app.clip(upper=30).value_counts().sort_index().plot(
    kind='bar', ax=ax, color='#4C72B0', edgecolor='white')
ax.set_title("Number of Bureau Credits per Applicant (capped at 30)", fontweight='bold')
ax.set_xlabel("# Bureau Credits")
ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig("09_bureau_credits_per_applicant.png", dpi=150)
plt.show()

# Previous application count
prev_per_app = previous_application.groupby('SK_ID_CURR').size()
print(f"\nPrevious Application — Count per applicant:\n{prev_per_app.describe().round(2)}")

# Bureau balance status distribution
if 'STATUS' in bureau_balance.columns:
    print(f"\nBureau Balance STATUS distribution:\n"
          f"{bureau_balance['STATUS'].value_counts().to_string()}")

# POS CASH NAME_CONTRACT_STATUS
if 'NAME_CONTRACT_STATUS' in POS_CASH_balance.columns:
    print(f"\nPOS CASH Contract Status:\n"
          f"{POS_CASH_balance['NAME_CONTRACT_STATUS'].value_counts().to_string()}")

# ============================================================
# 10. SUMMARY REPORT
# ============================================================
print("\n" + "=" * 65)
print("  SECTION 9: DATA UNDERSTANDING SUMMARY")
print("=" * 65)

summary = {
    "Total training applications":      len(application_train),
    "Total test applications":           len(application_test),
    "Default rate (train)":             f"{application_train['TARGET'].mean()*100:.2f}%",
    "Class imbalance ratio (0:1)":      f"{target_counts[0]:,} : {target_counts[1]:,}",
    "Columns in application_train":     application_train.shape[1],
    "Columns > 50% missing (train)":    int((application_train.isnull().mean() > 0.5).sum()),
    "Unique applicants in bureau":       bureau['SK_ID_CURR'].nunique(),
    "Records in installments_payments": len(installments_payments),
    "Records in credit_card_balance":   len(credit_card_balance),
    "Records in POS_CASH_balance":      len(POS_CASH_balance),
}

for k, v in summary.items():
    print(f"  {k:<45} {v}")

print("\nKey Observations:")
obs = [
    "1. Dataset is highly IMBALANCED: ~92% non-default vs ~8% default.",
    "2. DAYS_EMPLOYED contains 365,243 anomalous values (data entry error).",
    "3. EXT_SOURCE_1/2/3 show the strongest negative correlation with TARGET.",
    "4. Several columns have >60% missing values and may need dropping/imputation.",
    "5. bureau/previous_application provide rich historical credit behavior features.",
    "6. Application is the central table; all others join via SK_ID_CURR / SK_ID_PREV.",
]
for o in obs:
    print(f"  {o}")

print("\n  Data Understanding complete. Plots saved to working directory.")
