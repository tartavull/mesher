import numpy
import math
from bisect import bisect_left


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

def binary_search(array, value, lo=0, hi=None):   # can't use array to specify default for hi
    hi = hi if hi is not None else len(array) # hi defaults to len(array)   
    pos = bisect_left(array,value,lo,hi)          # find insertion position
    return (pos if pos != hi and array[pos] == value else -1) # don't walk off the end
