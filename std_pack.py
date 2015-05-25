
# Importing modules
modules = ['collections',
           'csv',
           'math',
           'os',
           'pdb',
           'pickle',
           're',
           'sys',
           'time',
           'scipy',
           'pylab']

modules1 = [('pandas', 'pd'),
            ('numpy', 'np'),
            ('networkx', 'nx'),
            ('random', 'rand')]

import matplotlib.pyplot as plt


for mod in modules:
    globals()[mod] = __import__(mod)

for mod, alias in modules1:
    globals()[alias] = __import__(mod)
            
from mpl_toolkits.mplot3d import Axes3D  # for 3D plots in matplotlib

# Defining commonly used directories
"""
Variable defined this way so that when everything is dumped into a folder,
everything will import properly without having to change directories again

code_path acts as a starting point as when code is run, the path containing
the code will automatically be in the search paths of python. From there,
the code navigates towards the root. From the root everything else can be
defined.
"""
code_path = os.getcwd()  # Current working directory
root = os.path.dirname(code_path)
data_path = root + '/Data/'
raw_path = data_path + 'Raw/'
text_path = raw_path + 'Text Version/'
processed_path = data_path + 'Processed Data/'
parse_path = processed_path + 'Parse Method/'
parse_dict = parse_path + 'Dictionaries/'
class_data = processed_path + 'Class Data/'
thesaurus_path = data_path + 'Thesaurus/'
scrape_path = thesaurus_path + 'scraped/'
thesaurus_words = data_path + 'words'

male_terms = ['he', 'his']
female_terms = ['she', 'her']

# Import NLTK
try:
    # This is for working on my Ubuntu only.
    sys.path.insert(0, '/mnt/sda2/nltk')
    import nltk

except:
    # Goes to the root to find a copy of NLTK that should be in folder
    os.chdir(root + '/nltk')
    import nltk

# Adding directories for server package importing
sys.path.insert(0, root)


# ## Administrative Functions ## #

def data_checker1():
    """
    checks all the pickle files a directory for:
    male_adj
    female_adj
    
    TODO:
    check data types (currently read, but no autocheck)
    output into some readable format (done)
    """
    files_to_check = os.listdir(class_data)
    with open(processed_path + 'Data Check.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        for pickle_name in files_to_check[1:]:  # [1:] needed due to listdir
            pickle_data = load_book(pickle_name)

            csv_writer.writerow([pickle_name] + list(pickle_data.__dict__.keys()))


def data_checker():
    """
    checks all the pickle files a directory for:
    male_adj
    female_adj
    
    TODO:
    check data types (currently read, but no autocheck)
    output into some readable format (done)
    """
    files_to_check = os.listdir(class_data)
    with open(processed_path + 'Data Check', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        for pickle_name in files_to_check[1:]:  # [1:] needed due to listdir
            pickle_data = load_book(pickle_name)

            csv_writer.writerow([pickle_name,
                                 str(attribute_checker(pickle_data, 'male_adj')),
                                 str(attribute_checker(pickle_data, 'female_adj'))])


def data_checker_ind(pickle_name, attribute, type):
    """
    Checks, for a single book, the input pickle for an attribute and
    if the attribute is of the right type.

    Returns:
    True if attribute and attribute type are as desired
    String to indicate which pickle and what attribute it lacks
    """
    # include some regex stuff to see if extension is present
    pickle_data = load_book(pickle_name)
    if attribute_checker(pickle_data, attribute):
        return True

    else:
        return False
        # pickle_name +\
        #    ' does not have the ' +\
        #    attribute +\
        #    ' attribute'


def data_checker_plus_add_adjs():
    """
    checks all the pickle files a directory for:
    male_adj
    female_adj
    
    TODO:
    check data types (currently read, but no autocheck)
    output into some readable format (done)
    """
    files_to_check = os.listdir(class_data)

    for pickle_name in files_to_check[1:]:
        pickle_data = load_book(pickle_name)
        
        if not (attribute_checker(pickle_data, 'male_adj') is dict):
            pickle_data.add_adjs()
            pickle_data.save_book()


def attribute_checker(data, attribute):
    """
    Checks if data has an attribute and returns the attribute type if there is

    Coded to be fed into data checkers which check based on data types
    """
    if hasattr(data, attribute):
        return type(getattr(data, attribute))
    else:
        return None


def load_book(filename):
    with open(class_data + filename, 'rb') as book_file:
        data = pickle.load(book_file)
    return data


# Line to demark what has been sorted into functionality
# ____________________________________________________


class Book():
    """
    Class is defined to store attributes of a book that I have used.
    Reason for this is to speed up accessing data from a book.

    So far, the following are included:
    title
    author
    year of publication
    
    add_tree(self, tree): the trees come from parse.py
    """
    # Attributes

    def __init__(self, filename):
        self.filename = filename
        author, title = filename.split('] ')
        author = author[1:]
        self.title = title
        self.author = author
        years = pickle.load(open(raw_path + 'Book Years', 'rb'))
        self.year = years[author][title]
        self.trees = []

    def add_tree(self, tree):
        self.trees.append(tree)

    def save_book(self):
        with open(class_data +
                  '[' + self.author + '] ' +
                  self.title + '.p',
                  'wb') as book_pickle:
            pickle.dump(self, book_pickle)

    def add_adjs(self):
        """
        NOTE: self.adj_graph comes from the parse code. Do not use this
        function if data is not from parse.
        """
        graph = self.adj_graph
        male_terms = ['he', 'his']
        female_terms = ['she', 'her']

        male_adj = {}
        for term in male_terms:
            for key in graph.edge[term].keys():
                try:
                    male_adj[key] += graph.edge[term][key]['weight']
                except KeyError:
                    male_adj[key] = graph.edge[term][key]['weight']

        female_adj = {}
        for term in female_terms:
            for key in graph.edge[term].keys():
                try:
                    female_adj[key] += graph.edge[term][key]['weight']
                except KeyError:
                    female_adj[key] = graph.edge[term][key]['weight']

        self.male_adj = male_adj
        self.female_adj = female_adj

 
def make_sent(filename):
    # Extracts sentences and closes raw file
    # Open file

    if type(filename) != str:
        filename = input(
            str(filename) +
            ' is not a string. Filename must be a string/n --->')

    # Splits into sentences
    with open(os.path.abspath(text_path + filename + '.txt'),
              'r', encoding='utf8') as raw:
        # Initialize the punkt module
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sents = []
        for line in raw:
            # I can add in a progress bar here
            sents.extend(sent_detector.tokenize(line.strip()))

        return sents


def make_tokens(sents):
    # Tokenize using the Stanford package
    tokenedsents = []
    from nltk.tokenize.stanford import StanfordTokenizer
    for line in sents:
        tokenedsents.append(StanfordTokenizer().tokenize(line))

    return tokenedsents


def tag_tokens(tokens):
    tagged_sents = []
    from nltk.tag.stanford import POSTagger
    st = POSTagger('/mnt/sda2/stanford-packages/stanford-postagger-2014-10-26/models/english-bidirectional-distsim.tagger',
                   encoding='utf8')

    print('Starting to tag sentences')
    """
    Progress Bar:
    """
    toolbar_width = 40

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))
    # return to start of line, after '['

    no_of_sents = len(tokens)
    no_of_ticks = 0
    sent_counter = 0

    for line in tokens:
        # Returns a list of a list of tuples
        tagged_sents.append(st.tag(line))

        # Updating bar
        sent_counter += 1
        trigger = (sent_counter * toolbar_width - 1) / no_of_sents
        if trigger >= no_of_ticks:
            while no_of_ticks < math.floor(trigger):
                sys.stdout.write("-")
                sys.stdout.flush()
                no_of_ticks += 1

    sys.stdout.write(">]\n")
    print('Done tagging')

    return tagged_sents


def add_edge(graph, source, sink):
    try:
        graph.edge[source][sink]['weight'] += 1
    except KeyError:
        graph.add_edge(source, sink, weight=1)
        """
 except AttributeError:
        pass  # looks like i tried to sweep a problem under
        """

