#Max Flow and Shortest Path Algorithms
#Homework No.3
class Grafo:
    def __init__(self):                             #Initialices graph             
        self.N = set()
        self.X = dict()
        self.Y = dict()
        self.size = dict()
        self.color = dict()
        self.vecinos = dict()  
        self.E = dict()

    def add_some(self, n, x=0, y=0, w=0, z=0):      #Adds a node and it's info to the graph
        self.N.add(n)              
        self.X[n] = x
        self.Y[n] = y
        self.size[n] = w
        self.color[n] = z
        if not n in self.vecinos:
            self.vecinos[n] = set()

    def connect_these(self, a, b, peso=1):          #Conects given nodes
        self.E[(a, b)] = self.E[(b, a)] = peso
        self.vecinos[a].add(b)
        self.vecinos[b].add(a)

    def complement_me(self):                        #Complement of the links in the graph
        comp = Grafo()
        for n in self.N:
            for m in self.N:
                if n != m and (n, m) not in self.E:
                    comp.add_some(n, self.X[n], self.Y[n], self.size[n], self.color[n])
                    comp.add_some(m, self.X[m], self.Y[m], self.size[m], self.color[m])
                    comp.connect_these(n, m)
        return comp

    def saveme_to(self, saving = "data.dat"):       #Saves the data of the graph to a file
        with open(saving, 'w') as archivo:
            for n in self.N:
                print(self.X[n], self.Y[n], self.size[n], self.color[n], sep = ' ', file=archivo)

    def connectme_by(self, choice, mode = 's'):     #Connects the nodes of the graph based in a parameter
       import pandas as pd
       modes =['s', 'p']
       if mode not in modes:
           raise ValueError ("Invalid connecting mode! Expected one of: %s " % modes)
       nodes = pd.DataFrame({
               'X' : self.X,
               'Y' : self.Y,
               'Size' : self.size,
               'Color' : self.color})
       nodes = nodes[['X', 'Y', 'Size', 'Color']]
       nodes = nodes.sort_values(by=[choice])
       x = nodes.index
       y = x.tolist()
       k = 0.5
       for n in range(len(y)-1):
           if mode is 's':
               self.connect_these(y[n], y[n+1])
           if mode is 'p':    
               diff_nodes = (self.color[y[n+1]] - self.color[y[n]])
               if diff_nodes <= 0.03:
                   self.connect_these(y[n], y[n+1], k)
               if 0.03 < diff_nodes <= 0.07:
                   k += 0.5
                   self.connect_these(y[n], y[n+1], k)
               if diff_nodes > 0.07:
                   k += 1
                   self.connect_these(y[n], y[n+1], k)
       return y

    def plotme_in(self, listing, saving, saving2 = "script.dat", mode = 's'):           #Generates the script to plot the data
        modes =['s', 'd']
        if mode not in modes:
           raise ValueError ("Invalid connecting mode! Expected one of: %s " % modes)
        with open(saving2, 'w') as archivo:
            print("set key off", file=archivo)
            print("set xrange [-0.1:1.1]", file=archivo)
            print("set yrange [-0.1:1.1]", file=archivo)
            if mode is 's':
                print("set palette model RGB", file=archivo)
                print("set palette rgbformulae 3, 11, 6", file=archivo)
                for n in range(len(listing)-1):
                    print("set arrow ", n+1, " from ", self.X[listing[n]], ",", self.Y[listing[n]], " to ", self.X[listing[n+1]], ",", self.Y[listing[n+1]], end=" ", file=archivo)
                    print("nohead back lw ", self.E[(listing[n], listing[n+1])], " lc \"black\" ", file=archivo)
                print("plot \"" + saving + "\" u 1:2:($3*10):4 w points pt 7 ps var palette", file=archivo)
            if mode is 'd':
                print("set palette model HSV", file=archivo)
                print("set palette rgbformulae 3, 2, 2", file=archivo)
                for n in range(len(listing)-1):
                    print("set arrow ", n+1, " from ", self.X[listing[n]], ",", self.Y[listing[n]], " to ", self.X[listing[n+1]], ",", self.Y[listing[n+1]], end=" ", file=archivo)
                    print("head filled size screen 0.02, 18 front lw ", self.E[(listing[n], listing[n+1])], " lc \"black\" ", file=archivo)
                print("plot \"" + saving + "\" u 1:2:($3*10):4 w points pt 7 ps var palette", file=archivo)

    def f_w(self):      #Shortest path algorithm
         d = {}
         for n in self.N:
              d[(n, n)] = 0
              for m in self.vecinos[n]:
                   d[(m, n)] = self.E[(n, m)]
         for intermedio in self.N:
              for desde in self.N:
                   for hasta in self.N:
                        di = None
                        if(desde, intermedio) in d:
                             di = d[(desde, intermedio)]
                        ih = None
                        if (intermedio, hasta) in d:
                             ih = d[(intermedio, hasta)]
                        if di is not None and ih is not None:
                             c = di + ih
                             if (desde, hasta) not in d or c < d[(desde, hasta)]:
                                  d[(desde, hasta)] = c
         return d

    def camino(self, s, t, c, f): #Augmenting path
         cola = [s]
         usados = set()
         camino = dict()
         while len(cola) > 0:
              u = cola.pop(0)
              usados.add(u)
              for (w, v) in c:
                   if w == u and v not in cola and v not in usados:
                        actual = f.get((u, v), 0)
                        dif = c[(u, v)] - actual
                        if dif > 0:
                             cola.append(v)
                             camino[v] = (u, dif)
         if t in usados:
              return camino
         else: 
              return None

    def f_f(self, c, s, t):    #Ford Fulkerson algorithm
         if s == t:
              return 0
         maximo = 0
         f = dict()
         while True:
              aum = self.camino(s, t, c, f)
              if aum is None:
                   break 
              incr = min(aum.values(), key = (lambda k: k[1]))[1]
              u = t
              while u in aum:
                   v = aum[u][0]
                   actual = f.get((v, u), 0) 
                   inverso = f.get((u, v), 0)
                   f[(v, u)] = actual + incr
                   f[(u, v)] = inverso - incr
                   u = v
              maximo += incr
         return maximo