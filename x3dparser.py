'''
Parses files in the X3D format

Created on 2012-02-20

@authors:
Sebastien Ouellet sebouel@gmail.com
'''
import xml.dom.minidom

import geometry

def parse_child_nodes(shapes):
    """ Parses the child nodes information for each shape """
    for shape in shapes:
        if shape.transform.transformations[-1] == "DEF" or shape.transform.transformations[-1] == "USE":
            shape.transform.name = shape.transform.values[-1]
            shape.name = shape.transform.name
        if len(shape.attributes) == 1:
            if shape.attributes[0] == "DEF" or shape.attributes[0] == "USE":
                shape.name = shape.attributes_values[0]
        if len(shape.attributes)>1:
            print "More than one attribute"
            print shape.attributes
        
        shape.type = shape.child_names[0]
        number = shape.child_nodes[0].attributes.length
        for attribute in xrange(number):
            shape.type_id.append(shape.child_nodes[0].attributes.item(attribute).localName)
            shape.type_values.append(shape.child_nodes[0].attributes.item(attribute).value)
        
        if len(shape.child_names)>1:
            print "More than one child node"
            print shape.child_names
        
        if shape.type == "IndexedFaceSet":
            for childNode in shape.child_nodes[0].childNodes:
                if childNode.localName == "Coordinate":
                    number = childNode.attributes.length
                    for i in xrange(number):
                        if childNode.attributes.item(i).localName == "point":
                            shape.pointCoordinate = childNode.attributes.item(i).value
            

def parse_file(x3dfile):
    """ Parses a single given file for shapes and their transform """
    shapes = []
    document = xml.dom.minidom.parse(x3dfile)
    for node_transform in document.getElementsByTagName("Transform"):
        current_transform = geometry.Transform()
        number = node_transform.attributes.length
        for transformation in xrange(number):
            current_transform.transformations.append(node_transform.attributes.item(transformation).localName)
            current_transform.values.append(node_transform.attributes.item(transformation).value)
        for node_shape in node_transform.getElementsByTagName("Shape"):
            current_shape = geometry.Shape(current_transform)
            shapes.append(current_shape)
            number = node_shape.attributes.length
            for attribute in xrange(number):
                current_shape.attributes.append(node_shape.attributes.item(attribute).localName)
                current_shape.attributes_values.append(node_shape.attributes.item(attribute).value)
            for current_node in node_shape.childNodes:
                name = current_node.localName
                if name != "Appearance" and name != None:
                    current_shape.child_names.append(name)
                    current_shape.child_nodes.append(current_node)
                    
    #For non-transformed shapes
    for node_shape in document.getElementsByTagName("Shape"):
            if node_shape.parentNode.localName != "Transform": 
                current_shape = geometry.Shape()
                shapes.append(current_shape)
                number = node_shape.attributes.length
                for attribute in xrange(number):
                    current_shape.attributes.append(node_shape.attributes.item(attribute).localName)
                    current_shape.attributes_values.append(node_shape.attributes.item(attribute).value)
                for current_node in node_shape.childNodes:
                    name = current_node.localName
                    if name != "Appearance" and name != None:
                        current_shape.child_names.append(name)
                        current_shape.child_nodes.append(current_node)       
    return shapes




