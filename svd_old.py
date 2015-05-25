import numpy as np
from std_pack import *

x = np.random.random((5, 7))
# print(x)
j, k, l = np.linalg.svd(x)
print(k)

"""
Creating the matrix based on predetermining the size:
First step is to create the list of adjs
Each book should have it's own array for the words
I will approach it in the fashion of a predetermined adj list
and then import the book's own adjs
make use of a counter based on the adj list to get the values
"""

# Split the thing to 2 phases
# 1) processing the words
# 2) Do the SVD
# That way I can add books without running the svd over and over again


def compiler(books, gender, method):
    """
    Takes books and adds it to the existing database

    Checks that the title is not already in the database
    """
    book_list = []
    svd_path = '/home/cyneo/Work/Scans/Processed Data/Adj Extracts/SVD/'
    adj_path = '/home/cyneo/Work/Scans/Processed Data/Adj Extracts/'

    with open(os.path.abspath(svd_path + 'Processed Books.csv'),
              'r+', encoding='utf8') as book_list_file:
        book_list_reader = csv.reader(book_list_file)
        for line in book_list_reader:
            if line:
                book_list.append(line[0])

    books_to_overwrite = []
    new_book = []
    for book in books:
        if book in book_list:
            books_to_overwrite.append(book)

        else:
            new_book.append(book)

    if len(books_to_overwrite) > 0:
        print('The following have been added before:')
        for book in books_to_overwrite:
            print(book)
        overwrite_options = input('Choose overwrite option:\n' +
                                  'a - All\n' +
                                  'n - None\n' +
                                  's - Some\n' +
                                  'x---> ')
        if overwrite_options == 's':
            for book in books_to_overwrite:
                overwrite = input(
                    'Overwrite? ' + book + ' (y/n)\n')
                overwrite = overwrite_check(overwrite)
                if overwrite == 'y':
                    print(book + " data WAS updated")

                else:
                    print(book + " data WAS NOT updated")

    for book in new_book:
        print(new_book)
        gender = 'm'
        methods = ['0', '1', '2']
        for method in methods:
            add_book_data(adj_path, svd_path, book, gender, method)

            # Updating the book list.
            # Done at the end in case errors happen with the code,
            # hence confusing whether the book is actually done.
        with open(os.path.abspath(svd_path + 'Processed Books.csv'),
                  'w', encoding='utf8') as book_list_file:
            book_list_writer = csv.writer(book_list_file, delimiter='\t',
                                          quoting=csv.QUOTE_MINIMAL)
            book_list_writer.writerow([book])


def add_book_data(adj_path, svd_path, book, gender, method):
    with open(path(adj_path, book, gender, method),
              'r', encoding='utf8') as adjs:
        adjs_reader = csv.reader(adjs, delimiter='\t',
                                 quoting=csv.QUOTE_MINIMAL)
        adj_counter = collections.Counter()

        for line in adjs_reader:
            adj_counter[line[1]] += 1
                
    with open(path(svd_path, book, gender, method),
                      'w', encoding='utf8') as adj_str_file:
        adjs_str_writer = csv.writer(adj_str_file,
                                     delimiter='\t',
                                     quoting=csv.QUOTE_MINIMAL)
        for word in adj_counter.keys():
            adjs_str_writer.writerow([word] + [adj_counter[word]])


def remove_words():
    pass


def overwrite_check(overwrite):
    if overwrite != 'y' and overwrite != 'n':
        overwrite = input("Please enter y or n\n---> ")
        overwrite = overwrite_check(overwrite)

    return overwrite


def svd1(book, gender):
    """
    Will run through all 3 methods in one run
    Do both genders?
    """
    svd_path = '/home/cyneo/Work/Scans/Processed Data/Adj Extracts/SVD'
    with open(os.path.abspath(svd_path + 'Processed Books.csv'),
              'r+', encoding='utf8') as book_list:
        pass

    adj_list = False  # Opens a master list that updates with new books
    gender = gender_check
    A = np.zeros(len(book_list), len(adj_list))

    # Initialize the counter
    adj_counter = Counter(adj_list)
    for element in adj_counter.keys():
        adj_counter[element] = 0

    # Load the book that is supposed to be analyzed
    for book in book_list:
        nx.read_graphml(graphml_path(book, 0, gender))  # placeholder: 'a'

    # Using the counter to count for a particular book

    row_value = [x for x in adj_counter.values()]

# Maybe make the counter a new function


def path(root, book_name, gender, method):
    gender = gender_check(gender)
    gender = gender + ' Adj Extract '
    adj_type = gender + str(method)
    path = os.path.abspath(root + adj_type + '/' + book_name + ' '
                           + adj_type + '.csv')

    return path


def gender_check(gender):
    if gender == 'm':
        gender = 'Male'
    
    elif gender == 'f':
        gender = 'Female'

    else:
        gender = input("Please enter m for male, f for female \n ---> ")
        gender = gender_check(gender)

    return gender
