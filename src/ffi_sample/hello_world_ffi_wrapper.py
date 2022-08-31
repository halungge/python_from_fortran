"""
defines a plugin called hello_plugin
"""

import cffi
ffi_builder = cffi.FFI()

build_path = "../../build/"

"""
define the api that we want to export in the DLL

if we had an existing C library with a .h file we could read that in and pass it to the ffi_builder.embedding_api()
we don't have that here so we define it inline and write a C type .h file, 

this .h file 
"""

header = """
extern void hello_world(void);
extern int sumup(int);
"""

with open(build_path + "hello_plugin.h", "w") as f:
    f.write(header)

ffi_builder.embedding_api(header)
"""
define the modules name from the Python point of view:
    makes this module available under module name to the python code (see below in 'module'),
    add additional C code, possibly constants, other includes...
"""
ffi_builder.set_source("hello_plugin", r'''
    #include "hello_plugin.h"
''')

module = """
from hello_plugin import ffi
import functools

@ffi.def_extern()
def hello_world():
    print("hello world!")
    
@ffi.def_extern()
def sumup(limit:int)->int:
   res = sum(range(limit + 1)) 
   return res    

"""

ffi_builder.embedding_init_code(module)
ffi_builder.emit_c_code(build_path + "hello_plugin.c")
ffi_builder.compile(tmpdir=build_path, target="libhello_plugin.*", verbose=True)