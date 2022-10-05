! run_field_sample.f90
program run_parallel
    use, intrinsic :: iso_c_binding
    use MPI
    implicit none


    integer ierr, my_rank, left_neighbor
    integer comm_world, group_world, comm_workers, group_workers, num_procs
    integer(c_int) vdim, GLOBAL_V_NUM, GLOBAL_VX_SIZE
    real(16), DIMENSION(24) :: data, res


    GLOBAL_V_NUM = 96



    call mpi_init(ierr)

     comm_world = MPI_COMM_WORLD
     call MPI_Comm_group(comm_world, group_world, ierr)
    !call MPI_Group_excl(group_world, 1, 0, group_worker, ierr)  ! process 0 not member
     call MPI_Comm_group(comm_world, group_workers, ierr)
     call MPI_Comm_create(comm_world, group_workers, comm_workers, ierr)
    call MPI_Comm_size(comm_workers, num_procs, ierr)



    call mpi_comm_rank(comm_workers, my_rank, ierr)
    !call mpi_send
    print*, my_rank,"out of " , num_procs,  ": hello_world"


    call mpi_finalize(ierr)
    end program run_parallel