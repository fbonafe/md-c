import ctypes as C
mdc = C.CDLL('../libmd.so')
mdc.main.argtypes = [C.c_float, C.c_float]
mdc.main(1000., 1000.)
