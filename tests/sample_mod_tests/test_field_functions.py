# noqa: D100
import numpy as np
from functional.ffront.fbuiltins import Dimension, float64
from functional.iterator.embedded import np_as_located_field

import sample_mod.field_functions
from sample_mod.field_functions import CellDim, KDim


def test_square():
    first_layer = np.array([1.0, 1.0, 2.0, 3.0, 5.0, 8.0])
    a = np.repeat(first_layer[:, np.newaxis], 3, axis=1)
    expected_result_layer = np.array([1.0, 1.0, 4.0, 9.0, 25.0, 64.0])
    output = np.zeros(a.shape, dtype=float64)

    state = {"input": a, "output": output}
    sample_mod.field_functions.square(state)
    res = state["output"]
    assert a.shape == res.shape
    assert np.allclose(res[:, 0], expected_result_layer)
    assert np.allclose(res[:, 1], expected_result_layer)
    assert np.allclose(res[:, 2], expected_result_layer)


def test_square_fields():
    input_array = np.asarray([[1.0, 1.0, 2.0, 3.0, 5.0, 8.0], [4.0, 3.4, 9.9, 4.0, 1.5, 1.2]])
    input_field = np_as_located_field(CellDim, KDim)(input_array)
    expected = np_as_located_field(CellDim, KDim)(input_array**2)
    output = np_as_located_field(CellDim, KDim)(np.zeros(input_array.shape, float64))
    sample_mod.field_functions.square_fields(input_field, output, offset_provider={})
    assert np.allclose(expected, output)
