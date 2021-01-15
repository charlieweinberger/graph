import sys
sys.path.append('src')
from tree import Tree

edges = [('a','c'), ('e','g'), ('e','i'), ('e','a'), ('d','b'), ('a','d'), ('d','f'), ('f','h'), ('d','j'), ('d','k')]
tree = Tree(edges)
tree.build_from_edges()

nodes = tree.nodes_breadth_first()
assert [node.value for node in nodes] == ['e','g','i','a','c','d','b','f','j','k','h'], [node.value for node in nodes]

nodes = tree.nodes_depth_first()
assert [node.value for node in nodes] == ['e','g','i','a','c','d','b','f','h','j','k'], [node.value for node in nodes]

print("passed all")