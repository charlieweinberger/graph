class Node():
    def __init__(self, value, index):
        self.value = value
        self.children = []
        self.index = index

# nodes_breadth_first and nodes_depth_first might not work because they are still based on an input of the value, not the index

class Tree():

    def __init__(self, edges, node_values):
        self.edges = edges
        self.tops = [pair[0] for pair in self.edges]
        self.bottoms = [pair[1] for pair in self.edges]
        
        self.node_values = node_values
        self.edges_values = [[self.node_values[i] for i in pair] for pair in self.edges]        
        
        self.root = self.get_root()

    def get_children(self, parent):
        ans = []
        for pair in self.edges:
            if pair[0] == parent:
                node_index = pair[1]
                node_value = self.node_values[node_index]
                node = Node(node_value, node_index)
                ans.append(node)
        return ans
    
    def get_parents(self, child):
        return [Node(pair[0], self.node_values.index(pair[0])) for pair in self.edges_values if pair[1] == child]
    
    def get_root(self):
        
        for top in self.tops:
            if top not in self.bottoms:
                head_index = top

        head_value = self.node_values[head_index]
        head_node = Node(head_value, head_index)
        return head_node
    
    def build_from_edges(self):
        
        node_array = [self.root]
        while len(node_array) != 0:
            
            child_array = []
            for node in node_array:
                new_children = self.get_children(node.index)
                node.children = new_children
                child_array += new_children
            
            node_array = list(child_array)

    def nodes_breadth_first(self):
        queue = [self.root]
        visited = []

        while len(queue) > 0:
            visited.append(queue[0])
            if queue[0].children != None:
                for child in queue[0].children:
                    queue.append(child)
            del queue[0]
        
        return visited
    
    def nodes_depth_first(self):
        stack = [self.root]
        visited = []

        while len(stack) > 0:
            visited.append(stack[0])
            if stack[0].children[::-1] != None:
                for child in stack[0].children[::-1]:
                    stack.insert(1, child)
            del stack[0]
        
        return visited