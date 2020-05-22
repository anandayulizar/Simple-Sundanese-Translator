# Using Booyer Moore Algorithm to find a keyword 
# in a given .txt files

class BM_Algorithm(object):
    def preProcessing(self):
        tempSet = set(self.text)
        self.last = {}
        for i in (tempSet):
            self.last[i] = -1
        for i in range(len(self.pattern)):
            self.last[self.pattern[i]] = i
        

    def setTextAndPattern(self, text, pattern):
        self.text = text.lower()
        self.pattern = pattern.lower()
        self.fail = self.preProcessing()

    def match(self):
        idxMatch = -1
        found = False
        textLength = len(self.text)
        patternLength = len(self.pattern)
        i = patternLength - 1
        j = patternLength - 1

        if patternLength > 0:
            while (i < textLength and not found):
                if (self.text[i] == self.pattern[j]):
                    if (j == 0):
                        idxMatch = i
                        found = True
                        i += patternLength
                        j = patternLength - 1
                    else:
                        i -= 1
                        j -= 1
                else:
                    lo = self.last[self.text[i]]
                    i = i + patternLength - min(j, 1 + lo)
                    j = patternLength - 1
        return idxMatch