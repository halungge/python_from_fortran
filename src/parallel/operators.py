from functional.ffront.decorator import field_operator, program
from functional.ffront.fbuiltins import Field

from parallel.dimensions import IDim, Ioff, JDim, Joff, VDim


@field_operator()
def _local_invert(v: Field[[VDim], float]) -> Field[[VDim], float]:
    return 1.0 / v


@program
def local_invert(v: Field[[VDim], float], res: Field[[VDim], float]):
    _local_invert(v, out=res)


@field_operator
def _cart_laplace(v: Field[[IDim, JDim], float]) -> Field[[IDim, JDim], float]:
    return v(Ioff[+1]) + v(Ioff[-1]) + v(Joff[+1]) + v(Joff[-1]) - 4.0 * v


@program
def cart_laplace(v: Field[[IDim, JDim], float], res: Field[[IDim, JDim], float]):
    # do not use halo...
    _cart_laplace(v, out=res[1:-1, 1:-1])
