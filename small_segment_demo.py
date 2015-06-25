import api
from mesh import Mesh

from mayavi import mlab


vertex = api.getSegmentMesh(47339,0,0,0,1668);

mesh_1 = Mesh(vertex)
mesh_1.displayStats()

vertex_2 = api.getSegmentMesh(47339,1,0,0,1668);
mesh_2 = Mesh(vertex_2)
mesh_2.displayStats()

mesh_1.merge(mesh_2)
mesh_1.displayStats()


mesh_1.weldVertices(0.002)
mesh_1.removeZeroAreaTriangles()
mesh_1.displayStats()
mesh_1.dump()

mesh_1.displayMesh(mlab)
mlab.show()
