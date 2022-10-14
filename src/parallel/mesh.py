import numpy as np

"""
constants
"""


class TorusMesh:

    def __init__(self, v_num:int, x_length:int):
        self.v2e_dim = 2
        self.neighbor_num = 2
        self.vertex_x_dim = x_length
        self.local_vertex_num = v_num
        self.local_edge_num = self.v2e_dim * v_num
        self.vertex_halo_size = self.neighbor_num * self.vertex_x_dim
        self.edge_halo_size = self.neighbor_num * self.vertex_x_dim
        self.vertex_num = self.local_vertex_num + self.vertex_halo_size
        self.edge_num = self.local_edge_num + self.edge_halo_size

        def _v2e2v_table():
            cols = int(self.local_vertex_num / self.vertex_x_dim)
            for c in range(cols):
                for r in range(self.vertex_x_dim):
                    t = [r+1, (r-1)%self.vertex_x_dim + cols * self.vertex_x_dim]
                    print(t)
            t = [[i+1, (i-1) % self.vertex_x_dim + self.vertex_x_dim, i-self.vertex_x_dim, i+self.vertex_x_dim] for i in range(self.vertex_x_dim,  self.local_vertex_num + self.vertex_x_dim)]
            t = np.asarray(t)
            #t = t % self.vertex_x_dim
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




