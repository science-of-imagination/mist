'''
Reports the frequency of relationships across a set of scenes

Created on 2012-03-29

@authors:
Sebastien Ouellet sebouel@gmail.com
'''
import random
from matplotlib import pyplot

def visualize(tables):
    """ Outputs a bar chart of the most common relationships """
    number = 15
    
    relationships = dict()
    for table in tables:
        within_same_scene = dict()
        for relationship in table.relationships:
            if relationship not in within_same_scene:
                if relationship not in relationships:
                    relationships[relationship] = 1
                else:
                    relationships[relationship] += 1
                within_same_scene[relationship] = 1
    
    relationships_list = sorted(relationships.items(), key=lambda x: x[1], reverse=True)
    
    for i in xrange(number):
        triple = relationships_list[i][0]
        print str(i+1)+": "+triple[0]+" "+triple[1]+" "+triple[2]
    
    left = [i*2 for i in xrange(number)]
    height = [relationships_list[i][1] for i in xrange(number)]
    pyplot.bar(left, height)
    pyplot.ylabel('Frequency')
    pyplot.title('Frequency of spatial relationships')
    pyplot.xticks([label+0.4 for label in left], [str(x) for x in xrange(1,number+1)] )

    pyplot.show()

