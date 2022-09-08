import cffi

builder = cffi.FFI()

build_path = "./build/"

header = """
extern void square(double *, int, int, double *);
"""

with open(build_path + "field_plugin.h", "w") as f:
    f.write(header)

builder.embedding_api(header)
builder.set_source("field_plugin", r'''#include "field_plugin.h"''')
module = """
import sample_mod.field_functions
import numpy as np
from field_plugin import ffi

def unpack(ptr, size_x, size_y) -> np.ndarray:
    # for now only 2d, invert for row/column precedence...
    shape = (size_y, size_x)
    length = np.prod(shape)
    c_type = ffi.getctype(ffi.typeof(ptr).item)
    ar = np.frombuffer(ffi.buffer(ptr, length * ffi.sizeof(c_type)), 
            dtype=np.dtype(c_type), 
            count=-1,
            offset=0).reshape(shape)
    return ar


def pack(ptr, arr: np.ndarray):
    # for now only 2d
    length = np.prod(arr.shape)
    c_type = ffi.getctype(ffi.typeof(ptr).item)
    ffi.memmove(ptr, np.ravel(arr), length * ffi.sizeof(c_type))


@ffi.def_extern()
def square(field, nx, ny, result):
    a = unpack(field, nx, ny)
    print(a)
    res = sample_mod.field_functions.square_ar(a)
    print(res)
    pack(result, res)
"""

builder.embedding_init_code(module)
builder.emit_c_code(build_path + "field_plugin.c")
builder.compile(tmpdir=build_path, target="libfield_plugin.*", verbose=True)
