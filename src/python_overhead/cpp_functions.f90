! Created by  on 02.11.22.

module cpp_functions
    use, intrinsic:: iso_c_binding
    implicit none
    interface
        subroutine field_copy_cpp(inp, outp, size_in, size_out) bind(c, name="field_copy")
             use iso_c_binding
             integer(c_long), value, intent(in)::size_in
             real(c_double), intent(in)::inp(size_in)
             integer(c_long), value, intent(in)::size_out
             real(c_double), intent(out)::outp(size_out)
        end subroutine field_copy_cpp
    end interface

end module cpp_functions