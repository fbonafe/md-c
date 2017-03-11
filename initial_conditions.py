""" 
.. module:: initial_conditions
    :platform: GNU Linux
    :synopsis: This module contains all the possible initial conditions for the program. Those are: Simple cubic, Fcc and Bcc. It returns an numpy array with the x, y, z coordinates of the positions of the particles.
.. moduleauthor:: TeaMD #WTPC17

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def simplecubic(size, n_particles):
    """ 
    Calculates the positions of particles when they are in a simple cubic crystaline shape. 
    
    :param density: density of particles
    :type density: double
    :param n_particles: total number of particles
    :type n_particles: int
    :returns: position (numpy.array (dim=3*n_particles) )
    
    """
    number_side = int(np.ceil(n_particles**(1./3.)))
    distance = size / number_side
    idx = 0
    positions = np.zeros(3*n_particles, dtype=np.float64)
    for i in range(number_side):
        for j in range(number_side):
            for k in range(number_side):
                if (idx == n_particles):
                    break
                positions[3 * idx + 0] = i * distance
                positions[3 * idx + 1] = j * distance
                positions[3 * idx + 2] = k * distance
                idx += 1
    return positions


def fcc(density,n_particles):
    """     
    Calculates the positions of particles when they are in a face-centered cubic crystaline shape. 
    
    :param density: density of particles
    :type density: double
    :param n_particles: total number of particles
    :type n_particles: int
    :returns: position (numpy.array (dim=3*n_particles) )
    
    """
    size = (n_particles / density)**(1/3.)
    number_side = (n_particles)**(1/3.)
    distance = size / number_side
    index_particle = 0
    position = np.zeros(3*n_particles, dtype=np.float64)

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


def bcc(density,n_particles):
    """
    Calculates the positions of particles when they are in a face-centered cubic crystaline shape. 
    
    :param density: density of particles
    :type density: double
    :param n_particles: total number of particles
    :type n_particles: int
    :returns: position (numpy.array (dim=3*n_particles) )
    
    """
    size = (n_particles / density)**(1/3.)
    number_side = (n_particles)**(1/3.)
    distance = size / number_side
    index_particle = 0
    position = np.zeros(3*n_particles, dtype=np.float64)

    for i in range(int(number_side)):
        for j in range(int(number_side)):
                for k in range(int(number_side)):
                    if index_particle == n_particles:
                        break
                    if j%2 == 0:
                        position[3*index_particle + 0] = i * distance
                        position[3*index_particle + 2] = k * distance
                    else:
                        position[3*index_particle + 0] = i * distance + 1/2.
                        position[3*index_particle + 2] = k * distance + 1/2.
                        
                    position[3*index_particle + 1] = j * distance
                    index_particle = index_particle + 1
    
    return position
