"""Simple mpi4py hello world program."""
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
comm_size = comm.Get_size()


left = (my_rank + 1) % comm_size
right = (my_rank - 1) % comm_size
data_me = np.array([my_rank], dtype=int)
data_right = np.empty(data_me.shape, dtype=int)
data_left = np.empty(data_me.shape, dtype=int)

# capital Send/Recv is used for buffers
comm.Send(data_me, dest=left, tag=0)
comm.Send(data_me, dest=right, tag=1)
comm.Recv(data_right, source=right, tag=0)
comm.Recv(data_left, source=left, tag=1)

print(f"right neighbor on rank {my_rank}: {data_right}")

if my_rank == 0:
    print("non blocking ---")


send_buf = np.random.rand(2, 2)
print(f" rank {my_rank}: my random values: {send_buf}")
recv_buf = np.zeros(send_buf.shape, dtype=float)


comm.Isend(send_buf, dest=left, tag=11)
req = comm.Irecv(recv_buf, tag=11)
req.wait()


print(
    f"rank {my_rank} got random data from right neighbor {recv_buf} (must not be zeros)"
)
