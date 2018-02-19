#Homework No.1,  Student: Astrid Gonzalez,  Course: Network Flow Optimization.
from random import random    #Enables use of random().
import pandas as pd          #Enables use of pd.
n = 100                      #The integer number of nodes to be generated.
aris_x = []                  #List of 'x' coordinates.
aris_y = []                  #List of 'y' coordinates.
size_w = []                  #List of sizes.
color_z = []                 #List of colors.

#A loop to generate 'n' number of times a rondom number for x, y, w, and z; and append them to respective lists.
for i in range(n):      
    x = random()        #a random coordinate for x.
    aris_x.append(x)   
    y = random()        #a random coordinate for y.
    aris_y.append(y)    
    w = random()        #a random size for the node i.
    size_w.append(w)    
    z = random()        #a random color for the node i.
    color_z.append(z)  

#Creates and gives format to a dataframe in order to include all the generated data.
nodes = pd.DataFrame({
        'X' : aris_x,
        'Y' : aris_y,
        'Size' : size_w,
        'Color' : color_z})
nodes.index += 1
nodes = nodes[['X', 'Y', 'Size', 'Color']]
nodes = nodes.sort_values(by=['Color'])                         #sorts the data in the dataframe based in column 'Color'.
nodes.to_csv("nodos.dat", sep=' ', header=False, index=False)   #saves dataframe to file.
aris_x = nodes['X'].tolist()                                    #saves ordered coordinates X in the original list.
aris_y = nodes['Y'].tolist()                                    #saves ordered coordinates Y in the original list.

#Opens a file named "aristas.dat"  this file will contain a script to be read by Gnuplot.
with open("aristas.dat", 'w') as archivo:                           
    print("set term png", file=archivo)                             #changes terminal to png.
    print("set output \"NFlow1.png\" ", file=archivo)               #sets name for the output image.
    print("set key off", file=archivo)                              #removes legend from graph.
    print("set title \"Grafo No.1\" ", file=archivo)                #sets title for the plot.
    print("set xrange [0:1]", file=archivo)                         #sets range for x axis.
    print("set yrange [0:1]", file=archivo)                         #sets range for y axis.
    print("set palette rgbformulae 3, 11, 6", file=archivo)         #changes colors of the palette.
    for i in range(n-1):                                            #a loop to generate 'n-1' number of times a set arrow command to link the nodes.
        print("set arrow ", i+1, " from ", aris_x[i], ",", aris_y[i], " to ", aris_x[i+1], ",", aris_y[i+1], " nohead filled lw 1 lc \"black\" ", file=archivo)
    print("plot \"nodos.dat\" u 1:2:($3*10):4 w points pt 7 ps var palette", file=archivo)           #command to plot the info from the data file.
    print("replot", file=archivo)                                   #replotting of the data so that links may be added to the graph.
