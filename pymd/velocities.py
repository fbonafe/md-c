#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rnd
import numpy as np


def random(n_particles):
    rnd.seed(6000)
    velocities = np.zeros((3*n_particles))
    for i in range(3*n_particles):
        velocities[i] = rnd.random()
    return velocities