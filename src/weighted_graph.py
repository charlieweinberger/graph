import sys
sys.path.append('src')
from graph import *

class Node():
    def __init__(self, index):
        self.index = index
        self.value = None
        self.d_value = 99999999
        self.neighbors = []

# python tests/test_weighted_graph.py

class WeightedGraph():

    def __init__(self, weights, vertex_values):
        self.weights = weights
        self.vertex_values = vertex_values
        self.nodes = None
        self.edges = None
        self.edge_weights_list = None
        self.build_from_edges()
    
    def find_indices(self, input_list):
        return [node.index for node in input_list]
    def same_node_as(self, node1, node2):
        return node1.index == node2.index
    def if_node_in(self, node, node_list):
        return node.index in self.find_indices(node_list)

    def build_from_edges(self):
        
        self.edges = list(self.weights.keys())
        self.edge_weights_list = list(self.weights.values())

        indices = []
        for pair in self.edges:
            for index in pair:
                if index not in indices:
                    indices.append(index)
        
        self.nodes = [Node(index = i) for i in sorted(indices)]

        for node in self.nodes:
            
            node_index = self.nodes.index(node)
            node.value = self.vertex_values[node_index]

            for pair in self.edges:
                if node.index in pair:
                    other_elem = [elem for elem in pair if elem != node.index][0]
                    node_elem = self.nodes[other_elem]
                    node.neighbors.append(node_elem)

    def set_d_values(self, starting_node_index):

        self.nodes[starting_node_index].d_value = 0
        starting_node = self.nodes[starting_node_index]
        current_node = starting_node
        visited = []

        while len(visited) != len(self.nodes):

            unvisited_neighbors = [neighbor for neighbor in current_node.neighbors if neighbor not in visited]

            for neighbor in unvisited_neighbors:  
                
                pair = (current_node.index, neighbor.index)
                if pair not in self.edges:
                    pair = (neighbor.index, current_node.index)
                new_possible_d_value = current_node.d_value + self.weights[pair]

                if new_possible_d_value < neighbor.d_value:
                    neighbor.d_value = new_possible_d_value
                
            if current_node not in visited:
                visited.append(current_node)
            
            d_values_list = [node.d_value for node in unvisited_neighbors]
            
            for node in unvisited_neighbors:
                if node.d_value == min(d_values_list) and node not in visited:
                    current_node = node

            if unvisited_neighbors == []:
                for node in current_node.neighbors:
                    if node in visited:
                        current_node = node
    
    def calc_distance(self, starting_node_index, ending_node_index):
        self.set_d_values(starting_node_index)
        for node in self.nodes:
            if self.same_node_as(node, self.nodes[ending_node_index]):
                return node.d_value

    def calc_shortest_path(self, starting_node_index, ending_node_index):

        self.set_d_values(starting_node_index)

        edge_list = []
        for edge in self.edges:
            d_value_diff = abs(self.nodes[edge[1]].d_value - self.nodes[edge[0]].d_value)
            if d_value_diff == self.weights[edge]:
                edge_list.append(edge)

        graph = Graph(edge_list)
        graph_shortest_path = graph.calc_shortest_path(starting_node_index, ending_node_index)
        return graph_shortest_path