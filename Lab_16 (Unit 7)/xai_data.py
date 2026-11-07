# Helper for Lab 16: loads the placement data and trains the decision tree
# (same settings as Lab 14, so the dashboard explains the Lab 5 model).

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def load_and_train():
    data = pd.read_csv("datasets/placement_processed.csv")
    X = data.drop(columns=["status", "salary"], errors="ignore")
    y = data["status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    return model, X_train, X_test, y_train, y_test
