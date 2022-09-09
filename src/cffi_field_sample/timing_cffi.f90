program time_cffi
    use, intrinsic :: iso_c_binding
    use field_functions
    implicit none

    integer(c_int) cdim, kdim
    integer :: max_runs, n
    real :: ct_start, ct_end
    real(8), DIMENSION(20, 20) :: a, res

    max_runs = 3000
    cdim = 20
    kdim = 20
    print *, "timing cffi: doing ", max_runs , "loops on ", cdim, "x", kdim, "array"
    call cpu_time(ct_start)
    do n = 0, max_runs
        call random_number(a)
        res = 0
        call square(a, cdim, kdim, res)
    end do
    call cpu_time(ct_end)
    print *, "total cpu time for loop:", ct_end - ct_start
    print *, "done"

    end program time_cffi