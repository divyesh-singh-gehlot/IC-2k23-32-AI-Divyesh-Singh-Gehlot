# Lab 14 - Part 3: Decision Tree Visualization

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import export_text, plot_tree

data = pd.read_csv("datasets/placement_processed.csv")
X = data.drop(columns=["status", "salary"], errors="ignore")

model = joblib.load("models/decision_tree.pkl")

# 1. the tree as text rules
print("Tree rules:\n")
print(export_text(model, feature_names=list(X.columns)))

# 2. the tree as a picture
plt.figure(figsize=(22, 10))
plot_tree(model, feature_names=list(X.columns),
          class_names=["Not placed", "Placed"],
          filled=True, rounded=True, fontsize=9)
plt.title("Decision Tree - Student Placement")
plt.savefig("Lab_14 (Unit 5)/outputs/decision_tree.png", dpi=110, bbox_inches="tight")
plt.close()

# 3. which features matter most
importance = pd.Series(model.feature_importances_, index=X.columns)
importance = importance.sort_values(ascending=False)
print("Feature importance:")
print(importance.round(3).to_string())

importance.sort_values().plot(kind="barh", color="steelblue")
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.savefig("Lab_14 (Unit 5)/outputs/feature_importance.png", dpi=120, bbox_inches="tight")
plt.close()
print("\nSaved decision_tree.png and feature_importance.png to outputs/")
