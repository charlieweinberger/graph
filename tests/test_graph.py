import sys
sys.path.append('src')
from graph import Graph

edges = [(0,1),(1,2),(1,3),(3,4),(1,4),(4,5)]
graph = Graph(edges)

print("\n0 -- 1 -- 2")
print("     | \ ")
print("     3--4 -- 5\n")

bf = graph.get_nodes_breadth_first(2)
assert [node.index for node in bf] == [2, 1, 0, 3, 4, 5]
print("passed get_nodes_breadth_first")

df = graph.get_nodes_depth_first(2)
assert [node.index for node in df] == [2, 1, 4, 5, 3, 0] # this is the "other" order
print("passed get_nodes_depth_first")