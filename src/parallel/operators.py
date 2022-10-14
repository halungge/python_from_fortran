
from functional.ffront.decorator import field_operator, program
from functional.ffront.fbuiltins import Field

from parallel.dimensions import VDim, IDim, JDim, Ioff, Joff


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


@field_operator
def _cart_laplace(v:Field[[IDim, JDim], float]) ->Field[[IDim, JDim], float]:
    return v(Ioff[+1])+ v(Ioff[-1]) + v(Joff[+1]) + v(Joff[-1]) - 4.0 * v

@program
def cart_laplace(v:Field[[IDim, JDim], float], res:Field[[IDim, JDim], float]):
    #do not use halo...
    _cart_laplace(v, out=res[1:-1, 1:-1])

# @field_operator
# def _laplace(v:Field[[VDim], float], num_neighbor:int)->Field[[VDim], float]:
#     return neighbor_sum(v, axis=V2E2VDim) - num_neighbor*v
#
# @program
# def laplace(v:Field[[VDim], float], num, outfield:Field[[VDim], float], lower:int, upper:int):
#     _laplace(v, num, out=outfield[lower:upper])
#
