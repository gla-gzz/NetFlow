from grafo import Grafo

G = Grafo()
l = [1, 2, 4]
k = 5
p = 0.3
mode = "d"
G.basicG(k, p, l, mode)
A, B = G.remove_n_check(mode, 10, l[1], k, "scr", "infi")
print(A)
print(B)

with open("indo.dat", 'w') as archivo:
    for i in range(0, len(A)):
        print(i, A[str(i)], B[str(i)], file=archivo)
        
with open("Script.dat", 'w')as archivo:
    print("set key off", file=archivo)
    print("set border 14", file=archivo)
    print("set xtics rotate 45", file=archivo)
    print("set xlabel 'Aristas removidas'", file=archivo)
    print("set ylabel 'Flujo max'", file=archivo)
    print("set y2label 'Tiempo de corrida'", file=archivo)
    print("plot 'indo.dat' u 1:2:xticlabels(1) axes x1y1 w lines lw 5 lc 'red' notitle,", end = ' ', file=archivo)        
    print("'indo.dat' u 1:3 axes x1y2 w lines lw 5 lc 'black' notitle", file=archivo)


