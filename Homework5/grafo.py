#Homework No.5 @gla-gzz

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

    def connectme_by(self, choice, mode1 = 'uw', mode2 = 'ud'):     #Connects the nodes of the graph based in a parameter
       import pandas as pd
       modes =['uw', 'w', 'ud', 'd']
       if mode1 not in modes or mode2 not in modes:
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
           if mode1 is 'uw' and mode2 is 'ud':
               self.connect_these(y[n], y[n+1])
           if mode1 is 'w' and mode2 is 'ud':    
               diff_nodes = (self.color[y[n+1]] - self.color[y[n]])
               if diff_nodes <= 0.03:
                   self.connect_these(y[n], y[n+1], k)
               if 0.03 < diff_nodes <= 0.07:
                   k += 0.5
                   self.connect_these(y[n], y[n+1], k)
               if diff_nodes > 0.07:
                   k += 1
                   self.connect_these(y[n], y[n+1], k)
           if mode1 is 'uw' and mode2 is 'd':
               self.connect_these(y[n], y[n+1])
               del self.E[(y[n+1], y[n])]
               self.vecinos[y[n+1]].remove(y[n])
           if mode1 is 'w' and mode2 is 'd':
               diff_nodes = (self.color[y[n+1]] - self.color[y[n]])
               if diff_nodes <= 0.03:
                   self.connect_these(y[n], y[n+1], k)
                   del self.E[(y[n+1], y[n])]
                   self.vecinos[y[n+1]].remove(y[n])
               if 0.03 < diff_nodes <= 0.07:
                   k += 0.5
                   self.connect_these(y[n], y[n+1], k)
                   del self.E[(y[n+1], y[n])]
                   self.vecinos[y[n+1]].remove(y[n])
               if diff_nodes > 0.07:
                   k += 1
                   self.connect_these(y[n], y[n+1], k) 
                   del self.E[(y[n+1], y[n])]
                   self.vecinos[y[n+1]].remove(y[n])
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
                    print("set arrow ", n+1, " from ", (self.X[listing[n]]), ",", (self.Y[listing[n]]), " to ", self.X[listing[n+1]], ",", self.Y[listing[n+1]], end=" ", file=archivo)
                    print("head filled size screen 0.02, 18 front lw ", self.E[(listing[n], listing[n+1])], " lc \"black\" ", file=archivo)
                print("plot \"" + saving + "\" u 1:2:3:4 w points pt 7 ps var palette", file=archivo)

    def shorty(self):      #Shortest path algorithm
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

    def fordy(self, c, s, t):    #Ford Fulkerson algorithm
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
        
    def much_time(self, measure_me, c = None, s = None, t = None):      #A function that measures the performance time of the flow algorithms
        import time
        if c is None:
            zero = time.perf_counter()
            solution = measure_me()
            final = (time.perf_counter() - zero)
            return final, solution
        else:
            zero = time.perf_counter()
            solution = measure_me(c, s, t)
            final = (time.perf_counter() - zero)
            return final, solution
    
    def loppy_loop(self, arch = "time.dat", loops = 1, Sizes = None):         #Creates graphs and does loops to get performance times of the algorithms and save them to file 
        from random import random
        ResultsS = dict()
        ResultsDS = dict()
        ResultsSP = dict()
        ResultsDP = dict()
        Results = set()
        Results = (ResultsS, ResultsSP, ResultsDS, ResultsDP)
        for size in Sizes:
            ResultsS[str(size) + " nodes"] = []
            ResultsDS[str(size) + " nodes"] = []
            ResultsSP[str(size) + " nodes"] = []
            ResultsDP[str(size) + " nodes"] = []
        for iteration in range(loops):
            for size in Sizes:
                x = None
                y = None
                z = None
                xy = None
                self = None
                self = Grafo()
                for i in range(size):
                    self.add_some("nodo " + str(i+1), random(), random(), random(), random())
                x = self.connectme_by("Color")
                timeS, solS = self.much_time(self.shorty)
                timeF, solF = self.much_time(self.fordy, self.E, x[0], x[size-1])
                ResultsS[str(size) + " nodes"].append((timeS, timeF))
                if iteration == loops-1 and size == Sizes[len(Sizes)-1]:
                    self.saveme_to("nodosS.dat")
                    self.plotme_in(x, "nodosS.dat", "aristasS.dat")
                y = self.connectme_by("Color", 'w')
                timeS, solS = self.much_time(self.shorty)
                timeF, solF = self.much_time(self.fordy, self.E, y[0], y[size-1])   
                ResultsSP[str(size) + " nodes"].append((timeS, timeF))
                if iteration == loops-1 and size == Sizes[len(Sizes)-1]:
                    self.saveme_to("nodosSP.dat")
                    self.plotme_in(y, "nodosSP.dat", "aristasSP.dat") 
                z = self.connectme_by("Color", 'uw', 'd')
                timeS, solS = self.much_time(self.shorty)
                timeF, solF = self.much_time(self.fordy, self.E, z[0], z[size-1])
                ResultsDS[str(size) + " nodes"].append((timeS, timeF)) 
                if iteration == loops-1 and size == Sizes[len(Sizes)-1]:
                    self.saveme_to("nodosDS.dat")
                    self.plotme_in(z, "nodosDS.dat", "aristasDS.dat", 'd')
                xy = self.connectme_by("Color", 'w', 'd')
                timeS, solS = self.much_time(self.shorty)
                timeF, solF = self.much_time(self.fordy, self.E, xy[0], xy[size-1])
                ResultsDP[str(size) + " nodes"].append((timeS, timeF)) 
                if iteration == loops-1 and size == Sizes[len(Sizes)-1]:
                    self.saveme_to("nodosDP.dat")
                    self.plotme_in(xy, "nodosDP.dat", "aristasDP.dat", 'd')
        with open(arch, 'w') as archivo:
            for result in Results:
                for size in Sizes:
                    if Results[0] == result:
                        for (i,j) in result[str(size) + " nodes"]:
                            print("S", size, format(i, '0.20f'), format(j, '0.20f'), file=archivo)
                    if Results[1] == result:
                        for (i,j) in result[str(size) + " nodes"]:
                            print("SP", size, format(i, '0.20f'), format(j, '0.20f'), file=archivo)
                    if Results[2] == result:
                        for (i,j) in result[str(size) + " nodes"]:
                            print("DS", size, format(i, '0.20f'), format(j, '0.20f'), file=archivo)
                    if Results[3] == result:
                        for (i,j) in result[str(size) + " nodes"]:
                            print("DP", size, format(i, '0.20f'), format(j, '0.20f'), file=archivo)                            


    def probGraph(self, n, prob, k):
        import random
        for i in range(n):
            self.add_some("nodo " + str(i))
        for node in self.N:
            while len(self.vecinos[node]) < 1:
                for i in range(n-1):
                    if ("nodo " + str(i)) != node:
                        if len(self.vecinos[node]) < k and len(self.vecinos["nodo " + str(i)]) < k:
                            Tprob = round(random.random(), 2)
                            if Tprob <= prob:
                                self.connect_these(node, "nodo " + str(i))  
    
    def disty(self):
        x = self.shorty()
        a = []
        for i in x:
            a.append(x[i])
        return (sum(a)/len(self.N)**2)
    
    def clustyy(self):
        import math
        clust = {}
        for nodo in self.N:
            a = 0
            for vecino in self.vecinos[nodo]:
                for vecinito in self.vecinos[nodo]:
                    if vecino != vecinito:
                        if vecinito in self.vecinos[vecino]:
                            a += 1
            a //= 2
            if a != 0:
                cotaMax = (math.factorial(len(self.vecinos[nodo])))/(math.factorial(2)*math.factorial(len(self.vecinos[nodo])-2))
                d = a/cotaMax
            else:
                d = 0.0
            clust[nodo] = d
        prom_C = 0
        for nodo in clust:
            prom_C += clust[nodo]
        prom_C /= len(clust)
        return prom_C
    
    def points_C(self, x,y, radius):
        import math as m
        n = len(self.N)
        ang = 360//n
        angles = []
        a = 0
        for i in range(n):
            a += ang
            rad = a * (m.pi/180)
            angles.append(rad)
        a = 0
        for node in self.N:
            self.X[node] = x + (radius * m.cos(angles[a]))
            self.Y[node] = y + (radius * m.sin(angles[a]))
            a += 1
            
    def plotme(self, saving2 = "script.dat"):           
        saving = "info.dat"
        n = len(self.N)
        self.points_C(n//2,n//2,n//2)
        with open("info.dat", 'w') as archivo:
            i = 1
            for node in self.N:
                print(self.X[node], self.Y[node], i, node, file=archivo)
                i += 1
        with open(saving2, 'w') as archivo:
            print("set key off", file=archivo)
            print("set xrange [-" + str(round(len(self.N)/10, 1)) + ":" + str(len(self.N)+round(len(self.N)/10, 1)) + "]", file=archivo)
            print("set yrange [-" + str(round(len(self.N)/10, 1)) + ":" + str(len(self.N)+round(len(self.N)/10, 1)) + "]", file=archivo)
            print("set palette model HSV", file=archivo)
            print("set palette rgb 3, 2, 2", file=archivo)
            print("unset colorbox", file=archivo)
            i = 1
            for node in self.vecinos:
                for vecino in self.vecinos[node]:
                    print("set arrow ", i, " from ", self.X[node], ",", self.Y[node], " to ", self.X[vecino], ",", self.Y[vecino], end=" ", file=archivo)
                    print("nohead back lw 2 lc \"black\" ", file=archivo)
                    i += 1
            print("plot \"" + saving + "\" u 1:2:3 w points pt 7 ps 5 palette, ", file=archivo)     
            
    def basicG(self, k, p, l, mode = "d"):
        import random
        for i in range(k):
            for j in range(k):
                self.add_some("nodo " + str(i+1)+str(j+1), i+1, j+1)
            i = 0
        if mode == "d":
            for i in range(k, 0, -1):
                for j in range(k, 1, -1):
                    self.connect_these("nodo " + str(i)+str(j), "nodo " + str(i)+str(j-1))
                    del self.E[("nodo " + str(i)+str(j-1), "nodo " + str(i)+str(j))]
                    self.vecinos["nodo " + str(i) + str(j-1)].remove("nodo " + str(i) + str(j))
            i = 0
            for j in range(k):
                for i in range(k-1):
                    self.connect_these("nodo " + str(i+1)+str(j+1), "nodo " + str(i+2)+str(j+1))
                    del self.E[("nodo " + str(i+2)+str(j+1), "nodo " + str(i+1)+str(j+1))]
                    self.vecinos["nodo " + str(i+2)+str(j+1)].remove("nodo " + str(i+1)+str(j+1))
            a = 0
            ctl = []
            for node in self.N:
                for nodo in self.N:
                    if round(random.random(),3) < p and node != nodo and a < 2 and node not in ctl:
                        ctl.append(node)
                        self.connect_these(node, nodo)
                        del self.E[(nodo, node)]
                        self.vecinos[node].remove(nodo)
                        a += 1                      
        if mode == "p":
            import numpy as np
            cll = []
            for i in range(k):
                for j in range(k-1):
                    z = int(np.random.normal(2,1))
                    while z < 1:
                            z = int(np.random.normal(2,1))
                    self.connect_these("nodo " + str(i+1)+str(j+1), "nodo " + str(i+1)+str(j+2), z)
                    cll.append(self.E[("nodo " + str(i+1)+str(j+1), "nodo " + str(i+1)+str(j+2))])
            i = 0
            for j in range(k):
                for i in range(k-1):
                    z = int(np.random.normal(2,1))
                    while z < 1:
                            z = int(np.random.normal(2,1))
                    self.connect_these("nodo " + str(i+1)+str(j+1), "nodo " + str(i+2)+str(j+1), z)
                    cll.append(self.E[("nodo " + str(i+1)+str(j+1), "nodo " + str(i+2)+str(j+1))])
            a = 0
            ctl = []
            for node in self.N:
                for nodo in self.N:
                    if round(random.random(),3) < p and node != nodo and a < 2 and node not in ctl:
                        ctl.append(node)
                        z = int(np.random.normal(2,1))
                        while z < 1:
                            z = int(np.random.normal(2,1))
                        self.connect_these(node, nodo, z)
                        cll.append(self.E[(node, nodo)])
                        a += 1
            return cll
            
    def visual(self, mode, k, listing = None, saving = "grafito.dat", saving2 = "grafeando.dat"):
        import math as m
        with open(saving2, 'w') as archivo:
            i = 1
            for node in self.N:
                print(i, node, self.X[node], self.Y[node], file=archivo)
                i += 1
        s = []
        if listing != None:
            for u in range(0, len(listing)-1):
                s.append((listing[u], listing[u+1]))
        else:
            s.append(("0", "0"))
        with open(saving, 'w') as archivo:
            print("set key off", file=archivo)
            print('set format x ""', file=archivo)
            print('set format y ""', file =archivo)
            print("set xrange [0.5:" + str(k+0.5) + "]", file = archivo)
            print("set yrange [0.5:" + str(k+0.5) + "]", file = archivo)
            print("set palette model HSV", file=archivo)
            print("set palette rgb 3, 2, 2", file=archivo)
            print("unset colorbox", file=archivo)     
            print("unset xtics", file=archivo)
            print("unset x2tics", file=archivo)
            print("unset ytics", file=archivo)
            print("unset y2tics", file=archivo)
            i = 1
            for (a,b) in self.E:
                if mode == "p":
                    print("set arrow ", i, " from ", self.X[a], ",", self.Y[a], " to ", self.X[b], ",", self.Y[b], end=" ", file=archivo)
                    print("nohead back lw " + str(self.E[(a, b)]) + " lc", end=" ", file=archivo)
                    if (a,b) in s or (b,a) in s:
                        print("\"red\" ", file=archivo)
                    else:
                        print("\"black\" ", file=archivo)
                    i += 1
                    timeF, solF = self.much_time(self.fordy, self.E, listing[0], listing[len(listing)-1])
                else:
                    ta = m.atan2(self.Y[b]-self.Y[a], self.X[b]-self.X[a])
                    radius = 0.1   
                    if m.degrees(ta) == 90.0 or m.degrees(ta) == -90.0:
                        radius = 0.17   
                    if m.degrees(ta) == 90.0 or -90.0 or 0.0 or 180.0:
                        b1 = self.X[b] + (radius * m.cos(ta+m.pi))
                        b2 = self.Y[b] + (radius * m.sin(ta-m.pi)) 
                    else:
                        b1 = self.X[b] + (radius * m.cos(ta))
                        b2 = self.Y[b] + (radius * m.sin(ta)) 
                    if self.E[(a,b)] != 0:
                        print("set arrow ", i, " from ", self.X[a], ",", self.Y[a], " to ", b1, ",", b2, end=" ", file=archivo)
                        print("lw 2 lc", end=" ", file=archivo)
                        if (a,b) in s:
                            print("\"red\" ", file=archivo)
                        else:
                            print("\"black\" ", file=archivo)                    
                        i += 1  
            si = m.sqrt(len(self.N))
            source = "nodo " + str(1) + str(int(si))
            sink = "nodo " + str(int(si)) + str(1)
            timeF, solF = self.much_time(self.fordy, self.E, source, sink)                           
            print("set style circle radius graph 0.02", file=archivo)
            print("plot \"" + saving2 + "\" u 4:5:1 w circles palette fill solid", file=archivo)
        return solF, timeF
        
    def manhattanPath(self, l):
        import math as m
        import random as r
        si = m.sqrt(len(self.N))
        source = "nodo " + str(1) + str(int(si))
        sink = "nodo " + str(int(si)) + str(1)
        queue = []
        visited = []
        visited.append(source)
        if len(self.vecinos[source]) == 0:
            return visited
        for (a,b) in self.E:
            if a == source:
                queue.append(b)
        x = queue[r.randint(0, len(queue)-1)]
        visited.append(x)
        while x not in self.vecinos[sink]:
            if sink in visited:
                print(visited)
                return visited
            if len(self.vecinos[x]) == 0:
                visited = self.manhattanPath(l)
            else:
                for i in range(1, r.randint(1,l)):
                    y = r.sample(self.vecinos[x], 1)
                    y = y[0]
                    n = 1
                    while y in visited:
                        y = r.sample(self.vecinos[x],1)
                        y = y[0]
                        n += 1
                        if n == 4:
                            visited = self.manhattanPath(l)
                            return visited
                    x = y
                    visited.append(x)
        visited.append(sink)
        print(visited)
        return visited
    
    def perco(self):
        import random as r
        s = r.choice(list(self.E.keys()))
        while self.E[s] == 0:
            s = r.choice(list(self.E.keys()))
        del self.E[s]
        a = []
        for i in s:
            a.append(i)
        if a[1] in self.vecinos[a[0]]:
            self.vecinos[a[0]].remove(a[1])
        
    
    def remove_n_check(self, mode, n, l, k, f, f1):
        A = {}
        B = {}
        u = 0
        h = self.manhattanPath(l)
        a, b = self.visual(mode, k, h, f +".dat", f1 + ".dat")
        A[str(u)] = a
        B[str(u)] = b
        self.perco()
        for u in range(1, n+1):
            h = self.manhattanPath(l)
            a, b = self.visual(mode, k, h, f + str(u) + ".dat", f1 + str(u) + ".dat")
            A[str(u)] = a
            B[str(u)] = b
            self.perco()
        return A, B
    
    
    


