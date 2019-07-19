#!/usr/bin/env python

from analysis import *

file = '2701.txt'
n = NovelAnalysis()
print('total words', n.getTotalNumberOfWords(file))
print('unique', n.getTotalUniqueWords())
print('most frequent:', n.get20MostFrequentWords(file))
print()
print('most intr freq (100):', n.get20MostInterestingFrequentWords())
print()
print('most intr freq (200):', n.get20MostInterestingFrequentWords(200))
print()
print('most intr freq (300):', n.get20MostInterestingFrequentWords(300))
print()
print('least frequent:', n.get20LeastFrequentWords())
print()
word = 'captain'
print('freq word:', word, n.getFrequencyOfWord(word))
print()
word = 'death'
print('freq word:', word, n.getFrequencyOfWord(word))
print()
word = 'ship'
print('freq word:', word, n.getFrequencyOfWord(word))
print()
word = 'ahab'
print('freq word:', word, n.getFrequencyOfWord(word))
print()
quote = 'it is not down in any map true places never are'
print('find quote (12)', quote, '\n', n.getChapterQuoteAppears(quote))
print()
quote = 'I try all things I achieve what I can'
print('find quote (79)', quote, '\n', n.getChapterQuoteAppears(quote))
print()
quote = 'ignorance is the parent of fear'
print('find quote (3)', quote, '\n' ,n.getChapterQuoteAppears(quote))
print()
for i in range(15):
    print('sentence:', n.generateSentence())
    print()

