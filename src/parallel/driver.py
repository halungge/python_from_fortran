from functional.iterator.embedded import np_as_located_field

from parallel.dimensions import VDim
from parallel.operators import local_invert


def run_step(comm, input, recv_buf, send_buf):
    comm.exchangeLeft(send_buf, recv_buf)
    input_field = np_as_located_field(VDim)(input)
    result_field = np_as_located_field(VDim)(send_buf)
    local_invert(input_field, result_field, offset_provider={})
