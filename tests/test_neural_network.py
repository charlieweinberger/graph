import sys
sys.path.append('src')
from neural_network import NeuralNetwork

edges = [
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 6),
    (4, 6),
    (5, 6)
]

bias_nodes = [2, 5]
nn = NeuralNetwork(edges, bias_nodes)
print(nn.get_paths(2))

data = [(0, 5), (2, 3), (5, 10)]
weights = [1 for _ in rage(len(edges))]
f = lambda x: max(0, x)
nn.fit(data, weights, f)