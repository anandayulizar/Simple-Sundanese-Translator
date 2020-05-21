from Reader import FolderReader, TextReader
from KMP_Algorithm import KMP_Algorithm
from BM_Algorithm import BM_Algorithm

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
    dictReader = TextReader()
    dictionary = dictReader.getFileContent(dictFolder.getFileByFilename(filename))
    leftSide, rightSide = splitDictionary(dictionary)

    # Split sentence to an array of words
    sentenceAsArr = inputSentence.split(' ')

    # Set the matcher to the choice of user
    matcher = KMP_Algorithm() if inputMatcher == 1 else BM_Algorithm()
    translated = []

    # Find the translation of each word
    for word in sentenceAsArr:
        found = False
        i = 0
        while (i < len(leftSide) and not found):
            matcher.setTextAndPattern(leftSide[i], word)
            result = matcher.matching()
            if (result != -1 and len(leftSide[i]) == len(word)):
                found = True
            else:
                i += 1
        translated.append(rightSide[i]) if found else translated.append(word)

    return ' '.join(translated)

if __name__ == '__main__':
    inputTranslation = int(input('Bahasa apa yang ingin anda terjemahkan? \n1. Indonesia \n2. Sunda \n'))
    dictionaryList = ['indonesia.txt', 'sunda.txt']
    filename = dictionaryList[inputTranslation - 1]

    inputSentence = input('Apa yang ingin anda translate? \n')
    # inputSentence = 'nama saya Riyugan'

    inputMatcher = int(input('Dengan algoritma apa anda menginginkan translator ini bekerja? \n1. KMP \n2. BM \n'))
    # inputMatcher = 1


    print("Hasil translasi:")
    translated = translate(filename, inputSentence, inputMatcher)
    print(translated)

# TODO - 21-05-2020
# 1. Translate dua kata
# 2. Tambahkan/abaikan teh
# 3. Read Dictionary berdasarkan nama file (ubah dari yang bekas tucil 4)

# TODO SOON
# 1. Regex
# 2. Aplikasikan ke web (Nanti akan lebih dirinci)
# etc

# Opsional
# 1. Kasih suggestion