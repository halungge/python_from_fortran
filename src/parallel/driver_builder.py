import cffi


cffi_functions_file = "driver.py"
build_path="."
plugin_name="driver_plugin"
c_header = """
extern void run_step(double* input, double* output, int xLength, int localSize);
extern void run_cart_step(double* input, double* output, int xLength, int localSize);
"""


def compile_cffi_plugin(plugin_name:str, c_header:str, cffi_functions_file:str, build_path="."):
    f"""
    creates a linkable C library for the functions in {cffi_functions_file} that are decorated with '@ffi.def_extern' and correspond to a C signature in the header string
    :param plugin_name: name of the plugin, a linkable C library with the name 'lib{plugin_name}.so' will be created in the build_path folder'
    :param c_header: C type header signature for the python functions.
    :param cffi_functions_file: input file that contains python functions correspondig to the signature in the '{c_header}' string, these functions must be decorated with @ffi.def_extern() and the file must contain the import 'from {plugin_name} import cffi'
    :param build_path: *optional* path to build directory
    :return:
    """
    c_header_file = plugin_name + ".h"
    with open("/".join([build_path, c_header_file]), "w") as f:
        f.write(c_header)

    builder = cffi.FFI()

    builder.embedding_api(c_header)
    builder.set_source(plugin_name, f'#include "{c_header_file}"')

    with open(cffi_functions_file) as f:
        module = f.read()

    builder.embedding_init_code(module)

    builder.compile(tmpdir=build_path, target=f"lib{plugin_name}.*", verbose=True)


compile_cffi_plugin(plugin_name=plugin_name, c_header=c_header, cffi_functions_file=cffi_functions_file)