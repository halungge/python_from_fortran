import numpy as np
from timing_plugin import ffi


# noqa: D414
@ffi.def_extern()
def do_nothing(inp: np.ndarray, outp: np.ndarray):
    pass


@ffi.def_extern()
def copy_array(inp: np.ndarray, outp: np.ndarray, n: int):
    outp[0:n] = inp[0:n]
