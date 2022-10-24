from functional.ffront.fbuiltins import Dimension, DimensionKind, FieldOffset

VDim = Dimension("Vertex")
EDim = Dimension("Edge")
V2E2VDim = Dimension("V2E2V", kind=DimensionKind.LOCAL)
V2E2V = FieldOffset("V2E2V", source=VDim, target=(EDim, V2E2VDim))


# cartesian

IDim = Dimension("I")
JDim = Dimension("J")
Ioff = FieldOffset("Ioff", source=IDim, target=(IDim,))
Joff = FieldOffset("Joff", source=JDim, target=(JDim,))
