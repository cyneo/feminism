#! /usr/local/python-3.4.3/bin/python3.4

from std_pack import *
import copy
from scipy import spatial, cluster


def clique_overlap(listofcliques):
    """
    To do the clique clique overlap, i will need to create a matrix
    of some sort and then add values to it.
    """
    # Initialize the matrix
    overlap_mat = np.ndarray((len(listofcliques), len(listofcliques)))

    # Calculating the overlap
    for m in range(len(listofcliques)):
        for n in range(len(listofcliques)):
            overlap_mat[m][n] = len(listofcliques[m] & listofcliques[n])

    # pickle.dump(overlap_mat, open(thesaurus_path +
    #                               'Clique Overlap Matrix.p',
    #                               'wb'),
    #             protocol=4)
    return overlap_mat


def hierarchical(graph):
    """
    I will need to take in a graph, find the cliques, then
    get the overlap, and then feed into the dendrogram

    # slicing indices
    index = Z['leaves']
    D = D[index,:]
    D = D[:,index]
    """
    listofcliques = clique_search(graph)
    overlap_mat = clique_overlap(listofcliques)
    # What i am tracking is theclique numbers and not the word numbers
    linkage_mat = scipy.cluster.hierarchy.linkage(overlap_mat,
                                                  method='complete')
    dendrogram = scipy.cluster.hierarchy.dendrogram(linkage_mat,
                                                    distance_sort='descending')
    plt.savefig(thesaurus_path + 'dendrogram.svg',
                format='svg', dpi=1200)
    node_order = dendrogram['leaves']
    overlap_mat = overlap_mat[node_order, :]
    overlap_mat = overlap_mat[:, node_order]
    fig = plt.figure()
    plt.imshow(overlap_mat)
    plt.savefig(thesaurus_path + 'implot of clique clique overlap.svg',
                format='svg', dpi=1200)
    plt.show()
    # return listofcliques
    pass


def sorted_adj_mat(overlap_mat, node_order=None, partitions=[], colors=[]):
    # G = nx.Graph(overlap_mat)
    # adjacency_matrix = nx.to_numpy_matrix(G, dtype=np.bool, nodelist=node_order)
    '''
    Need to find the node order using dendogram.
    
    '''
    linkage = scipy.cluster.hierarchy.linkage(overlap_mat,
                                              method='complete',
                                              metric='correlation')
    plt.subplot(1, 2, 1)
    # Get the leaves in descending order
    print(scipy.cluster.hierarchy.dendrogram(linkage,
                                             distance_sort='descending')['leaves'])
    plt.show()
    # Plot adjacency matrix in toned-down black and white
    fig = plt.figure(figsize=(5, 5))  # in inches
    plt.imshow(overlap_mat,
               interpolation="none")
    
    # The rest is just if you have sorted nodes by a partition and want to
    # highlight the module boundaries
    assert len(partitions) == len(colors)
    ax = plt.gca()
    for partition, color in zip(partitions, colors):
        current_idx = 0
        for module in partition:
            ax.add_patch(patches.Rectangle((current_idx, current_idx),
                                           len(module),  # Width
                                           len(module),  # Height
                                           facecolor="none",
                                           edgecolor=color,
                                           linewidth="1"))
            current_idx += len(module)
    plt.savefig(thesaurus_path + 'sorted adj mat.svg', format='svg', dpi=1200)


def something(k_value):
    sparse_overlap = pickle.load(open(thesaurus_path +
                                      'Sparse Overlap %s.p'
                                      % k_value,
                                      'rb'))
    m, n = sparse_overlap.shape
    clusters
    for m in range(m):
        for n in range(n):
            if n >= m:
                pass


def make_sparse(k_value, overlap_mat):
    for m in range(len(overlap_mat)):
        for n in range(len(overlap_mat)):
            if n == m and overlap_mat[m][n] == k_value:
                overlap_mat[m][n] = 1

            elif overlap_mat[m][n] >= k_value - 1:
                overlap_mat[m][n] = 1
        
    sparse_overlap = scipy.sparse.dok_matrix(overlap_mat)
    pickle.dump(sparse_overlap,
               open(thesaurus_path + 'Sparse Overlap %s.p' % k_value, 'wb'))
    pass


'''
cliques = pickle.load(open(thesaurus_path + 'cliques_nx.p', 'rb'))
cliques = [x for x in cliques if len(x) > 2]
clique_copy = copy.deepcopy(cliques)
for m in cliques:
    for n in cliques:
        if set(m).issubset(n) and m != n:
            clique_copy.remove(m)
'''

x = np.ndarray((6, 6))
x[0] = [5, 3, 2, 1, 3, 1]
x[1] = [3, 4, 2, 1, 1, 1]
x[2] = [2, 2, 3, 2, 1, 2]
x[3] = [1, 1, 2, 3, 0, 1]
x[4] = [3, 1, 1, 0, 4, 2]
x[5] = [1, 1, 2, 1, 2, 4]

# Graph from Palla
testg = nx.read_graphml(thesaurus_path + 'palla.graphml')

# Erdos Renyi model
ertest = nx.erdos_renyi_graph(30, 0.5)

# Small world model
smtest = nx.watts_strogatz_graph(30, 15, 0.5)

# Mini Graph
miniGraph = nx.read_graphml(data_path + 'mini graph.graphml')

# Plotting the clique size distribution
# clique_sizes = np.diagonal(overlap_mat)
# sorted_adj_mat(overlap_mat)
# del overlap_mat
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.hist(clique_sizes, bins=range(int(max(clique_sizes)) + 2))
# plt.title('Clique size distribution')
# plt.savefig(thesaurus_path + 'Degree Dist.png')


def clique_search_nx():
    G = nx.read_graphml(open(thesaurus_path + 'Thesaurus Graph.graphml'))
    cliques = list(nx.find_cliques(G))
    pickle.dump(cliques, open(thesaurus_path + 'cliques.p', 'wb'))


def clique_search(graph):
    """
    Clique overlap finding using Derenyi's method found in the nature
    supplementary information. Supposed to get equivalence of CFinder
    """
    """
    Method requirements:
    - k value

    Code to emulate CFinder

    Strategy is to find large compelte subgraphs in the network,
    then look for k-clique connected subgraphs
    Code is to do this:
    - Obtain all complete subgraphs (maximal cliques)
    - Clique clique overlap matrix
    - erase all off diagonal values less than k-1
    -> they cannot be in the same k-clique community


    - From what i see, clique finding with this method is sentitive to
    initial condition of the recursion.

    Benchmarking;
    Get the same results as posted in Palla's paper
    """
    max_deg = 0
    for node in graph.nodes():
        degree = graph.degree(node)
        if degree > max_deg:
            max_deg = degree

    cliques_ = set()

    def recursion(A, B, size):
        '''
        Recursion used to find cliques of size s
        - A would be a clique
        - B is the working list of nodes to check

        We don't have to worry about len(A) > size as we find from
        large to small. So bigger cliques would already have been found.
        Thus there is no need to do it as: if len(A) == size and len(B) == 0
        Because of startpoint, I don't need to worry about 'left out' nodes
        when stopping condition ending 'prematurely'
        '''
        if len(A) == size:
            # Clique of the correct size found
            return A

        # elifs are conditions of failure to find clique
        elif len(B) == 0:
            # Run out of neighbors, thus end
            pass

        else:  # Logic to transfer nodes to A
            A.append(B.pop(0))
            B = [x for x in graph.neighbors(A[-1]) if x in B]
            return recursion(A, B, size)
        pass

    # Finding the cliques
    for size in sorted(range(3, max_deg + 1), reverse=True):
        for node in graph.nodes():
            # If the degree is less than desired clique size, no way
            # it can be that size
            if graph.degree(node) >= size:
                A_orig = [node]
                B_orig = graph.neighbors(node)
                # The following loop is made to change starting point of
                # transfer into A list. This is done as I suspect that the
                # method is sensitive to intial condition
                for w in B_orig:
                    # Creating copies for recursion
                    A = copy.deepcopy(A_orig)
                    B = copy.deepcopy(B_orig)
                    # Adding start point w
                    A.append(B.pop(B.index(w)))
                    # Clearing out nodes that are not neighbors to w
                    B = [x for x in graph.neighbors(w) if x in B]
                    # Add to cliquesusing recursion
                    C = recursion(A, B, size)
                    if C:
                        cliques_.add(frozenset(C))

    cliques_ = sorted(cliques_, key=len, reverse=True)
    cliques = cliques_[:]

    for m in cliques_:
        for n in cliques_:
            if set(m).issubset(set(n)) and m != n:
                cliques.remove(m)
                break
    cliques = [x for x in cliques if len(x) >= 3]
    return cliques
    # pickle.dump(cliques, open('cliques.p', 'wb'))


'''
if __name__ == "__main__":
    import sys
    something(int(sys.argv[1]))
'''
