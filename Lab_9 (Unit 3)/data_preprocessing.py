# Lab 3 - Data Preprocessing (Student Placement Dataset)
# Day 1: dataset loading and exploratory data analysis (EDA)

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR.parent / "datasets" / "placement.csv"
TARGET_COLUMN = "status"


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


def main():
    try:
        print("\n[1] DATASET LOADING")
        raw_df = load_dataset(DATASET_PATH)
        print(f"Loaded {raw_df.shape[0]} rows, {raw_df.shape[1]} columns")

        print()
        explore_data(raw_df)

    except (ValueError, KeyError, OSError) as error:
        print(f"[ERROR] Pipeline failed: {error}")


if __name__ == "__main__":
    main()