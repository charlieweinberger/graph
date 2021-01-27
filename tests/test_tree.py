import sys
sys.path.append('src')
from tree import Tree

node_values = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
edges = [(0,2), (4,6), (4,8), (4,0), (3,1), (0,3), (3,5), (5,7), (3,9), (3,10)]

tree = Tree(edges, node_values)
tree.build_from_edges()

"""
The indices of the nodes are as follows:

    4
   /|\
  0 8 6
 /|
2 3__
 /|\ \
1 9 5 10
    |
    7

The values of the nodes are as follows:

    e
   /|\
  a i g
 /|
c d 
 /|\\
b j fk
    |
    h
"""

assert tree.root.value == 'e'
assert tree.root.index == 4

# Note: the following tests use sets {} rather than lists [].
# This way, you don't have to worry about order.

children = set(tree.root.children)

grandchildren = set([])
for child in children:
    grandchildren = grandchildren.union(set(child.children))

great_grandchildren = set([])
for grandchild in grandchildren:
    great_grandchildren = great_grandchildren.union(set(grandchild.children))

great_great_grandchildren = set([])
for great_grandchild in great_grandchildren:
    great_great_grandchildren = great_great_grandchildren.union(set(great_grandchild.children))

assert {node.index for node in children} == {0, 8, 6}
assert {node.value for node in children} == {'a', 'i', 'g'}

assert {node.index for node in grandchildren} == {2, 3}
assert {node.value for node in grandchildren} == {'c', 'd'}

assert {node.index for node in great_grandchildren} == {1, 9, 5, 10}
assert {node.value for node in great_grandchildren} == {'b', 'j', 'f', 'k'}

assert {node.index for node in great_great_grandchildren} == {7}
assert {node.value for node in great_great_grandchildren} == {'h'}

node_values = ['a', 'b', 'a', 'a', 'a', 'b', 'a', 'b', 'a', 'b', 'b']

"""
This means that the nodes will be as follows:
- the node with index 0 will have value 'a'
- the node with index 1 will have value 'b'
- the node with index 2 will have value 'a'
- the node with index 3 will have value 'a'
- the node with index 4 will have value 'a'
- the node with index 5 will have value 'b'
- the node with index 6 will have value 'a'
- the node with index 7 will have value 'b'
- the node with index 8 will have value 'a'
- the node with index 9 will have value 'b'
- the node with index 10 will have value 'b'
"""

edges = [(0,2), (4,6), (4,8), (4,0), (3,1), (0,3), (3,5), (5,7), (3,9), (3,10)]

tree = Tree(edges, node_values)
tree.build_from_edges()

"""
The indices of the nodes are as follows:

    4
   /|\
  0 8 6
 /|
2 3__
 /|\ \
1 9 5 10
    |
    7

The values of the nodes are as follows:

    a
   /|\
  a a a
 /|
a a 
 /|\\
b b bb
    |
    b
"""

assert tree.root.value == 'a'
assert tree.root.index == 4

children = set(tree.root.children)

grandchildren = set([])
for child in children:
    grandchildren = grandchildren.union(set(child.children))

great_grandchildren = set([])
for grandchild in grandchildren:
    great_grandchildren = great_grandchildren.union(set(grandchild.children))

great_great_grandchildren = set([])
for great_grandchild in great_grandchildren:
    great_great_grandchildren = great_great_grandchildren.union(set(great_grandchild.children))

assert {node.index for node in children} == {0, 8, 6}
assert {node.value for node in children} == {'a', 'a', 'a'}

assert {node.index for node in grandchildren} == {2, 3}
assert {node.value for node in grandchildren} == {'a', 'a'}

assert {node.index for node in great_grandchildren} == {1, 9, 5, 10}
assert {node.value for node in great_grandchildren} == {'b', 'b', 'b', 'b'}

assert {node.index for node in great_great_grandchildren} == {7}
assert {node.value for node in great_great_grandchildren} == {'b'}

print("passed all")