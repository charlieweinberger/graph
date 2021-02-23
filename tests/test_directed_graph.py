import sys
sys.path.append('src')
from directed_graph import DirectedGraph

edges = [(0,1),(1,2),(3,1),(4,3),(1,4),(4,5),(3,6)]
directed_graph = DirectedGraph(edges)

"""

0-->1-->2
    ^ \
    |  v
6<--3<--4-->5

"""

children_index_list = [[child.index for child in node.children] for node in directed_graph.nodes]
assert children_index_list == [[1], [2,4], [], [1,6], [3,5], [], []]

parents_index_list = [[parent.index for parent in node.parents] for node in directed_graph.nodes]
assert parents_index_list == [[], [0,3], [1], [4], [1], [4], [3]]

print("finished setting indices, children, and parents")

breadth_first_indices_4 = [node.index for node in directed_graph.nodes_breadth_first(4)]
# print("breadth_first_indices_4:", breadth_first_indices_4) # should give a breadth-first ordering, e.g. [4, 3, 5, 6, 1, 2]

depth_first_indices_4 = [node.index for node in directed_graph.nodes_depth_first(4)]
# print("depth_first_indices_4:", depth_first_indices_4) # returns a depth-first ordering, e.g. [4, 3, 6, 1, 2, 5]

print("finished nodes_breadth_first() and nodes_depth_first()")

assert directed_graph.calc_distance(0,3) == 3
assert directed_graph.calc_distance(3,5) == 3
assert directed_graph.calc_distance(0,5) == 3
assert directed_graph.calc_distance(4,1) == 2
assert directed_graph.calc_distance(2,4) == False

print("finished calc_distance()")

assert directed_graph.calc_shortest_path(0,3) == [0, 1, 4, 3]
assert directed_graph.calc_shortest_path(3,5) == [3, 1, 4, 5]
assert directed_graph.calc_shortest_path(0,5) == [0, 1, 4, 5]
assert directed_graph.calc_shortest_path(4,1) == [4, 3, 1]
assert directed_graph.calc_shortest_path(2,4) == False

print("finished calc_shortest_path()")