from grafo import Grafo
from random import random
n = 5
G = Grafo()
for i in range(n):
     G.add_some("nodo " + str(i+1), random(), random(), random(), random())
G.connectme_by("Color")
x = G.f_w()
print("F_w :", x)
y = G.f_f(G.E, "nodo 4", "nodo 5")
print("F_f :", y)

