from construct import *
import requests
from numpy import array, random, linspace, pi, ravel, cos, sin, empty
import numpy
from tvtk.api import tvtk
from mayavi.sources.vtk_data_source import VTKDataSource
from mayavi import mlab
import cPickle as pickle
import os.path

import ctypes 
import openctm 
import blob


def drawBox(min_x = 0.0, max_x=1.0, min_y=0.0, max_y=1.0, min_z=0.0, max_z=1.0):
	points = numpy.array([[min_x, min_y, min_z ], [max_x , min_y , min_z],[min_x, max_y , min_z],
												[max_x, max_y, min_z ],[max_x, max_y , max_z],[max_x,min_y, min_z],
												[max_x,min_y, max_z],	[min_x,min_y, min_z],[min_x,min_y, max_z],
												[min_x,max_y, min_z ],[min_x,max_y, max_z],[max_x,max_y, max_z],
												[min_x,min_y, max_z],[max_x,min_y, max_z]])


	view(points, opacity = 0.2)


def getCellPoints(cellID, mip ,x ,y ,z):

	path = "http://data.eyewire.org/cell/{0}/chunk/{1}/{2}/{3}/{4}/mesh".format(cellID * 10 + 1, mip ,x,y,z)
	
	try:
			r = requests.get(path)
	except Exception, e:
		print "couldn't get \n", path, " because," 
		print e
		return

	edge_length = 128 * (2 ** mip)

	vertex = Struct("vertex",
	     LFloat32("vx"),
	     LFloat32("vy"),
	     LFloat32("vz"),
	     LFloat32("nx"),
	     LFloat32("ny"),
	     LFloat32("nz")
	)

	meshParser = Array(len(r.content)/ 24 ,vertex)

	points = list()

	for vertex in meshParser.parse(r.content):

		output_x = edge_length * x + 0.5 * vertex.vx
		output_y = edge_length * y + 0.5 * vertex.vy
		output_z = 1.4 * edge_length * z + 1.4 * 0.5 * vertex.vz

		points.append(numpy.array([output_x ,output_y,output_z]))

	points = numpy.array(points)

	if len(points) == 0:
		return

	print "getting chunk {0}-{1}-{2} is not empty for cell {3}".format(x,y,z, cellID)
	

	min_x = int(edge_length * x)
	min_y = int(edge_length * y)
	min_z = int(edge_length * z)
	max_x = int(edge_length * x)
	max_y = int(edge_length * y)
	max_z = int(edge_length * z)
	drawBox(min_x, max_x, min_y, max_y, min_z, max_z)

	view(points)


def getVolumePoints(volume,x,y,z,segmentID):

	""" 
	$volumeID: integer, unique identifier for volume.
	$mip: integer, MIP-level - must be 0.
	$x, $y, $z: integer, the requested chunks position in the volume. For regular EyeWire volumes (256^3) it has to be either 0 or 1; or even higher for [Omni cubes][omni].
	$segmentID: integer, the segment to load
	"""

	path = "http://data.eyewire.org/volume/{0}/chunk/0/{1}/{2}/{3}/mesh/{4}".format(volume,x,y,z,segmentID)

	try:
		r = requests.get(path)
	except Exception, e:
		print "couldn't get \n", path, " because," 
		print e

	vertex = Struct("vertex",
     LFloat32("vx"),
     LFloat32("vy"),
     LFloat32("vz"),
     LFloat32("nx"),
     LFloat32("ny"),
     LFloat32("nz")
	)

	meshParser = Array(len(r.content)/ 24 ,vertex)

	points = list()

	for vertex in meshParser.parse(r.content):
		points.append(numpy.array([vertex.vx,vertex.vy,vertex.vz]))

	if len(points):
		saveOpenCTM(points)

		points = numpy.array(points)
		objects.append(points)



def view(points , opacity = 1.0):
	""" Open up a mayavi scene and display the dataset in it.
	"""

	triangles = list()
	for n in range(len(points) - 2  ):
		# if numpy.all(points[n] == points[n+1]) or numpy.all(points[n] == points[n+2]) or numpy.all(points[n+1] == points[n+2]):
		# 	continue

		triangles.append(numpy.array([n, n+1 , n+2]))

	triangles = numpy.array(triangles)
	scalars = random.random(points.shape)

	# The TVTK dataset.
	mesh = tvtk.PolyData(points=points, polys=triangles)
	mesh.point_data.scalars = scalars
	mesh.point_data.scalars.name = 'scalars'

	surf = mlab.pipeline.surface(mesh, opacity=opacity)
	mlab.pipeline.surface(mlab.pipeline.extract_edges(surf), color=(0, 0, 0), )


def saveOpenCTM(verts):

	verts = list(verts)
	faces = list()
	for n in range(len(verts) - 2  ):
		faces.append((n, n+1 , n+2))

	pVerts = blob.make_blob(verts, ctypes.c_float)
	pFaces = blob.make_blob(faces, ctypes.c_uint)
	pNormals = ctypes.POINTER(ctypes.c_float)()
	ctm = openctm.ctmNewContext(openctm.CTM_EXPORT)
	openctm.ctmDefineMesh(ctm, pVerts, len(verts), pFaces, len(faces), pNormals)
	openctm.ctmSave(ctm, "mesh.ctm")
	openctm.ctmFreeContext(ctm)



fig = mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))


# for x in range(1):
# 	for y in range(5):
# 		for z in range(3):
# 			getCellPoints(144,5,x,y,z)
#
# 			

if not os.path.isfile('objects.numpy'):	
	objects = list()

	for id in (654, 665, 1009, 1538, 1620, 1621, 1667, 1668, 1680, 1723, 1936, 1960, 2029, 2086, 2146, 2163, 2184, 2196, 2197, 2215, 2231, 2334, 2376, 2419, 2453, 2613):
		for x in range(2):
			for y in range(2):
				for z in range(2):
					getVolumePoints(47339,x,y,z,id)


	objects = numpy.array(objects)
	objects.dump('objects.numpy');
else:
	objects = numpy.load('objects.numpy')


# for seg in objects:
# 	view(seg)


first = 6
second = 13

# view(objects[first])
view(objects[first])

print objects[first].shape, objects[second].shape

new = list()


# for i in range(0,objects[first].shape[0]):
# 	add = True
# 	for j in range(0,objects[second].shape[0]):
# 		if numpy.all(objects[first][i] == objects[second][j]):
# 			print i,j
# 			add = False
# 			coord = list(objects[first][i])

# 			print coord
# 			mlab.points3d(coord[0], coord[1], coord[2], scale_factor=0.001, colormap="copper")
# 			break

mlab.savefig('meshes6.obj')




# 	if add:
# 		new.append(objects[0][i])

# view(numpy.array(new))





print "done"
mlab.show()


