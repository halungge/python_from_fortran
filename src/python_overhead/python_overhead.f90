! run_field_sample.f90
program python_overhead
    use, intrinsic :: iso_c_binding
    use python_functions
    use fortran_functions
    implicit none

    integer(c_int) runs, n
    real :: ct_start, ct_end, duration_cp_py, duration_cp_f, duration_nt_py, duration_nt_f, duration_cp_gt4py
    real(8), DIMENSION(1000000) :: a, res

    call random_number(a)
    runs = 100


    res = 0.
    ! do one call to consume general python startup
    call do_nothing_py(a, res)

    res = 0.
    call cpu_time(ct_start)
    do n =0, runs
        call do_nothing_py(a, res)
    end do
    call cpu_time(ct_end)
    duration_nt_py = (ct_end - ct_start)/real(runs)

    res = 0.
    call cpu_time(ct_start)
    do n = 0, runs
        call do_nothing(a, res)
    end do
    call cpu_time(ct_end)
    duration_nt_f = (ct_end - ct_start)/real(runs)

    res = 0.
    call cpu_time(ct_start)
    do n= 0, runs
        call copy_array_py(a, res, size(a))
    end do
    call cpu_time(ct_end)
    duration_cp_py = (ct_end - ct_start)/real(runs)

    res = 0.
    call cpu_time(ct_start)
    do n = 0, runs
        call copy_gt4py(a, res, size(a))
    end do
    call cpu_time(ct_end)
    duration_cp_gt4py = (ct_end - ct_start)/real(runs)

    res = 0.
    call cpu_time(ct_start)
    do n = 0, runs
        call copy(a, res)
    end do
    call cpu_time(ct_end)
    duration_cp_f = (ct_end - ct_start)/real(runs)
    print *, duration_nt_py, ",", duration_nt_f, ",",duration_cp_py, ",", duration_cp_f, ",", duration_cp_gt4py, ",", runs


end program python_overhead
