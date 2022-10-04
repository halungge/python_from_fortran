import numpy as np
from functional.iterator.embedded import np_as_located_field

from parallel.dimensions import VDim
from parallel.operators import local_invert


def test_invert():
    v = np.array([2.0, 2.0, 3.0, 3.0, 5.0, 8.0])
    v_field = np_as_located_field(VDim)(v)
    res_field = np_as_located_field(VDim)(np.zeros(v.shape))

    local_invert(v_field, res_field, offset_provider = {})
    assert np.allclose(res_field, [0.5, 0.5, 0.3333333333, 0.333333333333, 0.2, 0.125])