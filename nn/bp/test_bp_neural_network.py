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

# num_iterations_list = [1, 2, 5, 10, 50, 100, 200, 500]
num_iterations_list = [3]
alpha = 0.001

nn = NeuralNetwork(pairs, initial_weights, bias_nodes)
nn.fit(data, f, f_prime)
nn.calc_inputs()
nn.calc_dRSS_dn()
nn.calc_dRSS_dw()

nn.run_gradient_descent(num_iterations_list)

# rss_list = [self.calc_rss(self.gradient_descent(self.copy_dict(self.initial_weights), n, alpha)) for n in num_iterations_list]

# rss_list = []

# for n in num_iterations_list:
#     weights = copy_dict(self.initial_weights)
#     print_dict(self.initial_weights)
#     gradient_desc = self.gradient_descent(weights, n, alpha)
#     rss = self.calc_rss(gradient_desc)
#     rss_list.append(rss)

# # plot 1

# plt.figure(0)
# plt.plot(num_iterations_list, rss_list)
# plt.xlabel('num_iterations')
# plt.ylabel('rss')
# plt.savefig('bp_num_iterations_vs_rss.png')

# plot 2

# plt.figure(2)
# plt.scatter([point[0] for point in self.data], [point[1] for point in self.data], label='data')

# x_list = list(range(self.num_nodes + 1))

# initial_y_list = [self.predict(self.initial_weights, x) for x in x_list]
# plt.plot(x_list, initial_y_list, label='initial regressor')

# final_weights = self.gradient_descent(self.initial_weights, 1000, alpha)
# final_y_list = [self.predict(final_weights, x) for x in x_list]
# plt.plot(x_list, final_y_list, label='final regressor')

# plt.legend()
# plt.savefig('bp_data_vs_initial_regressor_vs_final_regressor.png')

# print('done')