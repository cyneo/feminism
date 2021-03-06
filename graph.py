"""
Have to run edge_weight before you can run graph
"""

import csv
import re
import networkx as nx
import matplotlib.pyplot as plt
import scipy
import numpy as np
import sys
import collections as coll
import os

# Importing NLTK
try:
    import nltk
except ImportError:
    sys.path.insert(0, '/mnt/sda2/nltk')
    import nltk

graph = nx.DiGraph()

with open(os.path.abspath('/home/cyneo/Work/Scans/Processed Data/Edge Weight/Girl 20 Edge Weight.csv'),
          'r', encoding='utf8') as file:
    file_reader = csv.reader(file, delimiter='\t',
                             quoting=csv.QUOTE_MINIMAL)

    for line in file_reader:
        graph.add_edge(line[0], line[1], weight=line[2])



with open(os.path.abspath('/home/cyneo/Work/Scans/Processed Data/Frequency Distribution/Girl 20 Frequency Distribution.csv'), 'r', encoding='utf8') as file:
    file_reader = csv.reader(file, delimiter='\t',
                             quoting=csv.QUOTE_MINIMAL)
    for line in file_reader:
        try:
            graph.node[line[0]]['Frequency'] = int(line[1])
        except KeyError:
            graph.add_node(line[0], Frequency=int(line[1]))
    nx.write_graphml(graph, os.path.abspath('/home/cyneo/Work/Scans/Processed Data/Girl 20 Word to Word.graphml'))


def runstuff():
    list1 = ["[Andrew O'Hagan] Be Near Me",
             "[Andrew O'Hagan] Our Fathers",
             "[David Lodge] Paradise News",
             'Girl 20']

    for item in list1:
        process_text(item)
        freqdist(item)
        update_in_out1(item)


def create_graph(filename):
    edge_weight(filename)
    with open(filepath(filename, 'Edge Weight'), 'r',
              encoding='utf8') as edge_weight_file:
        edge_weight_reader = csv.reader(edge_weight_file, delimiter='\t',
                                        quoting=csv.QUOTE_MINIMAL)

        full_graph = nx.DiGraph()

        for start, end, weight in edge_weight_reader:
            full_graph.add_edge(start, end, weight=int(weight))

    return full_graph

"""
everything below the line is current code. please remember to update
----
"""


def update_degrees1():
    # Create a folder with all the words in there
    # each file will have frequency and degrees
    # each line will be the new cumulative frequency and degrees
    list_of_files = os.listdir(
        '/home/cyneo/Work/Scans/Processed Data/Word Dictionary')
    list_of_words = set()
    for file in list_of_files:
        list_of_words.add(file.split()[0])

    # for every word in the freq dist
    # find the file
    # count lines
    # append to hubness
    

def plothub1():
    """
    this function is to plot the complied data
    Need a new function because of how the data is organized
    """
    pass


def update_freq_dist(filename):
    """
    Adds file into the exisiting compiled freq dist
    should input an existing freq dist file
    """
    pass


def update_in_out(filename):
    with open(filepath(filename, 'Edges'), 'r',
              encoding='utf8') as edge_file:
        edge_reader = csv.reader(edge_file, delimiter='\t',
                                 quoting=csv.QUOTE_MINIMAL)
        for predecessor, successor in edge_reader:
            chk_append_in_out(successor, predecessor, 'Predecessors')
            chk_append_in_out(predecessor, successor, 'Successors')


def chk_append_in_out(target_word, word_to_add, data):
    """
    this function opens the target word and checks if the word
    to be added is already in there.
    If it isn't, the word will get added in
    """
    # insert syntax to write to temp file
    import shutil

    filename = filepath1(data)
    dict_tmpfile = filepath1(data + ' tmp')

    with open(filename, 'r',
              encoding='utf8') as dict_file:
        dict_reader = csv.reader(dict_file, delimiter='\t',
                                 quoting=csv.QUOTE_MINIMAL)
        data = [l for l in dict_reader]

        for line in data:
            if type(line) == list and len(line) > 1:
                for word in line[1:]:
                    if word == word_to_add:
                        break

                    else:
                        line.append(word_to_add)
            else:
                line.extend(target_word, word_to_add)
 
    with open(dict_tmpfile, 'w', encoding='utf8') as dict_tmpfile:
        dict_writer = csv.writer(dict_tmpfile, delimiter='\t',
                                 quoting=csv.QUOTE_MINIMAL)
        for line in data:
            dict_writer.writerow(line)

    shutil.move(dict_tmpfile, filename)


def hubness(filename):
    with open(filepath(filename, 'Frequency Distribution'), 'r',
              encoding='utf8') as freq_dist_file:
        freq_dist_reader = csv.reader(freq_dist_file, delimiter='\t',
                                      quoting=csv.QUOTE_MINIMAL)

        full_graph = create_graph(filename)

        with open(filepath(filename, 'Hubness'),
                  'w', encoding='utf8') as hub_file:
            hub_writer = csv.writer(hub_file, delimiter='\t',
                                    quoting=csv.QUOTE_MINIMAL)
            for [node, freq] in freq_dist_reader:
                full_graph.add_node(node)
                out_hubness = full_graph.out_degree(node) / int(freq)
                in_hubness = full_graph.in_degree(node) / int(freq)
                hub_writer.writerow([node] + [freq] +
                                    [out_hubness] + [in_hubness])


def update_in_out1(filename):
    """
    Method used here is to write a file for all the targets
    The file will contain all the Predecessors and Successors,
    including repeats (chk_append_in_out1)
    The next step is to open evey word file,
    enter the entire file into working memory
    do a set, and then write the file.
    Prefer to do the read/write with temp to prevent errors
    """
    import shutil

    with open(filepath(filename, 'Edges'), 'r',
              encoding='utf8') as edge_file:
        edge_reader = csv.reader(edge_file, delimiter='\t',
                                 quoting=csv.QUOTE_MINIMAL)

        # edges = [l for l in edge_reader] #  List of lists
        
        for predecessor, successor in edge_reader:
            chk_append_in_out1(successor, predecessor, 'Predecessors')
            chk_append_in_out1(predecessor, successor, 'Successors')

    listtocheck = os.listdir(os.path.abspath(
        '/home/cyneo/Work/Scans/Processed Data/Word Dictionary/')
        )

    for item in listtocheck:
        filename = os.path.abspath(
            '/home/cyneo/Work/Scans/Processed Data/Word Dictionary/' + item)
        tempfile = os.path.abspath(
            '/home/cyneo/Work/Scans/Processed Data/Word Dictionary/'
            + 'tmp ' + item)

        with open(filename, 'r', encoding='utf8') as word_file:
            file_reader = csv.reader(word_file, delimiter='\t',
                                     quoting=csv.QUOTE_MINIMAL)
            list_of_things = [thing[0] for thing in file_reader]
            set_of_things = set(list_of_things)
            
        with open(tempfile, 'w', encoding='utf8') as temp_file:
            temp_writer = csv.writer(temp_file, delimiter='\t',
                                     quoting=csv.QUOTE_MINIMAL)
            for item in set_of_things:
                temp_writer.writerow([item])
        
        shutil.move(tempfile, filename)


def chk_append_in_out1(target_word, word_to_add, data):
    with open(filepath2(target_word, data),
              'a', encoding='utf8') as dict_file:
        dict_writer = csv.writer(dict_file, delimiter='\t',
                                 quoting=csv.QUOTE_MINIMAL)
        dict_writer.writerow([word_to_add])


def plothub(filename):
    """
    Use this to quickly plot the hubness of a text, after running hubness
    Arguments:
    - `filename`: Name of file to plot
    """
    with open(filepath(filename, 'Hubness'),
              'r', encoding='utf8') as hubness_file:
        hub_reader = csv.reader(hubness_file, delimiter='\t',
                                quoting=csv.QUOTE_MINIMAL)
        data = []
        frequency = []
        out_hubness = []
        in_hubness = []

        # Plotting the scatter
        fig = plt.figure()
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        for word, freq, outhubness, inhubness in hub_reader:
            frequency.append(freq)
            out_hubness.append(outhubness)
            in_hubness.append(inhubness)
            
        ax1.scatter(frequency, out_hubness)
        ax2.scatter(frequency, in_hubness)
        ax1.set_xlim(-5, 2500)
        ax1.set_ylim(-0.05, 2.05)
        ax2.set_xlim(-5, 2500)
        ax2.set_ylim(-0.05, 2.05)
        ax1.set_title('Out Hubness')
        ax2.set_title('In Hubness')
        plt.show()


def interestrange(filename, xlower, xupper, ylower, yupper):
    with open(filepath(filename, 'Hubness'),
              'r', encoding='utf8') as hubness_file:
        hub_reader = csv.reader(hubness_file, delimiter='\t',
                                quoting=csv.QUOTE_MINIMAL)
        outeresting = []
        interesting = []

        for word, freq, outhubness, inhubness in hub_reader:
            if float(freq) <= xupper and float(freq) >= xlower:
                if float(inhubness) <= yupper and float(inhubness) >= ylower:
                    interesting.append([word, freq, inhubness])
                if float(outhubness) <= yupper and float(outhubness) >= ylower:
                    outeresting.append([word, freq, outhubness])

        with open(filepath(filename, 'Interesting'),
                  'w', encoding='utf8') as interesting_file:
            interesting_writer = csv.writer(interesting_file, delimiter='\t',
                                            quoting=csv.QUOTE_MINIMAL)
            for word, freq, inhubness in interesting:
                interesting_writer.writerow([word] + [freq] + [inhubness])

        with open(filepath(filename, 'Outeresting'),
                  'w', encoding='utf8') as outeresting_file:
            outeresting_writer = csv.writer(outeresting_file, delimiter='\t',
                                            quoting=csv.QUOTE_MINIMAL)
            for word, freq, outhubness in outeresting:
                outeresting_writer.writerow([word] + [freq] + [outhubness])

"""
Everything here is a dependency for the stuff above
________________________________________________

"""


def dfs(graph):
    for node in graph.node:
        graph.node[node]['visited'] = 'undiscovered'

    path = nx.DiGraph()

    for node in graph.node:
        # print('Currently at ' + str(node))
        if graph.node[node]['visited'] == 'undiscovered':
            dfsvisit(graph, node, path)
        # else:
            # print('But ' + str(node) + ' is already discovered')
    return path


def dfsvisit(graph, node, path):
    graph.node[node]['visited'] = 'discovered'
    # print('Discovered ' + str(node))
    for successor in graph.successors(node):
        # print('I am going to visit ' + str(successor) + ' next')
        if graph.node[successor]['visited'] == 'undiscovered':
            # print('I have visited ' + str(successor))
            graph.node[successor]['visited'] = 'discovered'
            dfsvisit(graph, successor, path)
        if graph.node[successor]['visited'] == 'final':
            path.add_edge(node, successor)
    graph.node[node]['visited'] = 'final'


def drawgraph(graph):
    nx.draw(graph)
    plt.show()


def edge_weight(filename):
    with open(filepath(filename, 'Edge Weight'), 'w',
              encoding='utf8') as edge_weight_file:
        edge_weight_writer = csv.writer(edge_weight_file, delimiter='\t',
                                        quoting=csv.QUOTE_MINIMAL)
        histo = []
        with open(filepath(filename, 'Edges'), 'r',
                  encoding='utf8') as edge_file:
            edge_reader = csv.reader(edge_file, delimiter='\t',
                                     quoting=csv.QUOTE_MINIMAL)
            for row in edge_reader:
                match = False
                n = 0
                while n < len(histo):
                    if row == histo[n][0]:
                        histo[n][1] += 1
                        match = True
                        break
                    n += 1
                if match is False:
                    histo.append([row, 1])
        
        for strength in sorted(histo, key=lambda histo:
                               histo[1], reverse=True):
            edge_weight_writer.writerow([strength[0][0]] +
                                        [strength[0][1]] +
                                        [str(strength[1])])

            # when you open the csv, you will see some really weird things.
            # Don't worry the data is fine


def freqdist(filename):
    cnt = coll.Counter()  # Returns a dict
    with open(filepath(filename, 'Lemmatized Text'), 'r',
              encoding='utf8') as lemma_file:
        lemma_reader = csv.reader(lemma_file, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)

        for line in lemma_reader:
            for word in line:
                cnt[word] += 1

    with open(filepath(filename, 'Frequency Distribution'),
              'w', encoding='utf8') as freq_dist_file:
        freq_dist_writer = csv.writer(freq_dist_file, delimiter='\t',
                                      quoting=csv.QUOTE_MINIMAL)
        for key in cnt.keys():
            freq_dist_writer.writerow([key]+[cnt[key]])


def filepath(filename, data, root='/home/cyneo/Work/Scans/Processed Data/',
             filetype='.csv'):
    """
    A function that helps call absolute path for a document

    Input:
    Output:

    """
    path = os.path.abspath(root + data + '/' + filename +
                           ' ' + data + filetype)
    return path


def filepath1(
        data,
        root='/home/cyneo/Work/Scans/Processed Data/',
        filetype='.csv'):
    path = os.path.abspath(root + data + filetype)
    
    return path


def filepath2(
        word, data,
        root='/home/cyneo/Work/Scans/Processed Data/Word Dictionary/',
        filetype='.csv'):
    path = os.path.abspath(root + word + ' ' + data + filetype)
    
    return path

"""
Unused at the moment, and possibly obselete
_________________________________________________

"""

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%% START %%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

Algorithmn that is supposed to create a MST for the data.

Curent status:
This code has been put on hold as MST does not seem to give
a lot of useful information for determining the keywords
"""


def initial_graph(filename, full_graph):
    fan_out = nx.DiGraph()
    # holds all the edges of highest incoming strength
    fan_in = nx.DiGraph()
    # holds all the edges of highest outcoming strength

    # root = full_graph.edges()[-1:][0][0]
    # first edge added seems to be the last value in the .edges()
    for end_node in full_graph.node:
        # written as end_node because we want to go through every node
        # and look for incoming nodes of the highest strength
        current_max = 0  # stores the highest strength
        max_node = None  # stores the node with the highest strength
        for start_node in full_graph.predecessors(end_node):
            # predecessors pulls out all the incoming nodes
            if full_graph[start_node][end_node]['weight'] > current_max:
                current_max = full_graph[start_node][end_node]['weight']
                max_node = start_node
        fan_out.add_edge(max_node, end_node)  # Appends edge to nx

    for start_node in full_graph.node:
        # written as start_node because we want to go through every node
        # and look for outgoing nodes of the highest strength
        current_max = 0  # stores the highest strength
        max_node = None  # stores the node with the highest strength
        for end_node in full_graph.successors(start_node):
            # successors pulls out all the outgoing nodes
            if full_graph[start_node][end_node]['weight'] > current_max:
                current_max = full_graph[start_node][end_node]['weight']
                max_node = end_node
        fan_in.add_edge(start_node, max_node)  # Appends edge to fan_in
    nx.write_graphml(fan_out,
                     filename + " fan out.graphml")
    nx.write_graphml(fan_in, filename + " fan in.graphml")

    dfsfanout = dfs(fan_out)
    dfsfanin = dfs(fan_in)

    nx.write_graphml(dfsfanout, filename + ' dfsfanout.graphml')
    nx.write_graphml(dfsfanin, filename + ' dfsfanin.graphml')

    return dfsfanout, dfsfanin

    # To define a visited attribute, use graph.node[node]['visited'] = value
    # To call the visited attribute, use graph.node[node]['visited']
    # nx.full_graph.predecessors(node) will give the node that it is entering from
    # call weight by using full_graph[start][end]['weight']


def dfs_forests(filename):
    full_graph = create_graph(filename)
    fanout, fanin = initial_graph(filename, full_graph)
    dfsout = dfs(fanout)
    dfsin = dfs(fanin)
    out_deg = []
    in_deg = []
    for node in dfsout.nodes():
        out_deg.append((node, dfsout.out_degree(node)))

    for node in dfsin.nodes():
        in_deg.append((node, dfsin.in_degree(node)))

    out_deg = sorted(out_deg, key=lambda node: node[1], reverse=True)
    in_deg = sorted(in_deg, key=lambda node: node[1], reverse=True)

    with open(filepath(filename, 'Out Degree'), 'w',
              encoding='utf8') as out_deg_file:
            out_deg_writer = csv.writer(out_deg_file, delimiter='\t',
                                        quoting=csv.QUOTE_MINIMAL)
            for node in out_deg:
                out_deg_writer.writerow([node[0]] +
                                        [node[1]])

    with open(filepath(filename, 'In Degree'), 'w',
              encoding='utf8') as in_deg_file:
            in_deg_writer = csv.writer(in_deg_file, delimiter='\t',
                                       quoting=csv.QUOTE_MINIMAL)
            for node in in_deg:
                in_deg_writer.writerow([node[0]] +
                                       [node[1]])

    nx.write_graphml(dfsout, filename + ' forest out.graphml')
    nx.write_graphml(dfsin, filename + ' forest in.graphml')

"""
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

"""
