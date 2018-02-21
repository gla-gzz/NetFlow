class Grafo:
    def __init__(self):                          
        self.V = set()
        self.X = dict()
        self.Y = dict()
        self.size = dict()
        self.color = dict()
        self.vecinos = dict()
    def add_some(self, v):                      
        self.V.add(v)
        if not v in self.vecinos:
            self.vecinos[v] = set()
    def add_more(self, V, x, y, w, z):                
        self.X[V] = x
        self.Y[V] = y
        self.size[V] = w
        self.color[V] = z
        

