class Node():
    def __init__(self, index):
        self.index = index
        self.value = None
        self.distance = None
        self.previous = None
        self.neighbors = []

# might have to redo everything so that the class sorts by looking at nodes in self.nodes, not indices

class Graph():

    def __init__(self, edges):
        self.edges = edges
        self.nodes = []
        self.indices = []
    
    def find_indices(self, input_list):
        return [node.index for node in input_list]
    
    def same_node_as(self, node1, node2):
        return True if node1.index == node2.index else False

    def if_node_in(self, node, node_list):
        return True if node.index in self.find_indices(node_list) else False
    
    def get_neighbors(self, node):
        neighbors = []
        for pair in self.edges:
            if node.index in pair:
                for elem in pair:
                    if elem != node.index:
                        neighbor = Node(elem)
                        neighbors.append(neighbor)
        return neighbors
    
    def build_from_edges(self):

        indices = []
        for pair in self.edges:
            for index in pair:
                if index not in indices:
                    indices.append(index)
        
        self.nodes = [Node(index = i) for i in indices]

        for pair in self.edges:
            for index in pair:
                neighbor_index = [num for num in pair if num != index][0]
                self.nodes[index].neighbors.append(neighbor_index)
        
        self.indices = self.find_indices(self.nodes)

    def get_nodes_breadth_first(self, starting_node_index):

        starting_node = self.nodes[starting_node_index]
        queue = [starting_node]
        visited = []
        
        while queue != []:

            current_node = queue[0]
            current_neighbors = self.get_neighbors(current_node)
            unvisited_neighbors = [neighbor for neighbor in current_neighbors if not self.if_node_in(neighbor, queue + visited)]

            del queue[0]
            queue += unvisited_neighbors
            visited.append(current_node)
        
        return visited
    
    def get_nodes_depth_first(self, starting_node_index):

        starting_node = self.nodes[starting_node_index]
        stack = [starting_node]
        visited = []
        
        while stack != []:

            current_node = stack[0]
            current_neighbors = self.get_neighbors(current_node)

            unvisited_neighbors = [neighbor for neighbor in current_neighbors if not self.if_node_in(neighbor, stack + visited)]

            for neighbor in unvisited_neighbors:
                stack.insert(1, neighbor)
            del stack[0]
            visited.append(current_node)
        
        return visited
    
    def set_breadth_first_distance_and_previous(self, starting_node_index):

        self.build_from_edges()
        starting_node = self.nodes[starting_node_index]
        starting_node.distance = 0
        queue = [starting_node]
        visited = []
        
        while queue != []:

            current_node = self.nodes[queue[0].index]
            current_neighbors = self.get_neighbors(current_node)
            unvisited_neighbors = [neighbor for neighbor in current_neighbors if not self.if_node_in(neighbor, queue + visited)]

            for neighbor in unvisited_neighbors:
                for node_index in range(len(self.nodes)):
                    self_node = self.nodes[node_index]
                    if self.same_node_as(neighbor, self_node) and self_node.previous == None:
                        self.nodes[node_index].previous = current_node
                        self.nodes[node_index].distance = current_node.distance + 1

            del queue[0]
            queue += unvisited_neighbors
            visited += [current_node]
    
    def calc_distance(self, starting_node_index, ending_node_index):
        self.set_breadth_first_distance_and_previous(starting_node_index)
        for node in self.nodes:
            if self.same_node_as(node, self.nodes[ending_node_index]):
                return node.distance
    
    def calc_shortest_path(self, starting_node_index, ending_node_index):

        self.set_breadth_first_distance_and_previous(starting_node_index)
        starting_node = self.nodes[starting_node_index]
        current_node = self.nodes[ending_node_index]
        visited = [current_node]

        while not self.same_node_as(current_node, starting_node):
            current_node = current_node.previous
            visited.append(current_node)
        
        return self.find_indices(visited[::-1])