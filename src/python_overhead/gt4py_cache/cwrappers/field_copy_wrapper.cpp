#include <cpp_bindgen/export.hpp>
#include <gridtools/stencil/global_parameter.hpp>
#include <gridtools/storage/adapter/fortran_array_view.hpp>
#include "field_copy.cpp.inc"

namespace {
    void field_copy_impl(
        gridtools::fortran_array_view<double, 1, gridtools::integral_constants<int,1>> inp,
        gridtools::fortran_array_view<double, 1, gridtools::integral_constants<int,1>>outp) {
        auto a = inp
        long size_a = inp.bindgen_view_rank
        auto b = outp
        long size_b = outp.bindgen_view_rank
        field_copy<(a, b, size_a, size_b)
    }

    BINDGEN_EXPORT_BINDING_WRAPPED_2(field_copy_c, field_copy_impl);
    }


