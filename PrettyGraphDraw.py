import networkx as nx


def dfs_edges_no_repeated_cycles(G, source=None):
    if source is None:
        # Choose an arbitrary node if no source is specified
        source = next(iter(G.nodes))

    visited = set()  # Set to keep track of visited nodes globally.
    path = []  # List to keep the current traversal path

    def dfs_visit(node):
        visited.add(node)  # Mark the node as visited
        path.append(node)  # Add the node to the current path

        for child in G[node]:
            if child not in visited:
                # If the child has not been visited, yield the edge and continue DFS
                yield (node, child)
                yield from dfs_visit(child)
            elif child in path:
                # If the child is visited and is in the current path, we've found a cycle - do not yield the edge
                yield (node, child)
                continue
            else:
                # Child is visited but not in the current path, yield the edge
                # This means we're crossing paths but not forming a cycle in the context of this traversal
                yield (node, child)

        path.remove(node)  # Remove the node from the current path when backtracking

    # Start DFS from the source node and yield from its visit generator
    yield from dfs_visit(source)

def print_graph_from_dfs(dfs_edges, source):
    # Perform DFS and get the edges in the order they were explored
    #dfs_edges = list(nx.dfs_edges(G, source=source))

    # Create a mapping from node to list of child nodes
    graph_structure = {}
    for ss, t, fs in dfs_edges:
        if ss in graph_structure:
            graph_structure[ss].append(fs)
        else:
            graph_structure[ss] = [fs]

    path = []

    # Function to print the graph structure
    def print_branch(node, prefix='', is_tail=True):
        # Print current node
        line = f"{prefix}{'|-- ' if prefix else ''}{node}"
        print(line)
        path.append(node)

        # Recursively print each child
        if node not in graph_structure:
            return  # Base case: no children
        children = graph_structure[node]
        for i, child in enumerate(children):
            next_prefix = prefix + ('    ' if is_tail else '|   ')
            # Protect against loops
            if not child in path:
                print_branch(child, next_prefix, i == len(children) - 1)
            else:
                line = f"{prefix}{'    |-- ' if prefix else ''}{child}"
                print(line)

        path.remove(node) 

    # Start printing from the source node
    print_branch(source)

# Example usage
G = nx.DiGraph()
G.add_edges_from([('A', 'A'),('A', 'B'), ('B', 'C'), ('E', 'B'), ('C', 'A'), ('B', 'D'), ('D', 'E')])  # Example graph with cycles

edges = list(dfs_edges_no_repeated_cycles(G, 'A'))
print(edges)

# Example usage
print_graph_from_dfs(edges, source =edges[0][0])