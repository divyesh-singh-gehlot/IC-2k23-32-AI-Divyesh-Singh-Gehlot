# Lab 7 - Part 3: Local explanation - why did the model predict this for ONE student?
#   (a) the decision path (the exact rules this student followed)
#   (b) what-if analysis (how the prediction changes if a feature changes)

import sys

from xai_data import load_and_train

model, X_train, X_test, y_train, y_test = load_and_train()

# pick a student from the test set (change the number, or give it on the command line)
position = int(sys.argv[1]) if len(sys.argv) > 1 else 0
student = X_test.iloc[[position]]
actual = y_test.iloc[position]

probability = model.predict_proba(student)[0]
prediction = model.predict(student)[0]
names = list(X_test.columns)

print(f"Test student number {position}")
print("Actual status   :", "Placed" if actual == 1 else "Not placed")
print("Predicted status:", "Placed" if prediction == 1 else "Not placed")
print(f"Probability of being placed: {probability[1] * 100:.1f} %")

print("\nStudent details:")
print(student.T.rename(columns={student.index[0]: "value"}).to_string())

# ---- (a) decision path ----
print("\nRules followed by the tree:")
path = model.decision_path(student)
nodes = path.indices[path.indptr[0]:path.indptr[1]]
leaf = model.apply(student)[0]

for node in nodes:
    if node == leaf:
        continue
    feature = model.tree_.feature[node]
    threshold = model.tree_.threshold[node]
    value = student.iloc[0, feature]
    sign = "<=" if value <= threshold else ">"
    print(f"  {names[feature]} = {value:.2f} {sign} {threshold:.2f}")
print("  -> reaches a leaf and predicts", "Placed" if prediction == 1 else "Not placed")

# ---- (b) what-if analysis ----
print("\nWhat-if: change one important feature and see the probability")
print("Feature        Change    New probability   Difference")
top_features = ["degree_p", "etest_p", "hsc_p"]
for feature in top_features:
    for change in [-10, 10]:
        changed = student.copy()
        changed[feature] = min(max(changed[feature].iloc[0] + change, 0), 100)
        new_probability = model.predict_proba(changed)[0][1]
        difference = (new_probability - probability[1]) * 100
        print(f"{feature:12s}  {change:+4d}      {new_probability * 100:6.1f} %        {difference:+6.1f} %")
