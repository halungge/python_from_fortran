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
> python -m numpy.f2py communicator.f90 -m fortran_communicator -h communicator.pyf --overwrite-signature
> python -m numpy.f2py --f90exec=mpif90 --f77exec=mpif77 -c communicator.pyf communicator.f90 
```

then im python

```python
>>> from fortran_communicator import communicator
>>> communicator.setup_comm()

```

### TODO
- check data layour
- check args (intent(in), intent(out)) from the [`f2py` documentation](https://numpy.org/doc/stable/f2py/f2py.getting-started.html)