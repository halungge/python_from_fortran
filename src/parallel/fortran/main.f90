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



    idim = 32
    jdim = 64
    allocate(field(idim, jdim), result_field(idim, jdim))


    !call random_number(field)
    call get_my_rank(me)
    field = reshape((/(i, i=me, me + idim * jdim)/), (/idim, jdim/))
    print *
    if (my_rank == 0) then
        print *, "---grid halo information information---"
    end if

    print *, "rank ", me, "LEFT send buffer", field(1:idim, 2)
    print *, "rank ", me, "LEFT recv buffer", field(1:idim, 1)
    print *, "rank ", me, "RIGHT send buffer", field(1:idim, jdim-1)
    print *, "rank ", me, "RIGHT recv buffer", field(1:idim, jdim)
    print *
    print *

    call run_cart_step(field, result_field, idim, jdim)
    print *,"rank ", my_rank, " DONE"
    call cleanup()

end program run_parallel


