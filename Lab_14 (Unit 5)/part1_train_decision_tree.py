# Lab 14 - Part 1: Student Placement Prediction using a Decision Tree
# Uses the processed dataset from Lab 11 (all columns are already numbers).

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("datasets/placement_processed.csv")
print("Dataset shape:", data.shape)

# salary is only known AFTER a student is placed, so it cannot be a feature
X = data.drop(columns=["status", "salary"], errors="ignore")
y = data["status"]

print("Features:", list(X.columns))
print("Placed:", y.sum(), " Not placed:", len(y) - y.sum())

# 80% for training, 20% for testing (stratify keeps the same class ratio)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print("\nTraining rows:", len(X_train), " Testing rows:", len(X_test))

model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)

print("\nTree depth      :", model.get_depth())
print("Number of leaves:", model.get_n_leaves())
print("Train accuracy  :", round(model.score(X_train, y_train) * 100, 2), "%")
print("Test accuracy   :", round(model.score(X_test, y_test) * 100, 2), "%")

# predict for one new student
new_student = X_test.iloc[[0]]
prediction = model.predict(new_student)[0]
print("\nFirst test student predicted as:", "Placed" if prediction == 1 else "Not placed",
      "| actual:", "Placed" if y_test.iloc[0] == 1 else "Not placed")

joblib.dump(model, "models/decision_tree.pkl")
print("\nModel saved to ../models/decision_tree.pkl")
