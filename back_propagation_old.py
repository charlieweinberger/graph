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

rows = [[1, 2], [3, 4, 5], [6]]
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

        for node_index in node_list:

            if node_index in bias_nodes:
                i[node_index] = 1
            elif node_index in rows[0]:
                i[node_index] = point[0]
            else:
                i[node_index] = sum(weights[(a, b)] + f(i[a]) for a, b in initial_weights if node_index == b)

        inputs[point] = i
    
    return inputs

def final_node_output(weights, x):
    return f(get_inputs(weights, input_data=[(x, None)])[(x, None)][num_nodes])

inputs = get_inputs(initial_weights)
outputs = {point:{index:f(i) for index, i in inputs[point].items()} for point in data}

# calculating neural gradients

dRSS_dn = {x:0 for x in node_list}
dRSS_dn[num_nodes] = sum(2 * (outputs[point][num_nodes] - point[1]) for point in data)

for index in node_list[0:-1][::-1]:
    rows_index = [x for x, row in enumerate(rows) if index in row][0]
    for point in data:
        for index_above in rows[rows_index + 1]:
            if index_above in bias_nodes: continue
            dRSS_dn[index] += dRSS_dn[index_above] * f_prime(inputs[point][index_above]) * initial_weights[(index, index_above)]

# for point in data:
#     dRSS_dn[5] += dRSS_dn[6] * f_prime(inputs[point][6]) * initial_weights[(5, 6)]
#     dRSS_dn[4] += dRSS_dn[6] * f_prime(inputs[point][6]) * initial_weights[(4, 6)]
#     dRSS_dn[3] += dRSS_dn[6] * f_prime(inputs[point][6]) * initial_weights[(3, 6)]
    
# for point in data:
#     dRSS_dn[2] += dRSS_dn[3] * f_prime(inputs[point][3]) * initial_weights[(2, 3)] + dRSS_dn[4] * f_prime(inputs[point][4]) * initial_weights[(2, 4)]
#     dRSS_dn[1] += dRSS_dn[3] * f_prime(inputs[point][3]) * initial_weights[(1, 3)] + dRSS_dn[4] * f_prime(inputs[point][4]) * initial_weights[(1, 4)]

# calculating weight gradients

dRSS_dw = {pair:0 for pair in initial_weights}

for a, b in initial_weights:
    for point in data:
        dRSS_dw[(a, b)] += dRSS_dn[b] * f_prime(inputs[point][b]) * outputs[point][a]

# gradient descent

def calc_rss(weights):
    rss = 0
    for x, y in data:
        rss += (final_node_output(weights, x) - y) ** 2
    return rss

def gradient_descent(weights, num_iterations, alpha):
    for _ in range(num_iterations):
        weights = {pair:weight - alpha * dRSS_dw[pair] for pair, weight in weights.items()}
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

x_list = list(range(num_nodes + 1))

initial_y_list = [final_node_output(initial_weights, x) for x in x_list]
plt.plot(x_list, initial_y_list, label='initial regressor')

final_weights = gradient_descent(initial_weights, 1000, alpha)
final_y_list = [final_node_output(final_weights, x) for x in x_list]
plt.plot(x_list, final_y_list, label='final regressor')

plt.legend()
plt.savefig('bp_data_vs_initial_regressor_vs_final_regressor.png')