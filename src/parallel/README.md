# Goal 
the goal of this experiment is to find out how you can use [MPI communication](https://www.open-mpi.org/) for programs
interfacing Python and Fortran. 

## MPI4Py
see [mpi4py documentation](https://mpi4py.readthedocs.io/en/stable/)
`mpi4py` needs a running mpi installation, it provides Python wrapper around C MPI
For basic usage see examples in documentation or see [hello_mpi.py](./hello_mpi.py)

## basic observations for mpi4py
### initialization of mpi4py
MPI needs to be initialized with a call to `MPI_Init` this initialization must be done only once. You can always 
test whether mpi has already been initialized by calling `MPI_Initialized()`
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

### interfacing with Fortran
Misleadingly the `mpi4py` documentation only talks about wrapping Fortran MPI with `numpy.f2py`:  [wrapping mpi with numpy.f2py](https://mpi4py.readthedocs.io/en/stable/tutorial.html#wrapping-with-f2py) 
I tried generating a Python module from Fortran with `numpy.f2py`. The Fortran module would define a communicator and
some specific communication routines on it (see `fortran/communicator.f90`) Setting up this communicator and calling the
communication routines later on from Python via the `numpy.f2py` module does not work: The Python processor do not
access automatically the correct communicator with the pre allocated id, instead the spin up their own communicators 
which do not know of the MPI context such that each Python process has its own communicator only containing the process itself.

Instead for accessing a Fortran predefined processor `mpi4py` provides a class method on class method [f2py](https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.f2py) on the `Comm` class
that takes an integer Id (type of a Fortran communicator) and returns the corresponding `Comm` instance.

## Code content
### mpi4py hello world example 
[hello_mpi.py](hello_mpi.py)

run it with
```commandline
> mpiexec -np 4 python hello_mpi.py 
```

### fortran hello world example
[mpi_helloworld.f90](fortran/mpi_helloworld.f90)

run it with
```commandline
cd fortran
mpif90 mpi_helloworld.f90  -o mpi_hello_world
mpiexec -np 4 ./mpi_hello_world
```

### cartesian communicator in fortran
[call_communicator.f90](fortran/call_communiator.f90)
run it with
```commandline
cd fortran
mpif90 communicator.f90 call_communicator.f90  -o call_communicator
mpiexec -np 4 ./call_communicator
```

### using Fortran communicator from Python
#### setup
1. the entire experiment is driven by a Fortran main program. It initializes data arrays and creates a custom [communicator](fortran/communicator.f90)
2. define a Python function that calculates a stencil on a local field doing the necessary halo exchange in python. The 
halo exchange is done using a previousely defined communicator.
2. this Python program is called from the Fortran main program via the CFFI embedding to C and Fortran bindings  (see top level [README](../../README.md)))


#### Mesh and Topology
For simplicity we use a 2D Cartesian field and a Cartesian Topology in the communicator (see [communicator.f90](./fortran/communicator.90))

#### Communicator re-usage
The communicator in Fortran is represented by an integer value. This value needs to be passed to Python such that `mpi4py` 
can look up the correct communicator from the MPI runtime. To this end
`mpi4py` provides a method [f2py](https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.f2py)
that takes the integer value and returns the communicator instance
in the docs.



Run the example with
```bash
> cd src/parallel
> python driver_builder.py
```
creates the C shared library that captured by the Fortran interface in [driver.f90](./fortran/driver_interface.f90). It creates 
```commandline
driver_plugin.h
driver_plugin.c
driver_plugin.o
libdriver_plugin.so
```
in the current (`src/parallel/`) directory. Then

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
