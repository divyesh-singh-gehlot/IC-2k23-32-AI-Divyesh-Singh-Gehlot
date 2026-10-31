# Lab 3 - Analysis: compare preprocessing techniques and feature engineering
# Uses 5-fold cross-validated accuracy with Logistic Regression and a Decision Tree.

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

import data_preprocessing as dp

CV = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


def score(model, features, target):
    # mean and std of the 5 cross-validation accuracies
    scores = cross_val_score(model, features, target, cv=CV, scoring="accuracy")
    return scores.mean(), scores.std()


def build_model(kind, categorical, numeric, encoding):
    # encoding: "onehot" or "ordinal"; kind: "logreg" or "tree"
    if encoding == "onehot":
        encoder = OneHotEncoder(handle_unknown="ignore")
    else:
        encoder = OrdinalEncoder()
    scale = StandardScaler() if kind == "logreg" else "passthrough"
    transformer = ColumnTransformer([("cat", encoder, categorical), ("num", scale, numeric)])
    if kind == "logreg":
        model = LogisticRegression(max_iter=1000)
    else:
        model = DecisionTreeClassifier(max_depth=4, random_state=42)
    return Pipeline([("prep", transformer), ("model", model)])


def main():
    raw = dp.load_dataset(dp.DATASET_PATH)
    cleaned = dp.clean_data(raw)
    cats, nums = dp.CATEGORICAL_COLUMNS, dp.NUMERIC_COLUMNS
    rows = []

    # A. missing values: drop rows vs median/mode imputation
    dropped = cleaned.dropna(subset=nums + cats)
    imputed = dp.handle_missing_values(cleaned)
    for name, data in [("Drop rows with NaN", dropped), ("Median/mode imputation", imputed)]:
        target = (data[dp.TARGET_COLUMN] == "Placed").astype(int)
        for kind in ["logreg", "tree"]:
            mean, std = score(build_model(kind, cats, nums, "onehot"), data[cats + nums], target)
            rows.append(("Missing values", name, kind, len(data), mean, std))

    # B. encoding: label (ordinal) vs one-hot
    target = (imputed[dp.TARGET_COLUMN] == "Placed").astype(int)
    for name, enc in [("Label (ordinal) encoding", "ordinal"), ("One-hot encoding", "onehot")]:
        for kind in ["logreg", "tree"]:
            mean, std = score(build_model(kind, cats, nums, enc), imputed[cats + nums], target)
            rows.append(("Encoding", name, kind, len(imputed), mean, std))

    # C. scaling (only logistic regression, trees do not need scaling)
    transformer = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), cats),
                                     ("num", "passthrough", nums)])
    unscaled = Pipeline([("prep", transformer), ("model", LogisticRegression(max_iter=1000))])
    mean, std = score(unscaled, imputed[cats + nums], target)
    rows.append(("Scaling", "No scaling", "logreg", len(imputed), mean, std))
    mean, std = score(build_model("logreg", cats, nums, "onehot"), imputed[cats + nums], target)
    rows.append(("Scaling", "StandardScaler", "logreg", len(imputed), mean, std))

    # D. feature engineering: two new columns made from existing ones
    engineered = imputed.copy()
    engineered["avg_academic"] = engineered[["ssc_p", "hsc_p", "degree_p"]].mean(axis=1)
    engineered["academic_trend"] = engineered["degree_p"] - engineered["ssc_p"]
    new_nums = nums + ["avg_academic", "academic_trend"]
    for kind in ["logreg", "tree"]:
        base = score(build_model(kind, cats, nums, "onehot"), engineered[cats + nums], target)
        new = score(build_model(kind, cats, new_nums, "onehot"), engineered[cats + new_nums], target)
        rows.append(("Feature engineering", "Original features", kind, len(engineered), *base))
        rows.append(("Feature engineering", "+ avg_academic, academic_trend", kind, len(engineered), *new))

    # E. feature selection: top 5 features vs all features
    top5 = ["ssc_p", "hsc_p", "degree_p", "etest_p", "mba_p"]
    for kind in ["logreg", "tree"]:
        all_f = score(build_model(kind, cats, nums, "onehot"), imputed[cats + nums], target)
        sel = score(build_model(kind, [], top5, "onehot"), imputed[top5], target)
        rows.append(("Feature selection", "All 12 features", kind, len(imputed), *all_f))
        rows.append(("Feature selection", "Top 5 (SelectKBest)", kind, len(imputed), *sel))

    results = pd.DataFrame(rows, columns=["Experiment", "Technique", "Model", "Rows", "CV Accuracy", "Std"])
    results["CV Accuracy"] = (results["CV Accuracy"] * 100).round(2)
    results["Std"] = (results["Std"] * 100).round(2)
    print(results.to_string(index=False))

    dp.OUTPUT_DIR.mkdir(exist_ok=True)
    results.to_csv(dp.OUTPUT_DIR / "preprocessing_comparison.csv", index=False)

    baseline = max(target.mean(), 1 - target.mean()) * 100
    print(f"\nMajority-class baseline accuracy: {baseline:.2f}%")


if __name__ == "__main__":
    main()