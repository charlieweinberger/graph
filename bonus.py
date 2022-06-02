import sys
sys.path.append('src')
from directed_graph import DirectedGraph

def check_for_cycles(edges):

    graph = DirectedGraph(edges)

    for node in graph.nodes:

        nodes_to_check = [node]
        checked_nodes = [node]

        while nodes_to_check != []:

            current_node = nodes_to_check[0]

            if node in current_node.children:
                return True
            else:
                nodes_to_check.remove(current_node)
                checked_nodes.append(current_node)
                for child in current_node.children:
                    if child not in checked_nodes:
                        nodes_to_check.append(child)
    
    return False

assert check_for_cycles([(0,1),(1,2),(2,3)]) == False
assert check_for_cycles([(0,1),(1,2),(2,3),(3,0)]) == True
assert check_for_cycles([(0,1),(1,2),(2,3),(3,0),(3,4),(4,5)]) == True

print('tests complete')

# It loops through every node, and that node's children. If that child node is not a child of the current node, then it adds each of the current node's children into a list to check those nodes, and adds the current node to a checked_node list so it isn't checked again. While nodes_to_check is not empty, it checks every node in the list and tests if the original node is a child. If so, it returns True. If not, when all nodes have been checked, it returns False.