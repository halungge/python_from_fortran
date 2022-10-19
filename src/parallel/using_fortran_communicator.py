import os

import numpy as np
from mpi4py import MPI
from fortran.fortran_communicator import communicator



def main():
    """
    calling the fortran defined mpi communicator
    python module can be built with

    > cd fortran
    > python -m numpy.f2py communicator.f90 -m fortran_communicator -h communicator.pyf --overwrite-signature
    > python -m numpy.f2py --f90exec=mpif90 --f77exec=mpif77 -c communicator.pyf communicator.f90

    """
    len = 4
    communicator.setup_comm()
    send_buf = np.random.rand(len)
    my_rank = communicator.get_my_rank()
    print(f"python PID on rank {my_rank} {os.getpid()}")

    recv_buf_r = np.zeros(send_buf.shape)
    recv_buf_l = np.zeros(send_buf.shape)
    communicator.exchangeleft(send_buf, recv_buf_l)
    communicator.exchangeright(send_buf, recv_buf_r)
    print(f"me {my_rank}: sending {send_buf} received from left {recv_buf_l}" )
    MPI.Finalize()



if __name__ == "__main__":
    main()