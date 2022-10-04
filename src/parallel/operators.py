
import numpy as np
from functional.ffront.decorator import field_operator, program
from functional.ffront.fbuiltins import Dimension, Field, FieldOffset, DimensionKind, neighbor_sum
from functional.iterator.embedded import np_as_located_field

from parallel.dimensions import VDim, V2E2VDim, EDim, V2E2V


# @field_operator
# def _weighted_shifted_sum(vertices:Field[[VDim], float], edge_weights:Field[[EDim],float])->Field[[VDim], float]:
#     return neighbor_sum(vertices(V2E2V) * edge_weights, axis=V2E2VDim)
#
#
#
#
# @field_operator
# def _weighted_sum(v1:Field[[VDim], float], v2:Field[[VDim], float], weights:Field[[VDim],float])->Field[[VDim], float]:
#     return weights * (v1 + v2)
#
#
# @program
# def weighted_sum(v_1:Field[[VDim], float], v_2:Field[[VDim], float], weights:Field[[VDim], float], v_out:[[VDim], float]):
#     return _weighted_sum(v_1, v_2, weights, out=v_out)


@field_operator()
def _local_invert(v:Field[[VDim], float])->Field[[VDim], float]:
    return 1.0/v

@program
def local_invert(v:Field[[VDim], float], res:Field[[VDim], float]):
    _local_invert(v, out=res)
