
# Create a Vertex class to be used with the Graph class
class Vertex:
    def __init__(self, label, address):
        self.label = label
        # ADDING THE ADDRESS OF THE VERTEX TO COMPARE WITH PACKAGE DELIVERT ADDRESS
        self.address = address
        self.distance = float('inf')
        self.next = None
        self.visited = False

    def __repr__(self):
        return self.label

    def vertex_visited(self, visited):
        self.visited = visited

# Graph class is used to create a graph using vertex instances.  Has the ability
# to add a vertex, add a directed edge, or add an undirected edge to the graph object.
class Graph:
    def __init__(self):
        # holds vertex objects of neighboring vertices
        self.neighbor_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.neighbor_list[new_vertex] = []

    def add_directed_edge(self, start_vertex, end_vertex, weight = 1.0):
        self.edge_weights[(start_vertex, end_vertex)] = weight
        self.neighbor_list[start_vertex].append(end_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight = 1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def get_vertex_by_label(self, search_key):
        for key in self.neighbor_list.keys():
            if key.label == search_key:
                return key

    def get_vertex_by_address(self, search_key):
        for key in self.neighbor_list.keys():
            if key.address[0] == search_key:
                return key
        print('vertex not found')

    def get_edge_weight(self, start_vertex, end_vertex):
        for vertex, edge_distance in sorted(self.edge_weights.items(), key=lambda kv: kv[1]):
            if vertex[0] == end_vertex and vertex[1] == start_vertex:
                return edge_distance

    def get_vertices(self):
        return [i for i in self.neighbor_list]