import pathlib
import functional.otf.compilation.importer as imp


def load_precompiled_module(entrypoint_name):
    operator_hash = 'd8404acb42d954263c1f701c011ebf6126ca88bd67a0451bf9e3356b8c2931b6'
    module_lib_path = '/home/magdalena/Projects/exclaim/fortran_stuff/py4f/src/python_overhead/gt4py_cache/' + entrypoint_name + '_' + operator_hash + '/build/bin/' + entrypoint_name + '.cpython-310-x86_64-linux-gnu.so'
    module_path = pathlib.Path(module_lib_path)
    module = imp.import_from_path(module_path)
    print(f"loading {module}")
    compiled_fun = getattr(module, entrypoint_name)
    return compiled_fun
