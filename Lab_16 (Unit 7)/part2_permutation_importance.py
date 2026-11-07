# Lab 7 - Part 2: Permutation importance (works for ANY model)
# Idea: shuffle one feature in the test data. If accuracy drops a lot,
# the model relied on that feature. Repeat many times to get an average.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import permutation_importance

from xai_data import load_and_train

model, X_train, X_test, y_train, y_test = load_and_train()

result = permutation_importance(model, X_test, y_test, n_repeats=30,
                                random_state=42, scoring="accuracy")

perm = pd.DataFrame({
    "permutation_mean": result.importances_mean,
    "permutation_std": result.importances_std,
    "impurity": model.feature_importances_,
}, index=X_test.columns).sort_values("permutation_mean", ascending=False)

print("Drop in test accuracy when a feature is shuffled (30 repeats):\n")
print(perm.round(3).to_string())

print("\nRank by impurity importance   :", list(perm.sort_values("impurity", ascending=False).index[:3]))
print("Rank by permutation importance:", list(perm.index[:3]))

useless = list(perm[perm["permutation_mean"] <= 0].index)
print("\nShuffling these features did not hurt accuracy:", useless)

perm_sorted = perm.sort_values("permutation_mean")
plt.barh(perm_sorted.index, perm_sorted["permutation_mean"],
         xerr=perm_sorted["permutation_std"], color="darkorange")
plt.axvline(0, color="black", linewidth=0.8)
plt.title("Permutation Importance (drop in accuracy)")
plt.xlabel("Mean accuracy drop")
plt.savefig("Lab_16 (Unit 7)/outputs/permutation_importance.png", dpi=120, bbox_inches="tight")
plt.close()
print("\nSaved outputs/permutation_importance.png")
