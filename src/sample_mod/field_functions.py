# flake8: noqa D100, D103

import numpy as np
from functional.ffront.decorator import field_operator, program
from functional.ffront.fbuiltins import Dimension, Field, float64
from functional.iterator.embedded import np_as_located_field

CellDim = Dimension("Cell")
KDim = Dimension("K")


@field_operator
def _multiply_fields(
    a: Field[[CellDim, KDim], float64], b: Field[[CellDim, KDim], float64]
) -> Field[[CellDim, KDim], float64]:
    return a * b


@program
def multiply_fields(
    a: Field[[CellDim, KDim], float64],
    b: Field[[CellDim, KDim], float64],
    result: Field[[CellDim, KDim], float64],
):
    _multiply_fields(a, b, out=result)


def square_ar(a: np.ndarray) -> np.array:
    a_field = np_as_located_field(CellDim, KDim)(a)
    result = np_as_located_field(CellDim, KDim)(np.zeros(a.shape, dtype=float64))
    multiply_fields(a_field, a_field, result, offset_provider={})
    return np.asarray(result)


def square(state):
    """pass the result array inside **state"""
    a = state["input"]
    res = state["output"]
    assert res.shape == a.shape
    print("printing from python input = ", a[:])
    a_field = np_as_located_field(CellDim, KDim)(a)
    result = np_as_located_field(CellDim, KDim)(res)
    multiply_fields(a_field, a_field, result, offset_provider={})
    res = np.asarray(result)
    print("printing from python output = ", res[:])
