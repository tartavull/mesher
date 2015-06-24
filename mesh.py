import math
import util

from tvtk.api import tvtk

class Mesh:

	def __init__(self, vertex):

		if vertex == None or len(vertex) < 3:
			raise Exception('Not a valid vertex data')

		self.vertex = vertex

		self.triangles = self.trianglesFromVertex(self.vertex);

		self.displayStats()
		self.removeZeroAreaTriangles()
		self.displayStats()

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

		print len(remove)
		self.triangles[:] = [ item for i,item in enumerate(self.triangles) if i not in remove]


	def makeUniformGrid(self, grid_size):

		grid = dict()

		divs = int(math.ceil(1.0 / grid_size))
		for x in range(divs):
			grid[x] = dict()

			for y in range(divs):
				grid[x][y] = dict()

				for z in range(divs):
					grid[x][y][z] = list()

		return grid

		
		return grid

	def weldVertices(self, tolerance):

		grid = self.makeUniformGrid(tolerance)

		for vertex in self.vertex:
			xpos = int(math.floor(vertex[0] / tolerance))
			ypos = int(math.floor(vertex[1] / tolerance))
			zpos = int(math.floor(vertex[2] / tolerance))

			for x_grid in range(xpos-1, xpos+2):
				for y_grid in range(ypos-1, ypos+2):
					for z_grid in range(zpos-1, zpos+2):
						
						for neighbor in grid[x_grid][y_grid][z_grid]:

							if util.distanceBetweenVertex( neighbor , vertex ) < tolerance:
								print 'merge ' , neighbor ,' and ' , vertex 

						#If this can't be merge with any of the neighbors , add it to the list
						grid[x_grid][y_grid][z_grid].append(vertex)	 





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
		print 

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
		# mlab.pipeline.surface(mlab.pipeline.extract_edges(surf), color=(0, 0, 0))

		


