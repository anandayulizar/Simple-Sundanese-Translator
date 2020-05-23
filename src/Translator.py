from utils.reader import FolderReader, TextReader
from matcher.kmp_algorithm import KMP_Algorithm
from matcher.bm_algorithm import BM_Algorithm
from matcher.regex import Regex
import re

def mapTranslation(left, translation):
    # If left is equal to true, then map the left side of =
    # if False, map the right side of =
    equalsIdx = translation.index('=')
    return translation[:equalsIdx - 1] if left else translation[equalsIdx + 2:]

def splitDictionary(dictionary):
    # Map each of the left side and the right side of the dictionary
    leftSide = list(map(lambda x:mapTranslation(True, x), dictionary))
    rightSide = list(map(lambda x:mapTranslation(False, x), dictionary))

    return leftSide, rightSide

def findWord(leftSide, rightSide, matcher, word):
    # Find the word in the dictionary
    # And return the translation in array of results
    results = []
    j = 0
    while (j < len(leftSide)):
        matcher.setTextAndPattern(leftSide[j], word)
        result = matcher.match()
        if (result != -1 and len(leftSide[j]) == len(word)):
            results.append(rightSide[j])
        j += 1

    return results

def separateMark(word):
    # Remove punctuation mark that are in the list
    # from the word
    punctuationMark = [',', '.', '?', '!']
    tempMark = ''
    for mark in punctuationMark:
        if (mark in word):
            word = word.replace(mark, '')
            tempMark = mark
            break
    
    return word, tempMark

def translate(filename, inputSentence, inputMatcher):
    # Read dictionary folder and read each dictionary text
    dictFolder = FolderReader('dictionary')
    dictionary = dictFolder.getFileByFilename(filename)
    leftSide, rightSide = splitDictionary(dictionary)

    stopWordsFolder = FolderReader('stopWords')
    stopWords = stopWordsFolder.getFileByFilename(filename)

    subjectFolder = FolderReader('subject')
    if (filename == 'sunda.txt'):
        subject = subjectFolder.getFileByFilename('indonesia.txt')
        addStopWords = False
    else:
        subject = subjectFolder.getFileByFilename('sunda.txt')
        addStopWords = True

    # Split sentence to an array of words
    # Assumption: The sentence given contains a minimum of one word
    sentenceAsArr = inputSentence.split(' ')
    for word in sentenceAsArr:
        if (word in stopWords or word == ''):
            sentenceAsArr.remove(word)

    # Set the matcher to the choice of user
    matcher = KMP_Algorithm() if inputMatcher == 1 else BM_Algorithm() if inputMatcher == 2 else Regex()
    translated = []
    alternatives = {}

    # Find the translation of each word
    i = 0
    while (i < len(sentenceAsArr)):
        # found = False
        word = sentenceAsArr[i]        
        word, tempMark = separateMark(word)
        tempAlt = findWord(leftSide, rightSide, matcher, word)

        # Check for multi word tranlation that includes the current word
        # Example: tidak = henteu, tidak mau = embung
        isMultiWord = False
        tempIdx = i + 1
        multiWord = word
        while (tempIdx < len(sentenceAsArr) and not isMultiWord):
            multiWord += ' '+ sentenceAsArr[tempIdx]
            multiWord, tempMark2 = separateMark(multiWord)
            checkMultiWord = findWord(leftSide, rightSide, matcher, multiWord)
            if (len(checkMultiWord) > 0):
                tempAlt = list(checkMultiWord)
                i = tempIdx
                tempMark = tempMark2
                isMultiWord = True
                word = multiWord
            else:
                tempIdx += 1
                
        wordTranslation = (tempAlt.pop(0) if len(tempAlt) > 0 else word) + tempMark
        translated.append(wordTranslation)
        if (len(tempAlt) > 0):
            alternatives[word] = tempAlt

        if (translated[len(translated) - 1] in subject and addStopWords and i < len(sentenceAsArr) - 1):
            translated.append('teh')
        
        i += 1

    return translated, alternatives

if __name__ == '__main__':
    dictionaryList = ['indonesia.txt', 'sunda.txt']

    inputTranslation = int(input('Bahasa apa yang ingin anda terjemahkan? \n1. Indonesia \n2. Sunda \n'))
    filename = dictionaryList[inputTranslation - 1]

    inputSentence = input('Apa yang ingin anda translate? \n')

    inputMatcher = int(input('Dengan algoritma apa anda menginginkan translator ini bekerja? \n1. KMP \n2. BM \n3. Regex\n'))

    translated, alternatives = translate(filename, inputSentence, inputMatcher)
    print('Hasil translasi:')
    print(' '.join(translated))
    if (len(alternatives)> 0):
        print('Alternatif lain: ')
        for key, value in alternatives.items():
            print(key, end=': ')
            print(', '.join(value))