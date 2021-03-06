#! /usr/local/python-3.4.1/bin/python3.4

from std_pack import *
import igraph

"""
Characterizing graphs using igraph
Tries to import graphml created using igraph
Abandoned due to compatibility causing more issues than it solves
"""


graph = igraph.Graph()
graph = graph.Read_GraphML(thesaurus_path + 'Thesaurus Graph.graphml')
names = graph.vs["id"]
graph.vs['name'] = names

with open(thesaurus_path + 'Word List.txt', 'r') as file:
    list = [x for x in file]
    miniList = list[:400]
    del(list)

miniList = [x[:-1] for x in miniList]
miniGraph = igraph.Graph()
miniGraph.add_vertices(miniList)
miniGraph.vs['id'] = miniList  # This is so that nx can identify as well

# Returns list of list of same group words more of a verification method
# Generating the names of neighbors
neighbors = [(word, graph.neighbors(word)) for word in miniList]  # List of list of word
for (source, list) in neighbors:
    for sink in list:
        sink_name = graph.vs[sink]['name']
        # print(source, sink_name)
        try:
            # Determine if the sink is in graph
            miniGraph.add_edge(source, sink_name)

        # Not the best to call exception like this due to limited knowledge
        # on the errors that can occur
        except:
            # Adding vertex
            miniGraph.add_vertex(sink_name)
            miniGraph.vs.find(sink_name)['id'] = sink_name
            # Adding edges
            miniGraph.add_edge(miniGraph.vs.find(source),
                               miniGraph.vs.find(sink_name))

# Visualizing the graph in networkx:
# Save the igraph, then open the graph in networkx
def plotndraw(filename, root=thesaurus_path):
    graph = nx.read_graphml(root + filename)
    nx.draw_networkx(graph)
    plt.show()


# Pull names out
# x = [[graph.vs[x]['name'] for x in list] for list in graph.neighborhood(graph.vs[:10])]

"""
I have to take care of cross graph referencing. Using names
is a good way to do this.
"""

"""
there is some issue with the imported graphml created from nx
2 ways:
1:
generate the main graph using igraph

2:
Figure out how to add attributes to the igraph

1 might be faster than 2? Currently working on 2
"""


"""
for word in miniList:
    neighbors = graph.neighbors(word)
    for end in neighbors:
        miniGraph.add_edge(word, end)

nx.draw_networkx(miniGraph)
plt.show()
"""

"""
There is an error that says that one of the words in the
miniList is not in the graph. That means that there is a word that is
in the Done Words file that is not in the file.

Maybe look into how the data is scrapped and put all the code into the
same file.
"""

'''
"""
Finding the degree distribution of the graph.
Will be useful to take a look when doing the null model.
"""

degrees = list(nx.degree(graph).values())
a = np.histogram(degrees, bins=range(min(degrees), max(degrees) + 1, 1))

fig = plt.figure()
ax = fig.add_subplot(111)

ax.hist(degrees, bins=range(min(degrees), max(degrees) + 1, 1))
plt.title('Degree Distribution Words and First Synomym')
plt.savefig(thesaurus_path + 'Degree Dist.png')
plt.show()
'''
