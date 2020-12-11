class Node():
    def __init__(self, value):
        self.value = value
        self.children = []

class Tree():

    def __init__(self, edges):
        self.edges = edges
        self.root = Node(self.get_root()[0])
    
    def get_children(self, parent):
        ans_values_sorted = sorted([pair[1] for pair in self.edges if pair[0] == parent])
        return [Node(n) for n in ans_values_sorted]

    def get_parents(self, child):
        ans_values_sorted = sorted([pair[0] for pair in self.edges if pair[1] == child])
        return [Node(n) for n in ans_values_sorted]
        
    def get_root(self):
        children = [pair[1] for pair in self.edges]
        ans = []
        for pair in self.edges:
            if (pair[0] not in children) and (pair[0] not in ans):
                ans.append(pair[0])
        return ans

    def build_from_edges(self):
        
        node_array = [self.root]

        while len(node_array) != 0:

            child_array = []

            for node in node_array:

                new_children = self.get_children(node.value)
                node.children = new_children
                child_array += new_children
            
            node_array = list(child_array)