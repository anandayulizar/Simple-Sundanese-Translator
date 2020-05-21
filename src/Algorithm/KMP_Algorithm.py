# Using Knuth-Morris-Pratt (Algorithm) to find a keyword 
# in a given .txt files

class KMP_Algorithm(object):
    def preProcessing(self):
        textLength = len(self.text)
        fail = [0 for i in range(textLength)]

        j = 1
        while (j < textLength):
            k = j - 1
            itr = 0
            bk = 0
            while (itr < k):
                prefix = self.text[0:itr + 1]
                suffix = self.text[k - itr:k + 1]
                if (prefix == suffix):
                    bk = itr + 1
                itr += 1
            fail[j] = bk
            j += 1
        return fail

    def setTextAndPattern(self, text, pattern):
        self.text = text.lower()
        self.pattern = pattern.lower()
        self.fail = self.preProcessing()

    def matching(self):
        idxMatch = -1
        found = False
        patternLength = len(self.pattern)
        textLength = len(self.text)
        i = 0
        j = 0
        if patternLength > 0:
            while (i < textLength and not found):
                if (self.text[i] == self.pattern[j]):
                    if (j == patternLength - 1):
                        idxMatch = i -patternLength + 1
                        j = 0
                        found = True
                    else:
                        j += 1
                    i += 1
                elif (j > 0):
                    j = self.fail[j]
                else:
                    i += 1

        return idxMatch