"""
.. module:: pymd
   :platform: GNU Linux
   :synopsis: Python interface for a C code to run efficient MD simulations.

.. moduleauthor:: TeamMD WCTP17 <no@email.com>

"""

import ctypes as C
import numpy as np
import positions as pos
import velocities as vels
import time

c_float = C.c_float
c_double = C.c_double
c_int = C.c_int
c_fl_pointer = C.POINTER(C.c_float)
c_db_pointer = C.POINTER(C.c_double)
c_int_pointer = C.POINTER(C.c_int)

mdc = C.CDLL('../libmd.so')


class Cell(C.Structure):
    """
    Inteface to C structure.
    """
    _fields_ = [("particles", c_int_pointer),
                ("n_particles", c_int),
                ("neigh", c_int_pointer),
                ("nneigh", c_int),
                ("ix", c_int), ("iy", c_int), ("iz", c_int)]
                
    def __init__(self):
        """
        Defines properties of Verlet cell. Is called only by CellList class.
        """
        self.n_particles = 0
        self.nneigh = 0
        self.ix = 0
        self.iy = 0
        self.iz = 0

                
class CellList(C.Structure):
    """
    Inteface to C structure.
    """
    _fields_ = [("list", C.POINTER(Cell)),
                ("size", c_double),
                ("cells_side", c_int), ("ncells", c_int)]
                
    def __init__(self, sys):
        """
        Creates a list of cells.
        
        Args:
            sys (System): argument of class System.
        """
        size = 2.5
        self.cells_side = int(np.ceil(sys.size/size))
        self.size = sys.size/self.cells_side
        self.ncells = self.cells_side**3
        
        elements = (Cell * self.ncells)()
        self.list = C.cast(elements, C.POINTER(Cell))
        
        idx = 0
        for i in range(self.cells_side):
            for j in range(self.cells_side):
                for k in range(self.cells_side):
                    cell = Cell()
                    cell.ix = i
                    cell.iy = j
                    cell.iz = k
                    cell.nneigh = 0
                    
                    neigh = (c_int * self.ncells) ()
                    cell.neigh = C.cast(neigh, C.POINTER(c_int))
                    
                    particles = (c_int * sys.n_particles) ()
                    cell.particles = C.cast(particles, C.POINTER(c_int))
                    
                    self.list[idx] = cell
                    idx += 1

               
class Integrator(C.Structure):
    """
    Inteface to C structure.
    """
    _fields_ = [("timestep", c_double)]

    def __init__(self):
        """
        Initialices integrator properties.
        """
        self.timestep = 0.0

        
class System(C.Structure):
    """
    Inteface to C structure. Defines atributes of the system under study.
    """
    _fields_ = [("timestep", c_double), ("size", c_double), 
                ("position", c_db_pointer), ("velocity", c_db_pointer),
                ("force", c_db_pointer), 
                ("potential", c_double), ("kinetic", c_double),
                ("n_particles", c_int),
                ("n_steps", c_int), 
                ("rcut", c_double), ("phicut", c_double),
                ("nthreads", c_int)]
               
    def __init__(self, n_particles=1000, n_steps=1000, timestep=0.0005, saveevery=10):
        """
        Inteface to C structure.
        
        Args:
            n_steps (int): number of steps
            n_particles (int): number of particles
            timestep (int): time delta between steps
            size (float): length of simulation box size
            density (float): density in particles/Angstrom**3
            rcut (float): cutoff radius for pairwise interactions
            epsilon (float): epsilon paramenter in Lennard-Jones potential
            sigma (float): sigma paramenter in Lennard-Jones potential
        """
        density = 0.45

        self.n_steps = n_steps
        self.n_particles = n_particles        
        self.timestep = timestep
        self.size = (self.n_particles/density)**(1./3.)
        self.potential = 0.0
        self.kinetic = 0.0
        self.rcut = 2.5
        self.phicut = 4 * (self.rcut**(-12) - self.rcut**(-6))
        
        mdc.get_num_threads.restype = C.c_int
        self.nthreads = mdc.get_num_threads()
        
        self.position_a = pos.simplecubic(self.size, self.n_particles)
        self.force_a = np.zeros((3 * self.n_particles * self.nthreads),dtype=np.float64)
        self.init_velocities(from_C=True)       
        self.position = self.position_a.ctypes.data_as(c_db_pointer)
        self.force = self.force_a.ctypes.data_as(c_db_pointer)
        self.saveevery = saveevery
        
    def init_velocities(self, from_C=False):
        """
        Defines way to initialize velocities. Random for the moment.
        
        Args:
            from_C (bool): uses C rand() function with constant seed for initialization,
            otherwise uses Python's random module with constant seed
        """
        self.velocity_a = vels.random(self.n_particles)
        self.velocity = self.velocity_a.ctypes.data_as(c_db_pointer)
        if from_C:
            mdc.init_vels.argtypes = [C.POINTER(System)]
            mdc.init_vels(C.byref(self))
        
class MD(C.Structure):
    """
    This class with for loading the system and running the simulation
    """
    def __init__(self, system, clist, integ):
        """
        Initializes MD trajectory.
        
        Args:
            system (System): system object
            clist (CellList): cell list object
            integ (Integrator): integrator object
       
        .. note::
            All arguments must have been properly initialized.
    
        """
        self.system = system
        self.clist = clist
        self.integ = integ
        self.time = 0
        mdc.simpleloop.argtypes = [c_int, C.POINTER(System), 
                             C.POINTER(CellList), C.POINTER(Integrator)]
        mdc.init_vars.argtypes = [C.POINTER(System), 
                             C.POINTER(CellList), C.POINTER(Integrator)]
        mdc.omp_get_num_threads.restype = c_int 
        mdc.omp_get_num_threads.argtypes = None
        
        mdc.init_vars(C.byref(self.system), C.byref(self.clist), 
                           C.byref(self.integ))
            
    def run(self):
        """
        Runs MD with number of loops defined in MD.system.n_steps, separated
        in an outer loop in python with npysteps, and an inner loop run in C
        with ncsteps, such that system.n_steps = npysteps * ncsteps
        """
        outerloops = int(self.system.n_steps/self.system.saveevery)
        efile = open('energy.dat', 'w')
        tfile = open('time.dat', 'w')
        tic = time.time()
        elapsed = 0
        for i in range(outerloops):
            step = i * self.system.saveevery
            self.time = step * self.system.timestep
            efile.write("{:.3f}, {:.3f}, {:.3f}\n".format(self.system.potential, 
                        self.system.kinetic, 
                        self.system.potential+self.system.kinetic))
            tfile.write("{:d}, {:.3f}\n".format(step, elapsed))
            
            mdc.simpleloop(self.system.saveevery, C.byref(self.system), 
                              C.byref(self.clist), C.byref(self.integ))
            tac = time.time()
            elapsed = tac-tic
            print('Elapsed time: {:.5f}, ave time per step: {:.5f}'.format(
                  elapsed, elapsed/((i+1)*self.system.saveevery)))
        print('Total time: {:.5f} s'.format(elapsed))
        
        efile.close()
        tfile.close()

    def runInnerLoop(self, i):
        step = i * self.system.saveevery
        self.time = step * self.system.timestep
            
        self.mdc.simpleloop(self.system.saveevery, C.byref(self.system), 
                              C.byref(self.clist), C.byref(self.integ))
        return self.system.potential, self.system.kinetic

        
if __name__ == "__main__":
    my_system = System()
    my_clist = CellList(my_system)
    my_integ = Integrator()
    this_MD = MD(my_system, my_clist, my_integ)
    this_MD.run()