! Created by  on 27.10.22.

program call_python_communicator
    use, intrinsic::iso_c_binding
    use MPI
    use pycomm_interface

    intrinsic none

    integer nSteps, t, i, me, ierr, comm_id, left, right
    integer(c_int) idim, jdim
    real(c_double), allocatable :: field(:,:)
    real(c_double), allocatable:: result_field(:,:)
    integer status

    ! need to initialize MPI?
    !call mpi_init(ierr)

    comm_id = setup_ring_comm()
    call mpi_comm_rank(comm_id, me, ierr)


    idim = 4
    jdim = 8

    allocate(field(idim, jdim), result_field(idim, jdim))
    field = 0.0
    call random_number(field(:,2:jdim-1))

    call mpi_cart_shift(comm_id, 0, 1, left, right, ierr)
    call mpi_sendrecv(field(:, 2), jdim, MPI_DOUBLE, left, 0, field(:,jdim), jdim, MPI_DOUBLE, right, 0, comm_id,status, ierr)
    print(field)
    print*, "rank", my_rank, "result:", result_field




end program call_python_communicator