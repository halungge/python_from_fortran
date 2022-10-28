import cffi_plugin_builder

cffi_functions_file = "communicator.py"
build_path = "./build/"
plugin_name = "ringcomm_plugin"
c_header = """
extern int setup_comm();
"""

cffi_plugin_builder.compile_cffi_plugin(
    plugin_name=plugin_name, c_header=c_header, cffi_functions_file=cffi_functions_file
)


