#!/usr/bin/env python
from string import punctuation
import collections
import nltk
import sys
import re


class NovelAnalysis(object):
    """class for Project Gutenberg class NovelAnalysis"""
    def __init__(self):
        self.filename = ''
        self.chapterN = 0
        self.allWords = []
        self.sortedWords = []
        self.chapters = []
        self.uniqueWords = {}
        self.wordsByChapter = {}

    def readFile(self, file):
        '''
        takes in .txt file, tokenizes file, removes punctuation
        return revised tokens
        '''
        with open(file, 'r') as f:
            text = f.read()

        return text

    def tokenize(self, text):
        punct = set(punctuation)
        punct.add("--")
        punct.add("''")
        punct.add("``")
        punct.add("...")
        toks = nltk.word_tokenize(text)
        newToks = []
        for tok in toks:
            # remove punctuation
            if tok not in punct:
                newToks.append(tok.lower())
        return newToks


    def checkFilename(self):
        if not self.filename:
            sys.exit('.txt novel not known')


    def separateChapters(self):
        # read novel, separate by chapter
        # for each chapter, have a dictionary of word:count
        with open(self.filename, 'r') as f:
            text = f.read()
        text = text.replace('\n', ' ')
        chapters = re.split("CHAPTER [0-9]+\.", text, flags=re.IGNORECASE)[1:]
        self.chapters = chapters
        for idx, words in enumerate(chapters):
            toks = self.tokenize(words)
            counts = collections.Counter(toks)
            self.wordsByChapter[idx+1] = counts


    def getTotalNumberOfWords(self, file):
        '''
        takes in .txt file
        returns number of words in file
        '''
        self.filename = file
        text = self.readFile(file)
        toks = self.tokenize(text)
        self.allWords = toks
        return len(toks)


    def getTotalUniqueWords(self):
        ''' 
        return total number of unique words
        '''
        self.checkFilename()
        if not self.allWords:
            text = self.readFile(self.filename)
            self.allWords = self.tokenize(text)

        wordDict = {}
        for word in self.allWords:
            # encounter new word
            if word not in wordDict:
                wordDict[word] = 0
            wordDict[word] += 1

        self.uniqueWords = wordDict
        return len(wordDict)


    def get20MostFrequentWords(self, file):
        '''
        takes in a .txt file and returns an array of words and number of times
        they were used.
        return the 20 most frequently used words in the novel and 
        '''
        if not self.filename:
            self.filename = file
        if not self.allWords:
            text = self.readFile(self.filename)
            self.allWords = self.tokenize(text)
        if not self.uniqueWords:
            self.getTotalUniqueWords()

        freq = sorted(self.uniqueWords.items(), key=lambda kv: kv[1])
        self.sortedWords = freq[::-1]

        return self.sortedWords[:20]


    def get20MostInterestingFrequentWords(self):
        '''
        Implement a new algorithm that filters the most
        common 100 English words and then returns the 20 most frequently used
        words and the number of times they were used. 
        Since the list gives us 1000 words,
        feel free to tune your algorithm to filter the most common 100, 200,
        or 300 words and see how it affects the outcomes.
        '''
        self.checkFilename()
        commonFile = '1-1000.txt'
        with open(commonFile, 'r') as f:
            commonWords = f.read().splitlines()
        filterN = 100

        commonWords = [w.lower() for w in commonWords]
        commonWords = commonWords[:filterN]
   
        intrWords = []
        for word,count in self.sortedWords:
            if len(intrWords) == 20:
                break
            if word not in commonWords:
                intrWords.append([word,count])

        return intrWords


    def get20LeastFrequentWords(self):

        '''
        Returns the 20 LEAST frequently used
        words and the number of times they were used.
        '''
        self.checkFilename()
        if not self.sortedWords:
            self.get20MostFrequentWords(self.filename)

        return self.sortedWords[-20:]


    def getFrequencyOfWord(self, word):
        '''
        method that takes in a word and returns an array of the number of the times the 
        word was used in each chapter.
        Returns array of size equal to the number of chapters
        '''
        self.checkFilename()
        self.separateChapters()

        chaps = []
        for ch, counts in self.wordsByChapter.items():
            if word in counts:
                chaps.append(counts[word])
            else:
                chaps.append(0) 

        return chaps


    def getChapterQuoteAppears(self, quote):
        '''
        method takes in a string (the quote) and return a number (the chapter
        number) and be named getChapterQuoteAppears() . If the quote cannot be
        found in the book, your method should return -1.
        '''
        self.checkFilename()
        if not self.chapters:
            self.separateChapters()

        quote = self.tokenize(quote)
        quote = ' '.join(quote)
        size = len(quote)
        for ch, words in enumerate(self.chapters, start=1):
            toks = self.tokenize(words)
            toks = ' '.join(toks)
            if quote in toks:
                return ch 

        return -1



    def generateSentence(self):

        '''
        Many writers have a unique type of writing style that can be easily 
        recognized based on the types of words they use and their sentence 
        structures. For this part of the project, we want to generate a 
        sentence  in the author’s writing style. In order to do this, we 
        will generate a  sentence word by word. We will start off our
        sentence with the word ‘The’. To generate the rest of the sentence, 
        we will parse through the book, look for all the instances of the 
        word ‘the’, store the word that comes after ‘the’, then randomly 
        pick one of the words. We repeat this process
        20 times until we have randomly picked 19 other words to complete 
        our sentence
        '''
        word = 'the'
        sentence = 'The'


        return sentence

file = '2701.txt'
word = 'captain'
n = NovelAnalysis()
print('total words', n.getTotalNumberOfWords(file))
print('unique', n.getTotalUniqueWords())
print('most frequent', n.get20MostFrequentWords(file))
print()
print('most intr freq', n.get20MostInterestingFrequentWords())
print()
print('least frequent', n.get20LeastFrequentWords())
print()
print('freq word:', word, n.getFrequencyOfWord(word))
print()
quote = 'At day-break, the three mast-heads were punctually manned afresh.'
print('find quote (134)', quote, '\n' ,n.getChapterQuoteAppears(quote))
print()
quote = 'aye aye sir cheerily cried little'
print('find quote (48)', quote, '\n', n.getChapterQuoteAppears(quote))
print()









