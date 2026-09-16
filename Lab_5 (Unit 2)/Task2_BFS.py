"""
Breadth-First Search (BFS) — Graph Traversal

Finds the shortest path (minimum number of edges) between a start
and goal node in an unweighted graph, represented as an adjacency list.
"""

from collections import deque


def bfs(graph, start, goal):
    """
    Perform BFS on 'graph' from 'start' to 'goal'.

    Parameters:
        graph (dict): adjacency list, e.g. {'A': ['B', 'C'], ...}
        start (str): starting node
        goal (str): target node

    Returns:
        path (list or None): sequence of nodes from start to goal
        nodes_explored (int): number of nodes dequeued during search
    """
    if start not in graph or goal not in graph:
        raise ValueError("Start or goal node not present in the graph.")

    visited = {start}
    queue = deque([[start]])  # queue of paths, not just nodes
    nodes_explored = 0

    while queue:
        path = queue.popleft()
        current_node = path[-1]
        nodes_explored += 1

        if current_node == goal:
            return path, nodes_explored

        for neighbour in graph.get(current_node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                new_path = path + [neighbour]
                queue.append(new_path)

    return None, nodes_explored


def main():
    """Run BFS on a sample graph."""
    try:
        # Sample graph: could represent rooms in a maze, cities on a
        # route map, or nodes in any state-space problem.
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

        path, nodes_explored = bfs(graph, start_node, goal_node)

        if path is None:
            print(f"No path found between {start_node} and {goal_node}.")
            return

        print("--- BFS Result ---\n")
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