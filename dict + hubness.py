"""
This code creates a dictionary based on all edges contributing to degree.
For code that modifies degree based on unique words, use second version

Want to make it such that everything is hashable
Idealy, everything will happen from the lemmatized sents
word: freq:
      in_degree: number  # This should be updated when a new word is added
      out_degree: number  # This should be updated when a new word is added
      in_words: words: strength
                words: strength
      out_words: words: strength
                 words: strength
"""
import csv
import os
import pickle


def main_compile(lemmatized_file):
    hey_yeo = input('Do you want to overwrite? (y/n)')
    if hey_yeo == 'n':
        pass
    elif hey_yeo == 'y':
         
        book_dictionary = {}
        # Loads current library
        try:
            main_dict = pickle.load(open(filepath('Compiled',
                                                  data='Data',
                                                  filetype='p'),
                                         'rb+'))
        except FileNotFoundError:
            main_dict = {}

        with open(filepath(lemmatized_file), 'r', encoding='utf8') as file:
            file_reader = csv.reader(file, delimiter='\t',
                                     quoting=csv.QUOTE_MINIMAL)

            for line in file_reader:
                for n in range(len(line)):
                    try:
                        book_dictionary[line[n]]['freq'] += 1

                    except KeyError:
                        book_dictionary[line[n]] = {'freq': 1,
                                                    'in_degree': 0,
                                                    'out_degree': 0,
                                                    'predecessors': {},
                                                    'successors': {}}

                    try:
                        main_dict[line[n]]['freq'] += 1

                    except:
                        main_dict[line[n]] = {'freq': 1,
                                              'in_degree': 0,
                                              'out_degree': 0,
                                              'predecessors': {},
                                              'successors': {}}
                        # This should define the other nested things

                    # takes care of the successors
                    if n < len(line)-1:
                        try:
                            book_dictionary[line[n]]['successors'][line[n+1]] += 1
                            book_dictionary[line[n]]['out_degree'] += 1

                        except KeyError:
                            book_dictionary[line[n]]['successors'][line[n+1]] = 1
                            book_dictionary[line[n]]['out_degree'] += 1

                        try:
                            main_dict[line[n]]['successors'][line[n+1]] += 1
                            main_dict[line[n]]['out_degree'] += 1

                        except KeyError:
                            main_dict[line[n]]['successors'][line[n+1]] = 1
                            main_dict[line[n]]['out_degree'] += 1

                    # takes care of the predecessors
                    if n > 0 and n < len(line):
                        try:
                            book_dictionary[line[n]]['predecessors'][line[n-1]] += 1
                            book_dictionary[line[n]]['in_degree'] += 1

                        except KeyError:
                            book_dictionary[line[n]]['predecessors'][line[n-1]] = 1
                            book_dictionary[line[n]]['in_degree'] += 1

                        try:
                            main_dict[line[n]]['predecessors'][line[n-1]] += 1
                            main_dict[line[n]]['in_degree'] += 1

                        except KeyError:
                            main_dict[line[n]]['predecessors'][line[n-1]] = 1
                            main_dict[line[n]]['in_degree'] += 1
        # Compile the book hubness
        for word in book_dictionary:
            book_dictionary[word]['in_hubness'] = book_dictionary[word]['in_degree'] /\
                                                  book_dictionary[word]['freq']
            book_dictionary[word]['out_hubness'] = book_dictionary[word]['out_degree'] /\
                                                   book_dictionary[word]['freq']

        # Saving book to it's own unique .p file
        pickle.dump(book_dictionary, open(filepath(
            lemmatized_file, data='Data', filetype='p'), 'wb'))

        # Writing parts of the book data into a csv
        with open(os.path.abspath('/home/cyneo/Work/Scans/Processed Data/Extracted CSV/' + lemmatized_file + '.csv'), 'w') as book_file:
            book_writer = csv.writer(book_file)
            book_writer.writerow(['Word'] +
                                 ['Frequency'] +
                                 ['In Hubness'] +
                                 ['Out Hubness'])

            for word in book_dictionary:
                book_writer.writerow([word] +
                                     [book_dictionary[word]['freq']] +
                                     [book_dictionary[word]['in_hubness']] +
                                     [book_dictionary[word]['out_hubness']])

        # Compiles main hubness
        for word in main_dict:
            # In hubness
            main_dict[word]['in_hubness'] = main_dict[word]['in_degree'] /\
                                            main_dict[word]['freq']
            # Out hubness
            main_dict[word]['out_hubness'] = main_dict[word]['out_degree'] /\
                                             main_dict[word]['freq']

        # Saves main dict into .p file
        pickle.dump(main_dict, open(filepath('Compiled',
                                             data='Data',
                                             filetype='p'),
                                    'wb'))


        # Replace the file names with function
        # Writes parts of the compiled data into csv
        with open(os.path.abspath('/home/cyneo/Work/Scans/Processed Data/Extracted CSV/Compiled Test.csv'), 'w') as main_file:
            main_writer = csv.writer(main_file)
            main_writer.writerow(['Word'] +
                                 ['Frequency'] +
                                 ['In Hubness'] +
                                 ['Out Hubness'])

            for word in main_dict:
                main_writer.writerow([word] +
                                     [main_dict[word]['freq']] +
                                     [main_dict[word]['in_hubness']] +
                                     [main_dict[word]['out_hubness']])
        # Create a way to systematically check if a book has already been added
        # a way to not add a book
        # an overwrite mode


def book_compile(lemmatized_file):
    book_dictionary = {}

    with open(filepath(lemmatized_file), 'r', encoding='utf8') as file:
        file_reader = csv.reader(file, delimiter='\t',
                                 quoting=csv.QUOTE_MINIMAL)

        for line in file_reader:
            for n in range(len(line)):
                try:
                    book_dictionary[line[n]]['freq'] += 1

                except KeyError:
                    book_dictionary[line[n]] = {'freq': 1,
                                                'in_degree': 0,
                                                'out_degree': 0,
                                                'predecessors': {},
                                                'successors': {}}

                # Takes care of the successors
                if n < len(line)-1:
                    try:
                        book_dictionary[line[n]]['successors'][line[n+1]] += 1
                        book_dictionary[line[n]]['out_degree'] += 1

                    except KeyError:
                        book_dictionary[line[n]]['successors'][line[n+1]] = 1
                        book_dictionary[line[n]]['out_degree'] += 1

                # takes care of the predecessors
                if n > 0 and n < len(line):
                    try:
                        book_dictionary[line[n]]['predecessors'][line[n-1]] += 1
                        book_dictionary[line[n]]['in_degree'] += 1

                    except KeyError:
                        book_dictionary[line[n]]['predecessors'][line[n-1]] = 1
                        book_dictionary[line[n]]['in_degree'] += 1

    # compile the hubness
    for word in book_dictionary:
        book_dictionary[word]['in_hubness'] = book_dictionary[word]['in_degree'] /\
                                              book_dictionary[word]['freq']
        book_dictionary[word]['out_hubness'] = book_dictionary[word]['out_degree'] /\
                                               book_dictionary[word]['freq']

    # Saving it to it's own unique .p file
    pickle.dump(book_dictionary, open(filepath(
        lemmatized_file, data='Data', filetype='p'), 'wb'))

    # Writing parts of the data into a csv
    with open(os.path.abspath('/home/cyneo/Work/Scans/Processed Data/test.csv'), 'w') as book_file:
        book_writer = csv.writer(book_file)
        book_writer.writerow(['Word'] +
                             ['Frequency'] +
                             ['In Hubness'] +
                             ['Out Hubness'])

        for word in book_dictionary:
            book_writer.writerow([word] +
                                 [book_dictionary[word]['freq']] +
                                 [book_dictionary[word]['in_hubness']] +
                                 [book_dictionary[word]['out_hubness']])
    

def plothub(filename):
            with open(os.path.abspath('/home/cyneo/Work/Scans/Processed Data/Extracted CSV/' + filename + '.csv'), 'w') as hub_file:
                hub_reader = csv.reader(hub_file)
                

def filepath(filename,
             data='Lemmatized Text',
             root='/home/cyneo/Work/Scans/Processed Data/',
             filetype='csv'):
    return os.path.abspath(root + data + '/' + filename +
                           ' ' + data + '.' + filetype)



# Add in another book and check that the hubness is in the valid range
# Modularise some parts (for next thing)
# Make a swtich for overwrites
# Making use of exceptions to test keys
# This is to avoid for loops and other methods to test keys
# that will lose the power of using indexed structures

testdict = {}
try:
    testdict['hello'] += 1

except KeyError:
    testdict['hello'] = 1

# BIG PROBLEM: But may be obselete
# Importing the dictionary to create a graph.
