# MPI4Py
`mpi4py` needs a running mpi installation
see [mpi4py documentation](https://mpi4py.readthedocs.io/en/stable/)


## things to check
- [ ] upper vs lower case communication methods

on the Comm class there are several communication functions defined:
```
comm.Send(...)
comm.send(...)
```

It seems that the capital one expects buffers and data types (as it is used in MPI C interface) and can be used directly for python objects
implementing the buffer interface. The small case one takes any python object and pickles it.

```commandline
def Send(self, buf, dest, tag=0):
    
def send(self, obj, dest, tag=0): # real signature unknown; restored from __doc__
```
but I did not get the lower case one to run.

## intercommunication between languages
the goal is to check whether and how a communicator defined from a fortran code can be used/ accessed from within 
Python. The szenario being a model that is setup in Fortran and calls an embedded function (via CFFI or some wrapper)
library (see top level [README](../../README.md)). This function communicates a MPI communicator that has been setup
in the initial model setup.


## Mesh
to keep thing simple we only use vertices and edges and we split procs only along one dimension
the field is periodic that is the domain can be understood as torus where we only cut "slices".

We restrict shifts to V2E2V, or V2E: that is we shift from one Vertex along adjacent edges to the neighboring vertices. 
### vertices
We have a total number of `n_global_vertices = 96` vertices where on the proc-local dimension there are 8 vertical vertices.
That means that locally we have `n_global_vertices / 8 / num_procs` horizontal vertices. The number of halo vertices is always 2 * 8.

### edges
for each vertex there are 3 edges. With the available shiftings the mesh can be defined such that only non-proc-local (halo) edges are only needed from one neighbor.
Hence here aswell we need `2 * 8` halo edges.

(-> include pic)


## building with f2py

```commandline
> cd fortran
> python -m numpy.f2py communicator.f90 -m fortran_communicator -h communicator.pyf --overwrite-signature
> 
 
```
The first line generates a `communicator.pyf` 
wrapper that can be further manipulated by hand.

then im python

```python
>>> from fortran_communicator import communicator
>>> communicator.setup_comm()
>>> error = communicator.exchangeleft(a,b)
>>> communicator.cleanup()
```

### py2f and fortran args: intent(...)
`numpy` arrays that are fortran contiguous and has a `dtype` maching the fortran type

TODO: type list
the input array is directly passed. If this i not the case a Fortran contiguous copy is made and
passed to the Fortran routine. *The original array is not manipulated and stays the same.!*
If you want the manipulation to be reflected in the input array 
(Fortran `intent(inout)`) either use a Fortran contiguous array or use the (py2f specific)
`intent(inplace)` in the .py2f

#### intent(in)
creates an python input parameter in the python function
#### intent(out)
creates a return value, no corresponding input argument is taken. 
#### intent(inout)
creates an input parameter
#### input(inplace)
`py2f` addition (see above) use for inplace manipulation of non fortran contiguous arrays.

see [py2f doc](https://numpy.org/doc/stable/f2py/f2py.getting-started.html)

### TODO
- check data layout
- check args (intent(in), intent(out)) from the [`f2py` documentation](https://numpy.org/doc/stable/f2py/f2py.getting-started.html)


## main expertiment
- [ ] Fortran: program: initialize communicator
- [ ] Fortran: initialize local fields
- [x] python: gt4py program
- [x] python: driver: exchange + program call
- [x] python: cffi wrapper
- [x] Fortran: interface for driver call
- [ ] Fortran: call driver
- [ ] exercise: switch to unstructured grid!

## potential problems:
 - [ ] py2f: iso_c_binding??
 - [ ] how does py2f handle fortran arrays, layouting, what are the requirements there
 - [ ] cffi builder generalize

