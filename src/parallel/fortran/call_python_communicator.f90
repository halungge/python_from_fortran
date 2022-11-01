! Created by  on 27.10.22.

program call_python_communicator
    use, intrinsic::iso_c_binding
    use MPI
    use pycomm

    implicit none
    integer(c_int) idim, jdim
    real(c_double), allocatable :: field(:,:)
    real(c_double), allocatable:: result_field(:,:)
    logical mpi_done
    integer comm_id, left_rank, right_rank, my_rank, up_rank, down_rank
    integer status(MPI_STATUS_SIZE), ierr, name_len
    CHARACTER(LEN=MPI_MAX_OBJECT_NAME) comm_name

    comm_id = setup_ring_comm()
    call mpi_comm_get_name(comm_id, comm_name, name_len, ierr)
    call mpi_comm_rank(comm_id, my_rank, ierr)
    call mpi_cart_shift(comm_id, 1, 1, left_rank, right_rank, ierr)
    call mpi_cart_shift(comm_id, 0, 1, up_rank, down_rank, ierr)
    print *, "my_rank ", my_rank , "in communicator: ", comm_name, comm_id, "left node", left_rank, "right_node", right_rank
    if (up_rank /= my_rank .or. down_rank/=my_rank) then
        print *, "WARNING: communicator ", comm_name, comm_id, "is not a ring! upper node", up_rank, "lower_node", down_rank
    endif

    idim = 4
    jdim = 8
    allocate(field(idim, jdim), result_field(idim, jdim))
    field = 0.0
    call random_number(field(:,2:jdim-1))



    call mpi_sendrecv(field(:, 2), idim, MPI_DOUBLE, left_rank, 0, &
            field(:,jdim), idim, MPI_DOUBLE, right_rank, 0, comm_id, status, ierr)
    call mpi_sendrecv(field(:, jdim-1), idim, MPI_DOUBLE, right_rank, 1, &
            field(:, 1), idim, MPI_DOUBLE, left_rank, 1, comm_id, status, ierr)

    print *, " after exchange"
    print *, "rank", my_rank, "border left:",  field(:, 2)
    print *, "rank", my_rank, "halo left:", field(:,1)
    print *, "rank", my_rank, "border right:",  field(:, jdim-1)
    print *, "rank", my_rank, "halo right:", field(:,jdim)


    call mpi_finalized(mpi_done, ierr)
    if (.not. mpi_done .or. ierr /= 0) then
        call mpi_finalize(ierr)
    end if

end program call_python_communicator