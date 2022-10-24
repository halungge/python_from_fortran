! try using MPI communicators when interfaceing between Python and Fortran
!
!
! 1. sets up a communicator: from module communicator.f90
! 2. initializes some data arrays
! 3. call a python driver (C module embedding python via cffi):
!    each MPI process spins up a python interpreter and passes to communicator to be used together with data fields
!    within Python we do some calculation on the fields and halo exchange (see ../driver.py)
program run_parallel
    use, intrinsic :: iso_c_binding
    use MPI
    use communicator
    use driver
    implicit none

    integer nSteps, t, i, me, ierr, comm_id
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
    call get_comm_id(comm_id)

    call run_driver(comm_id, field, result_field, idim, jdim)
    call get_my_rank(my_rank)
    print*, "rank", my_rank, "result:", result_field

    call cleanup_comm()

end program run_parallel


