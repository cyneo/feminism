# Chu Liu Edmond's Algorithm Attempt 1
"""
Chu Liu Edmond's Algorithm is an algorithm performs a depth-first-search (DFS)
for directed graph. This is different from Prim's algorithm.

This was done as the approach at that time is to form a directed graph of all
the words, and see if there are hubs.

USAGE:
Call chuliu(filename)

Input:
csv file with edges and frequencies of each node

Output:
A directed graph (should be a graphml)

Nov 2014:
Phased out as that is no longer the approach that the project is taking.
"""

import csv
import networkx as nx
import matplotlib as plt


def chuliu(filename):
    with open(filename[:-4]+' freqdist.csv', 'r', encoding = 'utf8') as freqdistfile:
        freqdist_reader = csv.reader(freqdistfile, delimiter = '\t',
                               quoting = csv.QUOTE_MINIMAL)
        G = nx.DiGraph() # Initializes a directed graph
    with open (filename[:-4]+' freqdist.csv', 'r', encoding = 'utf8') as freqdist_file:
        freqdist_reader = csv.reader(freqdist_file, delimiter = '\t',
                                     quoting = csv.QUOTE_MINIMAL)
        
        for row in freqdist_reader:
            G.add_edge(row[0], row[1], weight=int(row[2]))
    return G

    
    
    
