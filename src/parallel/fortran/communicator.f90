module communicator
    use, intrinsic :: iso_c_binding
    use MPI
    implicit none
    integer ierr, tag, status(MPI_STATUS_SIZE)
    integer my_rank, left_neighbor, right_neighbor
    integer comm_world, group_world, comm_workers, group_workers, num_procs

    private :: ierr, tag, status


contains
    subroutine setup_comm
        call mpi_init(ierr)
        ! set up communicator
        comm_world = MPI_COMM_WORLD
        call MPI_Comm_group(comm_world, group_world, ierr)
        !call MPI_Group_excl(group_world, 1, 0, group_worker, ierr)  ! process 0 not member
        call MPI_Comm_group(comm_world, group_workers, ierr)
        call MPI_Comm_create(comm_world, group_workers, comm_workers, ierr)
        call MPI_Comm_size(comm_workers, num_procs, ierr)
        call mpi_comm_rank(comm_workers, my_rank, ierr)
        left_neighbor = mod((my_rank - 1 + num_procs), num_procs)
        right_neighbor = mod((my_rank + 1), num_procs)
        if (my_rank == 0) then
            print *, "setting up communicator"
            print *, "communication pattern:"
        end if
        call mpi_barrier(MPI_COMM_WORLD, ierr)
        print *, "me ", my_rank, ": left ", left_neighbor, ", right ", right_neighbor
        call mpi_barrier(MPI_COMM_WORLD, ierr)
    end subroutine setup_comm

    subroutine exchangeLeft(sendb, recvb, err)
        implicit none
        real*8, intent(in) :: sendb(:)
        real*8, intent(inout) :: recvb(:)
        integer, intent(out) :: err
        integer data_size, data_size_out

        data_size = size(sendb)
        data_size_out = size(recvb)
        if (data_size_out < data_size) then
            write(*,*) "receive buffer recvb to small"
            err = 1
            return
        end if


        call mpi_send(sendb, data_size, MPI_REAL, left_neighbor, tag, comm_workers, err)
        call mpi_recv(recvb, data_size_out, MPI_REAL, right_neighbor, tag, comm_workers, status, err)
        if (err .ne. 0) then
            print *, "me=", my_rank, " error receiving data from ", right_neighbor
        else
            print *, my_rank, " got data ", recvb
        end if

    end subroutine exchangeLeft

    subroutine cleanup
        call mpi_finalize(ierr)
    end subroutine cleanup
end module communicator