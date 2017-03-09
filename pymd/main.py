import ctypes as C
import numpy as np
import positions as pos
import velocities as vels
c_float = C.c_float
c_fl_pointer = C.POINTER(C.c_float)
c_int = C.c_int
c_int_pointer = C.POINTER(C.c_int)


class Cell(C.Structure):
    _fields_ = [("particles", c_int_pointer),
                ("n_particles", c_int),
                ("neigh", c_int_pointer),
                ("nneigh", c_int),
                ("ix", c_int), ("iy", c_int), ("iz", c_int)]

                
class CellList():
    _fields_ = [("list", C.POINTER(Cell)),
                ("size", c_float),
                ("cells_side", c_int), ("ncells", c_int)]

                
class Integrator():
    _fields_ = [("timestep", c_float)]


class System(C.Structure):
    _fields_ = [("timestep", c_float), ("size", c_float), 
                ("potential", c_float), ("kinetic", c_float),
                ("rcut", c_float), ("phicut", c_float),
                ("position", c_fl_pointer), ("velocity", c_fl_pointer),
                ("force", c_fl_pointer), ("n_particles", c_int),
                ("n_steps", c_int), ("nthreads", c_int)]
    
    def __init__(self):
        density = 0.45
        self.n_steps = 1000
        self.n_particles = 1000
        
        self.timestep = 0.0005
        self.size = (self.n_particles/density)**(1./3.)
        self.potential = 0.0
        self.kinetic = 0.0
        self.rcut = 2.5
        self.phicut = 4 * (self.rcut**(-12) - self.rcut**(-6))
        self.nthreads = 0
        
        nparr_position = pos.simplecubic(self.size, self.n_particles)
        nparr_velocity = vels.random(self.n_particles)
        nparr_forces = np.zeros((3 * self.n_particles))

        self.position = nparr_position.ctypes.data_as(c_fl_pointer)
        self.velocity = nparr_velocity.ctypes.data_as(c_fl_pointer)
        self.forces = nparr_forces.ctypes.data_as(c_fl_pointer)

        
class MD(C.Structure):
    def __init__(self):
        self.mdc = C.CDLL('../libmd.so')
        self.mdc.main.argtypes = [C.POINTER(System)]
        self.mdc.main.restype = c_int
    
    def run(self, system):
        self.mdc.main(C.byref(system))


my_system = System()
this_MD = MD()
this_MD.run(my_system)
