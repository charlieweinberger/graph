import math, random

def tanh(x):
    return (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))

class Node():
    def __init__(self, index):
        self.index = index
        self.children = []
        self.input = None
        self.output = None
        self.is_biased = False

class RandomNeuralNet():

    def __init__(self, node_layers, f, weight_range, mutation_rate):

        self.num_nodes = sum(node_layers)
        if len(node_layers) > 2: self.num_nodes += len(node_layers) - 2

        self.f = f

        self.nodes = [Node(index) for index in range(1, self.num_nodes + 1)]
        self.bias_node_indices = []

        self.weights = self.random_weights(node_layers, weight_range)

        for node in self.nodes:
            node.is_biased = node.index in self.bias_node_indices
        
        self.mutation_rate = mutation_rate
        self.rss = None

        self.connect_nodes()
    
    def random_weights(self, node_layers, weight_range):

        layer_rep = []
        counter = 1
        
        for i in range(len(node_layers)):
        
            num = node_layers[i]
            layer_rep.append([])

            if 0 < i < len(node_layers) - 1:
                num += 1
        
            for _ in range(num):
                layer_rep[i].append(counter)
                counter += 1

        pairs = []
        for i in range(len(layer_rep) - 1):
            
            layer = layer_rep[i]
            next_layer = layer_rep[i+1]
            
            if i+1 != len(layer_rep) - 1:
                self.bias_node_indices.append(next_layer[-1])
                next_layer = next_layer[:-1]

            for node_index_1 in layer:
                for node_index_2 in next_layer:
                    pairs.append(tuple([node_index_1, node_index_2]))

        return {w : random.randrange(weight_range[0]*1000, weight_range[1]*1000) / 1000 for w in pairs}

    def get_node(self, node_index):
        for node in self.nodes:
            if node.index == node_index:
                return node

    def connect_nodes(self):
        for key in self.weights:
            node_1, node_2 = self.get_node(key[0]), self.get_node(key[1])
            node_2.children.append(node_1)

    def set_node_vals(self, x):

        for node in self.nodes:
            
            if node.is_biased:
                node.output = 1 

            elif node.index == 1:
                node.input = x
                node.output = self.f(x)

            else:

                in_val = 0
                for in_node in node.children:
                    in_val += self.weights[(in_node.index, node.index)] * in_node.output

                node.input = in_val
                node.output = self.f(in_val)

    def predict(self, x):
        self.set_node_vals(x)
        return self.nodes[self.num_nodes - 1].output