module python_functions
    use, intrinsic :: iso_c_binding
    implicit none

    public
    interface
        subroutine do_nothing_py(inp, outp) bind(c, name='do_nothing')
            use iso_c_binding
            real(c_double), intent(in):: inp(:)
            real(c_double), intent(out) :: outp(:)
        end subroutine do_nothing_py

        subroutine copy_array_py(inp, outp, size) bind(c, name='copy_array')
            use iso_c_binding
            integer(c_int), value, intent(in)::size
            real(c_double), intent(in):: inp(size)
            real(c_double), intent(out) :: outp(size)
        end subroutine copy_array_py

        subroutine copy_gt4py(inp, outp, size) bind(c, name='copy_gt4py')
            use iso_c_binding
            integer(c_int), value, intent(in)::size
            real(c_double), intent(in)::inp(size)
            real(c_double), intent(out)::outp(size)
        end subroutine copy_gt4py
    end interface

end module python_functions