class Node():
    def __init__(self, index, is_biased):
        self.index = index
        self.children = []
        self.parents = []
        self.input_val = None
        self.output_val = None
        self.is_biased = is_biased
        self.dRSS = 0

class NeuralNet():

    def __init__(self, weights, f, data, bias_node_indices, normalize=False):
        
        self.weights = {k:v for k,v in weights.items()}
        self.num_nodes = max(elem for pair in self.weights for elem in pair)
        self.nodes = [Node(index, index in bias_node_indices) for index in range(1, self.num_nodes + 1)]
        
        self.f = f
        self.data = self.normalize_data(data, normalize)

        self.connect_nodes()

    def normalize_data(self, data, normalize):
        if not normalize:
            return data
        else:
            x = [point[0] for point in data]
            y = [point[1] for point in data]
            return [(10 * (px - min(x)) / (max(x) - min(x)), 10 * (py - min(y)) / (max(y) - min(y))) for px, py in data]

    def get_node(self, node_index):
        for node in self.nodes:
            if node.index == node_index:
                return node

    def connect_nodes(self):
        for key in self.weights:
            nodes = [self.get_node(char) for char in key]
            nodes[0].parents.append(nodes[1])
            nodes[1].children.append(nodes[0])

    def set_node_vals(self, x):

        for node in self.nodes:
            
            if node.is_biased:
                node.output_val = 1 

            elif node.index == 1:
                node.input_val = x
                node.output_val = self.f(x)

            else:
                
                in_val = 0
                for in_node in node.children:
                    in_val += self.weights[(in_node.index, node.index)] * in_node.output_val

                node.input_val = in_val
                node.output_val = self.f(in_val)
    
    def predict(self, x):
        self.set_node_vals(x)
        return self.nodes[self.num_nodes - 1].output_val
    
    def set_node_dRSS(self, point, f_prime):
        self.set_node_vals(point[0])
        for node in self.nodes[::-1]:
            if node.index == self.num_nodes:
                node.dRSS = 2 * (node.output_val - point[1])
            else:
                for out_node in node.parents:
                    node.dRSS = out_node.dRSS * f_prime(out_node.input_val) * self.weights[(node.index, out_node.index)]

    def weight_gradients(self, f_prime):
        gradients = {key:0 for key in self.weights}
        for key in self.weights:
            for point in self.data:
                self.set_node_dRSS(point, f_prime)
                nodes = [self.get_node(char) for char in key]
                gradients[key] += nodes[1].dRSS * f_prime(nodes[1].input_val) * nodes[0].output_val
        return gradients

    def rss(self):
        return sum((self.predict(x) - y) ** 2 for x, y in self.data)
    
    def gradient_desc(self, num_iterations, alpha, f_prime):
        for _ in range(num_iterations):
            gradients = self.weight_gradients(f_prime)
            self.weights = {k:v - alpha * gradients[k] for k,v in self.weights.items()}