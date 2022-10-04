from mpi4py import MPI  # implicitly calls MPI.Init
import numpy as np

from parallel.communicator import RingComm
from parallel.driver import run_step
from parallel.mesh import LocalMesh


def initialize_random_field(mesh):
    pass


def main():
    """
    steps:
    1. determine local mesh size -> to be moved to fortran
    2. setup local mesh -> to bemoved to fortran
    3. setup communicator.py -> to be moved to fortran
    4. initialize (local) field -> to be moved to fortran
    4.a) exhhange halo
    5. loop:
        (operator step
        halo exchange)
    6. derminate: reduction
    """
    GLOBAL_V_NUM = 96
    GLOBAL_VX_SIZE = 8

    # step 3. setup communicator
    comm = RingComm(MPI.COMM_WORLD)

    # step 1:

    #mesh = TorusMesh(GLOBAL_V_NUM/comm.size(), GLOBAL_VX_SIZE)

    mesh = LocalMesh(GLOBAL_V_NUM/comm.get_size())

    input =(3 + comm.get_rank()) * np.ones(int(mesh.get_local_size()))

    send_buf = np.zeros(input.shape)
    recv_buf = np.zeros(input.shape)

    run_step(comm, input, recv_buf, send_buf)

    print(f" me= {comm.get_rank()}: input field= {np.average(input)} result= {np.average(send_buf)} received from neighbor = { np.average(recv_buf)}")


if __name__ == "__main__":
    main()