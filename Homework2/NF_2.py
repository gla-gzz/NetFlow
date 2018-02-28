#Homework No.2
from grafo import Grafo
from random import random
"""G = Grafo()
G.add_some('a', 0.5, 0.8, 0.4, 0.01)
G.add_some('b', 0.5, 0.5, 0.7, 0.20)
G.add_some('c', 0.9, 0.1, 0.3, 0.11)
G.connect_these('a', 'b')
C = G.complement_me()"""

G = Grafo()
n = 10
for i in range(n):
    G.add_some("nodo" + str(i+1), i+1, i+1, random(), random())
G.saveme_to("nodos.dat")

