import matplotlib.pyplot as plt
plt.style.use('bmh')
from evolvingNN import *

def normalize_data(data):
    x, y = [point[0] for point in data], [point[1] for point in data]
    return [((px - min(x)) / (max(x) - min(x)), (2*(py - min(y)) / (max(y) - min(y))) - 1) for px, py in data]

data = normalize_data([
    (0.0, 7), (0.2, 5.6), (0.4, 3.56), (0.6, 1.23), (0.8, -1.03),
    (1.0, -2.89), (1.2, -4.06), (1.4, -4.39), (1.6, -3.88), (1.8, -2.64),
    (2.0, -0.92), (2.2, 0.95), (2.4, 2.63),  (2.6, 3.79), (2.8, 4.22),
    (3.0, 3.8), (3.2, 2.56), (3.4, 0.68), (3.6, -1.58), (3.8, -3.84),
    (4.0, -5.76), (4.2, -7.01), (4.4, -7.38), (4.6, -6.76), (4.8, -5.22)
])

num_nets = 30
node_layers = [1, 10, 6, 3, 1]
weight_range = [-0.2, 0.2]
mutation_rate = 0.05
evolvingNN = EvolvingNeuralNet(data, num_nets, tanh, node_layers, weight_range, mutation_rate)

graph_x = [x/1000 for x in range(0, 1000)]

plt.figure(0)
plt.scatter([point[0] for point in data], [point[1] for point in data])
for net in evolvingNN.nets:
    plt.plot(graph_x, [net.predict(x) for x in graph_x], color='blue')

generation_nums = [1, 2, 5, 10, 25, 50, 100, 200, 500, 1000, 1500, 2000, 2500]

avg_rss = []
for num in generation_nums:
    while evolvingNN.gen != num:
        evolvingNN.make_new_gen()
    avg_rss.append(evolvingNN.avg_rss())

for net in evolvingNN.nets:
    plt.plot(graph_x, [net.predict(x) for x in graph_x], color='red')
plt.savefig('nn/enn/enn_data_initial_regressor_vs_final_regressor.png')

plt.figure(1)
plt.plot(generation_nums, avg_rss)
plt.xlabel('# of generations')
plt.ylabel('average rss')
plt.savefig('nn/enn/enn_#_gens_vs_average_rss.png')