'''
Stores and manipulates the relationships computed

Created on 2012-03-18

@authors:
Sebastien Ouellet sebouel@gmail.com
'''
import templates
import tools

proximity_threshold = 0.90
good_threshold = 0.75

class RelationshipsTable:
    """ Database that includes a container for the relationships and functions that can
        be applied to the database to search through it """
    def __init__(self):
        self.shapes = []
        self.relationships = []
        self.relevant = []
        self.vectors = []
        
    def fill_vectors(self):
        """ Keeps a vector from the center of two shapes with the shape information, and the distance """
        for shape in self.shapes:
            for shape2 in self.shapes:
                if shape != shape2:
                    vector = tools.calculate_absolute_distance_center(shape, shape2)
                    distance = tools.calculate_length(vector)
                    self.vectors.append((shape,shape2,shape.name, shape2.name, vector,distance,shape.bounding_box[1][1]-shape.bounding_box[0][1]))
    
    def search_table(self, name1 = None, relation = None, name2 = None, mode = 0):
        """ Search the table according to the mode entered:
        0: the name of an object
        1: the relationship
        2: an object and the relationship
        3: two objects and the relationship
        4: two objects """
        found_relationships = []
        if mode == 0:
            for relationship in self.relationships:
                if relationship[0] == name1:
                    found_relationships.append(relationship)
        if mode == 4:
            for relationship in self.relationships:
                if relationship[0] == name1 and relationship[2] == name2:
                    found_relationships.append(relationship)
        if mode == 1:
            for relationship in self.relationships:
                if relationship[1] == relation:
                    found_relationships.append(relationship)
        if mode == 2:
            for relationship in self.relationships:
                if relationship[0] == name1 and relationship[1] == relation:
                    found_relationships.append(relationship)
        if mode == 3:
            for relationship in self.relationships:
                if relationship[0] == name1 and relationship[1] == relation and relationship[2] == name2:
                    found_relationships.append(relationship)
        
        return found_relationships
    
    def distance_find_relevant(self, shape1, relation):
        distance_relationships = (self.search_table(shape1.name, relation, mode = 2))
        for relationship in distance_relationships:
            if relationship[3] > good_threshold:
                self.relevant.append((shape1.name, relation, relationship[2]))       
        
    def find_relevant(self, shape1, relation):
        """ Fills a list with the relationships deemed most relevant to the scene """
        found_relationships = self.search_table(shape1.name, relation, mode = 2)
        
        distance_relationships = []
        for relationship in found_relationships:
            distance_relationships.extend(self.search_table(shape1.name, "isCloseTo", relationship[2], mode = 3))
            distance_relationships.extend(self.search_table(shape1.name, "isFarFrom", relationship[2], mode = 3))
        
        if len(found_relationships) == 0:
            return 0
        
        #shape_names = [relationship[2] for relationship in found_relationships]
        
        #print found_relationships
        #print distance_relationships
        
        products = []
        i = 0
        while i < len(found_relationships):
            if distance_relationships[i][1] == "isFarFrom":
                products.append((found_relationships[i][3]*(1-distance_relationships[i][3]), found_relationships[i][2]))
            else:
                products.append((found_relationships[i][3]*(distance_relationships[i][3]), found_relationships[i][2]))
            i += 1
        
        
        reference_name = max(products)[1]
        
        '''
        reference = None
        for shape in self.shapes:
            if shape.name == reference_name:
                reference = shape
        
        if reference == None:
            return 0
        '''
        
        self.relevant.append((shape1.name, relation, reference_name))
        
        new_relationships = self.search_table(reference_name, "isCloseTo", mode=2)

        for relationship in new_relationships:
            if relationship[3] > proximity_threshold and relationship[2] != shape1.name:
                self.relevant.append((shape1.name, relation, relationship[2]))        
        """
        for shape in self.shapes:
            if shape != shape1:
                other_shapes.append((shape, )
        """
        
    def complete_relevant(self,shape1):
        self.relevant.extend(self.search_table(shape1.name, "isContainedBy", mode= 2))
        self.relevant.extend(self.search_table(shape1.name, "contains", mode=2))
        self.relevant.extend(self.search_table(shape1.name, "protrudesFrom", mode=2))
