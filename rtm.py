import api
from mesh import Mesh

from mayavi import mlab


vertex = api.getSegmentVertex(47339,0,0,0,1668);
if vertex != None:
	mesh_1 = Mesh(vertex)
	# mesh.displayStats()
	# mesh.computeBoundingBox()

	# grid = mesh.makeUniformGrid(0.1)
	# mesh.addToUnifromGrid(0.1,grid)
	# mesh_1.displayMesh(mlab)

vertex_2 = api.getSegmentVertex(47339,1,0,0,1668);
mesh_2 = Mesh(vertex_2)



mesh_1.merge(mesh_2)
mesh_1.displayStats()
mesh_1.displayMesh(mlab)
mlab.show()


mesh_1.weldVertices(0.002)
mesh_1.removeZeroAreaTriangles()
mesh_1.displayStats()

mesh_1.displayMesh(mlab)


mlab.show()

