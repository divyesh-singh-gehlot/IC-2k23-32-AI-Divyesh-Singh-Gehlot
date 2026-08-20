# 2. Missionaries and Cannibals Problem

## 2.1 Aim / Problem Statement

### Aim
To implement the **Missionaries and Cannibals Problem** using Breadth-First Search (BFS) over an explicit state space, and find a safe sequence of boat crossings.

### Problem Statement
3 missionaries and 3 cannibals must cross a river using a boat that holds at most 2 people. On neither bank may cannibals ever outnumber missionaries (if any missionaries are present). Find a sequence of crossings that gets everyone across safely.

## 2.2 Algorithm

**State representation:** `(missionaries_left, cannibals_left, boat_position)`, where `boat_position = 1` means the boat is on the left bank, `0` means the right bank.

- **Initial state:** `(3, 3, 1)`
- **Goal state:** `(0, 0, 0)`
- **Production rules (operators):** move `(1,0)`, `(2,0)`, `(0,1)`, `(0,2)`, or `(1,1)` people across the river, applied only `IF` the resulting state keeps missionaries safe on both banks.

### Pseudocode
```text
START
Initialize start_state = (3, 3, boat=Left)
Initialize queue with start_state, mark visited

WHILE queue is not empty:
    current = dequeue()
    IF current is goal state:
        RETURN path to current

    FOR each possible move (m, c) in {(1,0),(2,0),(0,1),(0,2),(1,1)}:
        new_state = apply move to current
        IF new_state is valid AND not visited:
            mark visited
            enqueue new_state with parent = current

RETURN no solution
END
```

## 2.3 Implementation

```python
"""
Missionaries and Cannibals Problem
Solved using Breadth-First Search (BFS)
"""

from collections import deque


class State:
    """Represents a state in the search space."""

    def __init__(self, missionaries_left, cannibals_left, boat_left, parent=None, move=None):
        self.m_left = missionaries_left
        self.c_left = cannibals_left
        self.boat_left = boat_left
        self.parent = parent
        self.move = move  # (missionaries_moved, cannibals_moved)

    def is_valid(self):
        """Check if a state is valid (no missionaries get eaten)."""
        if self.m_left < 0 or self.c_left < 0:
            return False
        if self.m_left > 3 or self.c_left > 3:
            return False

        m_right = 3 - self.m_left
        c_right = 3 - self.c_left

        if self.m_left > 0 and self.m_left < self.c_left:
            return False
        if m_right > 0 and m_right < c_right:
            return False

        return True

    def is_goal(self):
        return self.m_left == 0 and self.c_left == 0 and self.boat_left == 0

    def __eq__(self, other):
        return (self.m_left == other.m_left and
                self.c_left == other.c_left and
                self.boat_left == other.boat_left)

    def __hash__(self):
        return hash((self.m_left, self.c_left, self.boat_left))

    def __repr__(self):
        return f"(M_left={self.m_left}, C_left={self.c_left}, Boat={'Left' if self.boat_left else 'Right'})"


def get_successors(state):
    """Generate all valid successor states from the current state."""
    successors = []
    possible_moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    direction = -1 if state.boat_left == 1 else 1

    for m, c in possible_moves:
        new_m_left = state.m_left + direction * m
        new_c_left = state.c_left + direction * c
        new_boat_left = 0 if state.boat_left == 1 else 1

        new_state = State(new_m_left, new_c_left, new_boat_left, parent=state, move=(m, c))

        if new_state.is_valid():
            successors.append(new_state)

    return successors


def bfs_solve():
    """Solve the problem using Breadth-First Search."""
    start_state = State(3, 3, 1)
    visited = set()
    queue = deque([start_state])
    visited.add(start_state)

    nodes_explored = 0

    while queue:
        current_state = queue.popleft()
        nodes_explored += 1

        if current_state.is_goal():
            return current_state, nodes_explored

        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                queue.append(successor)

    return None, nodes_explored


def reconstruct_path(goal_state):
    """Trace back from goal state to start state to get the solution path."""
    path = []
    state = goal_state
    while state is not None:
        path.append(state)
        state = state.parent
    path.reverse()
    return path


def print_solution(path):
    """Print the solution in a readable step-by-step format."""
    print("\n--- Solution Path ---\n")
    for i, state in enumerate(path):
        bank = "Left" if state.boat_left else "Right"
        if state.move is not None:
            m, c = state.move
            print(f"Step {i}: Move {m} missionary(ies) and {c} cannibal(s) -> boat now on {bank} bank")
        else:
            print(f"Step {i}: Initial state")
        print(f"         {state}\n")


def main():
    """Run the Missionaries and Cannibals Problem."""
    try:
        goal_state, nodes_explored = bfs_solve()

        if goal_state is None:
            print("No solution found.")
            return

        path = reconstruct_path(goal_state)
        print_solution(path)

        print("--- Performance Summary ---")
        print(f"Nodes explored : {nodes_explored}")
        print(f"Solution length: {len(path) - 1} moves")

    except Exception as e:
        print(f"An error occurred while solving the problem: {e}")


if __name__ == "__main__":
    main()
```

## 2.4 Results / Output

```text
--- Solution Path ---

Step 0: Initial state
         (M_left=3, C_left=3, Boat=Left)

Step 1: Move 0 missionary(ies) and 2 cannibal(s) -> boat now on Right bank
         (M_left=3, C_left=1, Boat=Right)

Step 2: Move 0 missionary(ies) and 1 cannibal(s) -> boat now on Left bank
         (M_left=3, C_left=2, Boat=Left)

Step 3: Move 0 missionary(ies) and 2 cannibal(s) -> boat now on Right bank
         (M_left=3, C_left=0, Boat=Right)

Step 4: Move 0 missionary(ies) and 1 cannibal(s) -> boat now on Left bank
         (M_left=3, C_left=1, Boat=Left)

Step 5: Move 2 missionary(ies) and 0 cannibal(s) -> boat now on Right bank
         (M_left=1, C_left=1, Boat=Right)

Step 6: Move 1 missionary(ies) and 1 cannibal(s) -> boat now on Left bank
         (M_left=2, C_left=2, Boat=Left)

Step 7: Move 2 missionary(ies) and 0 cannibal(s) -> boat now on Right bank
         (M_left=0, C_left=2, Boat=Right)

Step 8: Move 0 missionary(ies) and 1 cannibal(s) -> boat now on Left bank
         (M_left=0, C_left=3, Boat=Left)

Step 9: Move 0 missionary(ies) and 2 cannibal(s) -> boat now on Right bank
         (M_left=0, C_left=1, Boat=Right)

Step 10: Move 0 missionary(ies) and 1 cannibal(s) -> boat now on Left bank
         (M_left=0, C_left=2, Boat=Left)

Step 11: Move 0 missionary(ies) and 2 cannibal(s) -> boat now on Right bank
         (M_left=0, C_left=0, Boat=Right)

--- Performance Summary ---
Nodes explored : 15
Solution length: 11 moves
```

**Result (in words):** send 2 cannibals across → 1 cannibal back → 2 cannibals across → 1 cannibal back → 2 missionaries across → 1 missionary + 1 cannibal back → 2 missionaries across → 1 cannibal back → 2 cannibals across → 1 cannibal back → last 2 cannibals across. Everyone crosses safely in 11 moves.

## 2.5 Performance Analysis

| Metric | Result |
|---|---|
| Accuracy / Precision / Recall / F1 / Confusion Matrix | Not Applicable (search problem, not classification) |
| Nodes Explored | 15 |
| Solution Length (moves) | 11 |
| Search Strategy | BFS — guarantees shortest solution (optimal for uniform-cost moves) |
| Time Complexity | O(b^d) where b = branching factor, d = solution depth |
| Space Complexity | O(b^d) (BFS stores all visited/frontier states) |

## 2.6 Screenshots
![Console Output](Output/Task2.png)