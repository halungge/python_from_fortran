from mpi4py import MPI
from mpi4py.MPI import Comm


class RingComm:
    def __init__(self, communicator: Comm):
        self.ring_comm = MPI.Cartcomm(communicator)
        self.ring_comm.Set_name("python_ringcom")
        self.num_procs = self.ring_comm.Get_size()
        self.my_rank = self.ring_comm.Get_rank()
        self.left_neighbor_rank, self.right_neighbor_rank = self.ring_comm.Shift(0, 1)

    def get_left_rank(self):
        return self.left_neighbor_rank


    def get_fortran_comm_id(self):
        return self.ring_comm.f2py()

    def get_right_rank(self):
        return self.right_neighbor_rank

    def get_rank(self):
        return self.my_rank

    def get_size(self):
        return self.num_procs

    def exchangeLeft(self, send_buf, recv_buf):
        status = MPI.Status()
        self.ring_comm.Sendrecv(send_buf, dest=self.left_neighbor_rank, sendtag=12, recvbuf=recv_buf,
                                source=self.right_neighbor_rank, recvtag=12, status=status)

    def exchangeRight(self, send_buf, recv_buf):
        status = MPI.Status()
        self.ring_comm.Sendrecv(send_buf, dest=self.right_neighbor_rank, sendtag=12, recvbuf=recv_buf,
                                source=self.left_neighbor_rank, recvtag=12, status=status)
