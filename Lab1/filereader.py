import os
import re
from Lexer.lexer import Lexer
from Parser.parser import Parser


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
            sourceCode += '#'
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
        directoryPath = re.match(r'[A-Za-z]:/(\w+/)*', inputFileName).group(0)
        fileName = inputFileName[len(directoryPath):]
        outputFile = fileName.split('.')
        outputFileName = outputFile[0] + '-formatted.' + outputFile[1]

        resultFile = open(directoryPath + outputFileName, 'w')
        resultFile.write(text)
        resultFile.close()

        return directoryPath + outputFileName


def main():
    print('Enter path to directory with js files: ')
    dirName = input()

    if dirName == '':
        dirName = os.getcwd()

    print(dirName)


if __name__ == '__main__':
    sourceCode = FileReader.readFile('resources/input-code.txt')
    lexer = Lexer(sourceCode)
    lexer.execute()
    parser = Parser(lexer.getTokens())
    result = parser.execute()

    resultFile = open('resources/output-code.txt', 'w')
    resultFile.write(result)
    resultFile.close()

    lexer.printTokens()
