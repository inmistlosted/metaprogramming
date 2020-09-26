import os
import re
from Lexer.lexer import Lexer
from Parser.parser import Parser

JS_FILE_EXTENSION = '.js'


def getListOfFiles(dirName):
    listOfFiles = os.listdir(dirName)
    allFiles = list()

    for entry in listOfFiles:
        fullPath = os.path.join(dirName, entry)

        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def getAllJsFiles(dirPath):
    fileList = getListOfFiles(dirPath)
    jsFiles = list()

    for fileName in fileList:
        fileExt = os.path.splitext(fileName)[1]

        if fileExt == JS_FILE_EXTENSION:
            jsFiles.append(fileName)

    return jsFiles

def readFile():
    sourceFile = open('resources/input-code.txt', 'r')
    sourceCode = ""

    while True:
        line = sourceFile.readline()
        if not line:
            break

        sourceCode += line[0:len(line)-1]
        sourceCode += '#'
        if re.search('//', line):
            sourceCode += '\n'

    return sourceCode


def main():
    print('Enter path to directory with js files: ')
    dirName = input()

    if dirName == '':
        dirName = os.getcwd()

    print(dirName)


if __name__ == '__main__':
    sourceCode = readFile()
    lexer = Lexer(sourceCode)
    lexer.execute()
    parser = Parser(lexer.getTokens())
    result = parser.execute()

    resultFile = open('resources/output-code.txt', 'w')
    resultFile.write(result)
    resultFile.close()

    lexer.printTokens()
