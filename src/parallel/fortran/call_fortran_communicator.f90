! test program: calls the mpi communicator setup in communicator.f90
program call_fortran_communicator
    use, intrinsic :: iso_c_binding
    use communicator
    implicit none

    integer ierr
    integer(c_int) vdim, GLOBAL_V_NUM, GLOBAL_VX_SIZE, data_size
    real(c_double) :: outgoing(24), incoming(24)

    incoming = 0
    data_size = 24
    GLOBAL_V_NUM = 96
    call random_number(outgoing)


    call setup_comm()

    call exchangeLeft(outgoing, incoming, ierr)

    call cleanup_comm()

end program call_fortran_communicator


