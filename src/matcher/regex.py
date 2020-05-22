# Using Regex to find a keyword 
# in a given .txt files
import re

class Regex(object):
    def setTextAndPattern(self, text, pattern):
        self.text = text.lower()
        metaCharacter = '<([{\^-=$!|}])?*+.>'
        for char in metaCharacter:
            if (char in pattern):
                pattern = pattern.replace(char, '\\' + char)
        self.pattern = "(" + pattern.lower() + ")"

    def match(self):
        match = re.search(self.pattern, self.text)
        return 1 if match else -1