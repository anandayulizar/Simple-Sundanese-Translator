from Utils.Reader import FolderReader, TextReader
from Algorithm.KMP_Algorithm import KMP_Algorithm
from Algorithm.BM_Algorithm import BM_Algorithm
from Algorithm.Regex import Regex

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

    # Find the translation of each word
    if (len(sentenceAsArr) > 1):
        # If the sentence contain more than one word
        i = 0
        while (i < len(sentenceAsArr)):
            found = False
            j = 0
            while (j < len(leftSide) and not found):
                matcher.setTextAndPattern(leftSide[j], sentenceAsArr[i])
                result = matcher.matching()
                if (result != -1 and len(leftSide[j]) == len(sentenceAsArr[i])):
                    found = True
                else:
                    j += 1
            translated.append(rightSide[j]) if found else translated.append(sentenceAsArr[i])
            if (translated[len(translated) - 1] in subject and addTeh):
                translated.append('teh')
            
            i += 1
            
    else:
        # if the sentence only contain one word
        i = 0
        while (i < len(leftSide)):
            matcher.setTextAndPattern(leftSide[i], sentenceAsArr[0])
            result = matcher.matching()
            if (result != -1 and len(leftSide[i]) == len(sentenceAsArr[0])):
                translated.append(rightSide[i])
            i += 1
        if len(translated) == 0:
            translated.append(sentenceAsArr[0]) 

    return translated, len(sentenceAsArr) - 1

if __name__ == '__main__':
    dictionaryList = ['indonesia.txt', 'sunda.txt']

    inputTranslation = int(input('Bahasa apa yang ingin anda terjemahkan? \n1. Indonesia \n2. Sunda \n'))
    # inputTranslation = 1
    filename = dictionaryList[inputTranslation - 1]

    inputSentence = input('Apa yang ingin anda translate? \n')
    # inputSentence = ' nama '

    inputMatcher = int(input('Dengan algoritma apa anda menginginkan translator ini bekerja? \n1. KMP \n2. BM \n3. Regex\n'))
    # inputMatcher = 1

    translated, isSentence = translate(filename, inputSentence, inputMatcher)
    print('Hasil translasi:')
    if (isSentence):
        print(' '.join(translated))
    else:
        for alternative in translated:
            print(alternative)
            if (alternative == translated[0] and len(translated) > 1):
                print('Alternatif lain:')
    

# TODO - 21-05-2020
# 1. Translate dua kata

# TODO SOON
# 1. Aplikasikan ke web (Nanti akan lebih dirinci)
# etc