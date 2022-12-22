class Node():
    def __init__(self, index):
        self.index = index
        self.distance = None
        self.parents = []
        self.children = []

# To compute distances and shortest paths in a directed graph, you will use the same approach that you did in the plain old Graph, but instead of considering a node's neighbors each time, you will consider its children.

# Ex: edges = [(0,1),(1,2),(3,1),(4,3),(1,4),(4,5),(3,6)]

class DirectedGraph():

    def __init__(self, edges):
        self.edges = edges
        self.nodes = []
        self.build_from_edges()
    
    def get_node(self, index):
        for node in self.nodes:
            if node.index == index:
                return node

    def build_from_edges(self):

        self.nodes = [Node(self.edges[0][0])]

        for parent_index, child_index in self.edges:
            if child_index not in [n.index for n in self.nodes]:
                self.nodes.append(Node(child_index))
        
        for parent_index, child_index in self.edges:

            parent = self.get_node(parent_index)
            child = self.get_node(child_index)

            if child not in parent.children:
                parent.children.append(child)
            if parent not in child.parents:
                child.parents.append(parent)

    def nodes_breadth_first(self, starting_node_index):
        
        starting_node = self.nodes[starting_node_index]
        queue = [starting_node]
        visited = []
        
        while queue != []:

            current_node = queue[0]
            unvisited_children = [child for child in current_node.children if child not in queue + visited]
            # could sort unvisited_children to make answer more like Justin's answers

            del queue[0]
            queue += unvisited_children
            visited.append(current_node)
        
        return visited
    
    def nodes_depth_first(self, starting_node_index):
        
        starting_node = self.nodes[starting_node_index]
        stack = [starting_node]
        visited = []
        
        while stack != []:

            current_node = stack[0]
            unvisited_children = [child for child in current_node.children if child not in stack + visited]

            for child in unvisited_children:
                stack.insert(1, child)
            del stack[0]
            visited.append(current_node)
        
        return visited

    def set_breadth_first_distance_and_previous(self, starting_node_index):

        self.build_from_edges()
        self.nodes[starting_node_index].distance = 0
        starting_node = self.nodes[starting_node_index]
        queue = [starting_node]
        visited = []
        
        while queue != []:

            current_node = self.nodes[queue[0].index]
            unvisited_children = [child for child in current_node.children if child not in queue + visited]

            for child in unvisited_children:
                for node_index in range(len(self.nodes)):
                    self_node = self.nodes[node_index]
                    if child.index == self_node.index:
                        self.nodes[node_index].distance = current_node.distance + 1

            del queue[0]
            queue += unvisited_children
            visited += [current_node]

    def calc_distance(self, starting_node_index, ending_node_index):
        self.set_breadth_first_distance_and_previous(starting_node_index)
        for node in self.nodes:
            if node.index == ending_node_index:
                return node.distance

    def calc_shortest_path(self, starting_node_index, ending_node_index):

        self.set_breadth_first_distance_and_previous(starting_node_index)
        starting_node = self.nodes[starting_node_index]
        current_node = self.nodes[ending_node_index]
        visited = [current_node]

        while current_node.index != starting_node.index:
            
            current_node_changed = False
            for i in range(len(current_node.parents)):
                
                if current_node.parents[i].index != starting_node.index:
                    if current_node.parents[i].parents != []:
                        current_node = current_node.parents[i]
                        current_node_changed = True
                else:
                    current_node = current_node.parents[i]
                    current_node_changed = True

                if current_node_changed:
                    break

            if current_node in visited:
                return False
            visited.append(current_node)
        
        return [node.index for node in visited[::-1]]

# python tests/test_directed_graph.py