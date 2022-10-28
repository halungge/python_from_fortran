import pathlib

import numpy as np
from python_overhead.module_loader import load_precompiled_module
from timing_plugin import ffi


copy_gt4py_fun = load_precompiled_module('field_copy')

# noqa: D414
@ffi.def_extern()
def do_nothing(inp: np.ndarray, outp: np.ndarray):
    """
    Do nothing at all.

    Args:
        inp: input field
        outp: output field (untouched!)

    Returns:
    """


@ffi.def_extern()
def copy_array(inp: np.ndarray, outp: np.ndarray, n: int):
    outp[0:n] = inp[0:n]


def unpack(ptr, size) -> np.ndarray:
    """
    unpacks c pointer into a numpy array.

    :param ptr: c_pointer to the field
    :param sizes: tuple[int] the array dimensions
    :return: a numpy array with shape=(size_y, size_x)
    and dtype = ctype of the pointer
    """
    length = size
    c_type = ffi.getctype(ffi.typeof(ptr).item)
    ar = np.frombuffer(
        ffi.buffer(ptr, length * ffi.sizeof(c_type)),
        dtype=np.dtype(c_type),
        count=-1,
        offset=0,
    )
    return ar

@ffi.def_extern()
def copy_gt4py(inp, outp, size:int):
    inp = unpack(inp, size)
    outp = unpack(outp, size)
    copy_gt4py_fun(inp, outp, size, size)

