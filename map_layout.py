import random

class Vertex:
    """
    A vertex of the graph (a location on the toontown map).
    Keeps track of name of the vertex, its neighbors, and if the
    vertex is a playground.
    """
    def __init__(self, _node_name, _sprite_location, _playground):
        self.node_name = _node_name
        # self.sprite_location = _sprite_location # for pygame if needed
        self.neighbors = set()
        self.is_playground = _playground

    def add_neighbor(self, neighbor):
        """
        Add a neighbor to the vertex,
        """
        self.neighbors.add(neighbor)

    def get_neighbor(self):
        """
        Return a set of neighbors for this vertex.
        """
        return self.neighbors

    def get_name(self):
        """
        Return the name for this vertex.
        """
        return self.node_name
    
    def __str__(self):
        """
        str operator overload. Just returns the name of the vertex.
        """
        return self.node_name

    def get_info_tip(self):
        """
        Returns a formatted string for the vertex.
        Returns a - delimited string of each neighbor to this
        vertex.
        """
        return "--- {} ".format(''.join(["{} - ".format(nieghbor.node_name) for nieghbor in self.neighbors])[:-3])
    
    def __len__(self):
        """
        Length operator overload.
        Returns the number of neighbors this vertex has.
        """
        return len(self.neighbors)



class Toontown_Map:
    """
    The map (graph) of the full toontown map.
    """
    def __init__(self):
        """
        CONSTRUCTOR
        """
        self.vertices = {} # Dictionary --> Key: Vertex name --> Value: Vertex
        self.num_vertices = 0 # Number of vertices
        self.__initialize_map() # Initialize our map.
    
    def __initialize_map(self):
        """
        Prime our graph with the actual toontown map.
        Each element in the list is a tuple of tuples.
            The first element of the tuple if the source vertex.
            The second element is a list of each vertex that the source has a path to.
            The boolean (True/False) is to tell the node/vertex if that node/vertex is a playground or not.
        """
        nodes_and_neighbors =[
            (("Toontown Central", True), [("Silly Street", False), ("Loopy Lane", False), ("Punchline Place", False), ("Goofy Speedway", True)]),
            (("Donald\'s Dock", True), [("Barnacle Boulevard", False), ("Seaweed Street", False), ("Lighthouse Lane", False), ("Chip \'n Dale\'s Acorn Acres", True)]),
            (("Daisy Gardens", True), [("Elm Street", False), ("Maple Street", False), ("Oak Street", False)]),
            (("Minnie's Melodyland", True), [("Tenor Terrace", False), ("Alto Avenue", False), ("Baritone Boulevard", False)]),
            (("The Brrrgh", True), [("Sleet Street", False), ("Polar Place", False), ("Walrus Way", False)]),
            (("Donald\'s Dreamland", True), [("Lullaby Lane", False), ("Pajama Place", False)]),
            (("Goofy Speedway", True), [("Toontown Central", True)]),
            (("Chip \'n Dale\'s Acorn Acres", True), [("Donald\'s Dock", True), ("Chip \'n Dale\'s MiniGolf", True)]),
            (("Sellbot Headquarters", False), [("Oak Street", False)]),
            (("Cashbot Headquarters", False), [("Pajama Place", False)]),
            (("Lawbot Headquarters", False), [("Polar Place", False)]),
            (("Bossbot Headquarters", False), [("Chip \'n Dale\'s MiniGolf", True), ("Chip \'n Dale\'s Acorn Acres", True)]),
            (("Chip \'n Dale\'s MiniGolf", True), [("Bossbot Headquarters", False)]),
            (("Silly Street", False), [("Toontown Central", True), ("Elm Street", False)]), 
            (("Loopy Lane", False), [("Toontown Central", True), ("Alto Avenue", False)]),
            (("Punchline Place", False), [("Toontown Central", True), ("Barnacle Boulevard", False)]),
            (("Barnacle Boulevard", False), [("Donald\'s Dock", True), ("Punchline Place", False)]),
            (("Seaweed Street", False), [("Donald\'s Dock", True), ("Maple Street", False)]),
            (("Lighthouse Lane", False), [("Donald\'s Dock", True), ("Walrus Way", False)]),
            (("Elm Street", False), [("Daisy Gardens", True), ("Silly Street", False)]),
            (("Maple Street", False), [("Daisy Gardens", True), ("Seaweed Street", False)]),
            (("Oak Street", False), [("Daisy Gardens", True), ("Sellbot Headquarters", False)]),
            (("Tenor Terrace", False), [("Minnie's Melodyland", True), ("Lullaby Lane", False)]),
            (("Alto Avenue", False), [("Minnie's Melodyland", True), ("Loopy Lane", False)]),
            (("Baritone Boulevard", False), [("Minnie's Melodyland", True), ("Sleet Street", False)]),
            (("Sleet Street", False), [("The Brrrgh", True), ("Baritone Boulevard", False)]),
            (("Polar Place", False), [("The Brrrgh", True), ("Lawbot Headquarters", False)]),
            (("Walrus Way", False), [("The Brrrgh", True), ("Lighthouse Lane", False)]),
            (("Lullaby Lane", False), [("Donald\'s Dreamland", True), ("Tenor Terrace", False)]),
            (("Pajama Place", False), [("Donald\'s Dreamland", True), ("Cashbot Headquarters", False)])
        ]
        for vert, neighbors in nodes_and_neighbors:
            for neighbor in neighbors:
                # For each vertex and all its neighbors
                # Create an edge.
                self.add_edge(vert, neighbor)

    def add_vertex(self, _node, _sprite_location=[0, 0]):
        """
        Adds the passed in vertex to the vertex list.
        """
        self.num_vertices = self.num_vertices + 1
        newVertex = Vertex(_node[0], _sprite_location, _node[1])
        self.vertices[_node[0]] = newVertex
        return newVertex

    def get_vertex(self, _name):
        """
        Returns the vertex for the passed in name.
        Returns None if it was not found.
        """
        if _name in self.vertices:
            return self.vertices[_name]
        else:
            return None

    def __contains__(self, _name):
        """
        Overload operator for the 'in' keyword.
        """
        return _name in self.vertices

    def add_edge(self, _from, _to):
        """
        Creates an edge from vertex _from to vertex _to.
        """
        if _from[0] not in self.vertices: # The [0] index is the name of the vertex. [1] is a boolean value for if it is a playground
            self.add_vertex(_from)
        if _to[0] not in self.vertices:
            self.add_vertex(_to)
        self.vertices[_from[0]].add_neighbor(self.vertices[_to[0]])

    def get_vertices(self):
        """
        Returns a list of vertice names. (i.e. road names and playground names)
        """
        return self.vertices.keys()

    def __iter__(self):
        """
        Iterator operator overload.
        Iterates over each vertex.
        """
        return iter(self.vertices.values())
    
    def get_random_nodes(self, _pick=1, _playground=False, _exclude=set()):
        """
        Return a list of random vertices.
        Input: 
            _pick: Number of vertices (roads and playgrounds) to pick from teh map
            _playground: True/False. If we want to include playgrounds in our selection.
            _exclude: A set of vertices we do not want.
        """
        new_locations = random.sample([x for x in list(self.vertices.values()) if not x.is_playground and x not in _exclude], _pick)
        return new_locations


