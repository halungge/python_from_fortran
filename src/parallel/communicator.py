from mpi4py import MPI
from mpi4py.MPI import Comm


class RingComm:
    def __init__(self, communicator: Comm, local_grid_size=24):
        self.ring_comm = MPI.Comm(communicator)
        self.num_procs = self.ring_comm.Get_size()
        self.my_rank = self.ring_comm.Get_rank()
        self.left_neighbor_rank = (self.my_rank + 1) % self.num_procs
        self.right_neighbor_rank = (self.my_rank - 1) % self.num_procs

    def get_left_rank(self):
        return self.left_neighbor_rank

    def get_right_rank(self):
        return self.right_neighbor_rank

    def get_rank(self):
        return self.my_rank

    def get_size(self):
        return self.num_procs

    def exchangeLeft(self, send_buf, recv_buf):
        self.ring_comm.Send(send_buf, dest=self.left_neighbor_rank, tag=12)
        self.ring_comm.Recv(recv_buf, source=self.right_neighbor_rank, tag=12)
