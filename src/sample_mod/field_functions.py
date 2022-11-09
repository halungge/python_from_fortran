# flake8: noqa D100, D103

import numpy as np
from functional.program_processors.runners import gtfn_cpu
from functional.ffront.decorator import field_operator, program
from functional.ffront.fbuiltins import Dimension, Field, float64
from functional.iterator.embedded import np_as_located_field

from parallel.dimensions import IDim

CellDim = Dimension("Cell")
KDim = Dimension("K")
VDim = Dimension("Vertex")
EDim = Dimension("Edge")


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


@program(backend=gtfn_cpu.run_gtfn)
def square_fields(
    a: Field[[CellDim, KDim], float64], result: Field[[CellDim, KDim], float64]
):
    _multiply_fields(a, a, out=result)


def square_return(input_ar: np.ndarray) -> np.array:
    a_field = np_as_located_field(CellDim, KDim)(input_ar)
    result = np_as_located_field(CellDim, KDim)(np.zeros(input_ar.shape, dtype=float64))
    multiply_fields(a_field, a_field, result, offset_provider={})
    return np.asarray(result)


def square_output_param(input_ar: np.ndarray, output_ar: np.ndarray):
    input_field = np_as_located_field(CellDim, KDim)(input_ar)
    output_field = np_as_located_field(CellDim, KDim)(output_ar)
    multiply_fields(input_field, input_field, output_field, offset_provider={})


def square(state):
    """pass input and output arrays inside **state"""
    a = state["input"]
    res = state["output"]
    assert res.shape == a.shape
    # print("printing from python input = ", a[:])
    square_output_param(a, res)
    # print("printing from python output = ", res[:])


def square1(state):
    a = state["input"]
    res = square_return(a)
    state["output"] = res

@field_operator
def _field_copy(a: Field[[IDim], float64])->Field[[IDim], float64]:
    return a

@program(backend=gtfn_cpu.run_gtfn_persistent)
def field_copy(a: Field[[IDim], float64], b:Field[[IDim], float64]):
    _field_copy(a, out=b)

