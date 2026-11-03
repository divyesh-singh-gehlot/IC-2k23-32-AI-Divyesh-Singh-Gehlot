# Lab 14 - Part 2: Model Evaluation
# Confusion matrix, classification report and the effect of tree depth.

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, ConfusionMatrixDisplay,
                             f1_score, precision_score, recall_score)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("datasets/placement_processed.csv")
X = data.drop(columns=["status", "salary"], errors="ignore")
y = data["status"]

# same split as part 1 (same random_state)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

model = joblib.load("models/decision_tree.pkl")
y_pred = model.predict(X_test)

print("Accuracy :", round(accuracy_score(y_test, y_pred), 4))
print("Precision:", round(precision_score(y_test, y_pred), 4))
print("Recall   :", round(recall_score(y_test, y_pred), 4))
print("F1-score :", round(f1_score(y_test, y_pred), 4))

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion matrix (rows = actual, columns = predicted):")
print(cm)
tn, fp, fn, tp = cm.ravel()
print("True negatives :", tn, "| False positives:", fp)
print("False negatives:", fn, "| True positives :", tp)

print("\nClassification report:")
print(classification_report(y_test, y_pred, target_names=["Not placed", "Placed"]))

# a model that always says "Placed" - the baseline to beat
baseline = y_test.mean()
print("Baseline (always predict Placed):", round(baseline, 4))

ConfusionMatrixDisplay(cm, display_labels=["Not placed", "Placed"]).plot(cmap="Blues")
plt.title("Confusion Matrix - Decision Tree")
plt.savefig("Lab_14 (Unit 5)/outputs/confusion_matrix.png", dpi=120, bbox_inches="tight")
plt.close()

# effect of max_depth: a deeper tree fits the training data better but may overfit
print("\nDepth  Train acc  CV acc (5-fold)")
depths = list(range(1, 11))
train_scores = []
cv_scores = []
for d in depths:
    tree = DecisionTreeClassifier(max_depth=d, random_state=42)
    tree.fit(X_train, y_train)
    train_scores.append(tree.score(X_train, y_train))
    cv_scores.append(cross_val_score(tree, X_train, y_train, cv=5).mean())
    print(f"{d:5d}  {train_scores[-1]:9.3f}  {cv_scores[-1]:14.3f}")

plt.plot(depths, train_scores, marker="o", label="Train accuracy")
plt.plot(depths, cv_scores, marker="o", label="Cross-validation accuracy")
plt.xlabel("max_depth")
plt.ylabel("Accuracy")
plt.title("Effect of tree depth")
plt.legend()
plt.savefig("Lab_14 (Unit 5)/outputs/depth_vs_accuracy.png", dpi=120, bbox_inches="tight")
plt.close()
print("\nSaved plots to outputs/")
