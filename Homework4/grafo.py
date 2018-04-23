#Homework No.4 @gla-gzz

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


def get_stats(x):
    import pandas as pd
    datos = pd.DataFrame()
    with open(x, 'r') as archivo:
        for line in archivo:
            datos = datos.append(pd.Series(line.split()), ignore_index = True)
        datos.columns = ["Size", "Prob", "Dist", "Clust"]
        datos = datos.set_index(["Size"])
    datos[["Dist", "Clust"]] = datos[["Dist", "Clust"]].apply(pd.to_numeric)
    df1 = datos.groupby(["Size", "Prob"]).Dist.describe()
    df2 = datos.groupby(["Size", "Prob"]).Clust.describe()
    return df1, df2

def plot_stats(s, dt, dc, plotting):
    import pandas as pd
    S = [str(i) for i in s]
    x = []
    h = []
    for size in S:
        dt.loc[size].to_csv("T" + str(size) + ".dat", sep = ' ', index = True, header = False)
        dc.loc[size].to_csv("C" + str(size) + ".dat", sep = ' ', index = True, header = False)
        x.append("T" + str(size))
        h.append("C" + str(size))
        y = dt.index.levels[dt.index.names.index("Prob")]
        pr = []
        for i in y:
            pr.append(i)
    pr.reverse()
    for fSize in x:
        a = 1
        li = []
        datos = pd.DataFrame()
        with open(fSize + ".dat", 'r') as archivo:
            for line in archivo:
                li.append(a)
                a += 1
                datos = datos.append(pd.Series(line.split()), ignore_index = True)
        datos["in"] = li
        datos.to_csv(fSize + ".dat", sep = ' ', index = False, header = False)
        m = max(datos[8])
        mn = min(datos[6])
    for fSize in h:
        a = 1
        li = []
        datos2 = pd.DataFrame()
        with open(fSize + ".dat", 'r') as archivo:
            for line in archivo:
                li.append(a)
                a += 1
                datos2 = datos2.append(pd.Series(line.split()), ignore_index = True)
        datos2["in"] = li
        datos2.to_csv(fSize + ".dat", sep = ' ', index = False, header = False)
        m2 = max(datos2[8])
        mn2 = min(datos2[6])
        
    with open(plotting + ".dat", 'w') as archivo:
        print("", file=archivo)
    for size in S:
        with open(plotting + ".dat", 'a') as archivo:
            print("set output 'TC" + str(size) + "_" + plotting + ".eps' ", file=archivo)
            print("set key off", file=archivo)
            print("set border 14", file=archivo)
            print("set style data boxplot", file=archivo)
            print("set boxwidth 0.4", file=archivo)
            r = float(pr[len(pr)-1]) - float(pr[0])
            r /= 10
            print("set xrange [" + str(float(pr[0])-r) +":" + str(float(pr[len(pr)-1])+r) + "]", file=archivo)
            print("set yrange [" + str(float(mn) - ((float(m)-float(mn))/8)) + ":" + str(float(m) + ((float(m)-float(mn))/8)) + "]", file=archivo)
            print("set y2range [" + str(float(mn2) - ((float(m2)-float(mn2))/8)) + ":" + str(float(m2) + ((float(m2)-float(mn2))/8)) + "]", file=archivo)
            print("set y2tics", file=archivo)
            print("set xtics rotate 45", file=archivo)
            print("set xlabel 'Probability in log scale'", file=archivo)
            print("set ylabel 'Average distance'", file=archivo)
            print("set y2label 'Clustering coef.'", file=archivo)
            print("set style fill empty", file=archivo)
            print("plot '" + "T" + str(size) + ".dat' u 1:6:5:9:8:10:xticlabels(1) axes x1y1 w candlesticks lw 2 lc var notitle whiskerbars,", end = ' ', file=archivo)
            print("'" + "T" + str(size) + ".dat' u 1:7:7:7:7 axes x1y1 w candlesticks lt -1 notitle,", end = ' ', file=archivo)
            print("'" + "T" + str(size) + ".dat' u 1:7 axes x1y1 w lines lw 4 lc 'red' notitle,", end = ' ', file=archivo)        
            print("'" + "C" + str(size) + ".dat' u 1:6:5:9:8:10:xticlabels(1) axes x1y2 w candlesticks lw 2 lc var notitle whiskerbars,", end = ' ', file=archivo)
            print("'" + "C" + str(size) + ".dat' u 1:7:7:7:7 axes x1y2 w candlesticks lt -1 notitle,", end = ' ', file=archivo)
            print("'" + "C" + str(size) + ".dat' u 1:7 axes x1y2 w lines lw 4 lc 'black' notitle", file=archivo)
def coty(n, k):
    maxy = n*k
    print(maxy)
    
    
    
