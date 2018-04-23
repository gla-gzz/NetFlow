from grafo import Grafo, get_stats, plot_stats
import math

n = [10, 50, 100, 200]
prob = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
rep = 5
size = {}
f = "info2.dat"

for i in range(len(n)):
    size[n[i]] = []
    for p in prob:
        for r in range(rep):
            G = Grafo()
            k = n[i]//2
            G.probGraph(n[i], p, k)
            d = G.disty()
            c = G.clustyy()  
            size[n[i]].append((p, d, c))
            

with open(f, 'w') as archivo:
    for s in size:
        for (p, a, b) in size[s]:
            p = round(math.log2(p), 3)
            print(s, p, a, b, file=archivo)

pDi, pCl = get_stats(f)
plot_stats(n, pDi, pCl, "sDist")
