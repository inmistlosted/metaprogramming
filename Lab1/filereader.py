import os
import re

class FileReader(object):
    JS_FILE_EXTENSION = '.js'

    @staticmethod
    def getListOfFiles(dirName):
        listOfFiles = os.listdir(dirName)
        allFiles = list()

        for entry in listOfFiles:
            fullPath = os.path.join(dirName, entry)

            if os.path.isdir(fullPath):
                allFiles = allFiles + FileReader.getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)

        return allFiles

    @staticmethod
    def getAllJsFiles(dirPath):
        fileList = FileReader.getListOfFiles(dirPath)
        jsFiles = list()

        for fileName in fileList:
            fileExt = os.path.splitext(fileName)[1]

            if fileExt == FileReader.JS_FILE_EXTENSION:
                jsFiles.append(fileName)

        return jsFiles

    @staticmethod
    def readFile(filename):
        sourceFile = open(filename, 'r')
        sourceCode = ""

        while True:
            line = sourceFile.readline()
            if not line:
                break

            sourceCode += line[0:len(line) - 1]

            lineSymbols = list(line)
            if lineSymbols[len(line) - 1] == '\n':
                sourceCode += '#'
            else:
                sourceCode += lineSymbols[len(line) - 1]

            if re.search('//', line):
                sourceCode += '\n'


        return sourceCode

    @staticmethod
    def validatePath(path):
        return re.fullmatch(r'[A-Za-z]:/(\w+/?(\w+\.\w+)?)*', path)

    @staticmethod
    def isFile(name):
        return re.search(r'\.', name)

    @staticmethod
    def writeToFile(inputFileName, text):
        resultFile = open(inputFileName, 'w')
        resultFile.write(text)
        resultFile.close()

        return inputFileName
