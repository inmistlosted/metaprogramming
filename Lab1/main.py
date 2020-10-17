import sys
from filereader import FileReader
from Lexer.lexer import Lexer
from Formatter.formatter import Formatter



if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) >= 1 and len(args) <= 3:
        command = args[0]
        if command == '-h':
            print('\n-f [path to template] [path to file] - enter path to template to be used in formatting(e.g. resources/templates-settings.json") and path to file to be formatted')
            print('-v [path to file] - enter path to file to be analyzed')
        elif command == '-f':
            templateName = args[1]
            path = args[2]
            if FileReader.isFile(path):
                sourceCode = FileReader.readFile(path)
                lexer = Lexer(sourceCode)
                lexer.execute()
                formatter = Formatter("Formatting", lexer.getTokens(), path, templateName)
                result = formatter.execute()
                resultFile = FileReader.writeToFile(path, result)
                print('created file ' + resultFile)
            else:
                jsFiles = FileReader.getAllJsFiles(path)
                for file in jsFiles:
                    sourceCode = FileReader.readFile(file)
                    lexer = Lexer(sourceCode)
                    lexer.execute()
                    formatter = Formatter("Formatting", lexer.getTokens(), file, templateName)
                    result = formatter.execute()
                    resultFile = FileReader.writeToFile(file, result)
                    print('created file ' + resultFile)

        elif command == '-v':
            path = args[1]
            if FileReader.isFile(path):
                sourceCode = FileReader.readFile(path)
                lexer = Lexer(sourceCode)
                lexer.execute()
                formatter = Formatter("Error search", lexer.getTokens(), path)
                formatter.execute()
                print('Errors printed to file resources/logfile.txt')
            else:
                jsFiles = FileReader.getAllJsFiles(path)
                for file in jsFiles:
                    sourceCode = FileReader.readFile(file)
                    lexer = Lexer(sourceCode)
                    lexer.execute()
                    formatter = Formatter("Error search", lexer.getTokens(), file)
                    formatter.execute()
                    print('Errors printed to file resources/logfile.txt')
        else:
            print('unrecognized command')
    else:
        print('unrecognized command')