'''
You can edit the script to load different files, via the singlefile variable.
If you enable the multi_scenes variable, you'll call an application that computes the most common
relationships among the given set of scenes

Created on 2012-03-01

@authors:
Sebastien Ouellet sebouel@gmail.com
'''
import x3dparser
import templates
import database
import sys

####### Parameters #######

if len(sys.argv) > 1:
    singlefile = sys.argv[1]
else:
    singlefile = "shapes2.x3d"

multi_scenes = False

basefile = "applicable"
extension = ".x3d"
files = [basefile+str(incremented)+extension for incremented in xrange(1,6)]

dir_relations_supported = ("isRightOf", "isLeftOf", "isAbove", "isBelow", "isInFrontOf", "isBehind")

##########################

if multi_scenes:
    import designfrequency

def print_relationships(relationships):
    """ Prints a list of relationships """
    print "-----------------------------"
    for relationship in relationships:
        print_relationship(relationship)
    print "-----------------------------"

def print_relationship(triple):
    """ Prints a given relationship (in a list form) as a string """
    print triple[0]+" "+triple[1]+" "+triple[2]
    #print triple[0]+" "+triple[1]+" "+triple[2]+" "+str(triple[3])

def compute_without_opposites(shapes, directional_tree, other_relationships_tree, table):
    """ Computes relationships for all shapes but avoids computing the opposite of the relationships (A against B but not B against A) """
    for i in xrange(len(shapes)):
        shape1 = shapes[i]
        for j in xrange(len(shapes)):
            shape2 = shapes[j]
            if i < j:
                dr = templates.calculate_directions(directional_tree, shape1, shape2)
                for r in dr:
                    table.relationships.append(r)
                other = templates.calculate_other_relationships(other_relationships_tree, shape1, shape2)
                for r in other:
                    table.relationships.append(r)

def compute_everything(shapes, directional_tree, other_relationships_tree, table):
    """ Computes relationships between all shapes and stores them in the database """
    for shape1 in shapes:
            for shape2 in shapes:
                if shape1 != shape2:
                    dr = templates.calculate_directions(directional_tree, shape1, shape2)
                    for r in dr:
                        table.relationships.append(r)
                        #print r
                    other = templates.calculate_other_relationships(other_relationships_tree, shape1, shape2)
                    for r in other:
                        #print r
                        table.relationships.append(r)

def list_relationships(table, arguments, mode):
    """ List all relationships compatible with the arguments """
    if mode == 0:
        relationships = table.search_table(name1=arguments[1],mode=mode)
    if mode == 4:
        relationships = table.search_table(name1=arguments[1],name2=arguments[2],mode=mode)
    if mode == 1:
        relationships = table.search_table(relation=arguments[2],mode=mode)
    print_relationships(relationships)

def query_relationships(shape1=None, shape2=None, depth=None):
    """ Not used/Incomplete """
    pass

def interpret_commands(command, table):
    """ Parses a string command given by the user """
    arguments = command.split(" ")
    if arguments[0] == "relevant":
        print_relationships(table.relevant)
    elif arguments[0] == "list":
        if len(arguments) == 1:
            print_relationships(table.relationships)
        elif len(arguments) == 3:
            if arguments[1] == "None":
                list_relationships(table, arguments, 1)
            else:
                list_relationships(table, arguments, 4)
        else:
            list_relationships(table, arguments, 0)


def main(filename):
    """ Computes relationships and sets up a query interface for the user """
    ### Initialization
    directional_tree = templates.make_directional()
    other_relationships_tree = templates.make_other_relationships()
    table = database.RelationshipsTable()

    ### Parsing
    shapes = x3dparser.parse_file(filename)
    x3dparser.parse_child_nodes(shapes)

    ### Geometric representation
    for shape in shapes:
        shape.update_shape()
        shape.calculate_bounding_box()
        print shape.name, shape.bounding_box
    print ""

    ### Add scene information to shapes

    minCorner = []
    maxCorner = []

    for i in range(3):
        axevertices = [vertex[i] for shape in shapes for vertex in shape.bounding_box]
        minCorner.append(min(axevertices))
        maxCorner.append(max(axevertices))

    scene_bounding_box = [minCorner, maxCorner]

    for shape in shapes:
        shape.scene_bounding_box = scene_bounding_box

    ### Relationships computation

    #compute_without_opposites(shapes, directional_tree, other_relationships_tree, table)
    compute_everything(shapes, directional_tree, other_relationships_tree, table)

    table.shapes = list(shapes)

    for shape in shapes:
        for relation in dir_relations_supported:
            table.find_relevant(shape, relation)
        table.distance_find_relevant(shape,"isFarFrom")
        table.distance_find_relevant(shape,"isCloseTo")
        table.complete_relevant(shape)

    print len(table.relationships)
    print "Calculated", len(table.relevant), "relevant relationships."

    table.fill_vectors()
    
    for v in table.vectors:
        print v

    ### Interface
    command = "None"
    while command != "exit":
        print "\nObjects in the scene: "
        for shape in shapes:
            print shape.name
        command = raw_input('\nPossible queries (optional arguments between square brackets): \n"list [<name1>] [<relationship>] [<name2>]"\n"exit"\n"relevant"\n')
        print ""
        interpret_commands(command, table)

def main_multi(files):
    """ Is executed if the user wants to analyze many scenes at once and compare them """
    ### Initialization
    directional_tree = templates.make_directional()
    other_relationships_tree = templates.make_other_relationships()
    tables = []

    for file in files:
        tables.append(database.RelationshipsTable())
        table = tables[-1]
        ### Parsing
        shapes = x3dparser.parse_file(file)
        x3dparser.parse_child_nodes(shapes)

        ### Geometric representation
        for shape in shapes:
            shape.update_shape()
            shape.calculate_bounding_box()
            #print shape.name, shape.type, shape.location, shape.bounding_box
        print ""

        ### Relationships computation
        compute_without_opposites(shapes, directional_tree, other_relationships_tree, table)

        list_relationships(table, [0,"target","reference"], 4)

    #designfrequency.visualize(tables)

if multi_scenes:
    main_multi(files)
else:
    main(singlefile)


