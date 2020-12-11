import sys
sys.path.append('src')
from tree import Tree

edges = [('a','c'), ('e','g'), ('e','i'), ('e','a'), ('g','b'), ('a','d'), ('d','f'), ('f','h'), ('d','j'), ('c','k')]
tree = Tree(edges)

tree.build_from_edges()

assert tree.root.value == 'e'

assert sorted([node.value for node in tree.root.children]) == sorted(['a', 'i', 'g']), sorted([node.value for node in tree.root.children])

assert sorted([node.value for node in tree.root.children[0].children]) == sorted(['c', 'd']), sorted([node.value for node in tree.root.children[0].children]) # children of a
assert sorted([node.value for node in tree.root.children[1].children]) == sorted(['b']), sorted([node.value for node in tree.root.children[1].children]) # children of g
assert sorted([node.value for node in tree.root.children[2].children]) == sorted([]), sorted([node.value for node in tree.root.children[2].children]) # children of i

assert sorted([node.value for node in tree.root.children[1].children[0].children]) == sorted([]), sorted([node.value for node in tree.root.children[2].children[0].children]) # children of b
assert sorted([node.value for node in tree.root.children[0].children[0].children]) == sorted(['k']), sorted([node.value for node in tree.root.children[0].children[0].children]) # children of c
assert sorted([node.value for node in tree.root.children[0].children[1].children]) == sorted(['j', 'f']), sorted([node.value for node in tree.root.children[0].children[1].children]) # children of d

assert sorted([node.value for node in tree.root.children[0].children[0].children[0].children]) == sorted([]), sorted([node.value for node in tree.root.children[0].children[0].children[0].children]) # children of k
assert sorted([node.value for node in tree.root.children[0].children[1].children[0].children]) == sorted(['h']), sorted([node.value for node in tree.root.children[0].children[1].children[1].children]) # children of f
assert sorted([node.value for node in tree.root.children[0].children[1].children[1].children]) == sorted([]), sorted([node.value for node in tree.root.children[0].children[1].children[0].children]) # children of j

print("passed all tests")