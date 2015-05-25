"""
Phased out due to:
the change in direction of in the project
Chu Liu
"""
"""
A primative dfs method that should be burned out of existence
"""
import networkx as nx
import matplotlib.pyplot as plt


def dfs(graph):
    for node in graph.node:
        graph.node[node]['visited'] = 'undiscovered'

    path = nx.DiGraph()

    for node in graph.node:
        print('Currently at ' + str(node))
        if graph.node[node]['visited'] == 'undiscovered':
            dfsvisit(graph, node, path)
        else:
            print('But ' + str(node) + ' is already discovered')
    return path


def dfsvisit(graph, node, path):
    graph.node[node]['visited'] = 'discovered'
    print('Discovered ' + str(node))
    for successor in graph.successors(node):
        print('I am going to visit ' + str(successor) + ' next')
        if graph.node[successor]['visited'] == 'undiscovered':
            print('I have visited ' + str(successor))
            graph.node[successor]['visited'] = 'discovered'
            dfsvisit(graph, successor, path)
        if graph.node[successor]['visited'] == 'final':
            path.add_edge(node, successor)
    graph.node[node]['visited'] = 'final'


def drawgraph(graph):
    nx.draw(graph)
    plt.show()
