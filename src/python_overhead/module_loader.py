import pathlib
import functional.otf.compilation.importer as imp



def load_precompiled_module(entrypoint_name):
    operator_hash = 'e1f5d85b0bd9044374ad44d3e2eabd47e2d61b2f3335e05b4dc22fd0d244b60e'
    module_lib_path = '/tmp/gt4py_cache/' + entrypoint_name + '_' + operator_hash + '/bin/' + entrypoint_name + '.cpython-310-x86_64-linux-gnu.so'
    module_path = pathlib.Path(module_lib_path)
    module = imp.import_from_path(module_path)
    print(f"loading {module}")
    compiled_fun = getattr(module, entrypoint_name)
    return compiled_fun
