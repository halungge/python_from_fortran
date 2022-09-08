import pytest
import numpy as np
from functional.ffront.fbuiltins import float64
import sample_mod.field_functions


def test_square():
    first_layer  = np.array([1.0,1.0,2.0,3.0,5.0,8.0])
    a = np.repeat(first_layer[:, np.newaxis], 3, axis=1)
    expected_result_layer = np.array([1.0, 1.0, 4.0, 9.0, 25.0, 64.0])
    output = np.zeros(a.shape, dtype=float64)

    state = {"input": a, "output": output}
    sample_mod.field_functions.square(state)
    res = state["output"]
    assert a.shape == res.shape
    np.testing.assert_allclose(res[:, 0], expected_result_layer)
    np.testing.assert_allclose(res[:, 1], expected_result_layer)
    np.testing.assert_allclose(res[:, 2], expected_result_layer)
