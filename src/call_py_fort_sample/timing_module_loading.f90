program time_call_fort_py
    use, intrinsic :: iso_c_binding
    use callpy_mod
    implicit none

    integer :: max_runs, n
    real :: ct_start, ct_end
    real(8), DIMENSION(20, 20) :: a, res

    max_runs = 1
    print *, "timing cffi: doing ", max_runs , "loops on ", 20, "x", 20, "array"
    call cpu_time(ct_start)
    do n = 0, max_runs
        call random_number(a)
        res = 0
        call set_state("output", res)
        call set_state("input", a)
        call call_function("sample_mod.field_functions", "square")
        call get_state("output", res)
        call call_function("adapters.helpers", "get_max")
        call call_function("adapters.helpers", "to_zero_values")
        call call_function("builtins", "print")
        call get_state("output", res)
    end do
    call cpu_time(ct_end)
    print *, "total cpu time for loop:", ct_end - ct_start
    print *, "done"

    end program time_call_fort_py