import numpy as np
from std_pack import *
import pickle
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
"""
I need to compile the data from a book, compile into a central database
then do SVD on the database
I could do the book level in the parse side,
or i can read the graphml and then do the compilation from graphml

Convert graphml into a dictionary
Add the dictionary of the book to the main dictionary

The current data has nouns in them. It is useful for graphical
analysis. But they might affect the signal from SVD. Will take a look
and see if that is the case

I can start writing to accomodate both types, but fear of premature
optimization

"""

"""
ToDo:
1) Figure out how well DataFrame with string indices translates into
a numpy array for SVD, and how to get back the indices

2) Find a way to get the highest x number of singular values and get
the corresponting singluar vector

3) The results show very small s values on the order of -3. Accuracy
might be an issue.

edit: The s values went up significantly when males and females are done
separately, and the nouns are removed. Shows that there are no strong themes
in terms of nouns and adjs between genders. However very broad. So maybe
break into parts and then work on them individually and slowly mix and match
till satisfied.

4) Change the location of add books to the call for svd. Create overwrite
options Create option for copies of main dict, and (re)naming.
Checking for main dict should happen before the add book function.
The naming of main dict should then be passed into the add_book function since
the naming and saving happens in that function.

The words that are displayed are those that identified using the same order
of magnitude code

Current errors:


"""
        

def mass_run():
    books = ["[Andrew O'Hagan] Be Near Me",
             '[David Lodge] A Man of Parts',
             '[Graham Green] England Made Me',
             "[Hanif Kureishi] Gabriel's Gift",
             '[Hari Kunzru] Gods Without Men',
             '[Iain Sinclair] Dining on Stones',
             '[Ian McEwan] Amsterdam',
             '[Irvine Welsh] Ecstasy',
             '[Jonathan Coe] A Touch of Love',
             '[Kazuo Ishiguro] A Pale View of the Hills',
             '[Kingsley Amis] Ending Up',
             '[Malcolm Bradbury] Doctor Criminale',
             '[David Lodge] Author, Author',
             '[David Lodge] Changing Places',
             '[David Lodge] Deaf Sentence',
             '[David Lodge] Nice Work',
             '[David Lodge] Paradise News',
             '[David Lodge] The British Museum is Falling Down',
             '[David Lodge] Think',
             '[George Orwell] Keep the Aspidistra Flying',
             "[Hanif Kureishi] Gabriel's Gift",
             '[Hanif Kureishi] Love in a Blue Time',
             '[Hanif Kureishi] Midnight All Day',
             '[Hanif Kureishi] Midnight All Day',
             '[Hanif Kureishi] The Black Album',
             '[Hanif Kureishi] The Body',
             '[Hanif Kureishi] The Buddha of Suburbia',
             '[Hari Kunzru] Gods Without Men',
             '[Hari Kunzru] The Impressionist',
             '[Hari Kunzru] Transmission',
             '[Iain Sinclair] Dining on Stones',
             '[Iain Sinclair] Downriver',
             '[Iain Sinclair] Ghost Milk',
             '[Iain Sinclair] Hackney, that Rose-Red Empire',
             '[Iain Sinclair] Lights Out for the Territory',
             '[Iain Sinclair] London Orbital',
             '[Iain Sinclair] White Chappell, Scarlet Tracings',
             '[Ian McEwan] Amsterdam',
             '[Ian McEwan] Enduring Love',
             '[Ian McEwan] First Love, Last Rites',
             '[Ian McEwan] In Between the Sheets',
             '[Irvine Welsh] Ecstasy',
             '[Jonathan Coe] A Touch of Love',
             '[Kazuo Ishiguro] A Pale View of the Hills']

    graham = ['[Graham Green] A Burnt-Out Case',
              '[Graham Green] A Sort of Life',
              '[Graham Green] England Made Me',
              '[Graham Green] Monsignor Quixote',
              '[Graham Green] Our Man in Havana',
              '[Graham Green] Stamboul Train',
              '[Graham Green] The Comedians',
              '[Graham Green] The End of the Affair',
              '[Graham Green] The Heart of the Matter',
              '[Graham Green] The Human Factor',
              '[Graham Green] The Ministry of Fear',
              '[Graham Green] The Power and the Glory']

    for book in books:
        add_book(book, 'adj')


def make_data_frame(gender, pos='adj'):
    """
    Creates dataframe that stores
    """
    main_dict = pickle.load(open(parse_dict + 'Main Dictionary (' +
                                 pos + ').p', 'rb+'))

    with open(parse_dict + 'List of Added Books.csv',
              'r+', encoding='utf8') as books_file:
        book_list_reader = csv.reader(books_file, delimiter='\t',
                                      quoting=csv.QUOTE_MINIMAL)
        book_list = []

        for line in book_list_reader:
            book_list.extend(line)

    # Importing the years
    with open(raw_path + 'Book Years.csv', 'r', encoding='utf8') as years:
        year_reader = csv.reader(years, delimiter='\t',
                                 quoting=csv.QUOTE_MINIMAL)
        year_dict = {}
        for author, book, year in year_reader:
            year_dict['[' + author + '] ' + book] = year

    years = []
    # Adding years to the books and turning it into tuples:
    print('This data set consists of:')
    for book in range(len(book_list)):
        years.append(year_dict[book_list[book]])
        book_list[book] = (book_list[book], year_dict[book_list[book]])
        print(book_list[book])

    book_list = sorted(book_list, key=lambda year: year[1])
    years = sorted(years)
    for year in years:
        year = int(year)
    

    # Define a word list to use as a hashable index
    word_list = []
    for key in main_dict.keys():
        word_list.append(key)

    df = pd.DataFrame(np.zeros((len(word_list), len(book_list))),
                      index=word_list,
                      columns=book_list)
    
    print('Data Frame made')
    for book in book_list:
        # open dictionary then parse through key value pairs
        if gender == 'm':
            book_dict = pickle.load(open(parse_dict + book[0] +
                                         '_male_' + pos + '.p', 'rb+'))
            for word in book_dict.keys():
                df.loc[word, book] = book_dict[word]

        elif gender == 'f':
            book_dict = pickle.load(open(parse_dict + book[0] +
                                         '_female_' + pos + '.p', 'rb+'))
            for word in book_dict.keys():
                df.loc[word, book] = book_dict[word]

        else:
            return make_data_frame(input('Please select m/f:\n--->'))

    print('Data Frame done, starting SVD')
    df.to_pickle(parse_dict + 'Main DataFrame ' +
                 gender + '_' + pos + '.pkl')
    
    # The implementation of SVD
    # This part onwards needs to be revised
    # Get it to end up saving 3D plots
    u, s, v = np.linalg.svd(df)  # Returns ndarrays

    print('SVD done')

    no_of_s_values = 0

    s_val_order_of_mag = order_of_mag(s[0])
    for value in s:
        if order_of_mag(value) >= s_val_order_of_mag - 1:
            no_of_s_values += 1

        else:
            break

    """
    save_as = input('Save SVD data as?\n--->')
    with open(parse_dict + save_as + '.csv', 'w', encoding='utf8') as svd_dat:
        svd_dat_writer = csv.writer(svd_dat, delimiter='\t',
                                    quoting=csv.QUOTE_MINIMAL)
    """

    years = [int(y) for y in years]
    # Saving all figures into a PDF
    pp = PdfPages(parse_dict + 'Graphs.pdf')
    plt.hist(years, bins=(max(years) - min(years) - 1))
    plt.title('Distribution of Publication Dates')
    pp.savefig()

    # Check order of mag for u_i
    # For each s value:
    for x in range(no_of_s_values):
        u_vector = pd.Series(u[:, x], index=word_list)
        v_vector = pd.Series(v[:, x], index=years)
        highest_order = None

        # Find the highest order in u_i
        for element in range(len(u_vector)):
            if u_vector[element] != 0:
                order = order_of_mag(u_vector[element])
                if highest_order is None:
                    highest_order = order
                elif order > highest_order:
                    highest_order = order
        """
        high_uij = []  # can be used to plot, after getting corresponding v
        word_n_u = []
        for element in range(len(u_vector)):
            if order_of_mag(u_vector[element]) ==\
               (highest_order or (highest_order - 1)):
                # high_uij.append(element)  # Gives index
                word_n_u.append((word_list[element], u_vector[element]))

        word_n_u = sorted(word_n_u, key=lambda u_val: u_val[1])
        """
        # Defining the axes
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Plotting
        ax.scatter(years,
                   v[x])

        # Proper labelling
        ax.set_xlabel('Published Year')
        ax.set_ylabel('v value')
        plt.title(('s' + str(x) + ' = ' + str(s[x])))
        pp.savefig()
    pp.close()

    pickle.dump()


def add_book(book, mode='adj'):
    # Opens a book list
    # Check if the book is in the book list
    # Creates a dictionary of the book (book_dict)
    # as well as a dictionary of words (main_dict)
    # Overwrite only affects the book's dictionary

    overwrite, book_list = book_check(book)
    if not overwrite:
        return('Process stopped due to overwrite option')

    # Conversion will not happen if overwrite option stops
    # So I wrote the conversion to overwrite dictionaries
    male_adjs, female_adjs = convert_book(book, mode)
    # use this to get time stamp: time.strftime("%H:%M %d/%m/%Y")

    # To DO: A way to reset the library
    # Opening main dictionary
    try:
        main_dict = pickle.load(open(parse_dict + 'Main Dictionary (' +
                                     mode + ').p', 'rb+'))

    except FileNotFoundError:
        main_dict = {}

    dict_list = [male_adjs, female_adjs]
    for dictionary in dict_list:
        for key in dictionary.keys():
            # print(key)
            try:
                main_dict[key]
            except KeyError:
                main_dict[key] = True

    pickle.dump(main_dict, open(parse_dict + 'Main Dictionary (' +
                                mode + ').p', 'wb'))
    pickle.dump(male_adjs, open(parse_dict + book +
                                '_male_' + mode + '.p', 'wb'))
    pickle.dump(female_adjs, open(parse_dict + book +
                                  '_female_' + mode + '.p', 'wb'))


def convert_book(book, mode='adj'):
    """
    Extracts node frequencies from graphml
    Outputs dictionary with words and frequencies as keys and values
    """
    # Open graphml from parse_path
    graph = nx.read_graphml(parse_path +
                            book + '_' + mode +
                            '.graphml')

    male_adjs = {}
    female_adjs = {}

    male_terms = ['he', 'his']
    female_terms = ['she', 'her']

    for edge in graph.edges():
        for male_term in male_terms:
            if male_term in edge:
                for word in edge:
                    try:
                        male_adjs[word] += 1
                    except KeyError:
                        male_adjs[word] = 1
                
        for female_term in female_terms:
            if female_term in edge:
                for word in edge:
                    try:
                        female_adjs[word] += 1
                    except KeyError:
                        female_adjs[word] = 1

    # doing it this way means that I will only grab things that are directly connected to
    # the terms. In affect this will be the adjs as that is how i made the graphs

    # Removing the male/female terms
    male_adjs.pop('he', None)
    male_adjs.pop('his', None)
    female_adjs.pop('her', None)
    female_adjs.pop('she', None)

    return male_adjs, female_adjs

    """
    # This method is made obselete as we want to decouple
    # the genders, and POS to look at gender + adj only.
    dictionary = {}
    for node in graph.nodes():
        # print(node, graph.node[node]['Frequency'])
        try:
            dictionary[node] = graph.node[node]['Frequency']
        
        except KeyError:
            print('The following node has a KeyError: ' + node)
        
    return dictionary
    """


def book_check(book):
    with open(parse_dict + 'List of Added Books.csv',
              'r+', encoding='utf8') as books_file:
        book_list_reader = csv.reader(books_file, delimiter='\t',
                                      quoting=csv.QUOTE_MINIMAL)
        book_list = []
        for line in book_list_reader:
            book_list.extend(line)
    
        if book in book_list:
            overwrite = overwrite_check(book +
                                        ' has already been added.' +
                                        ' Overwrite? (y/n)' +
                                        '\n--->')
            return overwrite, book_list
        else:
            book_list_writer = csv.writer(books_file, delimiter='\t',
                                          quoting=csv.QUOTE_MINIMAL)
            book_list_writer.writerow([book])
            return True, book_list
            # instead of appending it to the book list and then
            # writing it, i can simply append to the file

        
def overwrite_check(message):
    overwrite = input(message)
    if overwrite == 'y':
        return True

    elif overwrite == 'n':
        return False

    else:
        return overwrite_check('Please input y/n.\n--->')


def order_of_mag(number):
    if number == 0:
        return 0
    elif number < 0:
        return order_of_mag(-number)
    elif number < 1:
        return -(order_of_mag(1/number) + 1)
    else:
        return(math.floor(math.log10(number)))
