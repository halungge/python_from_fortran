! simple fortran hello world MPI program: that uses MPI directly
program run_parallel
    use, intrinsic :: iso_c_binding
    use MPI
    implicit none

    integer ierr, tag, status(MPI_STATUS_SIZE)
    integer my_rank, left_neighbor, right_neighbor
    integer comm_world, group_world, comm_workers, group_workers, num_procs
    integer(c_int) GLOBAL_V_NUM, data_size
    real :: outgoing(24), incoming(24)
    !integer outgoing, incoming

    data_size = 24
    tag = 13
    GLOBAL_V_NUM = 96
    call random_number(outgoing)
    incoming = 0



    call mpi_init(ierr)
    ! set up communicator
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
    print * , "me ", my_rank, ": left ", left_neighbor, ", right ", right_neighbor
    call mpi_barrier(MPI_COMM_WORLD, ierr)


    ! exchange
    call mpi_send(outgoing, data_size, MPI_REAL, left_neighbor, tag, comm_workers,  ierr )
    call mpi_recv(incoming, data_size, MPI_REAL, right_neighbor, tag, comm_workers, status, ierr)

    if (ierr .ne. 0) then
        print *, "me=", my_rank, " error receiving data from ", right_neighbor
    end if
    print *, my_rank, " got data ", incoming
    call mpi_finalize(ierr)
end program run_parallel
