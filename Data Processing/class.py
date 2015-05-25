"""
11th Feb 2015:
converts files that do not have a class pickle at all.
Such files only have graphmls for their data and nothing else

THEREFORE:
this code only serves to speed up the ability to get the data into
cluster code, and nothing else.
and there is a need to go back to these books to add in the other attributes
that are present in the other books.

add_adjs:
Input:
_adj.graphml

Output:
class attributes called male_adj and female_adj

Missing Attributes:
sents
tokens
trees
sents_with_terms
nn_graph

10th Feb 2015:
Reviving the code to as a way to assist in the conversion of data into
classes.

20th Jan 2015:
Code here is used as a test to create a class that stores all the data of a
book so that it is easy to save all the information in the data folders,
as well as calling information in functions

Placed in phase out as the code has already been transfered into std_pack.py

USAGE:
Instantiate class by using variable = Book()

Input:
None

Output:
None

This class was never meant to be functional.
"""

import pickle
from std_pack import *

"""
This is code to write the data as a class so that I can hopefully
access the attributes in a much more convienient way in the future.

Data to be stored:
Author --> .author
Title --> .title
Year of publication --> .year
Trees --> nltk.Tree class
Graphs --> nx.Graph class
Words --> list of list of strings
Tags --> List of list of tuples
Male Adjs --> List of tuples (word, frequency)
Female Adjs --> List of tuples (word, frequency)


Questions:
This is a good problem as it allows me to load 2 things
side by side. But is it useful?
"""


class Book():
    """
    For books
    Want to get the male and female adjs from graphmls.
    Also want to get the frequencies from there.
    Gets it from looking at the weights of the edges
    The add_adjs will handle the file opening as long as
    book title is provided
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

    # Parse trees of each sentence in the book
    def add_tree(self, tree):
        self.tree.append(tree)

    def save_book(self):
        with open(class_data +
                  '[' + self.author + '] ' +
                  self.title + '.p',
                  'wb') as book_pickle:
            pickle.dump(self, book_pickle)

    def add_adjs(self):
        male_terms = ['he', 'his']
        female_terms = ['she', 'her']
        print('adding')
        with open(parse_path + self.filename + '_adj.graphml',
                  'r', encoding='utf8') as graph_file:
            graph = nx.read_graphml(graph_file)

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

        # might want to add in adjs as dcitionaires with freqyency as values
        # in such a case, i need to find a way to add weights


def fix_em():
    """
    Opens classless books, imports the titles that needed to be
    processed, and then calls the functions needed to add in the
    attributes into the class. all opening and closing of other
    data files related to the titles will be taken care of inside the
    class functions.
    """
    with open(data_path + 'classless books.csv') as files:
        books = csv.reader(files)

        for title in books:
            book = Book(title[0])
            book.add_adjs()
            book.save_book()
