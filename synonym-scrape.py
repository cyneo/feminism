from std_pack import *
from bs4 import BeautifulSoup
import requests
import re
import scipy.cluster.hierarchy as ch
import scipy
import igraph

"""
Code looks to scrape words from Word List.txt

Workflow:
scrape_word --> extract_synonyms
mass_scrape --> mass extract
goal is to scrape everything, and in a time limited way
"""
"""
word_master_list = pickle.load(open(parse_dict + 'Master Word List.p',
                                    'rb'))

with open(thesaurus_path + 'Word List.txt', 'w') as file:
    file.write("\n".join(list(word_master_list.global_male_adjs
                              | word_master_list.global_female_adjs)) + '\n')
"""


def scrape_word(word):
    '''
    Requests a page,
    Gets text form page
    Outputs file with text of page separated by newlines
    '''
    r = requests.get("http://www.thesaurus.com/browse/" + word)
    data = r.text
    soup = BeautifulSoup(data)

    """
    Pattern finds text between newlines
    Essentially extracting information line by line
    """
    pat = re.compile(r'''
    (         # Start group
    [^\n]     # Match not newline
    +         # Greedy
    )         # End group
    ''', re.VERBOSE | re.MULTILINE)  # MULTILINE takes care of boundaries

    broken = re.findall(pat, soup.get_text())
    with open('%s%s.txt' % (scrape_path, word), 'w') as file:
        file.write('\n'.join(broken)+'\n')


def mass_scrape(list_of_words=None):
    """
    Calls scrape_word for words in Word List.txt
    Done Words tracks which words are done (minimize scraping)
    """
    if list_of_words:
        for word in list_of_words:
            scrape_word(word)
            
    elif not list_of_words:
        words = set()
        with open(thesaurus_path + 'Word List.txt') as file:
            for word in file:
                words.add(word[:-1])

        done_words = set()
        with open(scrape_path + 'Done Words.txt') as file:
            for word in file:
                done_words.add(word[:-1])

        words_to_do = words - done_words

        for word in words_to_do:
            scrape_word(word)
            time.sleep(random.uniform(0.2, 5))
            done_words.add(word)
            print('scraped %s' % word)


def extract_synonyms(word, graph):
    """
    Opens scraped data file and pulls out synonyms
    Output: a list of synonyms
    """
    with open('%s%s.txt' % (scrape_path, word)) as file:
        broken = []  # Contains lines from the page
        for line in file:
            broken.append(line[:-1])

    # Commence search through lines for indicator of synonyms
    """
    Perhaps make use of the word\nstar structure to extract?
    Should be a better approach as there are alternate meanings that
    are not captured with the current method. Again, don't care about the
    time needed as we now have a server.
    As a bonus, get alternate meanings. Not priority.
    Approach1: Did this
    Create a forward search
    Create a temp that collects the previous line
    Create a logic that determines if line should be kept

    Approach 2:
    Do a reverse search and have logic for next line identification

    What about antonyms? They should be prohibited from being linked right?

    Benchmarking?
    Super high level is to get GA type. but overkill.
    """
    syns = []
    for n in range(len(broken)):
        if re.search('^no thesaurus results', broken[n], re.MULTILINE):
            break

        elif re.search('^star', broken[n], re.MULTILINE):
            syns.append(broken[n-1])

    if syns:
        for syn in syns:
            graph.add_edge(word, syn)

    elif not graph.has_node(word):
        graph.add_node(word)
        print(word)

    return graph

    """
        elif re.search('^Synonyms for ' + word, broken[n], re.MULTILINE):
            start = n

        elif re.search('^Antonyms for', broken[n], re.MULTILINE):
            end = n

            if ('start' in locals()) and ('end' in locals()):
                # There are still a lot of \n in there
                syns = [x for x in broken[start + 3:end] if not x == 'star']
                for syn in syns:
                    graph.add_edge(word, syn)
                return graph
            if 'start' not in locals():
                print('%s no start' % word)
            if 'end' not in locals():
                print('%s no end' % word)
            break
    """


def mass_extract(list_of_words=None):
    """
    Calls extract_synonyms for words found in Done Words.txt
    and adds the synonyms to the graph through adding edges
    """
    # Retrive words to process
    with open('%sDone Words.txt' % (scrape_path)) as file:
        words_to_extract = [x[:-1] for x in file]  # Removes \n
        extract_set = set()
        extract_set.update(words_to_extract)

    try:  # Checking if graph exists
        graph = nx.read_graphml(thesaurus_path +
                                'Thesaurus Graph.graphml')

    except FileNotFoundError:  # Creates if graph does not exist
        graph = nx.Graph()

    # Calls extract_synonyms for words in set
    for word in words_to_extract:
        graph = extract_synonyms(word, graph)

    nx.write_graphml(graph, thesaurus_path + 'Thesaurus Graph.graphml')


def iextract_synonyms(word, graph):
    syns = []
    for n in range(len(broken)):
        if re.search('^no thesaurus results', broken[n], re.MULTILINE):
            break

        elif re.search('^star', broken[n], re.MULTILINE):
            syns.append(broken[n-1])

    if syns:
        for syn in syns:
            graph.add_edge(word, syn)

    elif not graph.has_node(word):
        graph.add_node(word)
        print(word)

    return graph


def imass_extract(list_of_words=None):
    """
    Calls extract_synonyms for words found in Done Words.txt
    and adds the synonyms to the graph through adding edges
    """
    # Retrive words to process
    with open('%sDone Words.txt' % (scrape_path)) as file:
        words_to_extract = [x[:-1] for x in file]  # Removes \n
        extract_set = set()
        extract_set.update(words_to_extract)

    try:  # Checking if graph exists
        graph = nx.read_graphml(thesaurus_path +
                                'Thesaurus iGraph.graphml')

    except FileNotFoundError:  # Creates if graph does not exist
        graph = igraph.Graph()

    # Calls extract_synonyms for words in set
    for word in words_to_extract:
        graph = extract_synonyms(word, graph)

    nx.write_graphml(graph, thesaurus_path + 'Thesaurus iGraph.graphml')
'''
Write something to help track the words that are done properly and those
that are not.

Possible cases:
Syns extracted properly:
- Start found
- End Found

No syns:
- no syn
- no start
- no end

Syns, not extracted properly:
- Start found
- no end

- End found
- no start
'''

'''
if i do it in the form of enter a word and get a set of synonyms,
i will end up with exhaustive list.

keep a list of queries?
got to replace spaces with %20

using this method will only yield the first sense of the word.
'''


