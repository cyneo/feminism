#! /usr/local/python-3.4.1/bin/python3.4

from std_pack import *

graph = nx.read_graphml(thesaurus_path + 'Thesaurus Graph.graphml')

with open(thesaurus_path + 'Word List.txt', 'r') as file:
    list = [x[:-1] for x in file]
    miniList = list[:100]
    del(list)

miniGraph = nx.Graph()

# Generating the names of neighbors
for source in miniList:
    for sink in graph.neighbors(source):
        miniGraph.add_edge(source, sink)

nx.write_graphml(miniGraph, data_path + 'mini graph.graphml')

# Creates connected subgraphs
# List format should be removed when the graph
# List of graphs created
connected_subs = list(nx.connected_componet_subgraphs(miniGraph))
n = 0

for graph in connected_subs:
    nx.draw_networkx(graph)
    plt.savefig(str(n) + '.png', bbox_inches='tight')
    plt.clf()
    n += 1


def girvan_newman(G):
    # This was copied directly from the web. Could be older version of nx
    # This code only cuts big clusters into 2 smaller ones.
    """
    Algo does:
    Splitting based on edge betweeness

    Algo lacks:
    Modularity measures
    """
    if len(G.nodes()) == 1:
        return [G.nodes()]

    def find_best_edge(G0):  # G0 is naming to prevent confusion with G
        """
        Networkx implementation of edge_betweenness
        returns a dictionary. Make this into a list,
        sort it and return the edge with highest betweenness.
        """
        eb = nx.edge_betweenness_centrality(G0)
        # eb_il = eb.items()
        return max(eb, key=eb.get)

    components = nx.connected_component_subgraphs(G)
    
    if sum(1 for _ in components) == 1:
        # This means that only splits into 2 graphs
        print('proc')
        G.remove_edge(*find_best_edge(G))
        components = nx.connected_component_subgraphs(G)

    result = [c.nodes() for c in components]

    for c in components:
        result.extend(girvan_newman(c))

    return result

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
