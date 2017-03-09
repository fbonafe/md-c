#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def simplecubic(size, n_particles):
    number_side = int(np.ceil(n_particles**(1./3.)))
    distance = size / number_side;
    idx = 0
    positions = np.zeros((3*n_particles))
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