module pycomm
    use, intrinsic:: iso_c_binding
    implicit none

    public
    interface
        function setup_ring_comm() result(comm_id) bind(c, name="setup_ring_comm")
            integer(comm_id), intent(in) :: y
        end function setup_ring_comm
    end interface
end module pycomm