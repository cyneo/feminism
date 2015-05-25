"""
Phased out due to the introduction of parse method. The difference between the two
is that this code lemmatizes the words.
"""
'''
This set of code only serves to tokenize and lemmatize text that is fed into it
It will then output files of the different stages of processing
for manual checking of what went wrong where


Output Files:
edges
lemmatized sents

The reason why I wrote the code in a way that outputs and reads from files
is because I want to prevent cases where the size of an object gets
too big for the system to handle

Output will then go into graph.py for further processing
'''
import csv
import sys
import re
import os.path as osp
import os


# Importing NLTK
try:
    import nltk
except ImportError:
    sys.path.insert(0, '/mnt/sda2/nltk')
    import nltk

from nltk.stem import WordNetLemmatizer

"""
Write function that takes care of all the filenames in a loop.
Also have a tracker that takes care of which files are done.
"""


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
                   "[graham Green] Our Man in Havana",
                   "[Graham Green] Stamboul Train",
                   "[Graham Green] The Comedians",
                   "[Graham Green] The End of an Affair",
                   "[Graham Green] The Heart of the Matter",
                   "[Graham Green] The Human Factor",
                   "[Graham Green] THe Ministry of Fear",
                   "[Graham Green] The Power and Glory"]

    for item in list_to_run:
        process_text(item)


def process_text_st(filename):
    # Opening of File
    path_to_raw = '/home/cyneo/Work/Scans/Text Version/'

    if type(filename) != str:
        filename = input(
            str(filename) + ' is not a string. Filename must be a string/n --->')

    # Preparing to Tokenize
    with open(osp.abspath(path_to_raw + filename + '.txt'),
              'r', encoding='utf8') as raw:
        # Initialize the punkt module
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sents = []

        for line in raw:
            sents.extend(sent_detector.tokenize(line.strip()))
        
    """
    # Parsing
    tokenedsents = []
    from nltk.parse import stanford
    os.environ['STANFORD_PARSER'] = '/mnt/sda2/stanford-packages/stanford-parser-full-2014-10-31/stanford-parser.jar'
    os.environ['STANFORD_MODELS'] = '/mnt/sda2/stanford-packages/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models.jar'
    parser = stanford.StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
    for sentence in sentences:
        sentence.draw()
    """

    # Tokenizing
    # Make use of the tokenizer if want to modify the rules
    # tokenizer = nltk.RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    from nltk.tokenize.stanford import StanfordTokenizer
    for line in sents:
        tokenedsents.append(StanfordTokenizer().tokenize(line))
    # There are issues with the tokenizer
    # Cleaning up tokenizer
    """
    for line in range(len(tokenedsents)):
        for word in range(len(tokenedsents[line])):
            tokenedsents[line][word] = correction(tokenedsents[line][word])
    """
    # makes sentences using the makesent function below
    # tokenedtext=[]

    # Parts of Speech Tagging
    posSents = []
    from nltk.tag.stanford import POSTagger
    st = POSTagger('/mnt/sda2/stanford-packages/stanford-postagger-2014-10-26/models/english-bidirectional-distsim.tagger',
                   encoding='utf8')

    for line in tokenedsents:
        # Returns a list of a list of tuples
        posSents.append(st.tag(line))
        
    # del tokenedsents  # clears up memory

    # Lemmatization
    lemmatizer = WordNetLemmatizer()

    """
    The lemmatizer need to differentiate between the different kinds of words
    to do an accurate lemmatization. I suppose this can be done with a PoS
    tagging, and then shortening the PoS tagging into arguments that the
    lemmatizer can take.
    
    So far I have tried:
    'n' for nouns
    'v' for verbs
    'a' for adverbs and adjectives
    and they work
    """
    posdict = {'NN': 'n',
               'NNS': 'n',
               'VB': 'v',
               'VBD': 'v',
               'VBG': 'v',
               'VBP': 'v',
               'VBZ': 'v',
               'JJ': 'a',
               'JJR': 'a',
               'JJS': 'a',
               'RB': 'a',
               'RBR': 'a',
               'RBS': 'a'}

    punctlist = \
                [
                    '.',
                    ',',
                    '!',
                    '?',
                    "'",
                    '"',
                    '(',
                    ')'
                ]

    with open(filepath(filename, 'Lemmatized Text'),
              'w', encoding='utf-8') as lemma_file:
        lemma_writer = csv.writer(lemma_file, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        lemma_reader = csv.reader(lemma_file, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)

        for line in range(len(posSents)):
            holding = []
            for word in range(len(posSents[line])):
                # this for loop goes through each word in the sentence
                if posSents[line][word][1] in posdict:
                    # checks if POS is in posdict
                    holding.append(lemmatizer.lemmatize(
                        posSents[line][word][0],
                        posdict[posSents[line][word][1]]).lower())
                    # if true, lemmatize the word with the correct argument
                elif posSents[line][word][0] in punctlist:
                    pass  # so that the punctuation does not go in
                elif re.search('\w+', posSents[line][word][0]):
                    holding.append(posSents[line][word][0].lower())

            # Need to add in things to clean up the text before
            # writing into the file.
            # Things to clean:
            #
            holding = [word for word in holding if word != '']
            lemma_writer.writerow(holding)

    del posSents  # clears up memory

    with open(filepath(filename, 'Lemmatized Text'),
              'r', encoding='utf8') as lemma_file:
        lemma_reader = csv.reader(lemma_file, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        with open(filepath(filename, 'Edges'),
                  'w', encoding='utf8') as edge_file:
            edge_writer = csv.writer(edge_file, delimiter='\t',
                                     quoting=csv.QUOTE_MINIMAL)
            for line in lemma_reader:
                bigrams = nltk.bigrams(line)
                for tuple in bigrams:
                    edge_writer.writerow(tuple)


def process_text(filename):
    """
    This version of text processing uses the Punkt methods.
    """
    # Opening of File
    path_to_raw = '/home/cyneo/Work/Scans/Text Version/'

    if type(filename) != str:
        filename = input(
            str(filename) + ' is not a string. Filename must be a string/n --->')

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
        # Cleaning up tokenizer

        for line in range(len(tokenedsents)):
            for word in range(len(tokenedsents[line])):
                tokenedsents[line][word] = correction(tokenedsents[line][word])

        # makes sentences using the makesent function below
        # tokenedtext=[]

    # Parts of Speech Tagging
    posSents = []
    
    from nltk.tag.stanford import POSTagger
    st = POSTagger(encoding='utf8')

    for line in tokenedsents:
        # Returns a list of a list of tuples
        posSents.append(st.tag(line))
    del tokenedsents  # clears up memory

    # Lemmatization
    lemmatizer = WordNetLemmatizer()

    """
    The lemmatizer need to differentiate between the different kinds of words
    to do an accurate lemmatization. I suppose this can be done with a PoS
    tagging, and then shortening the PoS tagging into arguments that the
    lemmatizer can take.
    
    So far I have tried:
    'n' for nouns
    'v' for verbs
    'a' for adverbs and adjectives
    and they work
    """
    posdict = {'NN': 'n',
               'NNS': 'n',
               'VB': 'v',
               'VBD': 'v',
               'VBG': 'v',
               'VBP': 'v',
               'VBZ': 'v',
               'JJ': 'a',
               'JJR': 'a',
               'JJS': 'a',
               'RB': 'a',
               'RBR': 'a',
               'RBS': 'a'}

    punctlist = \
                [
                    '.',
                    ',',
                    '!',
                    '?',
                    "'",
                    '"',
                    '(',
                    ')'
                ]

    with open(filepath(filename, 'Lemmatized Text'),
              'w', encoding='utf-8') as lemma_file:
        lemma_writer = csv.writer(lemma_file, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        lemma_reader = csv.reader(lemma_file, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)

        for line in range(len(posSents)):
            holding = []
            for word in range(len(posSents[line])):
                # this for loop goes through each word in the sentence
                if posSents[line][word][1] in posdict:
                    # checks if POS is in posdict
                    holding.append(lemmatizer.lemmatize(
                        posSents[line][word][0],
                        posdict[posSents[line][word][1]]).lower())
                    # if true, lemmatize the word with the correct argument
                elif posSents[line][word][0] in punctlist:
                    pass  # so that the punctuation does not go in
                elif re.search('\w+', posSents[line][word][0]):
                    holding.append(posSents[line][word][0].lower())

            # Need to add in things to clean up the text before
            # writing into the file.
            # Things to clean:
            #
            holding = [word for word in holding if word != '']
            lemma_writer.writerow(holding)

    del posSents  # clears up memory

    with open(filepath(filename, 'Lemmatized Text'),
              'r', encoding='utf8') as lemma_file:
        lemma_reader = csv.reader(lemma_file, delimiter='\t',
                                  quoting=csv.QUOTE_MINIMAL)
        with open(filepath(filename, 'Edges'),
                  'w', encoding='utf8') as edge_file:
            edge_writer = csv.writer(edge_file, delimiter='\t',
                                     quoting=csv.QUOTE_MINIMAL)
            for line in lemma_reader:
                bigrams = nltk.bigrams(line)
                for tuple in bigrams:
                    edge_writer.writerow(tuple)

"""
Functions that are used above:

"""
# Correction for text from nltk tokenizer
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%% START %%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

                        
# Create patterns to be corrected
correction_patterns = \
                      (
                          #  ("/", "/", ''),
                          ("^ .", " ", ''),
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

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%% START %%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #


def filepath(filename, data, root='/home/cyneo/Work/Scans/Processed Data/',
             filetype='csv'):
    """
    A function that helps call absolute path for a document

    Input:
    Output:

    """
    path = os.path.abspath(root + data + '/' + filename +
                           ' ' + data + '.' + filetype)
    return path

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%% END %%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #


'''

def dialoguefilter(filename):
    """
    Dialogue Filter

    Returns a list of strings. Each list represents one new line in the text.
    """
    dialogue = []
    narrative = []
    with open(filename, encoding = 'utf8') as file:
        for line in file.readlines():
            dialogue.append(re.findall(r'[\'‘].*?[!\.,?—-][\'’]',line))
            narrative.extend(re.findall(r'[\'‘].*?[!\.,?—\-][\'’]', line))
            #narrative.extend(re.findall(r'[!\.,?—-][\'’].*?[\'‘]', line))
            
    
    return dialogue
'''

'''
To open and write to a different directory
with open(os.path.join('/home/cyneo/Work/python3/Data Processing/Processed Data/testing\ change\ directory.txt'), 'r') as read:
	with open(os.path.join('/home/cyneo/Work/python3/Data Processing/Processed Data/Hello', 'write.txt'), 'w') as write:
		for line in read:
			write.write(line)

Additional things that can be added into this would be to script it so that it reads from the excel file of the book names and then run it. That way I can run the script to get all the graph files processed.
'''

