"""
A* Search

Expands the node in the frontier with the lowest f(n) = g(n) + h(n),
where g(n) is the actual cost from start to n, and h(n) is the
heuristic estimate from n to goal. Guarantees the shortest path
as long as the heuristic is admissible (never overestimates).
"""

import heapq


def a_star_search(graph, heuristic, start, goal):
    """
    Parameters:
        graph (dict): adjacency list (unit edge cost assumed)
        heuristic (dict): node -> estimated distance to goal
        start (str): starting node
        goal (str): target node

    Returns:
        path (list or None): sequence of nodes from start to goal
        total_cost (int or None): g(n) of the goal node (path length)
        nodes_explored (int): number of nodes popped from the frontier
    """
    if start not in graph or goal not in graph:
        raise ValueError("Start or goal node not present in the graph.")

    # Priority queue entries: (f_value, g_value, node, path_so_far)
    frontier = [(heuristic[start], 0, start, [start])]
    visited = set()
    nodes_explored = 0

    while frontier:
        f_value, g_value, current_node, path = heapq.heappop(frontier)

        if current_node in visited:
            continue

        visited.add(current_node)
        nodes_explored += 1

        if current_node == goal:
            return path, g_value, nodes_explored

        for neighbour in graph.get(current_node, []):
            if neighbour not in visited:
                new_g = g_value + 1  # unit edge cost
                new_f = new_g + heuristic[neighbour]
                new_path = path + [neighbour]
                heapq.heappush(frontier, (new_f, new_g, neighbour, new_path))

    return None, None, nodes_explored


def main():
    """Run A* Search on the sample graph."""
    try:
        graph = {
            "A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
            "D": ["B"], "E": ["B", "F"], "F": ["C", "E", "G"], "G": ["F"],
        }
        heuristic = {"A": 3, "B": 3, "C": 2, "D": 4, "E": 2, "F": 1, "G": 0}

        start_node, goal_node = "A", "G"
        path, total_cost, nodes_explored = a_star_search(graph, heuristic, start_node, goal_node)

        if path is None:
            print(f"No path found between {start_node} and {goal_node}.")
            return

        print("--- A* Search Result ---\n")
        print(f"Path found : {' -> '.join(path)}")

        print("\n--- Performance Summary ---")
        print(f"Path length (cost) : {total_cost} edges")
        print(f"Nodes explored     : {nodes_explored}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()