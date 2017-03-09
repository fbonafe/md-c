import ctypes as C
import numpy as np
import positions as pos
import velocities as vels

c_float = C.c_float
c_double = C.c_double
c_int = C.c_int
c_fl_pointer = C.POINTER(C.c_float)
c_db_pointer = C.POINTER(C.c_double)
c_int_pointer = C.POINTER(C.c_int)
#c_db_pointer = C.c_void_p


#class Cell(C.Structure):
#    _fields_ = [("particles", c_int_pointer),
#                ("n_particles", c_int),
#                ("neigh", c_int_pointer),
#                ("nneigh", c_int),
#                ("ix", c_int), ("iy", c_int), ("iz", c_int)]
#
#                
#class CellList(C.Structure):
#    _fields_ = [("list", C.POINTER(Cell)),
#                ("size", c_double),
#                ("cells_side", c_int), ("ncells", c_int)]
#
#                
#class Integrator(C.Structure):
#    _fields_ = [("timestep", c_double)]
#

class System(C.Structure):
    _fields_ = [("timestep", c_double), ("size", c_double), 
                ("position", c_db_pointer), ("velocity", c_db_pointer),
                ("force", c_db_pointer), 
                ("potential", c_double), ("kinetic", c_double),
                ("n_particles", c_int),
                ("n_steps", c_int), 
                ("rcut", c_double), ("phicut", c_double),
                ("nthreads", c_int)]
               
    def __init__(self):
        density = 0.45
        self.n_steps = 1000
        self.n_particles = 10000
        
        self.timestep = 0.0005
        self.size = (self.n_particles/density)**(1./3.)
        self.potential = 0.0
        self.kinetic = 0.0
        self.rcut = 2.5
        self.phicut = 4 * (self.rcut**(-12) - self.rcut**(-6))
        self.nthreads = 4
        
        self.position_a = pos.simplecubic(self.size, self.n_particles)
        self.velocity_a = vels.random(self.n_particles)
        self.force_a = np.zeros((3 * self.n_particles * self.nthreads),dtype=np.float64)
        np.savetxt('pos.dat',self.position_a)
        
        self.position = self.position_a.ctypes.data_as(c_db_pointer)
        self.velocity = self.velocity_a.ctypes.data_as(c_db_pointer)
        self.force = self.force_a.ctypes.data_as(c_db_pointer)

        
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
