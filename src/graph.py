class Node():
    def __init__(self, index):
        self.index = index
        self.value = None
        self.neighbors = []

class Graph():

    def __init__(self, edges):
        self.edges = edges
        self.nodes = []
    
    def indices(self, input_list):
        return [node.index for node in input_list]
    
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

    def get_nodes_breadth_first(self, starting_index):

        queue = [self.nodes[starting_index]]
        visited = []
        
        while queue != []:

            current_node = queue[0]
            current_neighbors = self.get_neighbors(current_node)
 
            unvisited_neighbors = []
            for neighbor in current_neighbors:
                queue_plus_visited = self.indices(queue) + self.indices(visited)
                if neighbor.index not in queue_plus_visited:
                    unvisited_neighbors.append(neighbor)

            del queue[0]
            queue += unvisited_neighbors
            visited.append(current_node)
        
        return visited
    
    def get_nodes_depth_first(self, starting_index):

        stack = [self.nodes[starting_index]]
        visited = []
        
        while stack != []:

            current_node = stack[0]
            current_neighbors = self.get_neighbors(current_node)

            unvisited_neighbors = []
            for neighbor in current_neighbors:
                stack_plus_visited = self.indices(stack) + self.indices(visited)
                if neighbor.index not in stack_plus_visited:
                    unvisited_neighbors.append(neighbor)

            for neighbor in unvisited_neighbors:
                stack.insert(1, neighbor)
            del stack[0]
            visited.append(current_node)
        
        return visited