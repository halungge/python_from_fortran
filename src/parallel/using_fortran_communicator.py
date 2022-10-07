import numpy as np
from fortran.fortran_communicator import communicator



def main():
    """
    calling the fortran defined mpi communicator
    python module can be built with

    > cd fortran
    > python -m numpy.f2py communicator.f90 -m fortran_communicator -h communicator.pyf --overwrite-signature
    > python -m numpy.f2py --f90exec=mpif90 --f77exec=mpif77 -c communicator.pyf communicator.f90

    """
    communicator.setup_comm()
    send_buf = np.random.rand(96)
    recv_buf = np.zeros(send_buf.shape)
    communicator.exchangeleft(send_buf, recv_buf)
    my_rank = communicator.get_my_rank()
    print(f"me {my_rank} recevied {recv_buf}")
    communicator.cleanup()




if __name__ == "__main__":
    main()