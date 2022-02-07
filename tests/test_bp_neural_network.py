import matplotlib.pyplot as plt
plt.style.use('bmh')
import sys
sys.path.append('src')
from bp_neural_network import NeuralNetwork

pairs = [(1, 3), (1, 4), (2, 3), (2, 4), (3, 6), (4, 6), (5, 6)]
initial_weights = {pair : 1 for pair in pairs}
bias_nodes = [2, 5]

data = [(0, 5), (2, 3), (5, 10)]
f = lambda x: max(0, x)
f_prime = lambda x: 0 if x <= 0 else 1

num_iterations_list = [1, 2, 5, 10, 50, 100, 200, 500]
alpha = 0.0001

nn = NeuralNetwork(pairs, initial_weights, bias_nodes)
nn.fit(data, f, f_prime)
nn.calc_inputs()

nn.calc_dRSS_dn()

print(nn.node_list[6].dRSS_dn)
print(nn.node_list[5].dRSS_dn)

nn.calc_dRSS_dw()

node_1, node_2, node_3, node_4, node_5, node_6 = nn.node_list.values()
print(nn.dRSS_dw[(node_5, node_6)])

nn.run_gradient_descent(num_iterations_list, alpha)