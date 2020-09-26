from Lexer.token1 import Token

class Parser(object):
    def __init__(self, tokens):
        self.__tokens = tokens

    def execute(self):
        result = ""

        for token in self.__tokens:
            tokenValue = list(token.getValue())

            for i in range(0, len(tokenValue)):
                if tokenValue[i] == '#':
                    tokenValue[i] = '\n'

            tokenString = ''
            tokenString = tokenString.join(tokenValue)
            tokenResult = ' ' + tokenString + ' '

            result += tokenResult

        return result
