"""
FUn code to try and replicate the small world that Watts and Strogatz did
"""
from std_pack import *
from random import random
from random import randint


def somefun(no_of_runs=20):
    run = 1
    while run < no_of_runs:

        rand_links(create_graph(), p)
        run += 1
        pass

    
# Create graph
def create_graph(n=1000, k=5):
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    for start in range(n):
        for end in range(k):
            graph.add_edge(start, (start + end + 1) % 1000)
    return(graph)


# Randomize links
def rand_links(graph, p):
    n = 0
    edge_list = graph.edges()
    # can create an instance of graph.edges and then change the actual
    # graph without changing the list
    while n < len(edge_list):
        if random() < p:
            graph.remove_edge(edge_list[n][0], edge_list[n][1])
            graph.add_edge(edge_list[n][0], randint(0, 999))
        n += 1
    return graph


# Characterize graph
def characterize(graph):
    lengths = []
    clust_coeffs = []
    for node in graph.node.keys():
        clust_coeffs.append(graph.degree(node))
    return clust_coeffs
    cpl = None  # Charateristic path length
    cc = None  # Clustering coefficient

# Collect data

# Plot data
