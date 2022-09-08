program example
use callpy_mod
implicit none

real(8), DIMENSION(6, 3) :: a, res

a = reshape((/ 1.0,  1.0, 2.0, 3.0, 5.0, 8.0, 1.0,  1.0, 2.0, 3.0, 5.0, 8.0, 1.0,  1.0, 2.0, 3.0, 5.0, 8.0 /), shape(a))

call set_state("input", a)
! res could also be created inside python and handed back via the the global state
call set_state("output", res)
call call_function("sample_mod.field_functions", "square")
call get_state("output", res)
print *, res


end program example
