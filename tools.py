'''
A library of tools useful throughout the process of analyzing spatial relationships.

Created on 2012-02-21

@authors:
Sebastien Ouellet sebouel@gmail.com
'''
import math

def calculate_absolute_distance_center(shape1, shape2):
    """ Outputs the distance, as a vector, between the center of two shapes """
    vectorx= shape2.location[0]-shape1.location[0]
    vectory= shape2.location[1]-shape1.location[1]
    vectorz= shape2.location[2]-shape1.location[2]
    center= (vectorx, vectory, vectorz)
    return center

def calculate_absolute_distance_sides(shape1, shape2, axe):
    """ Outputs the distance as a single value between the opposite sides of two shapes. The two sides are defined by the given axe """
    shape1_min = shape1.bounding_box[0][axe]
    shape1_max = shape1.bounding_box[1][axe]
    shape2_min = shape2.bounding_box[0][axe]
    shape2_max = shape2.bounding_box[1][axe]
    
    if calculate_absolute_distance_center(shape1,shape2)[axe] >= 0:
        #print "positive"
        #print calculate_absolute_distance_center(shape1,shape2)[axe]
        sides = shape2_min - shape1_max
        #print sides
    else:
        #print "negative"
        #print calculate_absolute_distance_center(shape1,shape2)[axe]
        sides = shape2_max - shape1_min
        #print sides
    return sides

def calculate_length(vector):
    """ Outputs a single value computed to be the length of a given vector """
    return math.sqrt(sum([axe**2 for axe in vector]))

def calculate_side(shape, axe):
    """ Calculates the side of an object given an axe """
    return shape.bounding_box[1][axe]-shape.bounding_box[0][axe]

def calculate_volume(shape):
    """ Outputs the volume of the bounding box of a given shape """
    for side in xrange(3):
        shape.volume *= shape.bounding_box[1][side]-shape.bounding_box[0][side]
