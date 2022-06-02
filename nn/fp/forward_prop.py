import matplotlib.pyplot as plt
plt.style.use('bmh')

def copy_dict(dictionary):
    return {key:value for key, value in dictionary.items()}

def print_dict(dictionary):
    print({(pair[0].index, pair[1].index) : round(weight, 10) for pair, weight in dictionary.items()})

class Node():
    def __init__(self, index, is_bias=False):
        self.index = index
        self.is_bias = is_bias
        self.inputs = None
        self.outputs = None
        self.dRSS_dn = None

class NeuralNetwork():

    def __init__(self, pairs, initial_weights, bias_nodes):
        
        self.bias_nodes = bias_nodes
        self.num_nodes = max(elem for pair in pairs for elem in pair)
        self.node_list = {index : Node(index, index in self.bias_nodes) for index in range(1, self.num_nodes + 1)}

        self.pairs = [(self.node_list[a], self.node_list[b]) for a, b in pairs]
        self.weights = {(self.node_list[pair[0]], self.node_list[pair[1]]) : initial_weights[pair] for pair in pairs}

        self.rows = self.get_rows()

        self.data = None
        self.f = None
        self.f_prime = None

        self.dRSS_dw = {pair:0 for pair in self.pairs}

    def fit(self, data, f, f_prime):
        
        self.data = data
        self.f = f
        self.f_prime = f_prime

        for node in self.node_list.values():
            node.inputs  = {point:0 for point in self.data}
            node.outputs = {point:0 for point in self.data}
            node.dRSS_dn = {point:0 for point in self.data}