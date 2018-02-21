#Homework No.2
from grafo import Grafo
G = Grafo()
G.add_some('a')
G.add_some('b')
G.add_more('a', 0.5, 0.8, 0.4, 0.01)
G.add_more('b', 0.3, 0.5, 0.7, 0.20)
print("Coordenadas x: ", G.X)
print("Coordenadas y: ", G.Y)
print("Tamano: ", G.size)
print("Color: ", G.color)
print(G.V)

