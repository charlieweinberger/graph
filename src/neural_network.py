class NeuralNetwork():

    def __init__(self, edges, bias_nodes):
        self.edges = edges
        self.bias_nodes = bias_nodes
    
    def get_parents(self, index):
        return [edge[1] for edge in self.edges if edge[0] == index]

    def get_paths(self, starting_index):
        
        paths = []
        
        for i, parent in enumerate(self.get_parents(starting_index)):
            paths.append([starting_index, parent])

            for grandparent in self.get_parents(parent):
                paths[i].append(grandparent)
        
        return paths