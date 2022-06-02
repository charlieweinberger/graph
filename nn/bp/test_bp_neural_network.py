import matplotlib.pyplot as plt
plt.style.use('bmh')
import sys
sys.path.append('src')
from bp_neural_network import *

pairs = [(1, 3), (1, 4), (2, 3), (2, 4), (3, 6), (4, 6), (5, 6)]
initial_weights = {pair : 1 for pair in pairs}
bias_nodes = [2, 5]

data = [(0, 5), (2, 3), (5, 10)]
f = lambda x: max(0, x)
f_prime = lambda x: 0 if x <= 0 else 1

# num_iterations_list = [1, 2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 150, 200]
num_iterations_list = [1, 2, 5, 10, 15, 20, 25, 30]
alpha = 0.001

nn = NeuralNetwork(pairs, initial_weights, bias_nodes)
nn.fit(data, f, f_prime)
nn.calc_inputs()
nn.run_gradient_descent(num_iterations_list)