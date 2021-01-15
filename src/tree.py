class Node():
    def __init__(self, value):
        self.value = value
        self.children = []

# nodes_breadth_first and nodes_depth_first aren't perfect, because the order of each node's children in get_chilren is off (b/c the order in the original edges array is weird)

class Tree():

    def __init__(self, edges):
        self.edges = edges
        self.root = Node(self.get_root()[0])
    
    def get_children(self, parent):
        return [Node(pair[1]) for pair in self.edges if pair[0] == parent]
    def get_parents(self, child):
        return [Node(pair[0]) for pair in self.edges if pair[1] == child]
    def get_root(self):
        children = [pair[1] for pair in self.edges]
        ans = []
        for pair in self.edges:
            if (pair[0] not in children) and (pair[0] not in ans):
                ans.append(pair[0])
        return ans
    def build_from_edges(self):
        
        node_array = [self.root]
        while len(node_array) != 0:
            child_array = []
            for node in node_array:
                new_children = self.get_children(node.value)
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