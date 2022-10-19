program run_parallel
    use, intrinsic :: iso_c_binding
    use MPI
    use communicator
    use driver
    implicit none

    integer nSteps, t, i, me, ierr
    integer(c_int) idim, jdim
    real(c_double), allocatable :: field(:,:)
    real(c_double), allocatable:: result_field(:,:)

    call mpi_init(ierr)

    idim = 4
    jdim = 8

    allocate(field(idim, jdim), result_field(idim, jdim))
    field = 0.0

    call random_number(field(:,2:jdim-1))
    call setup_comm()
    call get_my_rank(me)
!    print *
!
!    print *, "rank ", me, "LEFT send buffer", field(1:idim, 2)
!    print *, "rank ", me, "LEFT recv buffer", field(1:idim, 1)
!    print *, "rank ", me, "RIGHT send buffer", field(1:idim, jdim-1)
!    print *, "rank ", me, "RIGHT recv buffer", field(1:idim, jdim)
!    print *

    call run_cart_step(field, result_field, idim, jdim)
    call cleanup()

end program run_parallel


