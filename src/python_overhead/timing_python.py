import numpy as np
from timing_plugin import ffi


@ffi.def_extern()
def do_nothing(inp: np.ndarray, outp: np.ndarray):
    """
    essentially to nothing resetting output to input pointer

    :param inp:
    :param outp:
    :return:
    """


@ffi.def_extern()
def copy_array(inp: np.ndarray, outp: np.ndarray, n: int):
    """
    copy input to output
    :param inp:
    :param outp:
    :param n: length of the array (needed for cffi)
    :return:
    """
    outp[0:n] = inp[0:n]
