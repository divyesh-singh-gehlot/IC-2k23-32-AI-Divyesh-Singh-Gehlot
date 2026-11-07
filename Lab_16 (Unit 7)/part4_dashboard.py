# Lab 7 - Part 4: Explainable AI Dashboard
# Puts the global explanations, the local explanation and the model
# performance together on one page.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

from xai_data import load_and_train

STUDENT = 0     # which test student to explain

model, X_train, X_test, y_train, y_test = load_and_train()
y_pred = model.predict(X_test)
names = list(X_test.columns)

accuracy = model.score(X_test, y_test)
baseline = max(y_test.mean(), 1 - y_test.mean())

# ---- numbers needed for the panels ----
impurity = pd.Series(model.feature_importances_, index=names).sort_values()
perm = permutation_importance(model, X_test, y_test, n_repeats=30, random_state=42)
perm_series = pd.Series(perm.importances_mean, index=names).sort_values()

student = X_test.iloc[[STUDENT]]
probability = model.predict_proba(student)[0][1]
prediction = "Placed" if model.predict(student)[0] == 1 else "Not placed"
actual = "Placed" if y_test.iloc[STUDENT] == 1 else "Not placed"

# what-if: effect of -10 / +10 marks on the three main features
what_if = {}
for feature in ["degree_p", "etest_p", "hsc_p"]:
    for change in [-10, 10]:
        changed = student.copy()
        changed[feature] = min(max(changed[feature].iloc[0] + change, 0), 100)
        what_if[f"{feature} {change:+d}"] = (model.predict_proba(changed)[0][1] - probability) * 100

# decision path as text
path = model.decision_path(student)
nodes = path.indices[path.indptr[0]:path.indptr[1]]
leaf = model.apply(student)[0]
rules = []
for node in nodes:
    if node == leaf:
        continue
    feature = model.tree_.feature[node]
    threshold = model.tree_.threshold[node]
    value = student.iloc[0, feature]
    sign = "<=" if value <= threshold else ">"
    rules.append(f"{names[feature]} = {value:.1f} {sign} {threshold:.1f}")

# ---- draw the dashboard ----
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Explainable AI Dashboard - Student Placement Prediction", fontsize=18, fontweight="bold")

# 1. global importance
axes[0, 0].barh(impurity.index, impurity.values, color="steelblue")
axes[0, 0].set_title("Global: feature importance (impurity)")

# 2. permutation importance
axes[0, 1].barh(perm_series.index, perm_series.values, color="darkorange")
axes[0, 1].axvline(0, color="black", linewidth=0.8)
axes[0, 1].set_title("Global: permutation importance")
axes[0, 1].set_xlabel("Drop in accuracy when shuffled")

# 3. confusion matrix
ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred),
                       display_labels=["Not placed", "Placed"]).plot(ax=axes[0, 2], cmap="Blues", colorbar=False)
axes[0, 2].set_title("Model performance: confusion matrix")

# 4. model summary text
axes[1, 0].axis("off")
summary = (
    "MODEL SUMMARY\n\n"
    f"Model            : Decision Tree (depth {model.get_depth()})\n"
    f"Test accuracy    : {accuracy * 100:.1f} %\n"
    f"Baseline accuracy: {baseline * 100:.1f} %\n"
    f"(always predicting the majority class)\n\n"
    f"STUDENT {STUDENT} (local explanation)\n\n"
    f"Actual    : {actual}\n"
    f"Predicted : {prediction}\n"
    f"P(placed) : {probability * 100:.1f} %"
)
axes[1, 0].text(0.02, 0.95, summary, va="top", fontsize=12, family="monospace")

# 5. what-if bars
values = list(what_if.values())
colors = ["seagreen" if v >= 0 else "firebrick" for v in values]
axes[1, 1].barh(list(what_if.keys()), values, color=colors)
axes[1, 1].axvline(0, color="black", linewidth=0.8)
for i, v in enumerate(values):              # write the number next to each bar
    axes[1, 1].text(v, i, f" {v:+.1f}", va="center", ha="left" if v >= 0 else "right")
axes[1, 1].set_xlim(min(-10, min(values) - 12), max(10, max(values) + 12))
axes[1, 1].set_title("Local: what if this student scored 10 less / 10 more?")
axes[1, 1].set_xlabel("Change in P(placed) in percentage points")

# 6. decision path text
axes[1, 2].axis("off")
axes[1, 2].text(0.02, 0.95, "DECISION PATH\n(rules this student followed)\n\n" + "\n".join(rules) +
                f"\n\n-> prediction: {prediction}", va="top", fontsize=12, family="monospace")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("Lab_16 (Unit 7)/outputs/xai_dashboard.png", dpi=110, bbox_inches="tight")
plt.close()
print("Dashboard saved to outputs/xai_dashboard.png")
print(f"Test accuracy {accuracy * 100:.1f} % vs baseline {baseline * 100:.1f} %")
