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


inputTranslation = int(input('''
Apa yang ingin anda terjemahkan?
1. Indonesia - Sunda
2. Sunda - Indonesia
'''))
# inputTranslation = 1

# Read dictionary folder and read each dictionary text
dictFolder = FolderReader('dictionary')
dictReader = TextReader()
dictionary = dictReader.getFileContent(dictFolder.getFileByIndex(inputTranslation - 1))
leftSide, rightSide = splitDictionary(dictionary)

inputSentence = input('Apa yang ingin anda translate?\n')
# inputSentence = 'nama saya Riyugan'
sentenceAsArr = inputSentence.split(' ')

inputMatcher = int(input('''
Dengan algoritma apa anda menginginkan translator ini bekerja?
1. KMP
2. BM
'''))
# inputMatcher = 1
matcher = KMP_Algorithm() if inputMatcher == 1 else BM_Algorithm()

translated = []
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

print("Hasil translasi:")
print(' '.join(translated))

# TODO - 21-05-2020
# 1. Translate dua kata
# 2. Tambahkan/abaikan teh
# 3. Read Dictionary berdasarkan nama file (ubah dari yang bekas tucil 4)
# 4. Bikin modularitas, jadi pas diterapin ke web tinggal panggil satu fungsi
#    udah bisa langsung dapet hasil translasi (jangan bad kayak tucil)

# TODO SOON
# 1. Regex
# 2. Aplikasikan ke web (Nanti akan lebih dirinci)
# etc

# Opsional
# 1. Kasih suggestion