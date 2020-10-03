import re
from filereader import FileReader
from Lexer.lexer import Lexer
from Parser.parser import Parser



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

templatesNames = ['TabsAndIndents', 'Spaces', 'BlackLines', 'Punctuation', 'a']

# Press the green button in the gutter to run the script.
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
                    if FileReader.validatePath(path) is None:
                        print('unrecognized path format')
                    else:
                        if FileReader.isFile(path):
                            sourceCode = FileReader.readFile(path)
                            lexer = Lexer(sourceCode)
                            lexer.execute()
                            parser = Parser(lexer.getTokens(), templateName)
                            result = parser.execute()
                            resultFile = FileReader.writeToFile(path, result)
                            print('created file ' + resultFile)
                        else:
                            jsFiles = FileReader.getAllJsFiles(path)
                            for file in jsFiles:
                                sourceCode = FileReader.readFile(path)
                                lexer = Lexer(sourceCode)
                                lexer.execute()
                                parser = Parser(lexer.getTokens(), templateName)
                                result = parser.execute()
                                resultFile = FileReader.writeToFile(path, result)
                                print('created file ' + resultFile)
        elif command[0:2] == '-v':
            parts = command.split()

            if len(parts) != 2:
                print('unrecognized command')
            else:
                path = parts[1]
                if FileReader.validatePath(path) is None:
                    print('unrecognized path format')
                else:
                    if FileReader.isFile(path):
                        sourceCode = FileReader.readFile(path)

                    else:
                        jsFiles = FileReader.getAllJsFiles(path)
                        for file in jsFiles:
                            sourceCode = FileReader.readFile(path)
        elif command == '-quit':
            break




        else:
            print('unrecognized command')




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
