"""
Code is intended to extract synonyms from Oxford dictionary.

Sidelined due to efficiency of scraping
"""

from std_pack import *
import copy

file = open(data_path + 'Oxford-Thesaurus-An-a-Z-Dictionary-of-Synonyms2.txt',
            encoding='utf-8')

file1 = open(data_path + 'Oxford-Thesaurus-An-a-Z-Dictionary-of-Synonyms3.txt',
             encoding='utf-8') 

"""
There should be something to check the form of each starting line.
If the line does not start in a particular form,
then bring up line for me to see.

There are two forms that I have identified so far:
1) Word definition in the form of
<word> <POS>. <sense number> <syn1>...: <example>. <sense number> <syn1>...

2) New POS for a word.
--<POS> <sense number> <syn1>...: <example>.

The fix will most likely be a regex pattern matching thing.
Read part 2 of Dive into Python

One possible  benefit of scripts is that the varibles are held so
I can fix errors
on the spot and continue iterators. I think.
"""
# This is making verbose patterns. Remember to add re.VERBOSE
# as an argument when using re.search
word_pattern = re.compile(r'''
(        # Start of word group
\b       # Start of word boundary
\D+?     # Any number of letters (non greedy)
\b       # End of word boundary
)        # End of word group
\s       # Single space
(        # Start of POS group
\b       # Start of word boundary
\D+?     # Any number of letters (non greedy)
\b       # End of word boundary
)        # End of POS group
\.       # Single period
''', re.VERBOSE)

# pos_pattern looks for the block after a POS is defined
pos_pattern = re.compile(r'''
\.       # Period from end of POS
\s       # Space after period
(.*)     # Group of everything
\.$      # Period at end of example sentence
''', re.VERBOSE)

sense_pattern = re.compile(r'''
(\d)     # Sense number
\s       # Space
(\D*)    # Synblock
\.       # Period for end of syn example
''', re.VERBOSE)

syn_pattern = re.compile(r'''
(\D*?)
[\,|:]
''', re.VERBOSE)

"""
How do I deal with POS that is on the next line?
I cannot go back.
So the best way is to join it to the parent, and then use a pattern to find
Either that or, scrape a site
Right now, I have information of all the senses of the words. But not way
to use that information in a meaningful manner.
"""

with open(data_path +
          'Oxford-Thesaurus-An-a-Z-Dictionary-of-Synonyms2.txt') as file:
    # Initializing stopcounter
    next(file)
    if 'stopcounter' not in locals():
        stopcounter = 0

    for n in range(stopcounter):
        next(file)

    for line in file:
        if word_pattern.search(line):
            word, pos = pattern.search(line).groups()
            synblocks = re.findall(sense_pattern, line)

            for sense, synblock in synblocks:
                syns = re.findall(syn_pattern, synblock)

            stopcounter += 1

        elif not pattern.search(line):
            pass


# re.findall(r'''(\D+?),''', x) This finds synonyms from synblocks problems: word right before eg
"""
'''
Script to join synonyms that have been broken at commas to be on the same line.
'''
with open(data_path + 'Oxford-Thesaurus-An-a-Z-Dictionary-of-Synonyms1.txt',
          'r', encoding='utf8') as read_here:
    with open(data_path +
              'Oxford-Thesaurus-An-a-Z-Dictionary-of-Synonyms2.txt',
              'w', encoding='utf8') as write_here:
        for line in read_here:
            if 'holding' in locals():
                write_here.write(holding[:-1] + ' ' + line)
                del holding
                print('ding')

            elif line[-2:-1] == ',':
                holding = line
                print('dong')

            else:
                write_here.write(line)
                print('piang')
"""
"""
'''
Script is used to bring words that are on a different line from their synonyms
to be on the same line. This is to make consistent rules for extraction later.
'''
with open(data_path + 'Oxford-Thesaurus-An-a-Z-Dictionary-of-Synonyms.txt',
          'r', encoding='utf8') as read_here:
    with open(data_path +
              'Oxford-Thesaurus-An-a-Z-Dictionary-of-Synonyms1.txt',
              'w', encoding='utf8') as write_here:
        for line in read_here:
            if 'holding' in locals():
                write_here.write(holding[:-1] + ' ' + line)
                del holding
                print('ding')

            elif ' ' in line:
                write_here.write(line)
                print('dong')

            elif ' ' not in line:
                holding = line
                print('piang')
"""


'''
Script is used to bring next pos to the first POS

Check line, and then join to cache_line if it fits the --n pattern
Do not write until the current line is not $--
'''
with open(data_path + 'Oxford-Thesaurus-An-a-Z-Dictionary-of-Synonyms2.txt',
          'r', encoding='utf8') as read_here:
    with open(data_path +
              'Oxford-Thesaurus-An-a-Z-Dictionary-of-Synonyms3.txt',
              'w', encoding='utf8') as write_here:
        lines = read_here.readlines()
        for n in range(len(lines)):
            if re.search(word_pattern, lines[n]):
                
'''
if it fits the pattern, then hold it until meet the pattern again. Not a good idea cos of the 1.12 that i saw
i want to delete these sorts of things away
do i throw everything into classes and dictionaries?
'''

pos_list = ['adj',
            'v',
            'n']


class Thesaurus_word():
    '''
    Store thesaurus word data
    '''
    def __init__(self, word):
        self.word = word
        
    def :
        pass
