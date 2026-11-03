# Lab 15 - Part 3: Linear Regression with a PyTorch training loop
# Task: predict a student's exam score from hours studied and attendance.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import torch.nn as nn

from student_data import load_split

torch.manual_seed(42)

d = load_split()
X_train = torch.tensor(d["X_train"])
X_test = torch.tensor(d["X_test"])
y_train = torch.tensor(d["y_train"])
y_test = torch.tensor(d["y_test"])
print("Training rows:", len(X_train), "| Testing rows:", len(X_test))

# ---- model, loss and optimizer ----
model = nn.Linear(2, 1)                 # score = w1*hours + w2*attendance + b
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

# ---- training loop ----
epochs = 200
losses = []
print("\nEpoch    Loss")
for epoch in range(epochs):
    prediction = model(X_train)             # 1. forward pass
    loss = loss_fn(prediction, y_train)     # 2. compute loss
    optimizer.zero_grad()                   # 3. clear old gradients
    loss.backward()                         # 4. compute new gradients
    optimizer.step()                        # 5. update weights

    losses.append(loss.item())
    if epoch == 0 or (epoch + 1) % 20 == 0:
        print(f"{epoch + 1:5d}  {loss.item():9.4f}")

# ---- what did the model learn? ----
w = model.weight.detach().numpy()[0]
b = model.bias.item()
mean, std = d["mean"], d["std"]

# convert weights back from scaled features to the original units
w_hours = w[0] / std[0]
w_attendance = w[1] / std[1]
intercept = b - (w[0] * mean[0] / std[0] + w[1] * mean[1] / std[1])

print("\nLearned rule (original units):")
print(f"  score = {intercept:.2f} + {w_hours:.2f} * hours + {w_attendance:.3f} * attendance")
print("True rule used to make the data:")
print("  score = 20.00 + 5.00 * hours + 0.300 * attendance")

# ---- model evaluation on the test set ----
model.eval()
with torch.no_grad():
    y_pred = model(X_test)

mse = loss_fn(y_pred, y_test).item()
mae = (y_pred - y_test).abs().mean().item()
ss_res = ((y_test - y_pred) ** 2).sum().item()
ss_tot = ((y_test - y_test.mean()) ** 2).sum().item()
r2 = 1 - ss_res / ss_tot

print("\nTest set evaluation:")
print(f"  MSE  = {mse:.3f}")
print(f"  RMSE = {mse ** 0.5:.3f}  (average error in marks)")
print(f"  MAE  = {mae:.3f}")
print(f"  R2   = {r2:.4f}")

# ---- predict for a new student ----
new_student = torch.tensor([[6.0, 80.0]])               # 6 hours, 80% attendance
new_scaled = (new_student - torch.tensor(mean)) / torch.tensor(std)
with torch.no_grad():
    new_score = model(new_scaled).item()
print(f"\nStudent with 6 hours and 80% attendance -> predicted score {new_score:.1f}")

# ---- plots ----
plt.plot(losses)
plt.yscale("log")
plt.xlabel("Epoch")
plt.ylabel("Training loss (MSE, log scale)")
plt.title("Training loss curve")
plt.savefig("Lab_15 (Unit 6)/outputs/loss_curve.png", dpi=120, bbox_inches="tight")
plt.close()

plt.scatter(y_test.numpy(), y_pred.numpy(), color="steelblue")
low, high = float(y_test.min()), float(y_test.max())
plt.plot([low, high], [low, high], "r--", label="perfect prediction")
plt.xlabel("Actual score")
plt.ylabel("Predicted score")
plt.title("Predicted vs actual (test set)")
plt.legend()
plt.savefig("Lab_15 (Unit 6)/outputs/predicted_vs_actual.png", dpi=120, bbox_inches="tight")
plt.close()

torch.save(model.state_dict(), "models/linear_regression.pt")
print("\nModel saved to ../models/linear_regression.pt")
print("Plots saved to outputs/")
