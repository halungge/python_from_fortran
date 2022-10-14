module driver
    use, intrinsic :: iso_c_binding
    implicit none

    public
    interface
        subroutine run_step(input, output, xLength, localSize) bind(c, name='run_step')
            use iso_c_binding
            integer(c_int), value, intent(in)::xLength, localSize
            real(c_double), intent(in):: input(localSize)
            real(c_double), intent(out) :: output(localSize)
        end subroutine run_step

        subroutine run_cart_step(input, output, ni, nj) bind(c, name='run_cart_step')
            use iso_c_binding
            integer(c_int), value, intent(in)::ni, nj
            real(c_double), intent(in):: input(:,:)
            real(c_double), intent(out) :: output(:,:)
        end subroutine run_cart_step
    end interface

end module driver