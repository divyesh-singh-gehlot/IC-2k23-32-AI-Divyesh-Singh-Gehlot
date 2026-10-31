"""
Depth-First Search (DFS) — Graph Traversal

Explores as far as possible along each branch before backtracking.
Unlike BFS, DFS does NOT guarantee the shortest path — it guarantees
finding *a* path if one exists, using less memory than BFS.
"""


def dfs(graph, start, goal):
    """
    Perform DFS on 'graph' from 'start' to 'goal' using an explicit stack
    (iterative, not recursive — avoids Python's recursion depth limit).

    Parameters:
        graph (dict): adjacency list, e.g. {'A': ['B', 'C'], ...}
        start (str): starting node
        goal (str): target node

    Returns:
        path (list or None): sequence of nodes from start to goal
        nodes_explored (int): number of nodes popped during search
    """
    if start not in graph or goal not in graph:
        raise ValueError("Start or goal node not present in the graph.")

    visited = set()
    stack = [[start]]  # stack of paths, not just nodes
    nodes_explored = 0

    while stack:
        path = stack.pop()          # LIFO: take the most recently added path
        current_node = path[-1]

        if current_node in visited:
            continue

        visited.add(current_node)
        nodes_explored += 1

        if current_node == goal:
            return path, nodes_explored

        # Push neighbours in reverse so the first neighbour is explored first
        for neighbour in reversed(graph.get(current_node, [])):
            if neighbour not in visited:
                new_path = path + [neighbour]
                stack.append(new_path)

    return None, nodes_explored


def main():
    """Run DFS on the same sample graph used for BFS."""
    try:
        graph = {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F"],
            "D": ["B"],
            "E": ["B", "F"],
            "F": ["C", "E", "G"],
            "G": ["F"],
        }

        start_node = "A"
        goal_node = "G"

        path, nodes_explored = dfs(graph, start_node, goal_node)

        if path is None:
            print(f"No path found between {start_node} and {goal_node}.")
            return

        print("--- DFS Result ---\n")
        print(f"Start node : {start_node}")
        print(f"Goal node  : {goal_node}")
        print(f"Path found : {' -> '.join(path)}")

        print("\n--- Performance Summary ---")
        print(f"Path length     : {len(path) - 1} edges")
        print(f"Nodes explored  : {nodes_explored}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()