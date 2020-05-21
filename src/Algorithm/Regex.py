# Using Regex to find a keyword 
# in a given .txt files
import re

class Regex(object):
    def setTextAndPattern(self, text, pattern):
        self.text = text.lower()
        self.pattern = "(" + pattern.lower() + ")"

    def matching(self):
        match = re.search(self.pattern, self.text)
        return 1 if match else -1