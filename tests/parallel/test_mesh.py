from parallel.mesh import TorusMesh, LocalMesh
import numpy as np





def test_v2e2v_table_size():
    mesh = TorusMesh(12, 3)
    v2e2v = mesh.get_offset_table()

    assert (12,4) ==  v2e2v.shape


def test_v2e2v_table():
    mesh = TorusMesh(12, 4)
    v2e2v = mesh.get_offset_table()
    non_local = [-1, -1, -1, -1]
    ref_table =np.asarray([non_local, # v0 non local node
                 non_local, # v1 non local node
                 non_local, # v2 non local node
                 non_local, # v3 non local node
                 [5, 7, 0, 8], #v4,
                 [6,4,1,9],    #v5
                 [7,5,2, 10],  #v6
                 [4,6,3,11],   #v7
                 [8,11,4,12],   #v8
                 [10, 8, 5, 13], #v9
                 [11, 9, 6, 14], #v10
                 [8,10,7,15], #11
                 [13, 15, 8, 16], #v12
                 [14, 12, 9,17], #13
                 [15,13,10, 10], #14
                 [12,14,11,19], #v15
                 non_local,  #16
                 non_local,  #17
                 non_local, #18
                 non_local #19
                 ])
    print(v2e2v)
    print(v2e2v.shape)
    print(ref_table.shape)
    assert np.all(np.asarray([4, 1, 3, 12]), v2e2v[0, :])
    assert np.all(ref_table[4:16, :], v2e2v)


def test_localmesh_offset():
    mesh = LocalMesh(12)
    assert mesh.get_offset_table() == [i for i in range(12)]

