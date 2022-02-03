import matplotlib.pyplot as plt
plt.style.use('bmh')

# information

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

num_nodes = max(elem for pair in initial_weights for elem in pair)

f = lambda x: max(0, x)
f_prime = lambda x: 0 if x <= 0 else 1

# fitting the data

def get_inputs(weights, input_data=data):

    inputs = {}

    for point in input_data:

        i = {k:[] for k in range(1, num_nodes + 1)}

        i[1] = point[0]
        i[2] = 1
        i[3] = weights[(1, 3)] * f(i[1]) + weights[(2, 3)] * f(i[2])
        i[4] = weights[(1, 4)] * f(i[1]) + weights[(2, 4)] * f(i[2])
        i[5] = 1
        i[6] = weights[(3, 6)] * f(i[3]) + weights[(4, 6)] * f(i[4]) + weights[(5, 6)] * f(i[5])

        inputs[point] = i
    
    return inputs

def n_6(weights, x):
    return f(get_inputs(weights, input_data=[(x, 0)])[(x, 0)][6])

# partial RSS derivatives

def bottom_row_dRSS_dw(a, b, weights):
    dRSS = 0
    for point, i in get_inputs(weights).items():
        dRSS += 2 * (f(i[6]) - point[1]) * f_prime(i[6]) * weights[(b, 6)] * f_prime(i[b]) * f(i[a])
    return dRSS

def middle_row_dRSS_dw(a, weights):
    dRSS = 0
    for point, i in get_inputs(weights).items():
        dRSS += 2 * (f(i[6]) - point[1]) * f_prime(i[6]) * f(i[a])
    return dRSS

def dRSS_dw(a, b, weights):
    if a in [1, 2]: return bottom_row_dRSS_dw(a, b, weights)
    else: return middle_row_dRSS_dw(a, weights)

# gradient descent

def calc_rss(weights):
    rss = 0
    for point in data:
        rss += (n_6(weights, point[0]) - point[1])**2
    return rss

def gradient_descent(weights, num_iterations, alpha):
    for _ in range(num_iterations):
        weights = {k:v - alpha*dRSS_dw(k[0], k[1], weights) for k, v in weights.items()}
    return weights

# running gradient descent

num_iterations = [1, 2, 5, 10, 50, 100, 200, 500, 1000]
alpha = 0.001
rss = [calc_rss(gradient_descent(initial_weights, n, alpha)) for n in num_iterations]

# plotting

# plot 1

plt.figure(0)
plt.plot(num_iterations, rss)
plt.xlabel('num_iterations')
plt.ylabel('rss')
plt.savefig('num_iterations_vs_rss.png')

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
plt.savefig('data_vs_initial_regressor_vs_final_regressor.png')