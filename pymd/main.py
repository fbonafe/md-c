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


class Cell(C.Structure):
    _fields_ = [("particles", c_int_pointer),
                ("n_particles", c_int),
                ("neigh", c_int_pointer),
                ("nneigh", c_int),
                ("ix", c_int), ("iy", c_int), ("iz", c_int)]
                
    def __init__(self):
        self.particles = C.byref(c_int)
        self.n_particles = 0
        self.neigh = C.byref(c_int)
        self.nneigh = 0
        self.ix = 0
        self.iy = 0
        self.iz = 0

                
class CellList(C.Structure):
    _fields_ = [("list", C.POINTER(Cell)),
                ("size", c_double),
                ("cells_side", c_int), ("ncells", c_int)]
                
#    def __init__(self):
#        self.list = C.c_void_p
#        self.size = 0.0
#        self.cells_side = 0
#        self.ncells = 0
                
class Integrator(C.Structure):
    _fields_ = [("timestep", c_double)]

    def __init__(self):
        self.timestep = 0.0
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
               
    def __init__(self, n_particles=100, n_steps=1000, timestep=0.0005, saveevery=10):
        density = 0.45

        self.n_steps = n_steps
        self.n_particles = n_particles
        
        self.timestep = timestep
        self.size = (self.n_particles/density)**(1./3.)
        self.potential = 0.0
        self.kinetic = 0.0
        self.rcut = 2.5
        self.phicut = 4 * (self.rcut**(-12) - self.rcut**(-6))
        self.nthreads = 4
        
        self.position_a = pos.simplecubic(self.size, self.n_particles)
        self.velocity_a = vels.random(self.n_particles)
        self.force_a = np.zeros((3 * self.n_particles * self.nthreads),dtype=np.float64)
        
        self.position = self.position_a.ctypes.data_as(c_db_pointer)
        self.velocity = self.velocity_a.ctypes.data_as(c_db_pointer)
        self.force = self.force_a.ctypes.data_as(c_db_pointer)
        
        self.saveevery = saveevery

        
class MD(C.Structure):
    def __init__(self, system, clist, integ):
        self.mdc = C.CDLL('../libmd.so')
        self.mdc.simpleloop.argtypes = [c_int, C.POINTER(System), 
                             C.POINTER(CellList), C.POINTER(Integrator)]
        self.mdc.init_vars.argtypes = [C.POINTER(System), 
                             C.POINTER(CellList), C.POINTER(Integrator)]
        self.mdc.omp_get_num_threads.restype = c_int 
        self.mdc.omp_get_num_threads.argtypes = None
        self.system = system
        self.clist = clist
        self.integ = integ
        self.mdc.init_vars(C.byref(self.system), C.byref(self.clist), 
                           C.byref(self.integ))
        self.time = 0
            
    def run(self):
        outerloops = int(self.system.n_steps/self.system.saveevery)
        efile = open('energy.dat', 'w')
        tfile = open('time.dat', 'w')
        for i in range(outerloops):
            step = i * self.system.saveevery
            self.time = step * self.system.timestep
            efile.write("{}, {}, {}\n".format(self.system.potential, 
                        self.system.kinetic, 
                        self.system.potential+self.system.kinetic))
            tfile.write("{}, {}\n".format(step, self.time))
            
            self.mdc.simpleloop(self.system.saveevery, C.byref(self.system), 
                              C.byref(self.clist), C.byref(self.integ))
        
        efile.close()
        tfile.close()

    def runInnerLoop(self, i):
        step = i * self.system.saveevery
        self.time = step * self.system.timestep
        #efile.write("{}, {}, {}\n".format(self.system.potential, 
        #                self.system.kinetic, 
        #                self.system.potential+self.system.kinetic))
        #tfile.write("{}, {}\n".format(step, self.time))
            
        self.mdc.simpleloop(self.system.saveevery, C.byref(self.system), 
                              C.byref(self.clist), C.byref(self.integ))
        
        #efile.close()
        #tfile.close()
        return 	self.system.potential, self.system.kinetic
#my_system = System()
#my_clist = CellList()
#my_integ = Integrator()
#this_MD = MD(my_system, my_clist, my_integ)
#this_MD.run()