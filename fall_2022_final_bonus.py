import sys
sys.path.append('src')
from directed_graph import DirectedGraph

"""

Suppose you have a directed graph with n nodes and m source nodes (i.e. nodes with no parents). Write pseudocode for an O(nm) algorithm that accomplishes the following:

    - If the graph is acyclic, then label each node with its depth (i.e. the distance to its furthest ancestor source node).
    - If the graph has a cycle, then return the nodes that are either in the cycle or are progeny of the cycle.

In your pseudocode, you may refer refer to "node.parents" or "node.children" but not "node.ancestors" nor "node.progeny."

Then, justify why your algorithm is O(nm).

"""

class Node():
    def __init__(self, index):
        self.index = index
        self.distance = None
        self.children = []

def get_node(nodes, index):
    for node in nodes:
        if node.index == index:
            return node

def senior_final_bonus_question(edges):

    # create graph, check for cycles

    cyclic = False
    cycle_initial_node = None

    nodes = [Node(edges[0][0])]
    for _, child_index in edges:

        for n in nodes:
            if child_index == n.index:
                cyclic = True
                cycle_initial_node = n
                break
                
        if not any(child_index == n.index for n in nodes):
            nodes.append(Node(child_index))
    
    print(f'\ncyclic: {cyclic}')

    for parent_index, child_index in edges:

        parent = get_node(nodes, parent_index)
        child = get_node(nodes, child_index)

        if child not in parent.children:
            parent.children.append(child)

    # depth first search

    initial_node = cycle_initial_node if cyclic else nodes[0]
    initial_node.distance = 0

    nodes_to_visit = [initial_node]
    visited = []

    while nodes_to_visit != []:

        current_node = nodes_to_visit[0]
        
        nodes_to_visit.remove(current_node)
        visited.append(current_node)

        for child in current_node.children:
            
            if child not in visited:
                nodes_to_visit.append(child)
        
            if not cyclic and not child.distance: # label distances
                child.distance = current_node.distance + 1

    if cyclic:
        print(f'nodes in or after the cycle: {[n.index for n in visited]}')
    else:
        print(f'node depths (index, depth): {[(n.index, n.distance) for n in nodes]}')

# 1 -> 11 -> 2 -> 3 -> 12 -> 7 -> 8 -> 14
#                 ^    |
#                 |    v
#                 6 <- 5 -> 10

senior_final_bonus_question([[1,11],[11,2],[2,3],[3,12],[12,5],[5,6],[6,3],[12,7],[7,8],[8,14],[5,10]])

# 11 -> 1 -> 8 -> 3 -> 20
#       |         |
#       v         v
#       7         5 -> 6

senior_final_bonus_question([[11,1],[1,8],[1,7],[8,3],[3,20],[3,5],[5,6]])