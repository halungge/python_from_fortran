import os
import sys
sys.path.insert(0, "/home/magdalena/Projects/exclaim/fortran_stuff/py4f/src/parallel")
import numpy as np
from functional.iterator.embedded import np_as_located_field

from parallel.dimensions import VDim, IDim, JDim
from parallel.operators import local_invert, cart_laplace
from fortran.fortran_communicator import communicator

from driver_plugin import ffi



def run_step_invert(comm, input, recv_buf, send_buf):
    comm.exchangeLeft(send_buf, recv_buf)
    input_field = np_as_located_field(VDim)(input)
    result_field = np_as_located_field(VDim)(send_buf)
    local_invert(input_field, result_field, offset_provider={})


def handle_error(exception, exc_value, traceback):
    print(f"exception {exception} value {exc_value}")
    if traceback is not None:
        print("original arguments were:")
        inptr = traceback.tb_frame.f_locals['input_ptr']
        print(f"input_ptr: type = {type(inptr)}  ")
        inptr = traceback.tb_frame.f_locals['output_ptr']
        print(f"output_ptr: type = {type(inptr)}  ")
        xl = traceback.tb_frame.f_locals['x_length']
        yl = traceback.tb_frame.f_locals['y_length']
        print(f"sizes {xl} x {yl}")

@ffi.def_extern(onerror=handle_error)
def run_cart_step(input_ptr:np.ndarray, output_ptr: np.ndarray, x_length:int, y_length:int):
    in_unpack = unpack(input_ptr, x_length, y_length)
    out_unpack = unpack(output_ptr, x_length, y_length)
    communicator.setup_comm()
    my_rank = communicator.get_my_rank()
    print(f"driver.py: rank {my_rank} python pid {os.getpid()}")
    print(f"driver.py: rank {my_rank} run_cart_step: before exchange params sending left ={in_unpack[1, 0:x_length]} receiving from right={in_unpack[0, 0:x_length]}, xlength={x_length}, ylength={y_length}")
    communicator.exchangeleft(in_unpack[1, 0:x_length], in_unpack[0, 0:x_length])
    communicator.exchangeright(in_unpack[y_length - 2, 0:x_length], in_unpack[y_length - 1, 0:x_length])
    print(f"driver.py: rank {my_rank} run_cart_step: after exchange params sending left ={in_unpack[1, 0:x_length]} received from right={in_unpack[0, 0:x_length]}, xlength={x_length}, ylength={y_length}")

    input_field = np_as_located_field(IDim, JDim)(in_unpack)
    output_field = np_as_located_field(IDim, JDim)(out_unpack)
    cart_laplace(input_field, output_field, offset_provider={"Ioff": IDim, "Joff":JDim})
    communicator.cleanup()

def unpack(ptr, size_x, size_y) -> np.ndarray:
    """
    unpacks a 2d c/fortran field into a numpy array.

    :param ptr: c_pointer to the field
    :param size_x: num of rows (i.e. left most index, continuous in fortran)
    :param size_y: num of cols (i.e. right index, with stride size_x
    :return: a numpy array with shape=(size_y, size_x)
    and dtype = ctype of the pointer
    """
    # for now only 2d, invert for row/column precedence...
    shape = (size_y, size_x)
    length = np.prod(shape)
    c_type = ffi.getctype(ffi.typeof(ptr).item)
    ar = np.frombuffer(
        ffi.buffer(ptr, length * ffi.sizeof(c_type)),
        dtype=np.dtype(c_type),
        count=-1,
        offset=0,
    ).reshape(shape)
    return ar
