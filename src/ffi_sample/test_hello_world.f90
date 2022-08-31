! test_hello_world.f90
program call_python
  use, intrinsic :: iso_c_binding
  implicit none
  integer(c_int) :: limit
  integer(c_int) :: sumup

  interface
     subroutine hello_world() bind (c)
     end subroutine hello_world

     function sumup(limit) result(res) bind(c, name="sumup")
         use, intrinsic :: iso_c_binding, only: c_int
        integer(c_int), intent(in) :: limit
     end function

  end interface


  call hello_world()
  limit = 5
  print *, "result from fortran summing up to ",limit, " is",  sumup(limit)

end program call_python