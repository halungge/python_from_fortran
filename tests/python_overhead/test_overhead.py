
import numpy as np
from functional.iterator.embedded import np_as_located_field

from python_overhead.module_loader import load_precompiled_module
from sample_mod.field_functions import IDim, field_copy


def test_load_existing_module():

    size = 10
    a = np.random.random(size)
    b = np.zeros(size)
    a_field = np_as_located_field(IDim)(a)
    b_field = np_as_located_field(IDim)(b)

    field_copy(a_field, b_field, offset_provider={})
    assert np.allclose(a, b)

    c = np.zeros(size)
    operator_name = 'field_copy'

    copy_precompiled = load_precompiled_module(operator_name)
    copy_precompiled(a, c, size, size)

    assert np.allclose(b, c)