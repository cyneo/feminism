"""
TODO:


Creates a matrix to study how the data clusters
"""


from std_pack import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
import scipy.cluster.hierarchy as ch
import scipy.spatial.distance as dist

def compile_dictionary(list_of_books=None):x
    """
    Compiles unique words and saves them into pickles.
    Default is to compile all available books in class_data

    Can input a specific list as well
    """
    if list_of_books is None:
        list_of_books = os.listdir(class_data)[1:]  # Checks dir for updated list
        book_list = []  # This will be the list that is in the dictionary
        for pickle_name in list_of_books:
            pickle_data = load_book(pickle_name)  # Stores book class data
            # Checks if attribute exists
            # If True, add into book_list
            if attribute_checker(pickle_data, 'male_adj'):
                book_list.append(pickle_name)

        # Instantiate the class which would then compile the dicitonary,
        # with book_list saved as an attribute
        print('The following books were added into the master dictionaries:')
        print('\n'.join(book_list))
        word_master_list = Word_dicitionary(book_list)

        # Saving the class instance as a pickle
        with open(parse_dict + 'Master Word List.p',
                  'wb') as dump_file:
            pickle.dump(word_master_list, dump_file)

    else:
        save_name = input('Save as?\n--->')
        for pickle_name in list_of_books:
            pickle_data = load_book(pickle_name)  # Stores book class data
            # Instantiate the class which would then compile the dictionary,
            # with book_list saved as an attribute
            if attribute_checker(pickle_data, 'male_adj'):
                book_list.append(pickle_name)

        print('The following books were added into the' +
              save_name +
              ' dictionaries:')
        print('\n'.join(book_list))
        word_master_list = Word_dicitionary(book_list)

        # Saving the class instance as a pickle
        with open(parse_dict + save_name +
                  '.p', 'wb') as dump_file:
            pickle.dump(word_master_list, dump_file)
        # create a new attribute called sbook_list_y
        # attribute should be a list that holds the book list sorted by year of pub


def cluster1(placeholder='Master Word List', sort_by='year'):
    # So far the code only processes males terms and not female
    with open(parse_dict + placeholder + '.p', 'rb') as master_word_list_file:
        word_master_list = pickle.load(master_word_list_file)

    column_index = {'author': [], 'title': [], 'year':[]}
    with open(raw_path + 'Book Years', 'rb') as file:
        years = pickle.load(file)
        for book in word_master_list.book_list:
            author, title = book[1:].split('] ')
            column_index['author'].append(author)
            column_index['title'].append(title)
            column_index['year'].append(years[author][title])
            # create a tuple that is fed into the index

    # Initializing DataFrames
    m_df = pd.DataFrame(np.zeros((len(word_master_list.global_male_adjs),
                                  len(word_master_list.book_list))),
                        index=word_master_list.global_male_adjs,
                        columns=word_master_list.book_list)

    f_df = pd.DataFrame(np.zeros((len(word_master_list.global_female_adjs),
                                  len(word_master_list.book_list))),
                        index=word_master_list.global_female_adjs,
                        columns=word_master_list.book_list)

    # Adding frequencies into the df
    # Add in a progress bar maybe?
    for book in word_master_list.book_list:
        book_pickle = load_book(book + '.p')
        for word in book_pickle.male_adj.keys():
            m_df.loc[word, book] = book_pickle.male_adj[word]

        for word in book_pickle.female_adj.keys():
            f_df.loc[word, book] = book_pickle.female_adj[word]

    # m_corr = m_df.corr()
    m_pdist = dist.pdist(f_df.transpose(), 'correlation')
    m_link = ch.linkage(m_pdist, method='complete', metric='correlation')
    ch.dendrogram(m_link, orientation='right', leaf_font_size=2, labels=list(zip(column_index['year'], column_index['author'])))
    plt.show()


def cluster(placeholder='Master Word List', sort_by='year'):
    # So far the code only processes males terms and not female
    with open(parse_dict + placeholder + '.p', 'rb') as master_word_list_file:
        word_master_list = pickle.load(master_word_list_file)

    column_index = {'author': [], 'title': [], 'year':[]}
    with open(raw_path + 'Book Years', 'rb') as file:
        years = pickle.load(file)
        for book in word_master_list.book_list:
            author, title = book[1:].split('] ')
            column_index['author'].append(author)
            column_index['title'].append(title)
            column_index['year'].append(years[author][title])
            # create a tuple that is fed into the index

    # Initializing DataFrames
    m_df = pd.DataFrame(np.zeros((len(word_master_list.global_male_adjs),
                                  len(word_master_list.book_list))),
                        index=word_master_list.global_male_adjs,
                        columns=word_master_list.book_list)

    f_df = pd.DataFrame(np.zeros((len(word_master_list.global_female_adjs),
                                  len(word_master_list.book_list))),
                        index=word_master_list.global_female_adjs,
                        columns=word_master_list.book_list)

    # Adding frequencies into the df
    # Add in a progress bar maybe?
    for book in word_master_list.book_list:
        book_pickle = load_book(book + '.p')
        for word in book_pickle.male_adj.keys():
            m_df.loc[word, book] = book_pickle.male_adj[word]

        for word in book_pickle.female_adj.keys():
            f_df.loc[word, book] = book_pickle.female_adj[word]

    # m_corr = m_df.corr()
    m_pdist = dist.pdist(f_df.transpose(), 'correlation')
    m_link = ch.linkage(m_pdist, method='complete', metric='correlation')
    ch.dendrogram(m_link, orientation='right', leaf_font_size=2, labels=list(zip(column_index['year'], column_index['author'])))
    plt.show()

    """
    All these were to help get the correlation matrix. Replaced with pd.corr()
    # At this point, frequencies added into df
    # z score normalization
    n_m_df = pd.DataFrame(np.zeros((len(word_master_list.global_male_adjs),
                                    len(word_master_list.book_list))),
                          index=word_master_list.global_male_adjs,
                          columns=word_master_list.book_list)
    n_f_df = pd.DataFrame(np.zeros((len(word_master_list.global_female_adjs),
                                    len(word_master_list.book_list))),
                          index=word_master_list.global_female_adjs,
                          columns=word_master_list.book_list)

    for book in word_master_list.book_list:
        n_m_df[book] = (m_df[book] - m_df[book].mean())/m_df[book].std(ddof=0)
        n_f_df[book] = (f_df[book] - f_df[book].mean())/f_df[book].std(ddof=0)

    # Next is to transpose
    n_m_df_t = n_m_df.transpose()
    mmt = n_m_df.dot(n_m_df_t)  # Word to word matrix
    mtm = n_m_df_t.dot(n_m_df)  # Book to book matrix

    n_f_df_t = n_f_df.transpose()
    fft = n_f_df.dot(n_f_df_t)  # Word to word matrix
    ftf = n_f_df_t.dot(n_f_df)  # Book to book matrix
    return m_df

    # Next to plot a color map of everything
    fig, ((m_bk, f_bk), (m_wd, f_wd)) = plt.subplots(2, 2)

    m_bk_im = m_bk.imshow(mtm)
    m_bk.set_title('Male Adj Between Books')
    m_bk_divider = make_axes_locatable(m_bk)
    m_bk_cax = m_bk_divider.append_axes("right", size='10%', pad=0.05)
    m_bk_cbar = plt.colorbar(m_bk_im, cax=m_bk_cax)

    m_wd_im = m_wd.imshow(mmt)
    m_wd.set_title('Male Adj Between Words')
    m_wd_divider = make_axes_locatable(m_wd)
    m_wd_cax = m_wd_divider.append_axes("right", size='10%', pad=0.05)
    m_wd_cbar = plt.colorbar(m_wd_im, cax=m_wd_cax)

    f_bk_im = f_bk.imshow(ftf)
    f_bk.set_title('Female Adj Between Books')
    f_bk_divider = make_axes_locatable(f_bk)
    f_bk_cax = f_bk_divider.append_axes("right", size='10%', pad=0.05)
    f_bk_cbar = plt.colorbar(f_bk_im, cax=f_bk_cax)

    f_wd_im = f_wd.imshow(fft)
    f_wd.set_title('Female Adj Between Words')
    f_wd_divider = make_axes_locatable(f_wd)
    f_wd_cax = f_wd_divider.append_axes("right", size='10%', pad=0.05)
    f_wd_cbar = plt.colorbar(f_wd_im, cax=f_wd_cax)
    plt.show()
    """
    # Save the things


class Word_dicitionary():
    """
    When instantiated, will accept a list of books, open the pickles,
    and pull out all the data into a set.
    """
    def __init__(self, list_of_books):
        # self.save_name = input('Save dictionary as?\n--> ')
        self.book_list = [x[:-2] for x in list_of_books]
        self.global_male_adjs = set()
        self.global_female_adjs = set()
        for pickle_name in list_of_books:
            pickle_data = load_book(pickle_name)
            self.global_male_adjs = self.global_male_adjs |\
                                    set(pickle_data.male_adj.keys())
            self.global_female_adjs = self.global_female_adjs |\
                                      set(pickle_data.female_adj.keys())


def cluster_old(filename):
    """
    Things to have (not in order)
    Split into male, female, both
    Load adjs: In what form shall it be?
    Normalize values
    Form matrix (DataFrame?)
    """
    """
    The cluster code is to take in the data from multiple books.
    One axis is to contain the words, and the other is to take the books
    I already have similar code exisiting that is in a pandas DataFrame
    The code can be found in svd
    """
    """
    There are a few ways that can normalize:
    Based on the total number of words used on a male/female
    """
    try:
        main_dict = pickle.load(open(parse_dict +
                                     'Main Dictionary (adj).p', 'rb+'))

    except FileNotFoundError:
        main_dict = {}

    # Forming DataFrame
    book_list = []
    with open(parse_dict + 'List of Added Books.csv',
              'r+', encoding='utf-8') as books_file:
        book_list_reader = csv.reader(books_file, delimiter='\t',
                                      quoting=csv.QUOTE_MINIMAL)
        for line in book_list_reader:
            book_list.extend(line)

    word_list = [x for x in main_dict.keys()]
    df = pd.DataFrame(np.zeroes((len(word_list), len(book_list))),
                      index=word_list,
                      columns=book_list)

    print('Data Frame Made')

    """
    at this point, all the information that has been imported deal with collective
    data and not with individual books themselves. So after this point, the code
    should focus on importing individual books.
    """
    """
    WHen importing the data, got to mind what the keys are and how to do it
    """
    for book in book_list:
        pass
