! run_field_sample.f90
program call_python
    use, intrinsic :: iso_c_binding
    implicit none
    integer(c_int) cdim, kdim
    real(8), DIMENSION(6, 3) :: a, res


    interface
        subroutine square(in, nx, ny, out) bind(c, name='square')
            use iso_c_binding
            integer(c_int), value, intent(in)::nx, ny
            real(c_double), intent(in):: in(nx, ny)
            real(c_double), intent(out) :: out(nx, ny)
        end subroutine square
    end interface

    a = reshape((/ 1.0,  1.0, 2.0, 3.0, 5.0, 8.0, 1.0,  1.0, 2.0, 3.0, 5.0, 8.0, 1.0,  1.0, 2.0, 3.0, 5.0, 8.0 /), shape(a))
    print *, "fortran input: field = ", a
    res = 0
    cdim = 6
    kdim = 3
    call square(a, cdim, kdim, res)
    print *, "fortran output: res =", res

    end program call_python