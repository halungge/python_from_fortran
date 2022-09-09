program example
use callpy_mod
implicit none

real(8), DIMENSION(6, 3) :: a, res, a1, res1
a = reshape((/ 1.0,  1.0, 2.0, 3.0, 5.0, 8.0, 1.0,  1.0, 2.0, 3.0, 5.0, 8.0, 1.0,  1.0, 2.0, 3.0, 5.0, 8.0 /), shape(a))

call set_state("input", a)
call set_state("output", res)
call call_function("sample_mod.field_functions", "square")
call get_state("output", res)
print *, "res (using square_output_param): ", res

!! the result could also be a return from a python function
! it must be set to the global state by python and the fortran caller must know its name and type, dimension
!! NOTE !!: we are overriding the values in the python global state !!
!! in any case the value used by by python to address the global state dictionary must be known to the fortran caller
a1 = a - 1.0
call set_state("input", a1)
! version using the "square_return" function instead of "square_output_param"
call call_function("sample_mod.field_functions", "square1")
call get_state("output", res1)
print *,"res1 (usint square_return): ",  res1

end program example
