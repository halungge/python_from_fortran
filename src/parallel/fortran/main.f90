program run_parallel
    use, intrinsic :: iso_c_binding
    use communicator
    use driver
    implicit none

    integer nSteps, t
    integer(c_int) idim, jdim
    real(8), allocatable :: field(:,:)
    real(8), allocatable:: result_field(:,:)

    idim = 96
    jdim = 96
    allocate(field(idim, jdim), result_field(idim, jdim))

    call random_number(field)
    result_field = 0

    call setup_comm()

    call run_cart_step(field, result_field, idim, jdim)

    print *,"DONE"
    call cleanup()

end program run_parallel


