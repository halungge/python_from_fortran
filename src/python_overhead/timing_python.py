import pathlib

import numpy as np
import functional.otf.compilation.importer as imp

from timing_plugin import ffi

def load_precompiled_module(entrypoint_name):
    operator_hash = 'e1f5d85b0bd9044374ad44d3e2eabd47e2d61b2f3335e05b4dc22fd0d244b60e'
    module_lib_path = '/tmp/gt4py_cache/' + entrypoint_name + '_' + operator_hash + '/bin/' + entrypoint_name + '.cpython-310-x86_64-linux-gnu.so'
    module_path = pathlib.Path(module_lib_path)
    module = imp.import_from_path(module_path)
    compiled_fun = getattr(module, entrypoint_name)
    return compiled_fun

copy_gt4py = load_precompiled_module('field_copy')

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

@ffi.def_extern()
def copy_gt4py(inp:np.ndarray, outp:np.ndarray, size:int):
    copy_gt4py(inp, outp, size, size)

