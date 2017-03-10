"""
.. module:: structure builder
   :platform: GNU Linux
   :synopsis: Python interface for a C code to run efficient MD simulations.

.. moduleauthor:: TeamMD WCTP17 <no@email.com>

"""
import numpy as np

def simplecubic(size, n_particles):
    """
    Buils simple structure of "n_particles" arranged in a cube lattice with 
    side length "size"
    
    Args:
        size (int): size of the cube
        n_particles (int): number of particles
    
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