module field_functions
    use, intrinsic :: iso_c_binding
    implicit none

    public
    interface
        subroutine square(in, nx, ny, out) bind(c, name='square')
            use iso_c_binding
            integer(c_int), value, intent(in)::nx, ny
            real(c_double), intent(in):: in(nx, ny)
            real(c_double), intent(out) :: out(nx, ny)
        end subroutine square

        subroutine square1(in, nx, ny, out) bind(c, name='square1')
            use iso_c_binding
            integer(c_int), value, intent(in)::nx, ny
            real(c_double), intent(in):: in(nx, ny)
            real(c_double), intent(out) :: out(nx, ny)
        end subroutine square1
    end interface

end module field_functions