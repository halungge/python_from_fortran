import numpy as np

"""
constants
"""


class TorusMesh:

    def __init__(self, v_num:int, vx_size:int):
        self.local_vertex_num = v_num
        self.local_edge_num = 3 * v_num
        self.vertex_x_dim = vx_size
        self.vertex_halo_size = 2 * self.vertex_x_dim
        self.edge_halo_size = 2 * self.vertex_x_dim
        self.vertex_num = self.local_vertex_num + self.vertex_halo_size
        self.edge_num = self.local_edge_num + self.edge_halo_size

        def _v2e2v_table():
            t = [[i-1, i+1, i-self.vertex_x_dim, i+self.vertex_x_dim] for i in range(0,  self.local_vertex_num)]
            t = np.asarray(t)
            t = t % self.vertex_x_dim
            return t

        self.v2e2v_table = _v2e2v_table()

    def get_offset_table(self):
        return self.v2e2v_table

    def get_local_size(self):
        return self.local_vertex_num




class LocalMesh:
    def __init__(self, local_size:int):
        self.local_num =local_size


    def get_local_size(self)->int:
        return self.local_num


    def get_offset_table(self):
        return np.asarray([i for i in range(self.local_num)])



