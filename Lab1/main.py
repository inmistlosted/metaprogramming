import re
from filereader import FileReader
from Lexer.lexer import Lexer
from Formatter.formatter import Formatter


templatesNames = ['TabsAndIndents', 'Spaces', 'Punctuation', 'All']

if __name__ == '__main__':
    while True:
        print('python JavaScriptFormatter ', end='')
        command = input()

        if command == '-h':
            print('\n-f [template name] [path to file] - enter template name to be used in formatting and path to file to be formatted')
            print('   available templates: TabsAndIndents, Spaces, BlackLines, Punctuation')
            print('-v [path to file] - enter path to file to be analyzed')
            print('-quit - enter to quit\n')
        elif command[0:2] == '-f':
            parts = command.split()

            if len(parts) != 3:
                print('unrecognized command')
            else:
                templateName = parts[1]
                path = parts[2]

                if templateName not in templatesNames:
                    print('unrecognized template')
                else:
                    if FileReader.isFile(path):
                        sourceCode = FileReader.readFile(path)
                        lexer = Lexer(sourceCode)
                        lexer.execute()
                        parser = Formatter("Formatting", lexer.getTokens(), templateName)
                        result = parser.execute()
                        resultFile = FileReader.writeToFile(path, result)
                        print('created file ' + resultFile)
                    else:
                        jsFiles = FileReader.getAllJsFiles(path)
                        for file in jsFiles:
                            sourceCode = FileReader.readFile(file)
                            lexer = Lexer(sourceCode)
                            lexer.execute()
                            parser = Formatter("Formatting", lexer.getTokens(), templateName)
                            result = parser.execute()
                            resultFile = FileReader.writeToFile(file, result)
                            print('created file ' + resultFile)
        elif command[0:2] == '-v':
            parts = command.split()

            if len(parts) != 2:
                print('unrecognized command')
            else:
                path = parts[1]
                if FileReader.isFile(path):
                    sourceCode = FileReader.readFile(path)
                    lexer = Lexer(sourceCode)
                    lexer.execute()
                    parser = Formatter("Error search", lexer.getTokens())
                    parser.execute()
                    print('Errors printed to file resources/logfile.txt')
                else:
                    jsFiles = FileReader.getAllJsFiles(path)
                    for file in jsFiles:
                        sourceCode = FileReader.readFile(file)
                        lexer = Lexer(sourceCode)
                        lexer.execute()
                        parser = Formatter("Error search", lexer.getTokens())
                        parser.execute()
                        print('Errors printed to file resources/logfile.txt')
        elif command == '-quit':
            break
        else:
            print('unrecognized command')

