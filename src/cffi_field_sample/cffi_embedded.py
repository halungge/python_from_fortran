import numpy as np
from field_plugin import ffi

import sample_mod.field_functions


def unpack(ptr, size_x, size_y) -> np.ndarray:
    # for now only 2d, invert for row/column precedence...
    shape = (size_y, size_x)
    length = np.prod(shape)
    c_type = ffi.getctype(ffi.typeof(ptr).item)
    ar = np.frombuffer(
        ffi.buffer(ptr, length * ffi.sizeof(c_type)),
        dtype=np.dtype(c_type),
        count=-1,
        offset=0,
    ).reshape(shape)
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
