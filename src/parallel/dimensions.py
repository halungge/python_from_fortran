from functional.ffront.fbuiltins import Dimension, Field, FieldOffset, DimensionKind, neighbor_sum
VDim = Dimension("Vertex")
EDim = Dimension("Edge")
V2E2VDim = Dimension("V2E2V", kind=DimensionKind.LOCAL)
V2E2V = FieldOffset("V2E2V", source=VDim, target=(EDim,V2E2VDim))