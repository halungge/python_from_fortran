module communicator
    use MPI
    implicit none
    integer ierr, tag, status(MPI_STATUS_SIZE)
    integer my_rank, left_neighbor, right_neighbor
    integer comm_world, group_world, comm_workers, group_workers, num_procs
    ! reconsider
    private :: ierr, tag, status


contains
    subroutine init(ierr)
        logical initialized
        integer, intent(out):: ierr
        call MPI_Initialized(initialized, ierr)
        if (.not. initialized) then
            print *, "communicator.f90: initalizing mpi first"
            call mpi_init(ierr)
        end if
    end subroutine init

    subroutine setup_comm
        call init(ierr)
        ! set up communicator
        comm_world = MPI_COMM_WORLD
        call MPI_Comm_group(comm_world, group_world, ierr)
        !call MPI_Group_excl(group_world, 1, 0, group_worker, ierr)  ! process 0 not member
        call MPI_Comm_group(comm_world, group_workers, ierr)
        call MPI_Comm_create(comm_world, group_workers, comm_workers, ierr)
        call MPI_Comm_size(comm_workers, num_procs, ierr)
        call MPI_comm_rank(comm_workers, my_rank, ierr)
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


    subroutine exchange(to,from, sendb, recvb,  err)
        implicit none
        real(8), intent(in) :: sendb(:)
        real(8), intent(inout) :: recvb(:)
        integer, intent(out) :: err
        integer, intent(in):: to, from
        integer data_size, data_size_out

        data_size = size(sendb)
        data_size_out = size(recvb)
        if (data_size_out < data_size) then
            write(*,*) "receive buffer recvb to small"
            err = 1
            return
        end if

        call mpi_send(sendb, data_size, MPI_DOUBLE, to, tag, comm_workers, err)
        call mpi_recv(recvb, data_size_out, MPI_DOUBLE, from, tag, comm_workers, status, err)
        if (err /=  0) then
            print *, "me=", my_rank, " error receiving data from ", from
        end if
    end subroutine exchange

    subroutine exchangeLeft(sendb, recvb, err)
        implicit none
        real(8), intent(in) :: sendb(:)
        real(8), intent(inout) :: recvb(:)
        integer, intent(out) :: err
        call exchange(left_neighbor, right_neighbor, sendb, recvb, err)
    end subroutine exchangeLeft

    subroutine exchangeRight(sendb, recvb, err)
        implicit none
        real(8), intent(in) :: sendb(:)
        real(8), intent(inout) :: recvb(:)
        integer, intent(out) :: err
        call exchange(right_neighbor, left_neighbor, sendb, recvb, err)
    end subroutine exchangeRight

    subroutine get_my_rank(y)
        integer, intent(out):: y
        y = my_rank
    end subroutine get_my_rank



    subroutine cleanup
        logical finalized
        call mpi_finalized(finalized, ierr)
        if (.not. finalized) then
            call mpi_finalize(ierr)
        end if
    end subroutine cleanup

end module communicator