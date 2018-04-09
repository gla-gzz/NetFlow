#Max Flow and Shortest Path Algorithms
#Homework No.3 @gla-gzz

from grafo import Grafo, get_stats, plot_stats
G = Grafo()
sizes = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]
iterations = 10
types = ['S', 'SP', 'DS', 'DP']
text = "tiempos.dat"
G.loppy_loop(text, iterations, sizes)        
short, maxflow = get_stats(text)
#plot_stats(sizes, short, "S_script")
plot_stats(sizes, maxflow, "M_script")

