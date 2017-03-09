import numpy as np
import matplotlib.pyplot as plt
#from plotter import Plotter # Del modulo <plotter> importo la clase <Plotter>
import sys
import plotter as p # Importo el modulo <plotter> y las cosas que use las tengo que nombrar con el p.
# Para pocas lineas es mas comoda la otra practica, pero asi queda mas ordenado 

my_plot = p.Plotter('tiempo','posicion')

i = 0
while i < 10 :
    x = i
    y = i**2
    my_plot.plot1(x,y)
    i+= 1
plt.show(block=True)