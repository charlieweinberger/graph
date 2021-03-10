class Node():
    def __init__(self, index):
        self.index = index
        self.value = None
        self.distance = None
        self.previous = None
        self.neighbors = []

class Graph():

    def __init__(self, edges):
        self.edges = edges
        self.nodes = []
    
    def if_node_in(self, node, node_list):
        return node.index in [node.index for node in node_list]
    
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
        
        self.nodes = [Node(index = i) for i in sorted(indices)]

        for pair in self.edges:
            for index in pair:
                neighbor_index = [num for num in pair if num != index][0]
                self.nodes[index].neighbors.append(neighbor_index)
    
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
        self.nodes[starting_node_index].distance = 0
        queue = [self.nodes[starting_node_index]]
        visited = []

        while queue != []:
            
            current_node = self.nodes[queue[0].index]
            current_dist = current_node.distance
            
            queue = queue[1:]
            visited.append(current_node)

            current_neighbors = [self.nodes[neighbor] for neighbor in current_node.neighbors]
            unvisited_neighbors = [neighbor for neighbor in current_neighbors if not self.if_node_in(neighbor, queue + visited)]
            
            for neighbor in unvisited_neighbors:
                neighbor.distance = current_dist + 1
                neighbor.previous = current_node

            queue += unvisited_neighbors
    
    def calc_distance(self, starting_node_index, ending_node_index):
        self.set_breadth_first_distance_and_previous(starting_node_index)
        for node in self.nodes:
            if node.index == ending_node_index:
                return node.distance
    
    def calc_shortest_path(self, starting_node_index, ending_node_index):

        self.set_breadth_first_distance_and_previous(starting_node_index)
        current_node = self.nodes[ending_node_index]
        visited = [ending_node_index]

        while current_node.index != starting_node_index:
            current_node = current_node.previous
            visited.append(current_node.index)
        
        return visited[::-1]