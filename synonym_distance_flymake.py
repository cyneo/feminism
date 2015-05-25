#! /usr/local/python-3.4.1/bin/python3

"""
Code to calculate distance between all nodes 
"""

from std_pack import *


def synonym_distance():
    graph = nx.read_graphml(thesaurus_path + 'Thesaurus Graph.graphml')
    """
    If neither the source nor target are specified
    return a dictionary of dictionaries with path[source][target]=L,
    where L is the length of the shortest path from source to target.
    """
    nx_calc = nx.shortest_path_length(graph)
    for start in nx_calc.keys():
        pass

    words = []

    with open(thesaurus_path + 'Word List.txt', 'a') as file:
        for word in file:
            words.append(word[:-1])

    df = pd.DataFrame(np.zeros((len(words), len(words))),
                      index='words', columns='words')
    
# this will extract individual distances
for start in a.keys():
    for end in a[start].keys():
        print(a[start][end])

# i need to find a way to extract this into a dataframe or ndarray
# Focus on the big picture. Write the skeleton for server
# and then refine things as you go along.
