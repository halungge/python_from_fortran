from parallel.mesh import TorusMesh, LocalMesh
import numpy as np





def test_v2e2v_table_size():
    mesh = TorusMesh(12, 3)
    v2e2v = mesh.get_offset_table()

    assert (12,4) ==  v2e2v.shape


def test_v2e2v_table():
    mesh = TorusMesh(12, 3)
    v2e2v = mesh.get_offset_table()
    print(v2e2v)
    #assert np.all(np.asarray([4, 1, 3, 12]), v2e2v[0, :])


def test_localmesh_offset():
    mesh = LocalMesh(12)
    assert mesh.get_offset_table() == [i for i in range(12)]