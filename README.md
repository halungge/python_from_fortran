# Calling Python from Fortran

* [stackoverflow](https://stackoverflow.com/questions/17075418/embed-python-into-fortran-90)
* [python embedding] (https://docs.python.org/2/extending/)

## Options and Tools
### using CFFI: 
  * [CFFI for embedding](https://cffi.readthedocs.io/en/latest/embedding.html)
  * [example blog post](https://www.noahbrenowitz.com/post/calling-fortran-from-python/) and corresponding [github repo] (https://github.com/nbren12/call_py_fort) This repository adds a library 
wrapper around the CFFI mechanism that is explained in the blog post. On top of  the plain CFFI wrapper and Fortran C Bindings it supports passing  data back and 
forth by packaging everything (including function names) in a STATE dict. The python functions used with the library all take this STATE dict as an argument and extract their "real" argument from it and set them back into the STATE, for example
```
def function(STATE):
    count = STATE.get("count", 0)
    # this code runs every function call
    print(f"function call_count {count}")
    STATE["count"] = count + 1
```
  
### [ForPy](https://github.com/ylikx/forpy):
is a library for embedding python written in Fortran. You initialize (and shutdown) the python runtime directly from 
within your fortran program. Python types are also created (and used) within the Fortran program and 
can then be cast into Fortran types.

  * (+) **small**, **readable code** 
  * (+) supports quite a few basic python data types, also "general python objects", and numpy arrays,
  * (?) how extendable is it?, can we use it with our datatypes. It might need lots of extending the library *in fortran* which we (I assume) don't want to do.
  * (?) types can be converted via cast function from python -> Fortran

In order to use we would have to further encapsulate the library and do the data mapping
in Fortran, which we don't want to do I guess...

### Others:
* [f2py](https://numpy.org/doc/stable/f2py/) that does it the other way round. But according to stackoverflow discussion above can also  be used
* ~~[forcallpy](https://forcallpy.readthedocs.io/en/latest/)~~ repo does not exist anymore

## ForPy example
see `src/forpy_sample`
### compile and run
the file `forpy_mod.F90` has been copied from `https://github.com/ylikx/forpy`
```bash
gfortran -c forpy_mod.F90
gfortran simple_forpy_example.f90 forpy_mod.o `python3-config --ldflags --embed`
```

## call py fort example
uses library from https://github.com/nbren12/call_py_fort
1. clone call_py_fort
```bash
mkdir -p lib
cd lib
git clone git@github.com:nbren12/call_py_fort.git
```
2. build the library
```commandline
cd call_py_fort
mkdir build
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
.venv/src/gt4py-functional/src/functional/ffront/decorator.py:235: UserWarning: Field View Program 'multiply_fields': Using default (<function executor at 0x7f9e1ac8add0>) backend.
  warnings.warn(
printing from python output =  [[ 1.  1.  4.  9. 25. 64.]
 [ 1.  1.  4.  9. 25. 64.]
 [ 1.  1.  4.  9. 25. 64.]]
   1.0000000000000000        1.0000000000000000        4.0000000000000000        9.0000000000000000        25.000000000000000        64.000000000000000        1.0000000000000000        1.0000000000000000        4.0000000000000000        9.0000000000000000        25.000000000000000        64.000000000000000        1.0000000000000000        1.0000000000000000        4.0000000000000000        9.0000000000000000        25.000000000000000        64.000000000000000     

```
## plain CFFI example
see `src/ffi_sample`


#### compile and run

1. compiling the ffi C bindings: 
```bash
cd src/cffi_sample
python sample_cffi_wrapper.py 
```
this generates a `.h` (because write it by hand in the code), `.c` (because `ffi_builder.emit_c_code()` is called) a `.o` and `lib*.so` file in the `$project/build` folder

2. compile the fortran example
```
cd src/cffi_sample
gfortran -o ../../build/sample_f run_cffi_sample.f90 -L../../build -lsample_plugin
```
and run it
```
> cd ../../build
> export LD_LIBRARY_PATH=/home/magdalena/Projects/exclaim/fortran_stuff/py4f/build/:$LD_LIBRARY_PATH
> ./hello_f
hello world!
```

there is a corresponding C program `run_cffi_sample.c` which calls the same python functions 
via the C wrapper from C.
```
cd src/cffi_sample
gcc -o ../../build/sample_c run_cffi_sample.c -L../../build -lsample_plugin
```
