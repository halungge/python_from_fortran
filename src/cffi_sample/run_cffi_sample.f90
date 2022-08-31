! run_cffi_sample.f90
program call_python
    use, intrinsic :: iso_c_binding
    implicit none
    integer(c_int) res

    interface
        subroutine hello_world() bind (c)
        end subroutine hello_world

        function sumup(limit) result(y) bind(c, name='sumup')
            use iso_c_binding
            integer(c_int), value, intent(in):: limit
            integer(c_int):: y
        end function sumup
    end interface

    call hello_world()
    res = sumup(5)
    print *, "fortran calling python, res=", res

    end program call_python