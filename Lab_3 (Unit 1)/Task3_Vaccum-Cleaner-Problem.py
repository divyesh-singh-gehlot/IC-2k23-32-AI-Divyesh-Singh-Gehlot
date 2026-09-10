"""
Vacuum Cleaner Problem
Solved using a Production Rule System (Simple Reflex Agent)

State representation: (location, status_A, status_B)
location: 'A' or 'B' (which room the vacuum is currently in)
status_A, status_B: 'Dirty' or 'Clean'
Goal: both rooms Clean
"""


class State:
    """Represents a state of the vacuum world."""

    def __init__(self, location, status_a, status_b):
        self.location = location
        self.status_a = status_a
        self.status_b = status_b

    def is_goal(self):
        """Goal state: both rooms are clean."""
        return self.status_a == "Clean" and self.status_b == "Clean"

    def current_status(self):
        """Return the dirt status of the room the vacuum is currently in."""
        return self.status_a if self.location == "A" else self.status_b

    def __repr__(self):
        return f"(Location={self.location}, A={self.status_a}, B={self.status_b})"


def apply_rule(state):
    """
    Production rules for the vacuum agent:
    RULE 1: IF current room is Dirty      THEN Suck
    RULE 2: IF current room is Clean AND at A THEN Move Right
    RULE 3: IF current room is Clean AND at B THEN Move Left
    """
    if state.current_status() == "Dirty":
        # RULE 1: Suck
        if state.location == "A":
            return State("A", "Clean", state.status_b), "Suck (clean room A)"
        else:
            return State("B", state.status_a, "Clean"), "Suck (clean room B)"

    elif state.location == "A":
        # RULE 2: Move Right
        return State("B", state.status_a, state.status_b), "Move Right (A -> B)"

    else:
        # RULE 3: Move Left
        return State("A", state.status_a, state.status_b), "Move Left (B -> A)"


def solve_vacuum(start_state, max_steps=20):
    """Run the production system until the goal state is reached."""
    trace = [(start_state, "Initial state")]
    current_state = start_state
    steps_taken = 0

    while not current_state.is_goal() and steps_taken < max_steps:
        next_state, action = apply_rule(current_state)
        trace.append((next_state, action))
        current_state = next_state
        steps_taken += 1

    return trace, steps_taken, current_state.is_goal()


def print_solution(trace):
    """Print the step-by-step trace of states and actions."""
    print("\n--- Solution Path ---\n")
    for i, (state, action) in enumerate(trace):
        print(f"Step {i}: {action}")
        print(f"         {state}\n")


def main():
    try:
        # Example: Room A is dirty, Room B is dirty, vacuum starts in A
        start_state = State("A", "Dirty", "Dirty")

        trace, steps_taken, goal_reached = solve_vacuum(start_state)

        print_solution(trace)

        print("--- Performance Summary ---")
        print(f"Goal reached   : {goal_reached}")
        print(f"Steps taken    : {steps_taken}")

    except Exception as e:
        print(f"An error occurred while solving the problem: {e}")


if __name__ == "__main__":
    main()