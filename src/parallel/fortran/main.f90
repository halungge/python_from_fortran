program run_parallel
    use, intrinsic :: iso_c_binding
    use communicator
    use driver
    implicit none

    integer nSteps, t, i, me, ierr
    integer(c_int) idim, jdim
    real(c_double), allocatable :: field(:,:)
    real(c_double), allocatable:: result_field(:,:)
    call setup_comm()



    idim = 4
    jdim = 8
    allocate(field(idim, jdim), result_field(idim, jdim))


    !call random_number(field)
    call get_my_rank(me)
    field = reshape((/(i, i=me, me + idim * jdim)/), (/idim, jdim/))
    call exchangeleft(field(1:idim, 2), field(1:idim, 1), ierr)
    print *, "rank ", me, "left send buffer", field(1:idim, 2)
    print *, "rank ", me, "left recv buffer", field(1:idim, 1)
    call exchangeright(field(1:idim, jdim-1), field(1:idim, jdim), ierr)
    print *, "rank ", me, "right send buffer", field(1:idim, jdim-1)
    print *, "rank ", me, "right recv buffer", field(1:idim, jdim)
    print *
    print *


    call run_cart_step(field, result_field, idim, jdim)

    print *,"DONE"
    call cleanup()

end program run_parallel


