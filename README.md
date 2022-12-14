# Calling Python from Fortran
Goal of this repo is to explore interoperability of Fortan and Python. Mainly, to explore how Python can be called 
from Fortran. That is *embedding* python into Fortran (not *extending* Python with Fortran)
Some discussion can be found here:

* [stackoverflow](https://stackoverflow.com/questions/17075418/embed-python-into-fortran-90)
* [python embedding] (https://docs.python.org/2/extending/)

## Content
1. Embedding Python
we explore several solutions/tools for embedding python. There is example code for each of them in 
[src](src) (see below.)
2. Python overhead: to assess the overhead created by starting a Python interpreter from Python some simple experiments 
were run. These can be found in [python_overhead](src/python_overhead/README.md)
2. Using MPI Communicators 
We explore how a [MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface). For Detail see the [README](src/parallel/README.md) 
in `src/parallel` 

## Embedding Python
### [CFFI](https://cffi.readthedocs.io) 
Resources: 
  * [CFFI for embedding](https://cffi.readthedocs.io/en/latest/embedding.html)
  * [example blog post](https://www.noahbrenowitz.com/post/calling-fortran-from-python/) and 
corresponding repo [call_py_fort](https://github.com/nbren12/call_py_fort) that adds some functionality around the CFFI mechanism

#### Examples using CFFI directly
see [cffi_sample](src/cffi_sample) or for an example using [gt4py](https://github.com/GridTools/gt4py/tree/functional): [cffi_field_sample](src/cffi_field_sample).

CFFI generates C source code and a C linked library. In order to use it in Fortran you need an additional
Fortran interface for the generated C header file. 


##### compile and run

1. compiling the ffi C bindings: 
```bash
cd src/cffi_sample
mkdir build
python sample_cffi_wrapper.py 
```
this generates a `.h` (because write it by hand in the code), `.c` (because `ffi_builder.emit_c_code()` is called) a `.o` and `lib*.so` file in the `$project/build` folder

2. compile the fortran example
```
export LIB=./build
gfortran -o ./sample_f -I$LIB -Wl,-rpath=$LIB -L$LIB run_cffi_sample.f90 -lsample_plugin
```
and run it
```
> ./sample_f
hello world!
python-print: summing up to 5 = 15
 fortran calling python, res=          15

```

there is a corresponding C program `run_cffi_sample.c` which calls the same python functions 
via the C wrapper from C.
```
cd src/cffi_sample
gcc -o ./sample_c -I$LIB -Wl,-rpath=$LIB -L$LIB run_cffi_sample.c -lsample_plugin
```

The process works analogousely for the field example
```bash
> cd src/cffi_field_sample
> mkdir build
> python cffi_fieldplugin_builder.py
> export LIB=./build
> gfortran -I$LIB -Wl,-rpath=$LIB -L$LIB  field_functions_mod.f90 run_field_sample.f90 -lfield_plugin
./a.out
fortran input: field =    1.0000000000000000        1.0000000000000000        2.0000000000000000        3.0000000000000000        5.0000000000000000        8.0000000000000000        1.0000000000000000        1.0000000000000000        2.0000000000000000        3.0000000000000000        5.0000000000000000        8.0000000000000000        1.0000000000000000        1.0000000000000000        2.0000000000000000        3.0000000000000000        5.0000000000000000        8.0000000000000000     
[[1. 1. 2. 3. 5. 8.]
 [1. 1. 2. 3. 5. 8.]
 [1. 1. 2. 3. 5. 8.]]
py4f/.venv/src/gt4py-functional/src/functional/ffront/decorator.py:235: UserWarning: Field View Program 'multiply_fields': Using default (<function executor at 0x7f85757fe830>) backend.
  warnings.warn(
[[ 1.  1.  4.  9. 25. 64.]
 [ 1.  1.  4.  9. 25. 64.]
 [ 1.  1.  4.  9. 25. 64.]]
 fortran output: res =   1.0000000000000000        1.0000000000000000        4.0000000000000000        9.0000000000000000        25.000000000000000        64.000000000000000        1.0000000000000000        1.0000000000000000        4.0000000000000000        9.0000000000000000        25.000000000000000        64.000000000000000        1.0000000000000000        1.0000000000000000        4.0000000000000000        9.0000000000000000        25.000000000000000        64.000000000000000     

```
##### Assessment
* (+) CFFI builder is quite simple to use.
* (+) CFFI provides direct functionality convert to numpy arrays via the buffer interface 
* (-) Fortran interface needs to written (or generated). 
* (+) From Fortran side the calling is quite natural, simply call a Fortran subroutine.
* (-) (*development mode only*) changes in the python code decorated with the @ffi.def_extern have to be run through the cffi 
generator `python xxx.py` before the get picked up 



#### [call_py_fort example](call_py_fort_sample)
Uses this [call_py_fort](https://github.com/nbren12/call_py_fort): This repository adds a library 
wrapper around the CFFI mechanism that is explained in the blog post. 
On top of  the plain CFFI wrapper and Fortran C Bindings it supports passing  data back and 
forth by packaging everything (including function names) in a STATE dict. The python functions used with the library all take this STATE dict as an argument and extract their "real" argument from it and set them back into the STATE, for example
```
def function(STATE):
    count = STATE.get("count", 0)
    # this code runs every function call
    print(f"function call_count {count}")
    STATE["count"] = count + 1
```


The library uses cffi under the hood to publish a functions that allow you to register and read data from to a global 
python dictionary called `STATE`.
`set_state...(...)`, `get_state_...(...)` and call any python module that uses this data.

##### compile and run the example
1. clone call_py_fort
```bash
mkdir -p lib
cd lib
git clone git@github.com:nbren12/call_py_fort.git
```
2. build the library
```bash
cd call_py_fort
mkdir build
cd build
cmake ..
make
```
3. build and run the fortran code 
```
> 
> export LIB=../../lib/call_py_fort/build/src/
> gfortran -I$LIB -Wl,-rpath=$LIB -L$LIB  field_functions.f90 -lcallpy
> ./a.out
printing from python input =  [[1. 1. 2. 3. 5. 8.]
 [1. 1. 2. 3. 5. 8.]
 [1. 1. 2. 3. 5. 8.]]
py4f/.venv/src/gt4py-functional/src/functional/ffront/decorator.py:235: UserWarning: Field View Program 'multiply_fields': Using default (<function executor at 0x7f9e1ac8add0>) backend.
  warnings.warn(
printing from python output =  [[ 1.  1.  4.  9. 25. 64.]
 [ 1.  1.  4.  9. 25. 64.]
 [ 1.  1.  4.  9. 25. 64.]]
   1.0000000000000000        1.0000000000000000        4.0000000000000000        9.0000000000000000        25.000000000000000        64.000000000000000        1.0000000000000000        1.0000000000000000        4.0000000000000000        9.0000000000000000        25.000000000000000        64.000000000000000        1.0000000000000000        1.0000000000000000        4.0000000000000000        9.0000000000000000        25.000000000000000        64.000000000000000     

```

##### Assessment
* (+) the interface is very general and let's you call any python function that is in loaded in you environment.
* python functions are called by name by importing the module on the fly and looking up the function. 
 All data has to be registered in the STATE dictionary and reading it from there again. 
  * (-) makes the interface generic but very chatty: from the Fortran side you have to know a lot of internals of your Python environment (variables, function names)
  * (-) compile time typesafety in Fortran is lost
  * (+) overhead from the lookup by name of python modules and STATE dict lookup turned out to be negligeable
* (+/-) (*development mode only*) due to the fact that the Python function is dynamically looked up, changes in the 
  function are automatically picked up by the fortran code. For direct use of CFFI the CFFI wrapper has to be 
regenerated. (This is only useful advantage during development when installing with pip -e ) 

  
### [ForPy](https://github.com/ylikx/forpy):
is a library for embedding python written in Fortran. You initialize (and shutdown) the python runtime directly from 
within your fortran program. Python types are also created (and used) within the Fortran program and 
can then be cast into Fortran types.

  * (+) **small**, **readable code** 
  * (+) supports quite a few basic python data types, also "general python objects", and numpy arrays,
  * (?) how extendable is it?, can we use it with our datatypes. It might need lots of extending the library *in fortran* which we (I assume) don't want to do.
  * (?) types can be converted via cast function from python -> Fortran
  * the focus of this library seem to be Fortran programmers that want to directly use python libraries (scipy, numpy): It provides
more the feeling of using a Python CLI from Fortran

In order to use we would have to further encapsulate the library and do the data mapping
in Fortran, which we don't want to do I guess...





### Others possible options, that were not explored:
* [f2py](https://numpy.org/doc/stable/f2py/) that does it the other way round. But according to stackoverflow discussion above can also  be used, you can call python from fortran via callbacks [TODO]
* ~~[forcallpy](https://forcallpy.readthedocs.io/en/latest/)~~ repo does not exist anymore
* [pyFort](http://pyfortran.sourceforge.net/pyfort/pyfort_reference.htm): also used for extending Python, that is calling Fortran from Python

## ForPy example
see `src/forpy_sample`

### compile and run
the file `forpy_mod.F90` has been copied from `https://github.com/ylikx/forpy`

```bash
gfortran -c forpy_mod.F90
gfortran simple_forpy_example.f90 forpy_mod.o `python3-config --ldflags --embed`
```


