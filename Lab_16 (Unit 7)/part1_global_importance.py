# Lab 16 - Part 1: Global explanation - which features does the model use?
# Decision trees give "impurity importance": how much each feature reduced
# the impurity (gini) across all the splits it was used in.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from xai_data import load_and_train

model, X_train, X_test, y_train, y_test = load_and_train()
print("Model test accuracy:", round(model.score(X_test, y_test) * 100, 2), "%")

importance = pd.Series(model.feature_importances_, index=X_train.columns)
importance = importance.sort_values(ascending=False)

print("\nImpurity-based feature importance:")
print(importance.round(3).to_string())

used = importance[importance > 0]
print("\nFeatures used by the tree:", len(used), "of", len(importance))
print("Top 3 features explain", round(importance.head(3).sum() * 100, 1), "% of the splits")

importance.sort_values().plot(kind="barh", color="steelblue")
plt.title("Global Feature Importance (impurity based)")
plt.xlabel("Importance")
plt.savefig("Lab_16 (Unit 7)/outputs/global_importance.png", dpi=120, bbox_inches="tight")
plt.close()
print("\nSaved outputs/global_importance.png")
