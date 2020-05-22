from Utils.Reader import FolderReader, TextReader
from Algorithm.KMP_Algorithm import KMP_Algorithm
from Algorithm.BM_Algorithm import BM_Algorithm
from Algorithm.Regex import Regex
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
    tempAlt = []
    j = 0
    while (j < len(leftSide)):
        matcher.setTextAndPattern(leftSide[j], word)
        result = matcher.match()
        if (result != -1 and len(leftSide[j]) == len(word)):
            tempAlt.append(rightSide[j])
        j += 1
    return tempAlt

def translate(filename, inputSentence, inputMatcher):
    # Read dictionary folder and read each dictionary text
    dictFolder = FolderReader('dictionary')
    textReader = TextReader()
    dictionary = textReader.getFileContent(dictFolder.getFileByFilename(filename))
    leftSide, rightSide = splitDictionary(dictionary)

    stopWordsFolder = FolderReader('stopWords')
    stopWords = textReader.getFileContent(stopWordsFolder.getFileByFilename(filename))

    subjectFolder = FolderReader('subject')
    if (filename == 'sunda.txt'):
        subject = textReader.getFileContent(subjectFolder.getFileByFilename('indonesia.txt'))
        addTeh = False
    else:
        subject = textReader.getFileContent(subjectFolder.getFileByFilename('sunda.txt'))
        addTeh = True

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
        tempAlt = findWord(leftSide, rightSide, matcher, word)

        isMultiWord = False
        temp = i
        while (temp + 1 < len(sentenceAsArr) and not isMultiWord):
            checkMultiWord = findWord(leftSide, rightSide, matcher, word + ' '+ sentenceAsArr[temp + 1])
            if (len(checkMultiWord) > 0):
                tempAlt = list(checkMultiWord)
                word += ' '+ sentenceAsArr[temp + 1]
                i = temp + 1
                isMultiWord = True
            else:
                temp += 1
                word += ' '+ sentenceAsArr[temp]
        
        translated.append(tempAlt.pop(0)) if len(tempAlt) > 0 else translated.append(sentenceAsArr[i])
        if (len(tempAlt) > 0):
            alternatives[sentenceAsArr[i]] = tempAlt

        if (translated[len(translated) - 1] in subject and addTeh and i < len(translated) - 1):
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
        
    # if (isSentence):
    #     print(' '.join(translated))
    # else:
    #     for alternative in translated:
    #         print(alternative)
    #         if (alternative == translated[0] and len(translated) > 1):
    #             print('Alternatif lain:')