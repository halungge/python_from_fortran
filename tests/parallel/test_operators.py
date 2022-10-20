import numpy as np
from functional.iterator.embedded import np_as_located_field

from parallel.dimensions import IDim, JDim, VDim
from parallel.operators import cart_laplace, local_invert


def test_invert():
    v = np.array([2.0, 2.0, 3.0, 3.0, 5.0, 8.0])
    v_field = np_as_located_field(VDim)(v)
    res_field = np_as_located_field(VDim)(np.zeros(v.shape))

    local_invert(v_field, res_field, offset_provider={})
    assert np.allclose(res_field, [0.5, 0.5, 0.3333333333, 0.333333333333, 0.2, 0.125])


def test_cart_laplace():
    v = np.random.rand(32, 32)

    def laplace_numpy(v: np.ndarray):
        return (
            v[:-2, 1:-1]
            + v[2:, 1:-1]
            + v[1:-1, :-2]
            + v[1:-1, 2:]
            - 4.0 * v[1:-1, 1:-1]
        )

    ref = laplace_numpy(v)

    v_field = np_as_located_field(IDim, JDim)(v)
    res = np_as_located_field(IDim, JDim)(np.zeros(v.shape))
    cart_laplace(v_field, res, offset_provider={"Ioff": IDim, "Joff": JDim})

    assert np.allclose(ref, res[1:-1, 1:-1])
