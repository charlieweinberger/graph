import matplotlib.pyplot as plt
plt.style.use('bmh')
import sys
sys.path.append('src')
from bp_neural_network import NeuralNetwork

initial_weights = {
    (1, 3): 1,
    (1, 4): 1,
    (2, 3): 1,
    (2, 4): 1,
    (3, 6): 1,
    (4, 6): 1,
    (5, 6): 1
}
bias_nodes = [2, 5]

data = [(0, 5), (2, 3), (5, 10)]
f = lambda x: max(0, x)
f_prime = lambda x: 0 if x <= 0 else 1

num_iterations = list(range(7))
# num_iterations = [1, 2, 5, 10, 50, 100, 200]
alpha = 0.001

nn = NeuralNetwork(initial_weights, bias_nodes)
nn.fit(data, f, f_prime)
nn.run_gradient_descent(num_iterations, alpha)