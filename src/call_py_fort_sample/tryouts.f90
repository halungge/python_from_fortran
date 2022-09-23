! play around
program example
use callpy_mod
implicit none

real(8), DIMENSION(6, 3) :: a, res
real(8), DIMENSION(3, 3):: rnd, mean_rnd

a = reshape((/ 1.0,  1.0, 2.0, 3.0, 5.0, 8.0, 1.0,  1.0, 2.0, 3.0, 5.0, 8.0, 1.0,  1.0, 2.0, 3.0, 5.0, 8.0 /), shape(a))

call call_function("adapters.helpers", "printstate")
call set_state("input", a)
! res could also be created inside python and handed back via the the global state
call set_state("output", res)
call call_function("sample_mod.field_functions", "square")
call get_state("output", res)
print *, res
call call_function("adapters.helpers", "printstate")
call random_number(rnd)
call set_state("rnd", rnd)
call call_function("adapters.helpers", "printstate")
mean_rnd = 6
call set_state("mean", mean_rnd)
call call_function("adapters.helpers", "printstate")
call call_function("adapters.helpers", "to_none")
call call_function("adapters.helpers", "printstate")
call call_function("adapters.helpers", "remove")
call call_function("adapters.helpers", "printstate")
call call_function("adapters.helpers", "addfoo")
call get_state("foo", rnd)

print * , rnd






end program example
