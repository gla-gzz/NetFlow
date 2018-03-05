#Homework No.2
from grafo import Grafo
from random import random

G = Grafo()
n = 100
for i in range(n):
    G.add_some("node " + str(i+1), random(), random(), random(), random())
G.saveme_to("nodos.dat")
x = G.connectme_by("Color")
G.plotme_in(x, "nodos.dat", "aristas1.dat")
G.plotme_in(x, "nodos.dat", "aristas2.dat", 'd')
y = G.connectme_by("Color", 'p')
G.plotme_in(y, "nodos.dat", "aristas3.dat")
G.plotme_in(y, "nodos.dat", "aristas4.dat", 'd')

