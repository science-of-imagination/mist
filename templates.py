'''
Creates trees of relationships, organized hierarchically, and associates the nodes of
the trees with functions (most of them returning a boolean value)

Created on 2012-02-21

@authors:
Sebastien Ouellet sebouel@gmail.com
'''
import math

import tools

####### Parameters #######

#first_fuz = 0.50
#second_fuz = 0.50

good_threshold = 0.75
acceptable_threshold = 0.50

##########################

class Tree:
    """ Basic type of object used to create the trees of relationships.
        The structure of those trees organizes knowledge about how the relationships interact,
        with a hierarchy of states """
    def __init__(self, state=None, test=None, if_true=None, if_false=None):
        self.state = state
        self.test = test
        self.left = if_true
        self.right = if_false

def make_directional():
    """ Creates trees of directional relationships and outputs them in a list """
    left = Tree(test=directional_test, if_true=Tree(state="isRightOf"), if_false=Tree(state="isLeftOf"))
    over = Tree(test=directional_test, if_true=Tree(state="isAbove"), if_false=Tree(state="isBelow"))
    front = Tree(test=directional_test, if_true=Tree(state="isInFrontOf"), if_false=Tree(state="isBehind"))
    return [left, over, front]

def make_other_relationships():
    """ Creates a tree of relationships and outputs it """
    protruding = Tree(state="protrudesFrom")
    containment = Tree(test=contain_test, if_true=Tree(state="contains"), if_false=Tree(state="isContainedBy"))
    intersect = Tree(state="intersects", test=protrude_test, if_true=protruding, if_false=containment)
    contact = Tree(test=contact_test, if_true=Tree(state="isAdjacentTo"), if_false=Tree())
    near = Tree(state="isCloseTo", test=intersect_test, if_true=intersect, if_false=contact)
    relational = Tree(test=far_test, if_true=Tree(state="isFarFrom"), if_false=near)
    return relational

def calculate_other_relationships(tree, shape1, shape2, depth=10):
    """ Takes the information from two shapes and interprets the tree to output a list of
        relationships which apply to those shapes """
    other_relationships = []
    counter = 1
    current_tree = tree
    while counter <= depth and current_tree.test != None:
        if current_tree.test(shape1, shape2):
            current_tree = current_tree.left
        else:
            current_tree = current_tree.right
        if current_tree.state != None:
            if current_tree.state == "isFarFrom":
                other_relationships.append((shape1.name,current_tree.state,shape2.name, far_test(shape1, shape2, membership=1)))
            elif current_tree.state == "isCloseTo":
                other_relationships.append((shape1.name,current_tree.state,shape2.name, far_test(shape1, shape2, membership=2)))
            else:    
                other_relationships.append((shape1.name,current_tree.state,shape2.name))
        counter += 1

    return other_relationships

def calculate_directions(trees, shape1, shape2):
    """ Interprets the tree of directional relationships for two shapes and decides if they are
        relevant given the individual contribution of their vector to the total distance """
    results = []
    i = 0
    for direction in trees:
        results.append(direction.test(shape1, shape2,i))
        i += 1
    distances = [math.fabs(value[0]) for value in results]
    booleans = [value[1] for value in results]

    to_remove = []
    for i in xrange(3):
        if tools.calculate_side(shape1, i) < tools.calculate_side(shape2, i):
            if shape1.bounding_box[1][i] < shape2.bounding_box[1][i] and shape1.bounding_box[0][i] > shape2.bounding_box[0][i]:
                to_remove.append(i)
        else:
            if shape1.bounding_box[1][i] > shape2.bounding_box[1][i] and shape1.bounding_box[0][i] < shape2.bounding_box[0][i]:
                to_remove.append(i)
    """
        if booleans[i]:
            if shape1.bounding_box[0][i] < shape2.bounding_box[1][i]:
                to_remove.append(i)
        else:
            if shape1.bounding_box[1][i] > shape2.bounding_box[0][i]:
                to_remove.append(i)
    """
    """
        if booleans[i]:
                if shape1.bounding_box[1][i] < shape2.bounding_box[1][i] and shape1.bounding_box[0][i] > shape2.bounding_box[0][i]:
                    to_remove.append(i)
        else:
            if shape1.bounding_box[1][i] > shape2.bounding_box[1][i] and shape1.bounding_box[0][i] < shape2.bounding_box[0][i]:
                to_remove.append(i)
    """
    
    for item in to_remove:
        distances[item] = 0.0
    
    #total_length = sum(distances) #Old way
    total_length = math.sqrt(sum([distance**2 for distance in distances]))
    if total_length != 0:
        proportions = []
        for direction in distances:
            proportions.append(float(direction)/total_length)

        #print proportions
        props = zip(proportions,trees,booleans)
        properties = []
        for prop in props:
            if prop[0] > acceptable_threshold:
                properties.append(prop)
        
        '''
        props.sort()
        properties = [(props[-1][1],props[-1][2])]
        if len(props) > 1:
            if props[-2][0] > first_fuz:
                properties.append((props[-2][1],props[-2][2]))
        if len(props) > 2:
            if props[-3][0] > second_fuz:
                properties.append((props[-3][1],props[-3][2]))
        '''
        directional_relationships = []
        for property in properties:
            if property[2]: # shape 1 is less far along an axe
                directional_relationships.append((shape1.name,property[1].left.state,shape2.name, property[0]))
            else:
                directional_relationships.append((shape1.name,property[1].right.state,shape2.name, property[0]))
        return directional_relationships       
    else:
        return []
        

def directional_test(shape1, shape2, direction):
    """ Computes the distance vector from the center of the shapes and returns it with a boolean
        indicating the direction of the vector """
    center_distance = tools.calculate_absolute_distance_center(shape1, shape2)[direction]
    #side_distance = tools.calculate_absolute_distance_sides(shape1, shape2, direction)
    if center_distance > 0:
        return (center_distance, False)
    else:
        return (center_distance, True)

def contact_test(shape1, shape2):
    """ Checks to see if two shapes are near enough to be called adjacent by comparing the
        distance from the center and their size """
    # Needs work
    return False

    sides1 = []
    for index in xrange(2):
        sides1.append(shape1.bounding_box[1][index] - shape1.bounding_box[0][index])
    sides2 = []
    for index in xrange(2):
        sides2.append(shape2.bounding_box[1][index] - shape2.bounding_box[0][index])

    side1 = min(sides1)
    side2 = min(sides2)
    side = min([side1, side2])

    distance = tools.calculate_length(tools.calculate_absolute_distance_center(shape1, shape2))
    num_shape1s_in_distance = math.fabs(float(distance) / side)
    if num_shape1s_in_distance <= 1.5 and not intersect_test(shape1, shape2):
        return True
    else:
        return False

def contain_test(shape1, shape2):
    """ Checks to see which of two shapes is the largest """
    if shape1.volume > shape2.volume:
        return True
    else:
        return False

def protrude_test(shape1, shape2):
    """ Checks to see if both corners of the bounding box of a shape extends
        beyond those of the other shape """
    containing = []
    for corner in xrange(2):
        for side in xrange(3):
            containing.append(shape1.bounding_box[corner][side]-shape2.bounding_box[corner][side])
    index = 0
    first = 0
    second = 0
    for difference in containing:
        if difference >= 0 and index < 3:
            first += 1
        if difference >= 0 and index > 2:
            second += 1
        index += 1
    if (first == 3 and second == 0) or (first == 0 and second == 3) or shape1.bounding_box == shape2.bounding_box:
        return False
    else:
        return True

def intersect_test(shape1, shape2):
    """ Checks to see if the distance vector between the center and the distance vector
        between the sides of two shapes are in the opposite direction """
    counter = 0
    for side in xrange(3):
        if tools.calculate_absolute_distance_sides(shape1, shape2, side)*tools.calculate_absolute_distance_center(shape1, shape2)[side] <= 0:
            counter += 1
    if counter > 2:
        return True
    else:
        return False

def far_value(distance):
    return (1/(1+30*math.e**(-7*distance)))

def near_value(distance):
    return 1-(1/(1+30*math.e**(-7*distance)))

def far_test(shape1, shape2, membership = 0):
    """ Checks to see if the distance is large enough between two shapes to determine they are
        far from each other, estimating the possible maximum distance between them as a baseline """
            
    xs = [vertex[0] for vertex in shape1.scene_bounding_box]
    ys = [vertex[1] for vertex in shape1.scene_bounding_box]
    zs = [vertex[2] for vertex in shape1.scene_bounding_box]
    
    corners = [(x,y,z) for x in xs for y in ys for z in zs]
    
    distances = [tools.calculate_length(((shape1.location[0]-corner[0]), (shape1.location[1]-corner[1]), (shape1.location[2]-corner[2]))) for corner in corners]
    
    maximum_distance = max(distances)
    
    distance = tools.calculate_length(tools.calculate_absolute_distance_center(shape1, shape2))
    
    relative_distance = float(distance)/maximum_distance
    
    value = far_value(relative_distance)
    
    #print shape1.name, value, shape2.name
    
    if membership == 1:
        return value
    if membership == 2:
        return near_value(relative_distance)
    
    if value > acceptable_threshold:
        return True
    else:
        return False
    
    """
    sides1 = []
    for index in xrange(2):
        sides1.append(shape1.bounding_box[1][index] - shape1.bounding_box[0][index])
    sides2 = []
    for index in xrange(2):
        sides2.append(shape2.bounding_box[1][index] - shape2.bounding_box[0][index])

    side1 = sum(sides1)/3.0
    side2 = sum(sides2)/3.0
    side = (side1+side2)/2.0

    distance = tools.calculate_length(tools.calculate_absolute_distance_center(shape1, shape2))
    num_shape1s_in_distance = math.fabs(distance / side)
    if num_shape1s_in_distance>=4:
        return True
    else:
        return False
    """


