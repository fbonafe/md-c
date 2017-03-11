"""
.. module:: initial_velocities
   :platform: GNU Linux
   :synopsis: Initial velocities distributions.

.. moduleauthor:: TeamMD WCTP17 <no@email.com>

"""
import random as rnd
import numpy as np


def random(n_particles):
    """
    Defines random velocities normalized to one for "n_particles".
    
    Args:
        n_particles (int): number of particles
    """
    rnd.seed(6000)
    velocities = np.zeros((3 * n_particles),  dtype=np.float64)
    for i in range(3*n_particles):
        velocities[i] = rnd.random()
    return velocities
    
def maxwellboltzmann(n_particles, temp, mass):
    """
    Defines normal distribution of velocities at a certain temperature
    according to the Maxwell-Boltzmann distribution.
    
    Args:
        n_particles (int): number of particles
        temp (double): temperature normalized by k_B
        mass (double): atomic mass
    """
    rnd.seed(6000)
    velocities = np.zeros(3*n_particles,  dtype=np.float64)
    for i in range(3*n_particles):
        velocities[i] = rnd.normal()
    velocities = velocities * np.sqrt(temp/mass)
    return velocities
