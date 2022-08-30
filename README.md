# Calling Python from Fortran

* [stackoverflow](https://stackoverflow.com/questions/17075418/embed-python-into-fortran-90)
* [python embedding] (https://docs.python.org/2/extending/)

## Options and Tools
* using CFFI: 
  * [example blog post](https://www.noahbrenowitz.com/post/calling-fortran-from-python/) and corresponding [github repo] (https://github.com/nbren12/call_py_fort)
    * [CFFI for embedding](https://cffi.readthedocs.io/en/latest/embedding.html)
* [ForPy](https://github.com/ylikx/forpy) : is actually a library for embedding python written in Fortran
  * (+) **small**, **readable code** 
  * (+) supports quite a few basic python data types, also "general python objects", and numpy arrays,
  * (?) how extendable is?, can we use it with our datatypes. It might need lots of extending the library *in fortran* which we (I assume) don't want to do.
  * (?) types can be converted via cast function
* [f2py] (https://numpy.org/doc/stable/f2py/) that does it the other way round. But according to stackoverflow discussion above can also  be used
* ~~[forcallpy](https://forcallpy.readthedocs.io/en/latest/)~~ repo does not exist anymore


## FFI example
see `src/ffi_sample`
### TODOs
* [ ] setup.py, setup.cfg, toml...
* [ ] fix doc strings in python code


#### compile and run

1. compiling the ffi C bindings: 
```
> python hello_world_ffi_wrapper.py 
```
this generates a `.h` (because write it by hand in the code), `.c` (because `ffi_builder.emit_c_code()` is called) a `.o` and `lib*.so` file in the `$project/build` folder

2. compile the fortran example
```
> gfortran -o ../../build/hello_f test_hello_world.f90 -L../../build -lhello_plugin
```
and run it
```
cd ../../build
> export LD_LIBRARY_PATH=/home/magdalena/Projects/exclaim/fortran_stuff/py4f/build/:$LD_LIBRARY_PATH
. ./hello_f
hello world!
```