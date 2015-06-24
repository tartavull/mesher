import numpy
import math

def list2DToNumpy( inputList ):

	aux_list = list()

	for element in inputList:
		aux_list.append(numpy.array(element))

	return numpy.array(aux_list)

def distanceBetweenVertex(vertex_1, vertex_2):

	x = math.pow(vertex_1[0] - vertex_2[0],2)
	y = math.pow(vertex_1[1] - vertex_2[1],2)
	z = math.pow(vertex_1[2] - vertex_2[2],2)

	return math.sqrt( x + y + z )
