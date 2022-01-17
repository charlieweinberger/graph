class Node():
    def __init__(self, index, is_bias=False):
        self.index = index
        self.is_bias = is_bias

edges = [
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 6),
    (4, 6),
    (5, 6)
]

class NeuralNetwork():

    def __init__(self, edges, bias_nodes):
        self.edges = [[Node(index, index in bias_nodes) for index in edge] for edge in edges]
    
    def get_parents(self, index):
        return [edge[1] for edge in self.edges if edge[0] == index]

    def get_paths(self, starting_index):
        
        paths = []

        for i, parent in enumerate(self.get_parents(starting_index)):
            paths.append([starting_index, parent])

            for j, grandparent in enumerate(self.get_parents(parent)):
                paths[i].append(grandparent)
        
        return paths
    
    def fit(self, data, weights, f):
        pass