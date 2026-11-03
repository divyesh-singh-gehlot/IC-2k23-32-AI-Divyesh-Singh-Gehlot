# Lab 15 - Part 1: Tensor Manipulation

import numpy as np
import torch

print("PyTorch version:", torch.__version__)

# ---- 1. creating tensors ----
a = torch.tensor([1, 2, 3, 4])
b = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
zeros = torch.zeros(2, 3)
ones = torch.ones(2, 3)
seq = torch.arange(0, 10, 2)

torch.manual_seed(42)          # same random numbers every run
rand = torch.rand(2, 3)

print("\n1. Creating tensors")
print("a    =", a)
print("b    =\n", b)
print("zeros=\n", zeros)
print("seq  =", seq)
print("rand =\n", rand)

# ---- 2. shape and data type ----
print("\n2. Shape and dtype")
print("b.shape =", b.shape, "| b.dtype =", b.dtype, "| b.ndim =", b.ndim)
print("a.dtype =", a.dtype)
print("a as float =", a.float())

# ---- 3. reshaping ----
x = torch.arange(12)
print("\n3. Reshaping")
print("x         =", x)
print("reshape(3, 4) =\n", x.reshape(3, 4))
print("reshape(2, 2, 3) shape =", x.reshape(2, 2, 3).shape)

# ---- 4. indexing and slicing ----
m = torch.arange(1, 13).reshape(3, 4)
print("\n4. Indexing and slicing")
print("m =\n", m)
print("m[0]      =", m[0])
print("m[1, 2]   =", m[1, 2])
print("m[:, 1]   =", m[:, 1])
print("m[1:, :2] =\n", m[1:, :2])
print("m[m > 6]  =", m[m > 6])

# ---- 5. arithmetic ----
p = torch.tensor([1.0, 2.0, 3.0])
q = torch.tensor([4.0, 5.0, 6.0])
print("\n5. Arithmetic")
print("p + q =", p + q)
print("p * q =", p * q)
print("p ** 2 =", p ** 2)
print("dot product =", torch.dot(p, q))

A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
B = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
print("A @ B (matrix multiplication) =\n", A @ B)

# ---- 6. broadcasting ----
print("\n6. Broadcasting")
print("A + 10 =\n", A + 10)
print("A + [100, 200] =\n", A + torch.tensor([100.0, 200.0]))

# ---- 7. aggregation ----
t = torch.tensor([[3.0, 1.0, 4.0], [1.0, 5.0, 9.0]])
print("\n7. Aggregation")
print("t =\n", t)
print("sum  =", t.sum(), "| mean =", t.mean(), "| max =", t.max())
print("sum along rows (dim=0)   =", t.sum(dim=0))
print("sum along columns (dim=1) =", t.sum(dim=1))
print("argmax =", t.argmax())

# ---- 8. transpose, concatenate, stack ----
print("\n8. Joining tensors")
print("t.T shape =", t.T.shape)
print("cat along rows    =\n", torch.cat([t, t], dim=0))
print("cat along columns =\n", torch.cat([t, t], dim=1))
print("stack shape =", torch.stack([t, t]).shape)

# ---- 9. numpy <-> torch ----
arr = np.array([1.0, 2.0, 3.0])
from_numpy = torch.from_numpy(arr)
back = from_numpy.numpy()
print("\n9. NumPy conversion")
print("numpy -> torch:", from_numpy)
print("torch -> numpy:", back)
