#include <cpp_bindgen/export.hpp>
#include <gridtools/stencil/global_parameter.hpp>
#include <gridtools/storage/adapter/fortran_array_view.hpp>
#include "field_copy.cpp.inc"

namespace {
    void field_copy_impl(
        gridtools::fortran_array_view<double, 1> inp,
        gridtools::fortran_array_view<double, 1>outp) {
        long size_inp = inp.bindgen_view_rank
        long size_outp = outp.bindgen_view_rank
        field_copy(inp, outp, size_inp, size_outp)
    }

    BINDGEN_EXPORT_BINDING_WRAPPED_2(field_copy_c, field_copy_impl);
    }


