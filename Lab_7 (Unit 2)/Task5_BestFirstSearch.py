"""
Greedy Best-First Search

Expands the node in the frontier with the lowest heuristic value h(n),
ignoring the cost already spent to reach it (unlike A*). Faster than
A* in practice but not guaranteed to find the shortest path.
"""

import heapq


def best_first_search(graph, heuristic, start, goal):
    """
    Parameters:
        graph (dict): adjacency list
        heuristic (dict): node -> estimated distance to goal
        start (str): starting node
        goal (str): target node

    Returns:
        path (list or None): sequence of nodes from start to goal
        nodes_explored (int): number of nodes popped from the frontier
    """
    if start not in graph or goal not in graph:
        raise ValueError("Start or goal node not present in the graph.")

    # Priority queue entries: (heuristic_value, node, path_so_far)
    frontier = [(heuristic[start], start, [start])]
    visited = set()
    nodes_explored = 0

    while frontier:
        h_value, current_node, path = heapq.heappop(frontier)

        if current_node in visited:
            continue

        visited.add(current_node)
        nodes_explored += 1

        if current_node == goal:
            return path, nodes_explored

        for neighbour in graph.get(current_node, []):
            if neighbour not in visited:
                new_path = path + [neighbour]
                heapq.heappush(frontier, (heuristic[neighbour], neighbour, new_path))

    return None, nodes_explored


def main():
    """Run Greedy Best-First Search on the sample graph."""
    try:
        graph = {
            "A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
            "D": ["B"], "E": ["B", "F"], "F": ["C", "E", "G"], "G": ["F"],
        }
        heuristic = {"A": 3, "B": 3, "C": 2, "D": 4, "E": 2, "F": 1, "G": 0}

        start_node, goal_node = "A", "G"
        path, nodes_explored = best_first_search(graph, heuristic, start_node, goal_node)

        if path is None:
            print(f"No path found between {start_node} and {goal_node}.")
            return

        print("--- Best-First Search Result ---\n")
        print(f"Path found : {' -> '.join(path)}")

        print("\n--- Performance Summary ---")
        print(f"Path length     : {len(path) - 1} edges")
        print(f"Nodes explored  : {nodes_explored}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()