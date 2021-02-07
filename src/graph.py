class Node():
    def __init__(self, index):
        self.index = index

class Graph():

    def __init__(self, edges):
        self.edges = edges

    def get_nodes_breadth_first(self, num):
        queue = [num]
        visited = []

        while queue != []:
            
            current_node = queue[0]
            
            unvisited_neighbors = []
            for pair in self.edges:
                if current_node in pair:
                    neighbor = [num for num in pair if num != current_node][0]
                    if neighbor not in (queue + visited):
                        unvisited_neighbors.append(neighbor)
        
            del queue[0]
            for neighbor in unvisited_neighbors:
                queue.append(neighbor)
            visited.append(current_node)

        return [Node(index) for index in visited]
    
    def get_nodes_depth_first(self, num):
        stack = [num]
        visited = []

        while stack != []:
            
            current_node = stack[0]
            
            unvisited_neighbors = []
            for pair in self.edges:
                if current_node in pair:
                    neighbor = [num for num in pair if num != current_node][0]
                    if neighbor not in (stack + visited):
                        unvisited_neighbors.append(neighbor)
        
            for neighbor in unvisited_neighbors:
                stack.insert(1, neighbor)
            del stack[0]
            visited.append(current_node)

        return [Node(index) for index in visited]