"""
Script that creates dendrograms. Wrote this to try writing scripts
"""

from std_pack import *
import scipy.cluster.hierarchy as ch

graph = nx.read_graphml(thesaurus_path +
                        'Thesaurus Graph.graphml')

words = graph.nodes()
words1 = []
for word in range(0, 100, 1):
    words1.append(words[word])
    words1.extend(graph[words[word]].keys())

pdist = np.identity(len(words1))
for start in words[:100]:
    for end in graph[start].keys():
        if pdist[words1.index(start)][words1.index(end)] != 1.:
            pdist[words1.index(start)][words1.index(end)] = 1.

plt.figure()
link = ch.linkage(pdist, method='single')
ch.dendrogram(link, orientation='right', labels=words)
plt.show()
