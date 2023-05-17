"""
Pseudo python driver.

to be used as fortran cffi plugin. Functions here in do
1. packing/unpackgin from fortran,
2. halo exchange using a look up for a fortran defined communicator
3. call gt4py stencil

and possible repeat step 2 and 3

"""
import mpi4py
import numpy as np
from driver_plugin import ffi
from gt4py.next.ffront.fbuiltins import Field, float64
from gt4py.next.iterator.embedded import np_as_located_field
from mpi4py import MPI
from mpi4py.MPI import Cartcomm, Comm

from parallel.dimensions import IDim, JDim, VDim
from parallel.operators import cart_laplace, local_invert

mpi4py.rc.initialize = False


def run_step_invert(comm, inp, recv_buf, send_buf):
    comm.exchangeLeft(send_buf, recv_buf)
    input_field = np_as_located_field(VDim)(inp)
    result_field = np_as_located_field(VDim)(send_buf)
    local_invert(input_field, result_field, offset_provider={})


def handle_error(exception, exc_value, traceback):
    """
    Error handler for embedded cffi.

    Args:
        exception: exception thrown in python
        exc_value: error value
        traceback: dictionary offering access to the original arguments of the python call

    """
    print(f"exception {exception} value {exc_value}")
    if traceback is not None:
        print("original arguments were:")
        inptr = traceback.tb_frame.f_locals["input_ptr"]
        print(f"input_ptr: type = {type(inptr)}  ")
        inptr = traceback.tb_frame.f_locals["output_ptr"]
        print(f"output_ptr: type = {type(inptr)}  ")
        xl = traceback.tb_frame.f_locals["x_length"]
        yl = traceback.tb_frame.f_locals["y_length"]
        print(f"sizes {xl} x {yl}")


@ffi.def_extern(onerror=handle_error)
def run_cart_step(
    comm_ptr: int,
    input_ptr: np.ndarray,
    output_ptr: np.ndarray,
    x_length: int,
    y_length: int,
):
    """
    Run one single step including unpacking, halo exchange and appliation of stencil.

    Args:
        comm_ptr: mpi communicator
        input_ptr: 2d input array
        output_ptr: 2d output array
        x_length: shape of the arrays x_length x y_length
        y_length:
    Returns:
    """
    in_unpacked = unpack(input_ptr, x_length, y_length)
    out_unpacked = unpack(output_ptr, x_length, y_length)
    comm = get_comm(comm_ptr)
    do_halo_exchange(comm, in_unpacked, x_length, verbose=True)
    input_field = np_as_located_field(IDim, JDim)(in_unpacked)
    output_field = np_as_located_field(IDim, JDim)(out_unpacked)
    cart_laplace(
        input_field, output_field, offset_provider={"Ioff": IDim, "Joff": JDim}
    )


@ffi.def_extern(onerror=handle_error)
def run(
    comm_ptr: int,
    input_ptr: np.ndarray,
    output_ptr: np.ndarray,
    x_length: int,
    y_length: int,
):
    def do_step(
        comm: Comm,
        in_field: Field[[IDim, JDim], float64],
        out_field: Field[[IDim, JDim], float64],
        verbose: bool,
    ):
        do_halo_exchange(comm, in_unpacked, x_length, verbose)
        cart_laplace(in_field, out_field, offset_provider={"Ioff": IDim, "Joff": JDim})
        in_field = out_field

    in_unpacked = unpack(input_ptr, x_length, y_length)
    out_unpacked = unpack(output_ptr, x_length, y_length)
    input_field = np_as_located_field(IDim, JDim)(in_unpacked)
    output_field = np_as_located_field(IDim, JDim)(out_unpacked)
    comm = get_comm(comm_ptr)
    for i in range(10):
        do_step(comm, input_field, output_field, verbose=i == 0)


def get_comm(comm_ptr: int):
    comm = MPI.Comm.f2py(comm_ptr)
    num_procs = comm.Get_size()
    topo = comm.Get_topology()
    name = comm.Get_name()
    my_rank = comm.Get_rank()
    left_neighbor, right_neighbor = comm.Shift(0, 1)
    print(
        f"using {name} ({comm_ptr}) : #procs {num_procs} topology {topo}, "
        f"rank {my_rank}, "
        f"left: {left_neighbor}, "
        f"right:{right_neighbor}"
    )
    return comm


def do_halo_exchange(comm: Cartcomm, field: np.ndarray, length, verbose: bool):
    left_neighbor, right_neighbor = comm.Shift(0, 1)
    comm.Sendrecv(
        field[1, 0:length], left_neighbor, 0, field[0, 0:length], right_neighbor, 0
    )
    if verbose:
        print(
            f"driver.py: rank {comm.Get_rank()} halo exchange: "
            f"after exchange params sending left ={field[1, 0:length]} "
            f"received from right={field[0, 0:length]}"
        )


def unpack(ptr, size_x, size_y) -> np.ndarray:
    """
    Unpack buffer.

    Unpacks a 2d c/fortran field into a numpy array


    Args:
        ptr: fortran buffer (2d array)
        size_x: num of rows (i.e. left most index, continuous in fortran)
        size_y: num of cols (i.e. right index, with stride size_x

    Returns:
        a numpy array with shape=(size_y, size_x) and dtype = ctype of the pointer

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
