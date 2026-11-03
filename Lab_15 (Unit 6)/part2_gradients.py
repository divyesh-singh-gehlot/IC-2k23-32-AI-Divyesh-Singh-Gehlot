# Lab 15 - Part 2: Gradient Computation (autograd)
# PyTorch records every operation and can compute derivatives with backward().

import torch

# ---- 1. one variable: y = x^2 + 3x + 1, so dy/dx = 2x + 3 ----
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x + 1
y.backward()
print("1. y = x^2 + 3x + 1 at x = 2")
print("   y =", y.item())
print("   dy/dx from PyTorch =", x.grad.item())
print("   dy/dx by hand (2x + 3) =", 2 * 2 + 3)

# ---- 2. a tiny model: prediction = w * x + b, loss = (prediction - target)^2 ----
w = torch.tensor(1.0, requires_grad=True)
b = torch.tensor(0.5, requires_grad=True)
x_in = 3.0
target = 10.0

prediction = w * x_in + b
loss = (prediction - target) ** 2
loss.backward()

print("\n2. Gradients of the loss")
print("   prediction =", prediction.item(), "| loss =", loss.item())
print("   dloss/dw from PyTorch =", w.grad.item())
print("   dloss/db from PyTorch =", b.grad.item())

# check with the formulas we get from calculus
manual_dw = 2 * (prediction.item() - target) * x_in
manual_db = 2 * (prediction.item() - target)
print("   dloss/dw by hand      =", manual_dw)
print("   dloss/db by hand      =", manual_db)

# ---- 3. gradients add up unless we reset them ----
z = torch.tensor(1.0, requires_grad=True)
print("\n3. Gradients accumulate (out = 5 * z, so the gradient is 5 each time)")
for i in range(3):
    out = z * 5
    out.backward()
    print(f"   after backward() call {i + 1}: z.grad = {z.grad.item()}")
z.grad.zero_()
print("   after zero_(): z.grad =", z.grad.item())

# ---- 4. one gradient descent step by hand ----
learning_rate = 0.01
with torch.no_grad():              # we do not want to track this update
    w_new = w - learning_rate * w.grad
    b_new = b - learning_rate * b.grad
print("\n4. One gradient descent step (lr = 0.01)")
print("   w:", w.item(), "->", round(w_new.item(), 4))
print("   b:", b.item(), "->", round(b_new.item(), 4))

new_loss = (w_new * x_in + b_new - target) ** 2
print("   loss before:", round(loss.item(), 4), "| loss after:", round(new_loss.item(), 4))

# ---- 5. turning tracking off ----
with torch.no_grad():
    result = w * 2
print("\n5. Inside no_grad(), requires_grad =", result.requires_grad)
