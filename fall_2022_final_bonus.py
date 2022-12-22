import sys
sys.path.append('src')
from directed_graph import DirectedGraph

def senior_final_bonus_question(edges):
    
    cyclic = False
    cycle_start = None

    graph = DirectedGraph(edges)

    initial_node = graph.nodes[0]
    initial_node.distance = 0

    # depth first search

    nodes_to_visit = [initial_node]
    visited = []

    while nodes_to_visit != []:

        current_node = nodes_to_visit[0]
        
        nodes_to_visit.remove(current_node)
        visited.append(current_node)

        for child in current_node.children:
            
            if child in visited: # check for cycle (if it's already been visited)
                cyclic = True
                cycle_start = child
            else:
                nodes_to_visit.append(child)

            if not cyclic and not child.distance: # label distances
                child.distance = current_node.distance + 1

    if cyclic:
        print('\ncycle found!')
        print(f'nodes in or after the cycle: {[n.index for n in visited[visited.index(cycle_start):]]}')
    else:
        print('\nno cycles found.')
        print(f'node depths (index, depth): {[(n.index, n.distance) for n in graph.nodes]}')

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