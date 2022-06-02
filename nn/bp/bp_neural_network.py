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

    def __init__(self, pairs, weights, bias_nodes):
        
        self.bias_nodes = bias_nodes
        self.num_nodes = max(elem for pair in pairs for elem in pair)
        self.nodes = {index : Node(index, index in self.bias_nodes) for index in range(1, self.num_nodes + 1)}

        self.pairs = [(self.nodes[a], self.nodes[b]) for a, b in pairs]
        self.initial_weights = {(self.nodes[pair[0]], self.nodes[pair[1]]) : weights[pair] for pair in pairs}

        self.rows = self.get_rows()

        self.data = None
        self.f = None
        self.f_prime = None

        self.dRSS_dw = {pair:0 for pair in self.pairs}

    def fit(self, data, f, f_prime):
        
        self.data = data
        self.f = f
        self.f_prime = f_prime

        for node in self.nodes.values():
            node.inputs  = {point:0 for point in self.data}
            node.outputs = {point:0 for point in self.data}
            node.dRSS_dn = {point:0 for point in self.data}

    def row_of(self, node, rows):
        for x, row in enumerate(rows):
            if node in row:
                return x

    def get_rows(self):

        rows = [[self.nodes[1]]]

        for a, b in self.pairs:

            row_of_a_index = self.row_of(a, rows)
            row_of_b_index = self.row_of(b, rows)

            if row_of_b_index == None:
                try:
                    rows[row_of_a_index + 1].append(b)
                except:
                    rows.append([b])

            if row_of_a_index == None:

                if a.index != 1 and a not in rows[row_of_b_index - 1]:
                    rows[row_of_b_index - 1].append(a)

        return rows

    def get_node_weight(self, a, b, weights):
        return weights[(self.nodes[a], self.nodes[b])]

    def calc_inputs(self):
        
        for point in self.data:
            
            for node in self.nodes.values():

                if node.is_bias:            node_input = 1
                elif node in self.rows[0]:  node_input = point[0]
                else:                       node_input = sum(self.initial_weights[(a, b)] * a.outputs[point] for a, b in self.pairs if b == node)

                node.inputs[point] = node_input
                node.outputs[point] = self.f(node_input)

    def calc_dRSS_dn(self, weights):

        for point in self.data:
            self.nodes[6].dRSS_dn[point] = 2 * (self.nodes[6].outputs[point] - point[1])

        for point in self.data:
            self.nodes[5].dRSS_dn[point] = self.nodes[6].dRSS_dn[point] * self.f_prime(self.nodes[6].inputs[point]) * self.get_node_weight(5, 6, weights)
            self.nodes[4].dRSS_dn[point] = self.nodes[6].dRSS_dn[point] * self.f_prime(self.nodes[6].inputs[point]) * self.get_node_weight(4, 6, weights)
            self.nodes[3].dRSS_dn[point] = self.nodes[6].dRSS_dn[point] * self.f_prime(self.nodes[6].inputs[point]) * self.get_node_weight(3, 6, weights)

        for point in self.data:
            
            self.nodes[2].dRSS_dn[point] = self.nodes[3].dRSS_dn[point] * self.f_prime(self.nodes[3].inputs[point]) * self.get_node_weight(2, 3, weights) + self.nodes[4].dRSS_dn[point] * self.f_prime(self.nodes[4].inputs[point]) * self.get_node_weight(2, 4, weights)

            self.nodes[1].dRSS_dn[point] = self.nodes[3].dRSS_dn[point] * self.f_prime(self.nodes[3].inputs[point]) * self.get_node_weight(1, 3, weights) + self.nodes[4].dRSS_dn[point] * self.f_prime(self.nodes[4].inputs[point]) * self.get_node_weight(1, 4, weights)

    def calc_dRSS_dw(self):
        for a, b in self.pairs:
            for point in self.data:
                self.dRSS_dw[(a, b)] += b.dRSS_dn[point] * self.f_prime(b.inputs[point]) * a.outputs[point]

    def calc_rss(self, weights):
        rss = 0
        for x, y in self.data:
            rss += (self.predict(weights, x) - y) ** 2
        return rss

    def predict(self, weights, x):

        i = {}

        output = lambda node_index: self.f(i[self.nodes[node_index].index])

        # print_dict(weights)

        i[1] = x
        i[2] = 1
        i[3] = weights[(self.nodes[1], self.nodes[3])] * output(1) + weights[(self.nodes[2], self.nodes[3])] * output(2)
        i[4] = weights[(self.nodes[1], self.nodes[4])] * output(1) + weights[(self.nodes[2], self.nodes[4])] * output(2)
        i[5] = 1
        i[6] = weights[(self.nodes[3], self.nodes[6])] * output(3) + weights[(self.nodes[4], self.nodes[6])] * output(4) + 1

        # for node in self.nodes.values():

        #     if node.is_bias:
        #         i[node.index] = 1
        #     elif node.index in self.rows[0]:
        #         i[node.index] = x
        #     else:
        #         i[node.index] = sum(weights[(a, b)] * self.f(i[a.index]) for a, b in self.initial_weights if b == node)

        return self.f(i[6])

    def gradient_descent(self, weights, num_iterations, alpha):
        for _ in range(num_iterations):
            self.calc_dRSS_dn(weights)
            self.calc_dRSS_dw()
            weights = {pair:weight - alpha * self.dRSS_dw[pair] for pair, weight in weights.items()}
        return weights

    def run_gradient_descent(self, num_iterations_list, alpha=0.001):

        rss_list = []
        for n in num_iterations_list:
            weights = copy_dict(self.initial_weights)
            gradient_desc = self.gradient_descent(weights, n, alpha)
            rss = self.calc_rss(gradient_desc)
            rss_list.append(rss)

        # plot 1

        plt.figure(1)
        plt.plot(num_iterations_list, rss_list)
        plt.xlabel('num_iterations')
        plt.ylabel('rss')
        plt.savefig('nn/bp/bp_num_iterations_vs_rss.png')

        # plot 2

        plt.figure(2)
        plt.scatter([point[0] for point in self.data], [point[1] for point in self.data], label='data')

        x_list = list(range(self.num_nodes + 1))

        initial_y_list = [self.predict(self.initial_weights, x) for x in x_list]
        plt.plot(x_list, initial_y_list, label='initial regressor')

        final_weights = self.gradient_descent(self.initial_weights, 1000, alpha)
        final_y_list = [self.predict(final_weights, x) for x in x_list]
        plt.plot(x_list, final_y_list, label='final regressor')

        plt.legend()
        plt.savefig('nn/bp/bp_data_vs_initial_regressor_vs_final_regressor.png')

        print('done')