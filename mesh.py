import math
import util

from tvtk.api import tvtk
import ctypes 
import openctm 
import blob

class Mesh:

	def __init__(self, vertex = None):

		if vertex == None:
			self.vertex = list()
			self.triangles = list()

		else:	
			self.vertex = vertex
			self.triangles = self.trianglesFromVertex(self.vertex);

	def trianglesFromVertex(self, vertex):

		triangles = list()

		for index in range(len(vertex) - 2):

			triangles.append( ( index , index+1, index+2) )


		return triangles;

	def removeZeroAreaTriangles(self):

		remove = set()

		for triangleIdx, triangle in enumerate(self.triangles):

			vertex_0 = self.vertex[triangle[0]]
			vertex_1 = self.vertex[triangle[1]]
			vertex_2 = self.vertex[triangle[2]]

			if  vertex_0 == vertex_1 or vertex_0 == vertex_2 or vertex_1 == vertex_2:
				
				remove.add(triangleIdx)


		self.triangles[:] = [ item for i,item in enumerate(self.triangles) if i not in remove]

	def getBucket(self, xpos, ypos, zpos):

		if not hasattr(self,'grid'):
			self.grid = dict()

		if not xpos in self.grid:
			self.grid[xpos] = dict()

		if not ypos in self.grid[xpos]:
			self.grid[xpos][ypos] = dict()

		if not zpos in self.grid[xpos][ypos]:
			self.grid[xpos][ypos][zpos] = list()

		return self.grid[xpos][ypos][zpos]

	def weldVertices(self, tolerance):

		idx_map = dict()
		for vertex_idx ,vertex in enumerate(self.vertex):
			xpos = int(math.floor(vertex[0] / tolerance))
			ypos = int(math.floor(vertex[1] / tolerance))
			zpos = int(math.floor(vertex[2] / tolerance))

			neighbor = self.findNeighborVertex(tolerance, vertex, xpos, ypos, zpos)			
						
			#If this can't be merge with any of the neighbors , add it to the list
			if neighbor:
				idx_map[vertex_idx] = neighbor[0]
			else:
				self.getBucket(xpos,ypos,zpos).append((vertex_idx, vertex))
				idx_map[vertex_idx] = vertex_idx	

		
		keep_vertex = sorted(set(idx_map.values()))
		self.vertex[:] = [ item for i,item in enumerate(self.vertex) if i in keep_vertex]

		for key  in idx_map: 
			value = idx_map[key]
			idx_map[key] = util.binary_search(keep_vertex,value)
		
		for triangle_idx , triangle in enumerate(self.triangles):

			self.triangles[triangle_idx] = (idx_map[triangle[0]] , idx_map[triangle[1]] , idx_map[triangle[2]])


	def findNeighborVertex(self, tolerance, vertex , xpos, ypos, zpos):

		grid_size = int(math.ceil(1.0 / tolerance))

		x_min = max(0,xpos-1)
		x_max = min(xpos+2, grid_size)

		y_min = max(0, ypos-1)
		y_max = min(ypos+2, grid_size)

		z_min = max(0, zpos-1)
		z_max = min(zpos+2, grid_size)
		
		for x_grid in range(x_min, x_max):
				for y_grid in range(y_min, y_max):
					for z_grid in range(z_min, z_max):
						
						for neighbor in self.getBucket(x_grid,y_grid,z_grid):

							if util.distanceBetweenVertex( neighbor[1] , vertex ) < tolerance:
								return neighbor

		return False


	def computeBoundingBox(self):

		#Initialize the boundingBox with values from the first vertex
		boundingBox = { 'max':{'x':self.vertex[0][0], 'y':self.vertex[0][1], 'z':self.vertex[0][2]},
										'min':{'x':self.vertex[0][0], 'y':self.vertex[0][1], 'z':self.vertex[0][2]}}

		for vertex in self.vertex:

			if vertex[0] > boundingBox['max']['x']:
				boundingBox['max']['x'] = vertex[0]

			if vertex[0] < boundingBox['min']['x']:
				boundingBox['min']['x'] = vertex[0]

			if vertex[1] > boundingBox['max']['y']:
				boundingBox['max']['y'] = vertex[1]

			if vertex[1] < boundingBox['min']['y']:
				boundingBox['min']['y'] = vertex[1]

			if vertex[2] > boundingBox['max']['z']:
				boundingBox['max']['z'] = vertex[2]

			if vertex[2] < boundingBox['min']['z']:
				boundingBox['min']['z'] = vertex[2]

		self.boundingBox = boundingBox

	def merge(self, mesh):

		offset = len(self.vertex)
		for triangle in mesh.triangles:

			vertex_idx_0 = triangle[0] + offset
			vertex_idx_1 = triangle[1] + offset
			vertex_idx_2 = triangle[2] + offset

			self.triangles.append( (vertex_idx_0, vertex_idx_1, vertex_idx_2) )


		#Concatentate vertex
		self.vertex = self.vertex + mesh.vertex

	def displayStats(self):
		print "There are " , len(self.triangles), " triangles and " , len(self.vertex), " points"

	def displayMesh(self, mlab):

		mesh = tvtk.PolyData(points=util.list2DToNumpy(self.vertex), polys=util.list2DToNumpy(self.triangles))
		surf = mlab.pipeline.surface(mesh, opacity=1.0)
		mlab.pipeline.surface(mlab.pipeline.extract_edges(surf), color=(0, 0, 0))

	def dump(self, filename = "mesh.ctm"):
		pVertex = blob.make_blob(self.vertex, ctypes.c_float)
		pTriangles = blob.make_blob(self.triangles, ctypes.c_uint)
		pNormals = ctypes.POINTER(ctypes.c_float)()
		ctm = openctm.ctmNewContext(openctm.CTM_EXPORT)
		openctm.ctmDefineMesh(ctm, pVertex, len(self.vertex), pTriangles, len(self.triangles), pNormals)
		openctm.ctmSave(ctm, filename)
		openctm.ctmFreeContext(ctm)

	def move(self, x_relative, y_relative, z_relative):

		for vertex_idx , vertex in enumerate(self.vertex):
			self.vertex[vertex_idx] = (vertex[0] + x_relative , vertex[1] + y_relative, vertex[2] + z_relative)

	def scale(self, x_scale, y_scale, z_scale):

		for vertex_idx , vertex in enumerate(self.vertex):
			self.vertex[vertex_idx] = (vertex[0] * x_scale , vertex[1] * y_scale, vertex[2] * z_scale)


