import matplotlib.pyplot as plt
plt.style.use('bmh')

class Node():
    def __init__(self, index, is_bias=False):
        self.index = index
        self.is_bias = is_bias
        self.inputs = None
        self.outputs = None
        self.dRSS_dn = 0

class NeuralNetwork():

    def __init__(self, pairs, weights, bias_nodes):
        
        self.bias_nodes = bias_nodes
        self.num_nodes = max(elem for pair in pairs for elem in pair)
        self.node_list = {index : Node(index, index in self.bias_nodes) for index in range(1, self.num_nodes + 1)}

        self.pairs = [(self.node_list[a], self.node_list[b]) for a, b in pairs]
        self.initial_weights = {(self.node_list[pair[0]], self.node_list[pair[1]]) : weights[pair] for pair in pairs}

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

    def run_gradient_descent(self, num_iterations_list, alpha=0.001):

        rss = [self.calc_rss(self.gradient_descent(self.copy_dict(self.initial_weights), n, alpha)) for n in num_iterations_list]

        # plot 1

        plt.figure(0)
        plt.plot(num_iterations_list, rss)
        plt.xlabel('num_iterations')
        plt.ylabel('rss')
        plt.savefig('bp_num_iterations_vs_rss.png')

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
        plt.savefig('bp_data_vs_initial_regressor_vs_final_regressor.png')

        print('done')

    def copy_dict(self, dictionary):
        return {key:value for key, value in dictionary.items()}

    def row_of(self, node, rows):
        for x, row in enumerate(rows):
            if node in row:
                return x

    def get_rows(self):

        rows = [[self.node_list[1]]]

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

    def calc_inputs(self):
        
        for point in self.data:
            
            for node in self.node_list.values():

                if node.is_bias:
                    node_input = 1
                elif node in self.rows[0]:
                    node_input = point[0]
                else:
                    node_input = sum(self.initial_weights[(a, b)] * a.outputs[point] for a, b in self.pairs if b == node)

                node.inputs[point] = node_input
                node.outputs[point] = self.f(node_input)

    def predict(self, weights, x):

        i = {}

        for node in self.node_list.values():

            if node.is_bias:
                i[node.index] = 1
            elif node.index in self.rows[0]:
                i[node.index] = x
            else:
                i[node.index] = sum(weights[(a, b)] * self.f(i[a.index]) for a, b in self.initial_weights if b == node)

        print(x)
        print({(pair[0].index, pair[1].index) : round(weight) for pair, weight in weights.items()})
        print({k:round(v) for k, v in i.items()}, '\n')

        return self.f(i[self.num_nodes])

    # def predict(self, weights, x):
        
    #     node = self.node_list[self.num_nodes]
    #     node_input = node.inputs[point]
    #     return self.f(node_input)

    def calc_dRSS_dn(self):

        final_node = self.node_list[self.num_nodes]
        final_node.dRSS_dn = sum(2 * (final_node.outputs[point] - point[1]) for point in self.data)

        for node in list(self.node_list.values())[0:-1][::-1]:
            for point in self.data:
                for node_above in self.rows[self.row_of(node, self.rows) + 1]:
                    if node_above.is_bias: continue
                    node.dRSS_dn += node_above.dRSS_dn * self.f_prime(node_above.inputs[point]) * self.initial_weights[(node, node_above)]
    
    def calc_dRSS_dw(self):
        for a, b in self.pairs:
            for point in self.data:
                self.dRSS_dw[(a, b)] += b.dRSS_dn * self.f_prime(b.inputs[point]) * a.outputs[point]

    def calc_rss(self, weights):
        rss = 0
        for x, y in self.data:
            rss += (self.predict(weights, x) - y) ** 2
        return rss

    def gradient_descent(self, weights, num_iterations, alpha):
        for _ in range(num_iterations):
            weights = {pair:weight - alpha * self.dRSS_dw[pair] for pair, weight in weights.items()}
        return weights