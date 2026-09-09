# 💧 Water Jug Problem

## 1. Aim / Problem Statement

### Aim

To implement the **Water Jug Problem** in Python using an algorithmic approach and determine a sequence of operations that measures an exact target amount of water using two jugs of given capacities.

### Problem Statement

Given two water jugs with capacities `X` litres and `Y` litres, initially both empty, measure exactly `T` litres of water using the following operations:

1. Fill a jug completely.
2. Empty a jug completely.
3. Pour water from one jug into the other until either:

   * The source jug becomes empty, or
   * The destination jug becomes full.

### Example

For:

```text
First Jug  = 5L
Second Jug = 7L
Target     = 4L
```

The program finds a sequence of operations that results in exactly **4 litres** of water in one of the jugs.

---

# 2. Algorithm

The program uses a **state-based iterative approach**.

A state is represented as:

```text
(a, b)
```

where:

* `a` = amount of water in the first jug.
* `b` = amount of water in the second jug.

Initially:

```text
(a, b) = (0, 0)
```

### Steps

1. Start with both jugs empty.
2. If the first jug is empty, fill it completely.
3. If the second jug is full, empty it.
4. Otherwise, pour water from the first jug into the second jug.
5. Calculate the amount that can be transferred using:

```python
amount = min(first_jug, second_capacity - second_jug)
```

6. Update the state of both jugs.
7. Continue until either jug contains the target amount.
8. Display every operation and the corresponding state.

### Pseudocode

```text
START

Set first_jug = 0
Set second_jug = 0

WHILE neither jug contains target:

    IF first_jug is empty:
        Fill first jug

    ELSE IF second_jug is full:
        Empty second jug

    ELSE:
        Pour water from first jug to second jug

    Display current state

Display "Target reached"

END
```

---

# 3. Implementation

The implementation follows modular programming principles and uses meaningful function and variable names.

```python
def water_jug(first_capacity, second_capacity, target):
    """
    Solve the Water Jug Problem using two jugs.

    Parameters:
        first_capacity (int): Capacity of the first jug.
        second_capacity (int): Capacity of the second jug.
        target (int): Required amount of water.

    Returns:
        None
    """

    first_jug = 0
    second_jug = 0

    while first_jug != target and second_jug != target:

        # Fill the first jug if it is empty.
        if first_jug == 0:
            first_jug = first_capacity
            print(f"Fill {first_capacity}L jug")

        # Empty the second jug if it is full.
        elif second_jug == second_capacity:
            second_jug = 0
            print(f"Empty {second_capacity}L jug")

        # Pour water from the first jug into the second jug.
        else:
            transferable_amount = min(
                first_jug,
                second_capacity - second_jug
            )

            first_jug -= transferable_amount
            second_jug += transferable_amount

            print(
                f"Pour {first_capacity}L -> "
                f"{second_capacity}L jug"
            )

        print(f"State: ({first_jug}, {second_jug})")
        print()


def main():
    """Run the Water Jug Problem."""

    first_capacity = 5
    second_capacity = 7
    target = 4

    water_jug(first_capacity, second_capacity, target)


if __name__ == "__main__":
    main()
```

---

# 4. Results / Output

### Input

```text
First Jug Capacity  : 5L
Second Jug Capacity : 7L
Target              : 4L
```

### Sample Output

```text
Fill 5L jug
State: (5, 0)

Pour 5L -> 7L jug
State: (0, 5)

Fill 5L jug
State: (5, 5)

Pour 5L -> 7L jug
State: (3, 7)

Empty 7L jug
State: (3, 0)

Pour 5L -> 7L jug
State: (0, 3)

Fill 5L jug
State: (5, 3)

Pour 5L -> 7L jug
State: (1, 7)

Empty 7L jug
State: (1, 0)

Pour 5L -> 7L jug
State: (0, 1)

Fill 5L jug
State: (5, 1)

Pour 5L -> 7L jug
State: (0, 6)

Fill 5L jug
State: (5, 6)

Pour 5L -> 7L jug
State: (4, 7)

Target reached!
```

### Result

The target amount of **4 litres** is successfully obtained in the first jug.

Final state:

```text
(4, 7)
```

---

# 5. Performance Analysis

Since this project implements an **algorithmic problem** rather than a machine-learning classification model, classification metrics are not applicable.

| Metric              | Result            |
| ------------------- | ----------------- |
| Accuracy            | Not Applicable    |
| Precision           | Not Applicable    |
| Recall              | Not Applicable    |
| F1-Score            | Not Applicable    |
| Confusion Matrix    | Not Applicable    |
| Model Visualization | Not Applicable    |
| Execution Time      | Depends on system |
| Space Complexity    | O(1)              |
| Time Complexity     | O(N)              |

### Why are ML Metrics Not Applicable?

**Accuracy, Precision, Recall, F1-score, and Confusion Matrix** are primarily used to evaluate classification models.

The Water Jug Problem does not predict class labels. Instead, it performs a sequence of deterministic operations to reach a target state.

Therefore, more relevant performance measures are:

* Number of operations
* Execution time
* Number of states generated
* Time complexity
* Space complexity

### Complexity

Let `N` represent the number of operations required to reach the target.

**Time Complexity:**

```text
O(N)
```

**Space Complexity:**

```text
O(1)
```

Only the current quantities of water in the two jugs are maintained.

---

# 6. Screenshots / Graphs / Visualization

## Console Output

Add a screenshot of your program execution here:

```text
![Console Output](Outputs/Task1.png)
```

### State Visualization

The solution can also be represented as a sequence of states:

```text
(0,0)
  ↓
(5,0)
  ↓
(0,5)
  ↓
(5,5)
  ↓
(3,7)
  ↓
(3,0)
  ↓
(0,3)
  ↓
(5,3)
  ↓
(1,7)
  ↓
(1,0)
  ↓
(0,1)
  ↓
(5,1)
  ↓
(0,6)
  ↓
(5,6)
  ↓
(4,7)
```

The final state contains **4 litres** in the first jug.

### Confusion Matrix

```text
Not Applicable
```

A confusion matrix is used for classification problems and is therefore not relevant to this algorithm.

---

# 7. Input Validation and Exception Handling

The program should validate the input before attempting to solve the problem.

Important conditions include:

* Jug capacities must be positive.
* Target must be non-negative.
* Target cannot be greater than the capacity of both jugs.
* Inputs should be integers.
* A target is possible only when it satisfies the mathematical conditions of the Water Jug Problem.

A robust implementation can use:

```python
def validate_input(first_capacity, second_capacity, target):
    """Validate Water Jug Problem inputs."""

    if not isinstance(first_capacity, int):
        raise TypeError("First jug capacity must be an integer.")

    if not isinstance(second_capacity, int):
        raise TypeError("Second jug capacity must be an integer.")

    if not isinstance(target, int):
        raise TypeError("Target must be an integer.")

    if first_capacity <= 0 or second_capacity <= 0:
        raise ValueError("Jug capacities must be positive.")

    if target < 0:
        raise ValueError("Target cannot be negative.")

    if target > max(first_capacity, second_capacity):
        raise ValueError(
            "Target cannot be greater than both jug capacities."
        )
```

This makes the program more reliable and prevents invalid inputs from causing unexpected behavior.

---

# 8. Coding Standards Followed

The implementation follows the required Python coding practices.

### Modular and Reusable Code

The main logic is placed inside:

```python
water_jug()
```

This allows the function to be reused with different jug capacities and targets.

### Meaningful Names

Descriptive names are used instead of short, unclear variable names:

```python
first_capacity
second_capacity
target
first_jug
second_jug
transferable_amount
```

### Comments and Documentation

Comments explain important operations, and a docstring documents the purpose and parameters of the function.

### Exception Handling

Invalid inputs are checked using:

```python
TypeError
ValueError
```

### PEP-8 Standards

The code follows common PEP-8 practices, including:

* 4-space indentation
* Meaningful `snake_case` names
* Proper spacing
* Function documentation
* Reasonable line lengths
* Separation of program logic into functions

---

# 9. Learning Outcomes

After completing this project, the following concepts were learned:

* Understanding the **Water Jug Problem**.
* Representing a problem using **states**.
* Understanding state transitions.
* Implementing an algorithm using Python.
* Using conditional statements and loops effectively.
* Understanding the use of `min()` for calculating transferable water.
* Learning how to design modular and reusable functions.
* Applying input validation and exception handling.
* Following **PEP-8** coding standards.
* Understanding the difference between algorithmic performance metrics and machine-learning evaluation metrics.
* Understanding **time and space complexity**.
* Learning how a sequence of states can be used to solve a problem systematically.

---

# 10. Conclusion

The Water Jug Problem was successfully implemented in Python using a state-based iterative algorithm.

For jug capacities of **5L and 7L**, the program successfully measures exactly **4L** of water.

The project demonstrates important programming and algorithmic concepts such as **state representation, problem solving, modular programming, input validation, complexity analysis, and clean Python coding practices**.
