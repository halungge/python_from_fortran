"""build a cffi module for testing simple python overhead."""
import cffi

builder = cffi.FFI()

build_path = "./build/"

header = """
extern void do_nothing(double *, double *);
extern void  copy_array(double *, double *, int size);
"""

with open(build_path + "timing_plugin.h", "w") as f:
    f.write(header)

builder.embedding_api(header)
builder.set_source("timing_plugin", r'''#include "timing_plugin.h"''')

with open("./timing_python.py") as f:
    module = f.read()

builder.embedding_init_code(module)
builder.compile(tmpdir=build_path, target="libtiming_plugin.*", verbose=True)
