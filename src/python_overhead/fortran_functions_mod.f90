module fortran_functions
    contains

    subroutine do_nothing(inp, outp)
        implicit none
        real(8), intent(in):: inp(:)
        real(8), intent(out)::outp(:)

    end subroutine do_nothing

    subroutine copy(inp, outp)
        implicit none
        real(8), intent(in):: inp(:)
        real(8), intent(out)::outp(:)
           outp = inp
    end subroutine copy
end module fortran_functions