"""
Phased out due to:
0: Amount of noise that it produced.

Replaced by:
Parse methods that look at how the words are used in the same sentence
to identify if the (fe)male term is the subject of the adjective
"""
"""
This code should try and look for sentences that have a male or female subject
and then look out for adjectives in the same sentence
Then extract those sentences and make a graph out of it.

USAGE:
Run the function run_adj(filename)
Can edit the methods that are called by (un)commenting methods

Input:
Raw file in txt format

Output Files:

Undirected graphml files.
Suffix: (Fe)Male Adj Extract X

WARNING!: The text here are not lemmatized

There are 3 methods that were employed to extract the adjectives.
0: Links the first adjective that follows a (fe)male term.
1: Links adjectives that are in the same sentence as a (fe)male
   term, and not other (fe)male terms in the same sentence
2: Links all (fe)male terms in a sentence to all the adjectives in
   the same sentence.
"""
import csv
import sys
import re
import os.path as osp
import os
import networkx as nx
from collections import *
import matplotlib
import matplotlib.pyplot as plt

# Importing NLTK
try:
    import nltk
except ImportError:
    sys.path.insert(0, '/mnt/sda2/nltk')
    import nltk


def run_all():
    list_to_run = ["[David Lodge] A Man of Parts",
                   "[David Lodge] Author. Author",
                   "[David Lodge] Changing Places",
                   "[David Lodge] Deaf Sentence",
                   "[David Lodge] How Far Can You Go",
                   "[David Lodge] Nice Work",
                   "[David Lodge] Paradise News",
                   "[David Lodge] The British Museum is Falling Down",
                   "[David Lodge] Therapy",
                   "[David Lodge] Think",
                   "[Graham Green] A Burnt-Out Case",
                   "[Graham Green] A Sort of Life",
                   "[Graham Green] England Made Me",
                   "[Graham Green] Monsignor Quixote",
                   "[Graham Green] Our Man in Havana",
                   "[Graham Green] Stamboul Train",
                   "[Graham Green] The Comedians",
                   "[Graham Green] The End of an Affair",
                   "[Graham Green] The Heart of the Matter",
                   "[Graham Green] The Human Factor",
                   "[Graham Green] THe Ministry of Fear",
                   "[Graham Green] The Power and Glory"]

    for item in list_to_run:
        # adj_extract0(item) recursion limit hit for a lot of the texts
        adj_extract1(item)
        adj_extract2(item)


def run_books():
    book_list = ["[David Lodge] A Man of Parts",
                 "[David Lodge] Author. Author",
                 "[David Lodge] Changing Places",
                 "[David Lodge] Deaf Sentence",
                 "[David Lodge] How Far Can You Go",
                 "[David Lodge] Nice Work",
                 "[David Lodge] Paradise News",
                 "[David Lodge] The British Museum is Falling Down",
                 "[David Lodge] Therapy",
                 "[David Lodge] Think",
                 "[Graham Green] A Burnt-Out Case",
                 "[Graham Green] A Sort of Life",
                 "[Graham Green] England Made Me",
                 "[Graham Green] Monsignor Quixote",
                 "[Graham Green] Our Man in Havana",
                 "[Graham Green] Stamboul Train",
                 "[Graham Green] The Comedians",
                 "[Graham Green] The End of an Affair",
                 "[Graham Green] The Heart of the Matter",
                 "[Graham Green] The Human Factor",
                 "[Graham Green] THe Ministry of Fear",
                 "[Graham Green] The Power and Glory"
             ]

    for book in book_list:
        run_adj(book)


def run_adj(filename):
    posSents = postext_st(filename)
    # adj_extract0(posSents, filename, creategraph='y')
    adj_extract1(posSents, filename, creategraph='y')
    adj_extract2(posSents, filename, creategraph='y')


def adj_extract0(posSents, filename, creategraph='y'):
    """
    Type 0:
    Returns (fe)male term and the adjective that follows

    Make use of recursive
    """
    # Initializing lists
    # posSents = postext_st(filename)
    maleterms = ['he', 'him', 'his', 'himself', 'man']
    femaleterms = ['she', 'her', 'hers', 'herself', 'woman', 'lady']
    malepair = []
    femalepair = []
    # male_adj = []
    # female_adj = []
    # male_adj_compiler = Counter()
    # female_adj_compiler = Counter()

    # Calls the recursive relations
    for line in range(len(posSents)):
        """
        The temp pairs are created so that it is possible to extract the
        link between the adj of a sentence
        """
        tempmalepair = []
        tempfemalepair = []

        # The tuples generated by the recursion is to get the relation between
        # the male terms and adj
        checkbyfrag(posSents[line], maleterms, tempmalepair)
        checkbyfrag(posSents[line], femaleterms, tempfemalepair)
        # Extend the 'dictionary' of adjs attached to the term
        # Because appending will append lists of tuples instead of extending
        # the tuples list
        malepair.extend(tempmalepair)
        femalepair.extend(tempfemalepair)

        """
        # Links adj in the same sentence
        if len(tempmalepair) > 1:
            for n in range(len(tempmalepair)):
                male_adj_compiler[tempmalepair[n][1]] += len(tempmalepair)-1
                for m in tempmalepair[n+1:]:
                    male_adj.append((tempmalepair[n][1], m[1]))

        if len(tempfemalepair) > 1:
            for n in range(len(tempfemalepair)):
                female_adj_compiler[tempfemalepair[n][1]]\
                    += len(tempfemalepair)-1
                for m in tempfemalepair[n+1:]:
                    female_adj.append((tempfemalepair[n][1], m[1]))
        """

    # Create all the graphs

    # Graphs of relation between (fe)male terms and adj
    male_graph = create_graph(malepair)
    female_graph = create_graph(femalepair)

    """
    # Graphs that relate adj within the same sentence
    male_adj_graph = create_graph(male_adj)
    female_adj_graph = create_graph(female_adj)
    """

    # Modifying frequencies as the nature of the create graph function
    # miscounts the (fe)male terms
    """
    for node in male_adj_graph.nodes():
        male_adj_graph.node[node]['frequency'] = male_adj_compiler[node]

    for node in female_adj_graph.nodes():
        female_adj_graph.node[node]['frequency'] = female_adj_compiler[node]
    """

    # Saving modified graphs
    nx.write_graphml(male_graph,
                     filepath(filename, 'Male Adj Extract 0',
                              filetype='.graphml'))
    nx.write_graphml(female_graph,
                     filepath(filename, 'Female Adj Extract 0',
                              filetype='.graphml'))

    """
    nx.write_graphml(male_adj_graph, filepath(filename,
                     'Male Adj to Adj 0', filetype='.graphml'))

    nx.write_graphml(female_adj_graph, filepath(filename,
                     'Female Adj to Adj 0', filetype='.graphml'))
    """

    # this section modifies the graphs to get the various
    # intercepts and exclusions
    male_adj_set = set(male_graph.nodes())
    female_adj_set = set(female_graph.nodes())

    male_only_adj = male_adj_set - female_adj_set
    female_only_adj = female_adj_set - male_adj_set
    male_and_female_adj = male_adj_set & female_adj_set
    
    for node in male_and_female_adj:
        male_graph.remove_node(node)
        female_graph.remove_node(node)
        # male_adj_graph.remove_node(node)
        # female_adj_graph.remove_node(node)

    nx.write_graphml(male_graph, filepath(filename,
                     'Male Only Extract 0', filetype='.graphml'))

    nx.write_graphml(female_graph, filepath(filename,
                     'Female Only Extract 0', filetype='.graphml'))

    """
    nx.write_graphml(male_adj_graph, filepath(filename,
                     'Male Only Adj to Adj 0', filetype='.graphml'))

    nx.write_graphml(female_adj_graph, filepath(filename,
                     'Female Only Adj to Adj 0', filetype='.graphml'))
    """

    # Create files to write the pairs
    with open(filepath(filename, 'Male Adj Extract 0'),
              'w', encoding='utf8') as adj0_mfile:
        adj0_mwriter = csv.writer(adj0_mfile, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        for pair in malepair:
            adj0_mwriter.writerow([pair[0]] + [pair[1]])

    with open(filepath(filename, 'Female Adj Extract 0'),
              'w', encoding='utf8') as adj0_ffile:
        adj0_fwriter = csv.writer(adj0_ffile, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        for pair in femalepair:
            adj0_fwriter.writerow([pair[0]] + [pair[1]])


def checkbyfrag(linefragment, terms, pair):
    """
    checkbyfrag returns a list of tuples
    the list that is returned is the list that was fed into the function
    """
    for word in range(len(linefragment)):
        if linefragment[word][0] in terms:
            new_fragment = linefragment[word:]
            for word1 in range(len(new_fragment)):
                if new_fragment[word1][1] in ['JJ', 'JJR', 'JJS']:
                    pair.append((linefragment[word][0], new_fragment[word1][0]))
                    refragment = new_fragment[word1:]
                    checkbyfrag(refragment, terms, pair)
                    break
            break


def adj_extract1(posSents, filename, creategraph='y'):
    """
    Type 1:
    Returns (fe)male term and all the adj in the same sentence
    without searching for other (fe)male terms in the sentence
    """
    # posSents = postext_st(filename)
    poslist = ['JJ', 'JJR', 'JJS']
    maleterms = ['he', 'him', 'his', 'himself', 'man']
    femaleterms = ['she', 'her', 'hers', 'herself', 'woman', 'lady']
    malepair = []
    femalepair = []
    male_adj = []
    female_adj = []
    # These two counters are to track the proper frequency
    # of the terms as the algo's nature causes extra counts of terms
    male_term_compiler = Counter()
    female_term_compiler = Counter()
    male_adj_compiler = Counter()
    female_adj_compiler = Counter()
 
    for line in range(len(posSents)):
        # Temp pairs are to track adj in a sentence
        tempmalepair = []
        tempfemalepair = []
        for word in range(len(posSents[line])):
            if posSents[line][word][0] in maleterms:
                male_term_compiler[posSents[line][word][0]] += 1
                for word1 in range(len(posSents[line])):
                    if posSents[line][word1][1] in poslist:
                        tempmalepair.append((posSents[line][word][0],
                                             posSents[line][word1][0]))
                break  # Break makes sure that only the first term is picked up

            elif posSents[line][word][0] in femaleterms:
                female_term_compiler[posSents[line][word][0]] += 1
                for word1 in range(len(posSents[line])):
                    if posSents[line][word1][1] in poslist:
                        tempfemalepair.append((posSents[line][word][0],
                                               posSents[line][word1][0]))
                break  # Break makes sure that only the first term is picked up

        # Logic to run only if more than 1 adj in sentence
        if len(tempmalepair) > 1:
            for n in range(len(tempmalepair)):
                male_adj_compiler[tempmalepair[n][1]] += len(tempmalepair)-1
                for m in tempmalepair[n+1:]:
                    male_adj.append((tempmalepair[n][1], m[1]))

        if len(tempfemalepair) > 1:
            for n in range(len(tempfemalepair)):
                female_adj_compiler[tempfemalepair[n][1]] += len(tempfemalepair)-1
                for m in tempfemalepair[n+1:]:
                    female_adj.append((tempfemalepair[n][1], m[1]))

        # Feeding everything back into the lists
        # Extend is used as append will append lists of tuples and not tuples
        malepair.extend(tempmalepair)
        femalepair.extend(tempfemalepair)

    # Creating the graphs

    # Graphs that link terms to adj
    male_graph = create_graph(malepair)
    female_graph = create_graph(femalepair)

    # Frequency adjustments for term frequency
    for term in maleterms:
        if male_graph.has_node(term):
            male_graph.node[term]['frequency'] = male_term_compiler[term]

    for term in femaleterms:
        if female_graph.has_node(term):
            female_graph.node[term]['frequency'] = female_term_compiler[term]

    # Graphs that link the adj within the same sentence
    male_adj_graph = create_graph(male_adj)
    female_adj_graph = create_graph(female_adj)

    # Frequency adjustment for adj
    for node in male_adj_graph.nodes():
        try:
            male_adj_graph.node[node]['frequency'] = male_adj_compiler[node]
        except KeyError:
                male_adj_graph.add_node(
                    node, frequency=male_graph.node[node]['frequency'])

    for node in female_adj_graph.nodes():
        try:
            female_adj_graph.node[node]['frequency'] = female_adj_compiler[node]
        except KeyError:
                female_adj_graph.add_node(
                    node, frequency=female_graph.node[node]['frequency'])

    # Writng the graphs
    
    # Extract files
    nx.write_graphml(male_graph,
                     filepath(filename, 'Male Adj Extract 1',
                              filetype='.graphml'))
    nx.write_graphml(female_graph,
                     filepath(filename, 'Female Adj Extract 1',
                              filetype='.graphml'))

    # Adj to Adj files
    nx.write_graphml(male_adj_graph, filepath(filename,
                     'Male Adj to Adj 1', filetype='.graphml'))
    nx.write_graphml(female_adj_graph, filepath(filename,
                     'Female Adj to Adj 1', filetype='.graphml'))

    # this section modifies the graphs to get the various
    # intercepts and exclusions
    male_adj_set = set(male_adj_compiler.keys())
    female_adj_set = set(female_adj_compiler.keys())

    male_only_adj = male_adj_set - female_adj_set
    female_only_adj = female_adj_set - male_adj_set
    male_and_female_adj = male_adj_set & female_adj_set
    
    for node in male_and_female_adj:
        male_graph.remove_node(node)
        female_graph.remove_node(node)
        male_adj_graph.remove_node(node)
        female_adj_graph.remove_node(node)

    nx.write_graphml(male_graph, filepath(filename,
                     'Male Only Extract 1', filetype='.graphml'))

    nx.write_graphml(female_graph, filepath(filename,
                     'Female Only Extract 1', filetype='.graphml'))

    nx.write_graphml(male_adj_graph, filepath(filename,
                     'Male Only Adj to Adj 1', filetype='.graphml'))

    nx.write_graphml(female_adj_graph, filepath(filename,
                     'Female Only Adj to Adj 1', filetype='.graphml'))


    # Create files to write the pairs
    with open(filepath(filename, 'Male Adj Extract 1'),
              'w', encoding='utf8') as adj1_mfile:
        adj1_mwriter = csv.writer(adj1_mfile, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        for pair in malepair:
            adj1_mwriter.writerow([pair[0]] + [pair[1]])

    with open(filepath(filename, 'Female Adj Extract 1'),
              'w', encoding='utf8') as adj1_ffile:
        adj1_fwriter = csv.writer(adj1_ffile, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        for pair in femalepair:
            adj1_fwriter.writerow([pair[0]] + [pair[1]])


def adj_extract2(posSents, filename, creategraph='y'):
    """
    Type 2
    Returns (fe)male terms and the adjs in the same sentence
    searchs for other (fe)male terms in the same sentence and links
    all terms to the same adjs
    """
    # Initializes Lists
    # posSents = postext_st(filename)
    poslist = ['JJ', 'JJR', 'JJS']
    maleterms = ['he', 'him', 'his', 'himself', 'man']
    femaleterms = ['she', 'her', 'hers', 'herself', 'woman', 'lady']
    malepair = []
    femalepair = []
    male_adj = []
    female_adj = []
    male_term_compiler = Counter()
    female_term_compiler = Counter()
    male_adj_compiler = Counter()
    female_adj_compiler = Counter()

    for line in range(len(posSents)):
        tempmaleterms = []
        tempfemaleterms = []
        tempadj = []
        for word in range(len(posSents[line])):
            if posSents[line][word][0] in maleterms:
                tempmaleterms.append(posSents[line][word][0])

            elif posSents[line][word][0] in femaleterms:
                tempfemaleterms.append(posSents[line][word][0])

            elif posSents[line][word][1] in poslist:
                tempadj.append(posSents[line][word][0])

        # do something to bind the pairs and send it to the top
        for term in tempmaleterms:
            male_term_compiler[term] += 1
            for adj in tempadj:
                malepair.append((term, adj))

        for term in tempfemaleterms:
            female_term_compiler[term] += 1
            for adj in tempadj:
                femalepair.append((term, adj))
        
        if tempmaleterms:
            for n in range(len(tempadj)):
                male_adj_compiler[tempadj[n]] += len(tempadj) - 1
                for m in tempadj[n+1:]:
                    male_adj.append((tempadj[n], m))

        if tempfemaleterms:
            for n in range(len(tempadj)):
                female_adj_compiler[tempadj[n]] += len(tempadj) - 1
                for m in tempadj[n+1:]:
                    female_adj.append((tempadj[n], m))

    # Creating the graphs

    # Graphs that link terms to adj
    male_graph = create_graph(malepair)
    female_graph = create_graph(femalepair)

    # Frequency adjustments for term frequency
    for term in maleterms:
        if male_graph.has_node(term):
            male_graph.node[term]['frequency'] = male_term_compiler[term]

    for term in femaleterms:
        if female_graph.has_node(term):
            female_graph.node[term]['frequency'] = female_term_compiler[term]

    # Graphs that link the adj within the same sentence
    male_adj_graph = create_graph(male_adj)
    female_adj_graph = create_graph(female_adj)

    # Frequency adjustment for adj
    for node in male_graph.nodes():
        if node not in maleterms:
            try:
                male_adj_graph.node[node]['frequency'] = male_adj_compiler[node]
            except KeyError:
                male_adj_graph.add_node(
                    node, frequency=male_graph.node[node]['frequency'])

    for node in female_graph.nodes():
        if node not in femaleterms:
            try:
                female_adj_graph.node[node]['frequency'] = female_adj_compiler[node]
            except KeyError:
                female_adj_graph.add_node(
                    node, frequency=female_graph.node[node]['frequency'])

    # Writng the graphs
    
    # Extract files
    nx.write_graphml(male_graph,
                     filepath(filename, 'Male Adj Extract 2',
                              filetype='.graphml'))
    nx.write_graphml(female_graph,
                     filepath(filename, 'Female Adj Extract 2',
                              filetype='.graphml'))

    # Adj to Adj files
    nx.write_graphml(male_adj_graph, filepath(filename,
                     'Male Adj to Adj 2', filetype='.graphml'))
    nx.write_graphml(female_adj_graph, filepath(filename,
                     'Female Adj to Adj 2', filetype='.graphml'))

    # Create files to write the pairs
    with open(filepath(filename, 'Male Adj Extract 2'),
              'w', encoding='utf8') as adj2_mfile:
        adj2_mwriter = csv.writer(adj2_mfile, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        for pair in malepair:
            adj2_mwriter.writerow([pair[0]] + [pair[1]])

    with open(filepath(filename, 'Female Adj Extract 2'),
              'w', encoding='utf8') as adj2_ffile:
        adj2_fwriter = csv.writer(adj2_ffile, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        for pair in femalepair:
            adj2_fwriter.writerow([pair[0]] + [pair[1]])

    # this section modifies the graphs to get the various
    # intercepts and exclusions
    male_adj_set = set(male_adj_compiler.keys())
    female_adj_set = set(female_adj_compiler.keys())

    male_only_adj = male_adj_set - female_adj_set
    female_only_adj = female_adj_set - male_adj_set
    male_and_female_adj = male_adj_set & female_adj_set

    for node in male_and_female_adj:
        male_graph.remove_node(node)
        female_graph.remove_node(node)
        male_adj_graph.remove_node(node)
        female_adj_graph.remove_node(node)

    nx.write_graphml(male_graph, filepath(filename,
                     'Male Only Extract 2', filetype='.graphml'))

    nx.write_graphml(female_graph, filepath(filename,
                     'Female Only Extract 2', filetype='.graphml'))

    nx.write_graphml(male_adj_graph, filepath(filename,
                     'Male Only Adj to Adj 2', filetype='.graphml'))

    nx.write_graphml(female_adj_graph, filepath(filename,
                     'Female Only Adj to Adj 2', filetype='.graphml'))


def create_graph(edges):
    """
    Creates a graph by feeding a list of edges into the function

    Output:
    Frequency of each node
    Weight of each edge
    """
    graph = nx.Graph()
    # Compiling the weights
    edge_compiler = Counter()
    source_compiler = Counter()
    target_compiler = Counter()
    for pair in edges:
        edge_compiler[pair] += 1
        source_compiler[pair[0]] += 1
        target_compiler[pair[1]] += 1

    # Adding weights to the graphs
    for source in source_compiler.keys():
        graph.add_node(source, frequency=source_compiler[source])

    for target in target_compiler.keys():
        graph.add_node(target, frequency=target_compiler[target])
    for edge in edge_compiler.keys():
        graph.add_edge(edge[0], edge[1], weight=edge_compiler[edge])

    return graph

def frequency_correction():
    pass


# Correction for text from nltk tokenizer
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%% START %%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

                        
# Create patterns to be corrected
correction_patterns = \
                      (
                          #  ("/", "/", ''),
                          ("^ ", " ", ''),
                          ('^‘.+', '‘', ''),
                          ("^'.", "'", ''),
                          ('^".', '"', ''),
                          ("^“.", "“", ''),

                          (". $", " +$", ''),
                          ('."$', '"$', ''),
                          (".”$", "”$", ''),
                          (".,’$",  ',’$', ''),
                          ('.’$', '’$', ''),
                          (".'$'", "'$'", ''),
                          ('.,$', ',$', ''),
                          ('.\.$', '\.$', ''),
                          ('.—$', '—$', ''),
                          ('.-$', '-$', '')

                      )
# Add in new lines for new patterns.
# Each pattern must be in the form:
# pattern, search, replace
# Pattern to correction
# Search for place to place correction
# Correction to be made


# Defining a function to generate functions that follow the rules
def build_match_and_apply_functions(pattern, search, replace):
    def matches_rule(word):
        return re.search(pattern, word)

    def apply_rule(word):
        return re.sub(search, replace, word)

    return (matches_rule, apply_rule)
    

# Creates a list of generated functions using the generator function
correction_rules = \
                  [
                      build_match_and_apply_functions(pattern, search, replace)
                      for (pattern, search, replace) in correction_patterns
                  ]


# Creates a function to run the list of functions
def correction(word):
    for matches_rule, apply_rule in correction_rules:
        if matches_rule(word):
            word = apply_rule(word)
    return(word)


def testrule(word):
    word = correction(word)
    print(word)

# After all this trouble, all you have to do is to
# update the correction_patterns
# call correction in desired function

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #


def filepath(filename, data,
             root='/home/cyneo/Work/Scans/Processed Data/Adj Extracts/', filetype='.csv'):
    path = os.path.abspath(root + data + '/' + filename +
                           ' ' + data + filetype)
    return path


def postext_st(filename):
    # Opening of File
    path_to_raw = '/home/cyneo/Work/Scans/Text Version/'

    if type(filename) != str:
        raise IOError('Filename must be a string')

    # Preparing to Tokenize
    with open(osp.abspath(path_to_raw + filename + '.txt'),
              'r', encoding='utf8') as raw:
        # Initialize the punkt module
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sents = []

        for line in raw:
            sents.extend(sent_detector.tokenize(line.strip()))
    
    tokenedsents = []
    # Tokenizing
    from nltk.tokenize.stanford import StanfordTokenizer
    for line in sents:
        tokenedsents.append(StanfordTokenizer().tokenize(line))

    # Parts of Speech Tagging
    posSents = []
    from nltk.tag.stanford import POSTagger
    st = POSTagger('/mnt/sda2/stanford-packages/stanford-postagger-2014-10-26/models/english-bidirectional-distsim.tagger',
                   encoding='utf8')

    for line in tokenedsents:
        # Returns a list of a list of tuples
        posSents.append(st.tag(line))

    return posSents


def postext(filename):
    # Opening of File
    path_to_raw = '/home/cyneo/Work/Scans/Text Version/'

    if type(filename) != str:
        raise IOError('Filename must be a string')

    # Preparing to Tokenize
    with open(osp.abspath(path_to_raw + filename + '.txt'),
              'r', encoding='utf8') as raw:
        # Initialize the punkt module
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sents = []
        for line in raw:
            sents.extend(sent_detector.tokenize(line.strip()))

        # Tokenizing
        # Make use of the tokenizer if want to modify the rules
        # tokenizer = nltk.RegexpTokenizer('\w+|\$[\d\.]+|\S+')
        from nltk.tokenize.punkt import PunktWordTokenizer
        tokenedsents = []
        for line in sents:
            tokenedsents.append(PunktWordTokenizer().tokenize(line))
        
        # There are issues with the tokenizer
        # Cleaning up tokenizer results
        
        for line in range(len(tokenedsents)):
            for word in range(len(tokenedsents[line])):
                tokenedsents[line][word] = correction(tokenedsents[line][word])

        # makes sentences using the makesent function below
        # tokenedtext=[]

    # Parts of Speech Tagging
    posSents = []
    for line in tokenedsents:
        # Returns a list of a list of tuples
        posSents.append(nltk.pos_tag(line))

    return posSents

    # change to the lemmatized text hello?
    # lemmatized text does not have pos tagging


