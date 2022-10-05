! run_field_sample.f90
program run_parallel
    use, intrinsic :: iso_c_binding
    use MPI
    implicit none

    integer ierr, tag, status
    integer my_rank, left_neighbor, right_neighbor
    integer comm_world, group_world, comm_workers, group_workers, num_procs
    integer(c_int) vdim, GLOBAL_V_NUM, GLOBAL_VX_SIZE, data_size
    real(16), DIMENSION(24) :: data, res
    tag = 13
    GLOBAL_V_NUM = 96


    call mpi_init(ierr)

    comm_world = MPI_COMM_WORLD
    call MPI_Comm_group(comm_world, group_world, ierr)
    !call MPI_Group_excl(group_world, 1, 0, group_worker, ierr)  ! process 0 not member
    call MPI_Comm_group(comm_world, group_workers, ierr)
    call MPI_Comm_create(comm_world, group_workers, comm_workers, ierr)
    call MPI_Comm_size(comm_workers, num_procs, ierr)

    call mpi_comm_rank(comm_workers, my_rank, ierr)
    !print *, my_rank, "out of ", num_procs, ": hello_world"

    left_neighbor = mod((my_rank - 1 + num_procs), num_procs)
    right_neighbor = mod((my_rank +1), num_procs)
    if (my_rank == 0) then
        print *, "communication pattern:"
    end if
    call mpi_barrier(MPI_COMM_WORLD, ierr)
    print * , "me ", my_rank, "left ", left_neighbor, " right ", right_neighbor
    call mpi_barrier(MPI_COMM_WORLD, ierr)

    data = real(my_rank)
    call mpi_send(data, data_size, MPI_FLOAT, left_neighbor, tag, comm_workers,  ierr )
    call mpi_recv(res, data_size, MPI_FLOAT, right_neighbor, tag, comm_workers, MPI_STATUS_IGNORE, ierr)

    !print *, my_rank, " got data ", res
    call mpi_finalize(ierr)
end program run_parallel