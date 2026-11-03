# Helper used by Lab 15 parts 3 and 4: makes / loads the student score dataset.
# The data is generated with a known formula plus noise, so we can check
# whether the model recovers the real relationship.

import os

import numpy as np
import pandas as pd

DATA_PATH = "datasets/student_scores.csv"


def make_dataset(path=DATA_PATH, n=200, seed=42):
    rng = np.random.default_rng(seed)
    hours = rng.uniform(1, 10, n).round(1)
    attendance = rng.uniform(50, 100, n).round(0)
    noise = rng.normal(0, 4, n)

    # true rule: score = 20 + 5 * hours + 0.3 * attendance + noise
    score = (20 + 5 * hours + 0.3 * attendance + noise).clip(0, 100).round(1)

    data = pd.DataFrame({"hours_studied": hours, "attendance": attendance, "score": score})
    data.to_csv(path, index=False)
    return data


def load_split(test_fraction=0.2, seed=42):
    if not os.path.exists(DATA_PATH):
        print("Dataset not found, creating", DATA_PATH)
        make_dataset()
    data = pd.read_csv(DATA_PATH)

    X = data[["hours_studied", "attendance"]].values.astype("float32")
    y = data[["score"]].values.astype("float32")

    # shuffle with a fixed seed, then split
    order = np.random.default_rng(seed).permutation(len(data))
    n_test = int(len(data) * test_fraction)
    test_idx, train_idx = order[:n_test], order[n_test:]

    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # scale the features using the TRAINING mean and std only
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    return {
        "X_train": (X_train - mean) / std, "X_test": (X_test - mean) / std,
        "y_train": y_train, "y_test": y_test,
        "mean": mean, "std": std, "data": data,
    }
