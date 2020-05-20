import os

class FolderReader(object):
    def __init__(self, foldername):
        self.foldername = foldername
        self.folderPath = os.path.join(os.getcwd(), os.pardir, foldername)
        self.files = os.listdir(self.folderPath)

    def printAllFile(self):
        for file in (self.files):
            print(file)

    def getFileByIndex(self, idxFile):
        filename = self.files[idxFile]
        return os.path.join(self.folderPath, filename)

class TextReader(object):
    def getFileContent(self, filename):
        lineList = list()
        with open(filename) as file:
            lineList = [line.replace('\u200b', '').replace('\n', '') for line in file]

        return lineList

    def getFileContentAsString(self, filename):
        return "".join(self.getFileContent(filename))