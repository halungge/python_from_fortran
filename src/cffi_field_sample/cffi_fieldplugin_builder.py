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

with open("cffi_embedded.py") as f:
    module = f.read()

builder.embedding_init_code(module)
builder.compile(tmpdir=build_path, target="libfield_plugin.*", verbose=True)
