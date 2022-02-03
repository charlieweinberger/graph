import matplotlib.pyplot as plt
plt.style.use('bmh')

class NeuralNetwork():

    def __init__(self, initial_weights, bias_nodes):
        
        self.initial_weights = initial_weights
        self.bias_nodes = bias_nodes
        
        self.num_nodes = max(elem for pair in self.initial_weights for elem in pair)
        self.node_list = list(range(1, self.num_nodes + 1))
        self.rows = self.get_rows()

        self.data = None
        self.f = None
        self.f_prime = None
    
        self.inputs = None
        self.outputs = None

        self.dRSS_dn = {x:0 for x in self.node_list}
        self.dRSS_dw = {pair:0 for pair in self.initial_weights}

    def fit(self, data, f, f_prime):
        self.data = data
        self.f = f
        self.f_prime = f_prime
    
    def run_gradient_descent(self, num_iterations, alpha=0.001):

        self.inputs = self.get_inputs(self.initial_weights, self.data)
        self.outputs = {point : {node_index : self.f(node_input) for node_index, node_input in self.inputs[point].items()} for point in self.data}

        self.calc_dRSS_dn()
        self.calc_dRSS_dw()

        rss = [self.calc_rss(self.gradient_descent(self.initial_weights, n, alpha)) for n in num_iterations]

        # plot 1

        plt.figure(0)
        plt.plot(num_iterations, rss)
        plt.xlabel('num_iterations')
        plt.ylabel('rss')
        plt.savefig('bp_num_iterations_vs_rss.png')

        # plot 2

        plt.figure(2)
        plt.scatter([point[0] for point in self.data], [point[1] for point in self.data], label='data')

        x_list = list(range(self.num_nodes + 1))

        initial_y_list = [self.final_node_output(self.initial_weights, x) for x in x_list]
        plt.plot(x_list, initial_y_list, label='initial regressor')

        final_weights = self.gradient_descent(self.initial_weights, 1000, alpha)
        final_y_list = [self.final_node_output(final_weights, x) for x in x_list]
        plt.plot(x_list, final_y_list, label='final regressor')

        plt.legend()
        plt.savefig('bp_data_vs_initial_regressor_vs_final_regressor.png')

        print('done')

    def row_of(self, index, rows):
        for x, row in enumerate(rows):
            if index in row:
                return x

    def get_rows(self):

        rows = [[1]]

        for a, b in self.initial_weights:

            row_of_a_index = self.row_of(a, rows)
            row_of_b_index = self.row_of(b, rows)

            if row_of_b_index == None:
                try:
                    rows[row_of_a_index + 1].append(b)
                except:
                    rows.append([b])

            if row_of_a_index == None:

                if a != 1 and a not in rows[row_of_b_index - 1]:
                    rows[row_of_b_index - 1].append(a)
                    
        return rows
    
    def get_inputs(self, weights, input_data):

        inputs = {}

        for point in input_data:

            i = {}

            for node_index in self.node_list:

                if node_index in self.bias_nodes:
                    i[node_index] = 1
                elif node_index in self.rows[0]:
                    i[node_index] = point[0]
                else:
                    i[node_index] = sum(weights[(a, b)] + self.f(i[a]) for a, b in self.initial_weights if node_index == b)

            inputs[point] = i
        
        return inputs
    
    def final_node_output(self, weights, x):
        return self.f(self.get_inputs(weights, input_data=[(x, None)])[(x, None)][self.num_nodes])
    
    def calc_dRSS_dn(self):

        self.dRSS_dn[self.num_nodes] = sum(2 * (self.outputs[point][self.num_nodes] - point[1]) for point in self.data)

        for index in self.node_list[0:-1][::-1]:
            for point in self.data:
                for index_above in self.rows[self.row_of(index, self.rows) + 1]:
                    if index_above in self.bias_nodes: continue
                    self.dRSS_dn[index] += self.dRSS_dn[index_above] * self.f_prime(self.inputs[point][index_above]) * self.initial_weights[(index, index_above)]
    
    def calc_dRSS_dw(self):
        for a, b in self.initial_weights:
            for point in self.data:
                self.dRSS_dw[(a, b)] += self.dRSS_dn[b] * self.f_prime(self.inputs[point][b]) * self.outputs[point][a]
    
    def calc_rss(self, weights):
        rss = 0
        for x, y in self.data:
            rss += (self.final_node_output(weights, x) - y) ** 2
        return rss
    
    def gradient_descent(self, weights, num_iterations, alpha):
        for _ in range(num_iterations):
            weights = {pair:weight - alpha * self.dRSS_dw[pair] for pair, weight in weights.items()}
        return weights