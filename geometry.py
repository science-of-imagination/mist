'''
Transforms the data parsed from the file into geometrical representations of the objects.
Implements:
- IndexedFaceSet (used by Blender export function)
- Cone
- Box
- Sphere
- Cylinder
- Transform translation

Created on 2012-02-20

@authors:
Sebastien Ouellet sebouel@gmail.com
'''
import tools
from math import *

class Transform:
    """ Stores all the information parsed from the file about the transform node for a shape """
    def __init__(self):
        self.transformations = []
        self.values = []
        self.name = None

class Shape:
    """ Stores all the information parsed from the file for a shape and
        computes a few numerical attributes """
    def __init__(self, transform=Transform()):
        self.transform = transform
        self.attributes = []
        self.attributes_values = []
        self.child_names = []
        self.child_nodes = []
        self.type_id = []
        self.type_values = []
        self.location = [0,0,0]
        self.name = "None"
        self.type = None
        self.bounding_box = None
        self.scale = 1
        self.radius = 1
        self.height = 2
        self.size = [2,2,2]
        self.bottomRadius = 1
        self.pointCoordinate = []
        self.volume = 1
        self.scene_bounding_box = None

    def update_shape(self):
        """ Takes information from the parser to find numerical values
            for the location and size of objects """
        ### Updating all shapes
        for attribute in zip(self.transform.transformations,self.transform.values):
            if attribute[0] == "translation":
                self.location = read_values(attribute)

        """
        if attribute[0] ==
        """

        ### Updating according to type
        if self.type == "Box":
            for attribute in zip(self.type_id,self.type_values):
                if attribute[0] == "size":
                    self.size = read_values(attribute)

        if self.type == "IndexedFaceSet" > 0:
            strings_list = self.pointCoordinate.split(" ")
            self.pointCoordinate = []
            index = 0
            vertex = []
            for point in strings_list:
                if len(point) > 0:
                    if point[-1] == ",":
                        vertex.append(eval(point[:-1]))
                    else:
                        vertex.append(eval(point))
                    if index == 2:
                        self.pointCoordinate.append(vertex)
                        vertex = []
                        index = 0
                    else:
                        index += 1

        if self.type == "Sphere":
            for attribute in zip(self.type_id,self.type_values):
                if attribute[0] == "radius":
                    self.radius = eval(attribute[1])

        if self.type == "Cone":
            for attribute in zip(self.type_id,self.type_values):
                if attribute[0] == "bottomRadius":
                    self.bottomRadius = eval(attribute[1])
                if attribute[0] == "height":
                    self.height = eval(attribute[1])

        if self.type == "Cylinder":
            for attribute in zip(self.type_id,self.type_values):
                if attribute[0] == "radius":
                    self.radius = eval(attribute[1])
                if attribute[0] == "height":
                    self.height = eval(attribute[1])

    def calculate_bounding_box(self):
        """ Computes a bounding box in the form [min_vertex, max_vertex] """
        if self.type == "Box":
            minCorner = list(self.location)
            maxCorner = list(self.location)
            a = zip(self.size,maxCorner)
            newMaxCorner = []
            for value in a:
                newMaxCorner.append(value[1] + value[0]/2.0)
            b = zip(self.size,minCorner)
            newMinCorner = []
            for value in b:
                newMinCorner.append(value[1]-value[0]/2.0)
            self.bounding_box = [newMinCorner, newMaxCorner]

        elif self.type == "Sphere":
            minCorner = list(self.location)
            maxCorner = list(self.location)
            newMaxCorner = []
            for value in maxCorner:
                newMaxCorner.append(value + self.radius)
            newMinCorner = []
            for value in minCorner:
                newMinCorner.append(value - self.radius)
            self.bounding_box = [newMinCorner, newMaxCorner]

        elif self.type == "Cone":
            minCorner = list(self.location)
            maxCorner = list(self.location)
            newMaxCorner = []
            count = 0
            for value in maxCorner:
                count +=1
                if count == 2:
                    newMaxCorner.append(value + self.height/2.0)
                else:
                    newMaxCorner.append(value + self.bottomRadius)
            newMinCorner = []
            count = 0
            for value in minCorner:
                count +=1
                if count == 2:
                    newMinCorner.append(value - self.height/2.0)
                else:
                    newMinCorner.append(value - self.bottomRadius)
            self.bounding_box = [newMinCorner, newMaxCorner]

        elif self.type == "Cylinder":
            minCorner = list(self.location)
            maxCorner = list(self.location)
            newMaxCorner = []
            count = 0
            for value in maxCorner:
                count +=1
                if count == 2:
                    newMaxCorner.append(value + self.height/2.0)
                else:
                    newMaxCorner.append(value + self.radius)
            newMinCorner = []
            count = 0
            for value in minCorner:
                count +=1
                if count == 2:
                    newMinCorner.append(value - self.height/2.0)
                else:
                    newMinCorner.append(value - self.radius)
            self.bounding_box = [newMinCorner, newMaxCorner]

        elif self.type == "IndexedFaceSet":
            minCorner = []
            maxCorner = []
            for i in xrange(3):
                axevertices = [vertex[i] for vertex in self.pointCoordinate]
                minCorner.append(self.location[i]+min(axevertices))
                maxCorner.append(self.location[i]+max(axevertices))
            self.bounding_box = [minCorner, maxCorner]

        tools.calculate_volume(self)

        """
        ### Update all shapes

        for attribute in zip(self.transform.transformations,self.transform.values):
            if attribute[0] == "rotation":
                rotation_matrix = []
                values = read_values(attribute)
                vector = values[:3]
                angle = values[3]
                length = x3d_tools.calculate_length(vector)
                vector = [axe/length for axe in vector]
                line0 = [cos(angle)+(vector[1]**2)*(1-cos(angle)), vector[0]*vector[1]*(1-cos(angle))-(vector[2]*sin(angle)), vector[0]*vector[2]*(1-cos(angle))-(vector[1]*sin(angle))
        """

    def oriented_bouding_box(self):
        """ Not used/Incomplete """
        pass

def read_values(attribute):
        """ Takes a strings and outputs a list of numerical values taken from the string """
        strings_list = attribute[1].split(" ")
        values = []
        for value in strings_list:
                values.append(eval(value))
        return values

