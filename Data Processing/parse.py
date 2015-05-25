from std_pack import *
"""
# Loading the parser
from nltk.parse import stanford
os.environ['STANFORD_PARSER'] = '/mnt/sda2/stanford-packages/stanford-parser-full-2014-10-31/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = '/mnt/sda2/stanford-packages/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models.jar'
parser = stanford.StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

from nltk.tag.stanford import POSTagger
st = POSTagger('/mnt/sda2/stanford-packages/stanford-postagger-2014-10-26/models/english-bidirectional-distsim.tagger',
               encoding='utf8')

from nltk.tokenize.stanford import StanfordTokenizer

# design so that I don't parse if I don't have to
# write functions for the different conditions
# the point of the functions is to give different types of data

sent = st.tag(StanfordTokenizer().tokenize(
    '''His furry panda.'''))

sentences = parser.tagged_parse_sents((sent,))
psentence = nltk.tree.ParentedTree.convert(sentences)

"""


def run_books():
    '''
    This function was created because there was a gap between updated
    methods and old ones. This function serves to close the gap. The
    real workhorse is main()
    '''
    books = os.listdir(text_path)[1:]
    # Checking attributes and calling the right funcitons to run
    for book in books:
        if book[-1:] == '~':
            # Checks if the book already has a class implementation
            # if yes, check if it has tokens
            if (book[:-5] + '.p') in os.listdir(class_data):
                # Check if the class has tokens/sents
                # (which means it is a class that is only holds adjs and
                # the graph)
                # pass if it has
                if data_checker_ind(book[:-5] + '.p', 'tokens', list):
                    pass
                # else, run the whole thing to capture tokens and trees
                # although running add_adjs again is a waste of time
                # it is not that long
                else:
                    # run the parse thing
                    main(book[:-5])
            else:
                main(book[:-5])

        else:
            # Checks if the book already has a class implementation
            # if yes, check if it has tokens
            if (book[:-4] + '.p') in os.listdir(class_data):
                # Check if the class has tokens/sents
                # (which means it is a class that is only holds adjs and
                # the graph)
                # pass if it has
                if data_checker_ind(book[:-4] + '.p', 'tokens', list):
                    pass
                # else, run the whole thing to capture tokens and trees
                # although running add_adjs again is a waste of time
                # it is not that long
                else:
                    # run the parse thing
                    main(book[:-4])
            else:
                main(book[:-4])


def main(filename):
    """
    Function calls:
    
    """
    # Creating a class implementation for the book
    book = Book(filename)

    # Timestamping
    print(time.strftime("%d/%m/%Y %H:%M:%S ") + 'Starting on: ' + filename)

    # Identifying targets
    terms = ['his', 'her', 'he', 'she']

    # Basic information extraction of the book
    sents = make_sent(filename)  # Extracting sentences from the file
    book.sents = sents  # Adding attribute to class
    tokens = make_tokens(sents)  # Making sentence tokens
    book.tokens = tokens  # Adding attribute to class

    # Getting desired sentences
    sents_to_parse = []
    for line in tokens:
        if len(line) < 40:
            for word in line:
                if word.lower() in terms:
                    sents_to_parse.append(line)
                    break

    book.sents_with_terms = sents_to_parse

    # Performing POS tagging
    tagged_sents = tag_tokens(sents_to_parse)
    book.tagged_sents = tagged_sents

    adj_graph = nx.Graph()
    nn_graph = nx.Graph()

    print(time.strftime("%d/%m/%Y %H:%M:%S ") +
          'Starting to parse the sentences of: ' + filename)

    """
    Progress bar
    --- Start ---
    """
    toolbar_width = 40

    # toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))
    # return to start of line, after '['

    no_of_sents = len(tagged_sents)
    no_of_ticks = 0
    sent_counter = 0
    
    """
    --- End ---
    """

    # Creating parse trees for each sentence
    for sentence in tagged_sents:
        parsed_sent = parse(sentence)  # This gives a tree
        pparsed_sent = nltk.tree.ParentedTree.convert(parsed_sent[0])
        book.add_tree(pparsed_sent)
        positions = pparsed_sent[0].treepositions()
        for position in positions:
            try:
                variable_to_test = pparsed_sent[0][position].label()

            except AttributeError:
                variable_to_test = pparsed_sent[0][position]
            
            if variable_to_test.lower() == 'her' or\
               variable_to_test.lower() == 'his':
                prps_proc(adj_graph, nn_graph, pparsed_sent[0], position)

            elif variable_to_test.lower() == 'he' or\
                 variable_to_test.lower() == 'she':
                # pass
                prp_proc(adj_graph, pparsed_sent[0], position)
        
        # Updating bar
        sent_counter += 1
        trigger = (sent_counter * toolbar_width - 1) / no_of_sents
        if trigger >= no_of_ticks:
            while no_of_ticks < math.floor(trigger):
                sys.stdout.write("-")
                sys.stdout.flush()
                no_of_ticks += 1
        
    sys.stdout.write(">]\n")
        
    book.adj_graph = adj_graph
    book.nn_graph = nn_graph
    book.add_adjs()
    print(time.strftime("%d/%m/%Y %H:%M:%S ") + 'Finished: ' + filename)
    book.save_book()


def parse(tagged_sent):
    """
    Function that calls parser for tagged sentences.
    """
    from nltk.parse import stanford
    os.environ['STANFORD_PARSER'] = '/mnt/sda2/stanford-packages/stanford-parser-full-2014-10-31/stanford-parser.jar'
    os.environ['STANFORD_MODELS'] = '/mnt/sda2/stanford-packages/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models.jar'
    parser = stanford.StanfordParser(
        model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

    return parser.tagged_parse_sents((tagged_sent,))


def prp_proc(graph, tree, position):
    """
    Looks through the parse trees and finds the correct phrase, and then looks
    for the ADJ in the phrase

    Logic:
    Adj usually appears only after a PRP.
    Need to go up the tree, then find THE VP on the right
    In the VP, go to the next level, and find if there is a VB.
    If there is a VB, look for ADJP among siblings and take the JJ
    This will only be triggered if a PRP is found
    """
    # PRP will show NP 2 levels up, so I can just cut up:
    # Position of the NP of PRP:
    prp_root = position[:-2]

    # Prevent error from no sibling:
    if tree[prp_root].right_sibling():
        # Right Sibling Position
        # Defined to offset by one position as treeposition takes
        # reference from super tree. But my input tree is from a
        # level deeper
        rsp = tree[prp_root].right_sibling().treeposition()[1:]
        # if a VP tree found, explore children:
        if tree[rsp].label() == 'VP':
            # if VB child found
            vb = explore_children(tree[rsp], 'VB')
            if type(vb) is int:
                # find ADJP:
                adjp = explore_children(tree[rsp], 'ADJP')
                # if ADJP child found:
                if type(adjp) is int:
                    jj = explore_children(tree[rsp][adjp], 'JJ')
                    if type(jj) is int:
                        # Add source and sink and adjust frequency:
                        try:
                            graph.node[tree[position].lower()]['Frequency'] += 1
                        except KeyError:
                            graph.add_node(
                                tree[position].lower(),
                                POS=tree[position[:-1]].label(),
                                Frequency=1)
                        try:
                            graph.node[tree[rsp][adjp][jj][0]]['Frequency']\
                                += 1
                        except KeyError:
                            graph.add_node(
                                tree[rsp][adjp][jj][0],
                                POS='JJ',
                                Frequency=1)

                        # Add edge from PRP to JJ
                        add_edge(graph,
                                 tree[position].lower(),
                                 tree[rsp][adjp][jj][0])


def prps_proc(adj_graph, nn_graph, tree, position):
    """
    Searches through the parse trees and finds the correct phrase,
    and extracts the ADJ once correct phrase is found
    """
    wanted_pos = ['JJ',
                  'NN',
                  'RB',
                  'PR']
    np_position = position[:-2]
    words_to_link = {'PR': [],
                     'NN': [],
                     'JJ': [],
                     'RB': []}
    # here, next is called to skip first value which is the np
    for item in next(tree[np_position].subtrees()):
        if item.pos()[0][1][:2] == 'PR':
            words_to_link[item.pos()[0][1][:2]].append(item.pos()[0][0].lower())
            try:
                nn_graph.node[item.pos()[0][0].lower()]['Frequency'] += 1
                adj_graph.node[item.pos()[0][0].lower()]['Frequency'] += 1
            except KeyError:
                nn_graph.add_node(
                    item.pos()[0][0].lower(),
                    POS=item.pos()[0][1][:2],
                    Frequency=1)

                adj_graph.add_node(
                    item.pos()[0][0].lower(),
                    POS=item.pos()[0][1][:2],
                    Frequency=1)

        if item.pos()[0][1][:2] == 'NN':
            words_to_link[item.pos()[0][1][:2]].append(item.pos()[0][0].lower())
            try:
                nn_graph.node[item.pos()[0][0].lower()]['Frequency'] += 1
            except KeyError:
                nn_graph.add_node(
                    item.pos()[0][0].lower(),
                    POS=item.pos()[0][1][:2],
                    Frequency=1)

        if item.pos()[0][1][:2] == 'JJ':
            words_to_link[item.pos()[0][1][:2]].append(item.pos()[0][0].lower())
            try:
                adj_graph.node[item.pos()[0][0].lower()]['Frequency'] += 1
            except KeyError:
                adj_graph.add_node(
                    item.pos()[0][0].lower(),
                    POS=item.pos()[0][1][:2],
                    Frequency=1)

    """
    Linking up the words
    """
    # Linking Pronouns to Adjectives
    for pronoun in words_to_link['PR']:
        for adj in words_to_link['JJ']:
            add_edge(adj_graph, pronoun, adj)
            if words_to_link['NN']:
                for noun in words_to_link['NN']:
                    add_edge(adj_graph, adj, noun)
                    try:
                        adj_graph.node[noun]['Frequency'] += 1
                    except KeyError:
                        adj_graph.add_node(
                            noun,
                            POS='NN',
                            Frequency=1)

    # Linking nouns to adjectives
    if words_to_link['JJ']:
        for noun in words_to_link['NN']:
            for adjective in words_to_link['JJ']:
                add_edge(nn_graph, noun, adjective)

    # Linking adverbs to adjectives:
    if words_to_link['RB']:
        for adjective in words_to_link['JJ']:
            for adverb in words_to_link['RB']:
                add_edge(adj_graph, adjective, adverb)

    # I want to add in some kind of ordering in the links
    # explore_children and tuple inequalities might get that


def explore_children(sub_tree, look_for):
    """
    i want:
    a start point (sub_tree)
    something to look at the next layer (sub_tree.treepositions())
    something to look for (look_for)
    output a generic result (type(return))
    output a coordinate (index)
    """
    sub_positions = sub_tree.treepositions()
    no_sib = 0
    for sub_position in sub_positions:
        if len(sub_position) == 1:
            no_sib += 1

    for index in range(no_sib):
        if sub_tree[index].label()[:len(look_for)] == look_for:
            return index
    
