# Lab 3 - Data Preprocessing (Student Placement Dataset)
# Day 1: loading + EDA
# Day 2: cleaning, missing values, label encoding
# Day 3: feature selection, visualization, full pipeline

from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # save plots to files instead of opening windows
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import LabelEncoder

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR.parent / "datasets" / "placement.csv"
TARGET_COLUMN = "status"
CATEGORICAL_COLUMNS = ["gender", "ssc_b", "hsc_b", "hsc_s",
                       "degree_t", "workex", "specialisation"]
NUMERIC_COLUMNS = ["ssc_p", "hsc_p", "degree_p", "etest_p", "mba_p"]
OUTPUT_DIR = BASE_DIR / "outputs"


# ---------------- 1. Dataset loading ----------------
def generate_sample_dataset(path, n_rows=215, seed=42):
    # makes a sample dataset with the same columns as the Campus Recruitment data
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "sl_no": np.arange(1, n_rows + 1),
        "gender": rng.choice(["M", "F"], n_rows, p=[0.65, 0.35]),
        "ssc_p": rng.normal(67, 10, n_rows).clip(40, 90).round(2),
        "ssc_b": rng.choice(["Central", "Others"], n_rows),
        "hsc_p": rng.normal(66, 11, n_rows).clip(40, 97).round(2),
        "hsc_b": rng.choice(["Central", "Others"], n_rows),
        "hsc_s": rng.choice(["Commerce", "Science", "Arts"], n_rows, p=[0.5, 0.4, 0.1]),
        "degree_p": rng.normal(66, 7, n_rows).clip(50, 91).round(2),
        "degree_t": rng.choice(["Comm&Mgmt", "Sci&Tech", "Others"], n_rows, p=[0.55, 0.40, 0.05]),
        "workex": rng.choice(["Yes", "No"], n_rows, p=[0.35, 0.65]),
        "etest_p": rng.uniform(50, 98, n_rows).round(2),
        "specialisation": rng.choice(["Mkt&Fin", "Mkt&HR"], n_rows),
        "mba_p": rng.normal(62, 6, n_rows).clip(51, 78).round(2),
    })

    # placement chance depends on marks and work experience
    score = (
        0.06 * (df["ssc_p"] - 67) + 0.05 * (df["hsc_p"] - 66)
        + 0.08 * (df["degree_p"] - 66) + 0.9 * (df["workex"] == "Yes")
        + 0.02 * (df["etest_p"] - 74) + 0.7
    )
    placed = rng.random(n_rows) < 1 / (1 + np.exp(-score))
    df["status"] = np.where(placed, "Placed", "Not Placed")

    # salary only exists for placed students
    df["salary"] = np.where(placed, rng.normal(290000, 90000, n_rows).clip(200000, 940000).round(-3), np.nan)

    # add some dirty data so the cleaning steps have work to do
    for col in ["ssc_p", "hsc_p", "etest_p", "mba_p"]:
        df.loc[rng.choice(n_rows, 6, replace=False), col] = np.nan
    df.loc[rng.choice(n_rows, 4, replace=False), "hsc_s"] = np.nan
    df.loc[rng.choice(n_rows, 5, replace=False), "gender"] = df["gender"].str.lower()
    df = pd.concat([df, df.sample(4, random_state=seed)], ignore_index=True)

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def load_dataset(path):
    # read the csv, make a sample file if it is not there
    try:
        if not path.exists():
            print(f"[INFO] {path.name} not found. Generating sample dataset.")
            return generate_sample_dataset(path)
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise ValueError("The dataset file is empty.")
    except pd.errors.ParserError as error:
        raise ValueError(f"Could not parse the dataset: {error}")


# ---------------- 2. Exploratory data analysis ----------------
def explore_data(df):
    print("=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")

    print("\nFirst 5 rows:")
    print(df.head().to_string())

    print("\nData types:")
    print(df.dtypes.to_string())

    print("\nSummary statistics (numeric):")
    print(df.describe().round(2).to_string())

    print("\nMissing values per column:")
    missing = df.isnull().sum()
    print(missing[missing > 0].to_string() if missing.any() else "None")

    print(f"\nDuplicate rows: {df.duplicated().sum()}")

    print(f"\nTarget distribution ('{TARGET_COLUMN}'):")
    print(df[TARGET_COLUMN].value_counts().to_string())


# ---------------- 3. Data cleaning ----------------
def clean_data(df):
    cleaned = df.copy()
    rows_before = len(cleaned)

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    print(f"Removed {rows_before - len(cleaned)} duplicate rows.")

    # remove extra spaces and fix case ('m' -> 'M')
    for column in CATEGORICAL_COLUMNS:
        cleaned[column] = cleaned[column].astype("string").str.strip()
    cleaned["gender"] = cleaned["gender"].str.upper()

    # serial number is not useful for prediction
    cleaned = cleaned.drop(columns=["sl_no"], errors="ignore")

    # percentages must be between 0 and 100
    for column in NUMERIC_COLUMNS:
        invalid = ~cleaned[column].between(0, 100) & cleaned[column].notna()
        cleaned.loc[invalid, column] = np.nan
    return cleaned


# ---------------- 4. Missing value handling ----------------
def handle_missing_values(df):
    # numeric -> median, categorical -> mode, salary NaN -> 0 (not placed)
    imputed = df.copy()

    for column in NUMERIC_COLUMNS:
        median_value = imputed[column].median()
        count = imputed[column].isnull().sum()
        imputed[column] = imputed[column].fillna(median_value)
        if count:
            print(f"  {column}: filled {count} missing with median = {median_value:.2f}")

    for column in CATEGORICAL_COLUMNS:
        mode_value = imputed[column].mode()[0]
        count = imputed[column].isnull().sum()
        imputed[column] = imputed[column].fillna(mode_value)
        if count:
            print(f"  {column}: filled {count} missing with mode = '{mode_value}'")

    imputed["salary"] = imputed["salary"].fillna(0)
    return imputed


def compare_missing_strategies(df_with_missing):
    # compares drop / mean / median on one column
    column = "etest_p"
    series = df_with_missing[column]
    results = pd.DataFrame({
        "Strategy": ["Original (with NaN)", "Drop rows", "Mean imputation", "Median imputation"],
        "Rows": [len(series), series.dropna().shape[0], len(series), len(series)],
        "Mean": [series.mean(), series.dropna().mean(), series.fillna(series.mean()).mean(), series.fillna(series.median()).mean()],
        "Std": [series.std(), series.dropna().std(), series.fillna(series.mean()).std(), series.fillna(series.median()).std()],
    }).round(2)
    print(f"\nComparison of missing-value strategies on '{column}':")
    print(results.to_string(index=False))


# ---------------- 5. Label encoding ----------------
def encode_labels(df):
    encoded = df.copy()
    mappings = {}

    for column in CATEGORICAL_COLUMNS + [TARGET_COLUMN]:
        encoder = LabelEncoder()
        encoded[column] = encoder.fit_transform(encoded[column].astype(str))
        mappings[column] = {label: int(code) for code, label in enumerate(encoder.classes_)}

    print("Label encoding mappings:")
    for column, mapping in mappings.items():
        print(f"  {column}: {mapping}")
    return encoded, mappings


# ---------------- 6. Feature selection ----------------
def select_features(df, k=5):
    # salary is left out because it is only known after a student is placed (data leakage)
    features = df.drop(columns=[TARGET_COLUMN, "salary"])
    target = df[TARGET_COLUMN]

    correlations = features.corrwith(target).abs().sort_values(ascending=False)

    selector = SelectKBest(score_func=f_classif, k=k).fit(features, target)
    scores = pd.Series(selector.scores_, index=features.columns).sort_values(ascending=False)
    selected = list(features.columns[selector.get_support()])

    print("\nAbsolute correlation with target:")
    print(correlations.round(3).to_string())
    print("\nANOVA F-scores:")
    print(scores.round(2).to_string())
    print(f"\nTop {k} selected features: {selected}")
    return selected, scores


# ---------------- 7. Data visualization ----------------
def visualize_data(raw_df, encoded_df, feature_scores):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. histograms of numeric columns
    raw_df[NUMERIC_COLUMNS].hist(bins=15, figsize=(12, 7), edgecolor="black")
    plt.suptitle("Distribution of Numeric Features")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "01_numeric_distributions.png", dpi=120)
    plt.close()

    # 2. placement status for a few categorical columns
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for axis, column in zip(axes, ["gender", "workex", "specialisation"]):
        sns.countplot(data=raw_df, x=column, hue=TARGET_COLUMN, ax=axis)
        axis.set_title(f"Placement by {column}")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_placement_by_category.png", dpi=120)
    plt.close()

    # 3. box plot to check outliers
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=raw_df[NUMERIC_COLUMNS])
    plt.title("Box Plot of Numeric Features (Outlier Check)")
    plt.savefig(OUTPUT_DIR / "03_boxplot_outliers.png", dpi=120)
    plt.close()

    # 4. correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(encoded_df.drop(columns=["salary"]).corr(), annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("Correlation Heatmap (Encoded Features)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_correlation_heatmap.png", dpi=120)
    plt.close()

    # 5. feature scores
    plt.figure(figsize=(8, 5))
    feature_scores.sort_values().plot(kind="barh", color="steelblue")
    plt.title("Feature Scores (ANOVA F-test)")
    plt.xlabel("F-score")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_feature_scores.png", dpi=120)
    plt.close()

    print(f"Saved 5 plots to: {OUTPUT_DIR}")


def main():
    try:
        print("\n[1] DATASET LOADING")
        raw_df = load_dataset(DATASET_PATH)
        print(f"Loaded {raw_df.shape[0]} rows, {raw_df.shape[1]} columns")

        print()
        explore_data(raw_df)

        print("\n" + "=" * 60)
        print("DATA CLEANING")
        print("=" * 60)
        cleaned_df = clean_data(raw_df)

        compare_missing_strategies(cleaned_df)

        print("\n" + "=" * 60)
        print("MISSING VALUE HANDLING")
        print("=" * 60)
        imputed_df = handle_missing_values(cleaned_df)
        print(f"Missing values remaining: {imputed_df.isnull().sum().sum()}")

        print("\n" + "=" * 60)
        print("LABEL ENCODING")
        print("=" * 60)
        encoded_df, _ = encode_labels(imputed_df)

        print("\n" + "=" * 60)
        print("FEATURE SELECTION")
        print("=" * 60)
        _, feature_scores = select_features(encoded_df, k=5)

        print("\n" + "=" * 60)
        print("DATA VISUALIZATION")
        print("=" * 60)
        visualize_data(imputed_df, encoded_df, feature_scores)

        processed_path = DATASET_PATH.parent / "placement_processed.csv"
        encoded_df.to_csv(processed_path, index=False)
        print(f"\nProcessed dataset saved to: {processed_path.name}")

    except (ValueError, KeyError, OSError) as error:
        print(f"[ERROR] Pipeline failed: {error}")


if __name__ == "__main__":
    main()