import matplotlib.pyplot as plt
plt.style.use('bmh')

# info given

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
rows = [[1, 2], [3, 4, 5], [6]] # eventually turn into a function
num_nodes = max(elem for pair in initial_weights for elem in pair)
nodes = list(range(1, num_nodes + 1))

data = [(0, 5), (2, 3), (5, 10)]
f = lambda x: max(0, x)
f_prime = lambda x: 0 if x <= 0 else 1

# calculating inputs and outputs

def get_inputs(weights, input_data=data):

    inputs = {}

    for point in input_data:

        i = {}

        for node_index in nodes:

            if node_index in bias_nodes:
                i[node_index] = 1
            elif node_index in rows[0]:
                i[node_index] = point[0]
            else:
                i[node_index] = sum(weights[(a, b)] + f(i[a]) for a, b in initial_weights if node_index == b)

        inputs[point] = i
    
    return inputs

inputs = get_inputs(initial_weights)
outputs = {pair:{index:f(i) for index, i in inputs[pair].items()} for pair in data}

# calculating neural gradients

dRSS_dn = {x:None for x in nodes}

# look at paper, but loop through all points

dRSS_dn[6] = sum(2 * (outputs[pair][6] - pair[1]) for pair in data)

# initial weights = 1

# dRSS_dn_5 = dRSS_dn[6] * f_prime(...) * initial_weights[...]
# dRSS_dn_5 = dRSS_dn[6] * 1 * 1
dRSS_dn[5] = dRSS_dn[6]
dRSS_dn[4] = dRSS_dn[6]
dRSS_dn[3] = dRSS_dn[6]

dRSS_dn[2] = dRSS_dn[3] + dRSS_dn[4]
dRSS_dn[1] = dRSS_dn[3] + dRSS_dn[4]

# calculating weight gradients

dRSS_dw = {}

for pair in initial_weights:
    
    a, b = pair
    
    # dRSS_dw[pair] = dRSS_dn[b] * f_prime(...) * n_a
    # dRSS_dw[pair] = dRSS_dn[b] * 1 * n_a
    dRSS_dw[pair] = dRSS_dn[b] * f()

# gradient descent

def calc_rss(weights):
    rss = 0
    for pair in data:
        rss += (n_6(weights, pair[0]) - pair[1])**2
    return rss

def gradient_descent(weights, num_iterations, alpha):
    for _ in range(num_iterations):
        weights = {pair:weight - alpha * dRSS_values[pair] for pair, weight in weights.items()}
    return weights

# running gradient descent

num_iterations = [1, 2, 5, 10, 50, 100, 200]
alpha = 0.001
rss = [calc_rss(gradient_descent(initial_weights, n, alpha)) for n in num_iterations]

# plotting

# plot 1

plt.figure(0)
plt.plot(num_iterations, rss)
plt.xlabel('num_iterations')
plt.ylabel('rss')
plt.savefig('bp_num_iterations_vs_rss.png')

# plot 2

plt.figure(2)
plt.scatter([point[0] for point in data], [point[1] for point in data], label='data')

x_list = list(range(7))

initial_y_list = [n_6(initial_weights, x) for x in x_list]
plt.plot(x_list, initial_y_list, label='initial regressor')

final_weights = gradient_descent(initial_weights, 1000, alpha)
final_y_list = [n_6(final_weights, x) for x in x_list]
plt.plot(x_list, final_y_list, label='final regressor')

plt.legend()
plt.savefig('bp_data_vs_initial_regressor_vs_final_regressor.png')