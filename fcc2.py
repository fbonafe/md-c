import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def simple_cubic(density,n_particles):
    size = (n_particles / density)**(1/3.)
    number_side = (n_particles)**(1/3.)
    distance = size / number_side
    index_particle = 0
    position = np.zeros(3*n_particles)

    for i in range(int(number_side)):
        for j in range(int(number_side)):
                for k in range(int(number_side)):
                    if index_particle == n_particles:
                        break
                    if (j%2 != 0 and i%2 != 0) or (j%2 == 0 and i%2 == 0):
                        position[3*index_particle + 2] = k * distance
                    elif (j%2 != 0 and i%2 == 0) or (j%2 == 0 and i%2 != 0):
                        position[3*index_particle + 2] = k * distance + 1/2.
                        
                    position[3*index_particle + 0] = i * distance
                    position[3*index_particle + 1] = j * distance
                    index_particle = index_particle + 1
    
    return position

n_particles=27
x=np.zeros(n_particles)
y=np.zeros(n_particles)
z=np.zeros(n_particles)

for i in range(n_particles):
    x[i] = simple_cubic(1,n_particles)[3*i]
    y[i] = simple_cubic(1,n_particles)[3*i+1]
    z[i] = simple_cubic(1,n_particles)[3*i+2]

fig= plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(x,y,z)
ax.plot(x,np.zeros(n_particles),np.zeros(n_particles),'r')
ax.plot(np.zeros(n_particles),y,np.zeros(n_particles),'g')
ax.plot(np.zeros(n_particles),np.zeros(n_particles),z,'b')
plt.show()