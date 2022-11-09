//example from GridTools repo
//TODO [ml] DELETE once its working
#include <iostream>

// In this example, we demonstrate how the cpp_bindgen library can be used to export functions to C and Fortran.

namespace {
    void print_number(int i) { std::cout << "Printing from C++: " << i << std::endl; }

    // Exports a unary function with the name `print_number_from_cpp`, which forwards to `print_number`.
    BINDGEN_EXPORT_BINDING_WRAPPED(print_number_from_cpp, print_number);
} // namespace