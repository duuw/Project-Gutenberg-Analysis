#!/usr/bin/env python
from string import punctuation
import collections
import nltk
import sys
import re
import numpy as np

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
        takes in .txt file
        returns text from given file
        '''
        with open(file, 'r') as f:
            text = f.read()

        return text

    def tokenize(self, text):
        '''
        tokenizes text, removing punctuation marks
        '''
        punct = set(punctuation)
        punct.add("--")
        punct.add("''")
        punct.add("``")
        punct.add("...")
        toks = nltk.word_tokenize(text)
        newToks = []
        for tok in toks:
            # remove punctuation and numbers
            if tok not in punct and not tok.isnumeric():
                newToks.append(tok.lower())
        return newToks


    def checkFilename(self):
        if not self.filename:
            sys.exit('.txt novel not known')


    def separateChapters(self):
        '''
        separates novel by chapters and stores corresponding text to chapter
        '''
        # read novel, separate by chapter
        # for each chapter, have a dictionary of word:count
        with open(self.filename, 'r') as f:
            text = f.read()
        text = text.replace('\n', ' ')
        chapters = re.split("CHAPTER [0-9]+\.", text, flags=re.IGNORECASE)[1:]
        self.chapters = chapters
        for idx, words in enumerate(chapters,start=1):
            toks = self.tokenize(words)
            counts = collections.Counter(toks)
            self.wordsByChapter[idx] = counts


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
        returns total number of unique words
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
        returns the 20 most frequently used words in the novel and 
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


    def get20MostInterestingFrequentWords(self, filterN=100):
        '''
        filters the most common 100 English words and then returns 
        the 20 most frequently used words and the number of times they were used. 
        '''
        self.checkFilename()
        commonFile = '1-1000.txt'
        with open(commonFile, 'r') as f:
            commonWords = f.read().splitlines()

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
        returns the 20 LEAST frequently used
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
        returns array of size equal to the number of chapters
        '''
        self.checkFilename()
        self.separateChapters()
        word = word.lower()
        chaps = []
        for ch, counts in self.wordsByChapter.items():
            if word in counts:
                chaps.append(counts[word])
            else:
                chaps.append(0) 
        print(sum(chaps))
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
        print(quote)
        size = len(quote)
        for ch, words in enumerate(self.chapters, start=1):
            toks = self.tokenize(words)
            toks = ' '.join(toks)
            if quote in toks:
                return ch 

        # quote not found in novel
        return -1



    def generateSentence(self):

        '''
        generate a sentence word by word by start with the word ‘The’ 
        returns a randomly generated sentence with 20 words
        '''
        self.checkFilename()
        if not self.allWords:
            text = self.readFile(self.filename)
            self.allWords = self.tokenize(text)

        # look through words and save words that follow (with counts)
        bigrams = self.findBigrams()

        word = 'the'
        sentence = ['The']
        while len(sentence) < 20:
            # obtain probabilities based on counts
            words = [(w,c) for w,c in bigrams[word].items()]
            total = sum([c for w,c in words])
            probs = [float(c/total) for w,c in words]
            # randomly pick next word
            arr = np.random.choice(len(words), 1, p=probs)
            word = words[arr[0]][0]
            sentence.append(word)

        final = ' '.join(sentence)
        return "'" + final + "'"


    def findBigrams(self):
        '''
        creates a dictionary of bigrams with word frequencies
        '''
        bigrams = collections.defaultdict(dict)

        for w1, w2 in zip(self.allWords, self.allWords[1:]):
            if w1 not in bigrams:
                bigrams[w1][w2] = 0
            elif w2 not in bigrams[w1]:
                bigrams[w1][w2] = 0
            bigrams[w1][w2] += 1

        return bigrams

