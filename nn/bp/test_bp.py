import matplotlib.pyplot as plt
plt.style.use('bmh')
from bp import *

weights = {(1, 3): 1, (1, 4): 1, (2, 3): 1, (2, 4): 1, (3, 6): 1, (4, 6): 1, (5, 6): 1}
bias_node_indices = [2, 5]

f = lambda x: max(0, x)
f_prime = lambda x: 1 if x > 0 else 0
data = [(0, 5), (2, 3), (5, 10)]

net = NeuralNet(weights, f, data, bias_node_indices)

plt.figure(0)
plt.scatter([point[0] for point in data], [point[1] for point in data], label='data')
x = list(range(7))
plt.plot(x, [net.predict(i) for i in x], label='initial regressor')

num_iterations = [1, 2, 5, 10, 25, 50, 100, 200, 500]
alpha = 0.001

rss = []
for i in num_iterations:
    net = NeuralNet(weights, f, data, bias_node_indices)
    net.gradient_desc(i, alpha, f_prime)
    rss.append(net.rss())

plt.plot(x, [net.predict(i) for i in x], label='final regressor')
plt.legend()
plt.savefig('nn/bp/bp_data_vs_initial_regressor_vs_final_regressor.png')

plt.figure(1)
plt.plot(num_iterations, rss)
plt.xlabel('num iterations')
plt.ylabel('rss')
plt.savefig('nn/bp/bp_num_iterations_vs_rss.png')