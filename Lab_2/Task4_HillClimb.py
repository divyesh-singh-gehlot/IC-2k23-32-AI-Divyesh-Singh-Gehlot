"""
Hill Climbing Search

At each step, moves to the neighbour with the lowest heuristic value
(closest estimated distance to goal). Stops when the goal is reached
or when no neighbour improves on the current node (local optimum) —
this is "Simple Hill Climbing" and does NOT backtrack.
"""


def hill_climbing(graph, heuristic, start, goal):
    """
    Parameters:
        graph (dict): adjacency list
        heuristic (dict): node -> estimated distance to goal
        start (str): starting node
        goal (str): target node

    Returns:
        path (list): sequence of nodes visited (may not reach goal)
        reached_goal (bool): whether the goal was actually reached
        nodes_explored (int): number of nodes visited
    """
    if start not in graph or goal not in graph:
        raise ValueError("Start or goal node not present in the graph.")

    current_node = start
    path = [current_node]
    nodes_explored = 1

    while current_node != goal:
        neighbours = graph.get(current_node, [])

        if not neighbours:
            break  # Dead end, no way forward

        # Pick the neighbour with the lowest heuristic value
        best_neighbour = min(neighbours, key=lambda n: heuristic[n])

        # Stop if no neighbour improves on the current node (local optimum)
        if heuristic[best_neighbour] >= heuristic[current_node]:
            break

        current_node = best_neighbour
        path.append(current_node)
        nodes_explored += 1

    return path, current_node == goal, nodes_explored


def main():
    """Run Hill Climbing on the sample graph."""
    try:
        graph = {
            "A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
            "D": ["B"], "E": ["B", "F"], "F": ["C", "E", "G"], "G": ["F"],
        }
        heuristic = {"A": 3, "B": 3, "C": 2, "D": 4, "E": 2, "F": 1, "G": 0}

        start_node, goal_node = "A", "G"
        path, reached_goal, nodes_explored = hill_climbing(graph, heuristic, start_node, goal_node)

        print("--- Hill Climbing Result ---\n")
        print(f"Path taken   : {' -> '.join(path)}")
        print(f"Goal reached : {reached_goal}")

        print("\n--- Performance Summary ---")
        print(f"Path length     : {len(path) - 1} edges")
        print(f"Nodes explored  : {nodes_explored}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()