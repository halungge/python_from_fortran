! run_field_sample.f90
program run_parallel
    use, intrinsic :: iso_c_binding
    use communicator
    implicit none

    integer ierr
    integer(c_int) vdim, GLOBAL_V_NUM, GLOBAL_VX_SIZE, data_size
    real :: outgoing(24), incoming(24)

    incoming = 0
    data_size = 24
    GLOBAL_V_NUM = 96
    call random_number(outgoing)


    call setup_comm()

    call exchangeLeft(outgoing, incoming, ierr)

    call cleanup()

end program run_parallel


