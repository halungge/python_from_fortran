! simple_forpy_example.f90
program call_python
  use forpy_mod
  implicit none

  integer::ierror
  type(tuple):: args
  type(module_py) :: mymodule
  type(object) :: return_value
  type(list) :: paths
  integer:: returned


  ierror = forpy_initialize()


! manipulating sys.path to add local python functions     =:-0
  ierror = get_sys_path(paths)
  ierror = paths%append("../sample_mod")
  ierror = import_py(mymodule, "my_functions")

  print *, ">> calling simple python hello world from fortran:"
  ierror = call_py(return_value, mymodule, "hello_world")

  print *, ">> calling generic python function with variable args, without args, ignoring return:"
  ierror = call_py_noret(mymodule, "print_args")

  print *,">> calling python function with signature func(int)->int:"
  ierror = tuple_create(args, 1)
  ierror = args%setitem(0, 5)
  ierror = call_py(return_value, mymodule, "sumup", args)
  ierror = cast(returned, return_value)
  print *, "returned from python sumup() to calling fortran", returned


  call args%destroy
  call mymodule%destroy
  call return_value%destroy
  call paths%destroy

  call forpy_finalize

end program call_python