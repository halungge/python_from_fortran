# Goal 
the goal of this experiment is to find out how you can use [MPI communication](https://www.open-mpi.org/) for programs
interfacing Python and Fortran. 

## MPI4Py
see [mpi4py documentation](https://mpi4py.readthedocs.io/en/stable/)
`mpi4py` needs a running mpi installation, it provides Python wrapper around C MPI
For basic usage see examples in documentation or see [hello_mpi.py](./hello_mpi.py)

## basic observations
### initialization of mpi4py
MPI needs to be initialized with a call to `MPI_Init` this initialization must be done only once. 
`from mpi4py import MPI`
calls `MPI_init` implicitly so if you want to do the initialization by hand, before the import of `MPI` do
```python
import mpi4py
mpi4py.rc.initialize=False
```


### upper vs lower case communication methods
on the `Comm` class 
in `mpi4py`  there are communication functions defined that differ only in the case of the first letter:
```
comm.Send(...)
comm.send(...)
(...)
```
The capital one expects buffers and data types (as it is used in MPI C interface) and can be used directly for python objects
implementing the Puffer buffer interface. The lower case ones supposedly take any python object and pickle it. Since we
are interested in Fortran/C arrays and numpy ndarrays we need to *upper case* ones

### running the hello_mpi example
```commandline
> mpiexec -np 4 python hello_mpi.py 
```

## intercommunication experiment
### setup
1. the entire experiment is driven by a Fortran main program. It initializes data arrays and creates a custom communicator.
2. define a python function that calculates a stencil on a local field doing the necessary halo exchange in python. The 
halo exchange is done using a previousely defined communicator.
2. this python program is called from the Fortran main program via the CFFI embedding with Fortran bindings  (see top level [README](../../README.md)))


### Mesh and Topology
For simplicity we use a 2D Cartesian field and a Cartesian Topology in the communicator (see [communicator.f90](./fortran/communicator.90))

### Communicator re-usage
the communicator in Fortran is represented by an integer value. This value needs to be passed to python such that python can
look up the correct communicator from the MPI runtime.
`mpi4py` provides a class method [f2py](https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.f2py)on the `Comm` class 
that takes the integer value and returns the communicator instance
This is not to be confused with the example about [wrapping mpi with numpy.f2py](https://mpi4py.readthedocs.io/en/stable/tutorial.html#wrapping-with-f2py) in the docs.



### How to build and run the example
Running
```bash
> python driver_builder.py
```
creates the C shared library that captured by the Fortran interface in [driver.f90](./fortran/driver.f90). It creates 
```commandline
driver_plugin.h
driver_plugin.c
driver_plugin.o
libdriver_plugin.so
```
in the current directory

```commandline
> cd fortran
> export LIB=../
> mpif90 -I$LIB -Wl,-rpath=$LIB -L$LIB  communicator.f90 driver.f90 main.f90 -ldriver_plugin -o run_parallel
> mpiexec -n 4 ./run_parallel
```





## experiment
- [x] Fortran: program: initialize communicator
- [x] Fortran: initialize local fields
- [x] python: gt4py program
- [x] python: driver: exchange + program call
- [x] python: cffi wrapper
- [x] Fortran: interface for driver call

## TODOs:
-  [ ] opposite direction: create communicator in python and use it from Fortran 
 - [ ] generate Fortran Interface for generated C Library 
 - [ ] cffi builder generalize
- [ ] exercise: switch to unstructured grid!
