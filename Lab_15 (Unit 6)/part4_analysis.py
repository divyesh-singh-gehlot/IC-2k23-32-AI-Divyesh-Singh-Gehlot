# Lab 15 - Part 4: Analysis
#   (a) PyTorch model vs a traditional ML model (scikit-learn)
#   (b) How the learning rate affects convergence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from student_data import load_split

d = load_split()
X_train, X_test = torch.tensor(d["X_train"]), torch.tensor(d["X_test"])
y_train, y_test = torch.tensor(d["y_train"]), torch.tensor(d["y_test"])


def train(lr, epochs=200):
    torch.manual_seed(42)
    model = nn.Linear(2, 1)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    losses = []
    for epoch in range(epochs):
        loss = loss_fn(model(X_train), y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    return model, losses


# ---------- (a) PyTorch vs scikit-learn ----------
model, losses = train(lr=0.1)
with torch.no_grad():
    torch_pred = model(X_test).numpy()

sk = LinearRegression().fit(d["X_train"], d["y_train"])
sk_pred = sk.predict(d["X_test"])

print("(a) PyTorch vs scikit-learn on the test set")
print("Model                MSE      R2")
print(f"PyTorch (SGD)    {mean_squared_error(d['y_test'], torch_pred):8.3f}  {r2_score(d['y_test'], torch_pred):.4f}")
print(f"scikit-learn     {mean_squared_error(d['y_test'], sk_pred):8.3f}  {r2_score(d['y_test'], sk_pred):.4f}")

print("\nLearned weights (scaled features):")
print("PyTorch     :", model.weight.detach().numpy()[0].round(3), round(model.bias.item(), 3))
print("scikit-learn:", sk.coef_[0].round(3), round(float(sk.intercept_[0]), 3))

# ---------- (b) learning rate and convergence ----------
print("\n(b) Training loss after different numbers of epochs")
print("Learning rate    10 epochs   50 epochs  200 epochs")
plt.figure(figsize=(8, 5))
for lr in [0.001, 0.01, 0.1, 0.9, 1.1]:
    _, loss_history = train(lr)
    print(f"{lr:12}  {loss_history[9]:11.3f} {loss_history[49]:11.3f} {loss_history[199]:11.3g}")
    plt.plot(loss_history, label=f"lr = {lr}")

plt.yscale("log")
plt.xlabel("Epoch")
plt.ylabel("Training loss (log scale)")
plt.title("Effect of the learning rate")
plt.legend()
plt.savefig("Lab_15 (Unit 6)/outputs/learning_rate_comparison.png", dpi=120, bbox_inches="tight")
plt.close()
print("\nSaved outputs/learning_rate_comparison.png")
