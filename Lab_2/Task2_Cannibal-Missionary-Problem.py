"""
Missionaries and Cannibals Problem
Solved using Breadth-First Search (BFS)

State representation: (missionaries_left, cannibals_left, boat_position)
boat_position: 1 = left bank, 0 = right bank
Goal: move all 3 missionaries and 3 cannibals to the right bank
      without cannibals ever outnumbering missionaries on either bank.
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