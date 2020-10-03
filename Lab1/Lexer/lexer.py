import re
from Lexer.token1 import Token
from Lexer.dictionary import Dictionary


def sortByValLength(currStringTokens):
    return sorted(currStringTokens, key=lambda token: len(token.getValue()), reverse=True)


def sortByIndex(currStringTokens):
    return sorted(currStringTokens, key=lambda token: token.getIndex())


class Lexer(object):
    def __init__(self, sourceCode):
        self.__sourceCode = sourceCode
        self.__dictionary = Dictionary()
        self.__tokens = []

    def execute(self):
        codeWithNoComms = self.__findBigComments(self.__sourceCode)
        self.__currStringTokens = []
        currStringCopy = codeWithNoComms

        currStringCopy = self.__findComments(currStringCopy)
        currStringCopy = self.__findLiterals(currStringCopy)
        currStringCopy = self.__findSymbols(currStringCopy)
        currStringCopy = self.__findAllWords(currStringCopy)
        currStringCopy = self.__findNumbers(currStringCopy)
        currStringCopy = self.__findOperators(currStringCopy)
        currStringCopy = self.__findOperators(currStringCopy)
        currStringCopy = self.__findPunktMarks(currStringCopy)
        self.__findAllErrors(currStringCopy)
        self.__sortCurrStringTokens(codeWithNoComms)

        self.__tokens.extend(self.__currStringTokens)

    def getTokens(self):
        return self.__tokens

    def __findAllWords(self, string):
        pattern = r'\b[A-Za-z_]\w*\b'
        result = re.findall(pattern, string)

        for word in result:
            if self.__isKeyWord(word):
                self.__currStringTokens.append(Token("keyword", word))
            else:
                self.__currStringTokens.append(Token("identifier", word))
            matcher = re.search(word, string)
            string = string[0:matcher.start()] + string[matcher.end():]

        return string

    def __isKeyWord(self, word):
        for keyWord in self.__dictionary.getKeyWords():
            if word == keyWord:
                return True

        return False

    def __findBigComments(self, code):
        pattern = r'/\*.*?\*/'
        result = re.findall(r'/\*.*?\*/', code)

        for comment in result:
            self.__tokens.append(Token("comments", comment))

            comment = self.__replace(comment)
            matcher = re.search(comment, code)
            code = code[0:matcher.start()] + code[matcher.end():]

        return code

    def __findComments(self, string):
        pattern = r'//.*\n'
        result = re.findall(pattern, string)

        for comment in result:
            self.__tokenizeComment(comment)

            comment = self.__replace(comment)
            matcher = re.search(comment, string)
            string = string[0:matcher.start()] + string[matcher.end():]

        return string

    def __tokenizeComment(self, comment):
        self.__currStringTokens.append(Token("comments", comment[0:len(comment)-1]))

    def __findLiterals(self, string):
        pattern = r'\".*?\"'
        result = re.findall(pattern, string)

        for literal in result:
            self.__currStringTokens.append(Token("literal", literal))

            literal = self.__replace(literal)
            matcher = re.search(literal, string)
            string = string[0:matcher.start()] + string[matcher.end():]

        return string

    def __findSymbols(self, string):
        pattern = r'\'.*?\''
        result = re.findall(pattern, string)

        for symbol in result:
            matcher = re.search(symbol, string)
            string = string[0:matcher.start()] + string[matcher.end():]
            self.__currStringTokens.append(Token("symbolic constant", symbol))

        return string

    def __findNumbers(self, string):
        pattern = r'\b\d+\.?\d*\b'
        result = re.findall(pattern, string)

        for number in result:
            matcher = re.search(number, string)
            string = string[0:matcher.start()] + string[matcher.end():]
            self.__currStringTokens.append(Token("numeric constant", number))

        return string

    def __findOperators(self, string):
        pattern = r'(?:^|(?<=[^+&^|*/%<>=!?:-]))[+&^|*/%<>=!?:-][+&^|*/%<>=!?:-][+&^|*/%<>=!?:-](?=[^+&^|*/%<>=!?:-]|$)|(?:^|(?<=[^+&^|*/%<>=!?:-]))[+&^|*/%<>=!?:-][+&^|*/%<>=!?:-](?=[^+&^|*/%<>=!?:-]|$)|(?:^|(?<=[^+&^|*/%<>=!?:-]))[+&^|*/%<>=!?:-](?=[^+&^|*/%<>=!?:-]|$)'
        result = re.findall(pattern, string)
        lastEntry = 0

        for operator in result:
            if self.__isOperator(operator):
                self.__currStringTokens.append(Token("operator", operator))

                operator = self.__replace(operator)
                matcher = re.search(operator, string[lastEntry:])
                string = string[0:matcher.start()] + string[matcher.end():]
            else:
                operator = self.__replace(operator)
                matcher = re.search(operator, string[lastEntry:])
                lastEntry = matcher.end()

        return string

    def __isOperator(self, word):
        for operator in self.__dictionary.getOperators():
            if word == operator:
                return True
        return False

    def __findPunktMarks(self, string):
        pattern = r'[,.<>(){}\[\];]'
        result = re.findall(pattern, string)

        for mark in result:
            self.__currStringTokens.append(Token("punctuation mark", mark))

            mark = self.__replace(mark)
            matcher = re.search(mark, string)
            string = string[0:matcher.start()] + string[matcher.end():]

        return string

    def __findAllErrors(self, string):
        pattern = r'#'
        result = re.findall(pattern, string)

        for newLine in result:
            self.__currStringTokens.append(Token("new line", newLine))

            matcher = re.search(newLine, string)
            string = string[0:matcher.start()] + string[matcher.end():]

        string = re.sub('\s\s+', ' ', string)
        string = re.sub('\s*$', '', string)
        string = re.sub('^\s*', '', string)

        if string != '':
            errors = string.split(' ')
            for error in errors:
                self.__currStringTokens.append(Token("error", error))


    def __sortCurrStringTokens(self, currString):
        self.__currStringTokens = sortByValLength(self.__currStringTokens)
        letters = list(currString)

        for token in self.__currStringTokens:
            tokenVal = list(token.getValue())
            breakLoop = False

            for i in range(0, len(letters)-len(tokenVal)+1):
                if breakLoop:
                    break

                for j in range(0, len(tokenVal)):
                    if letters[i+j] != tokenVal[j]:
                        break
                    elif j == len(tokenVal)-1:
                        for k in range(0, len(tokenVal)):
                            letters[i+k] = '@'
                        token.setIndex(i)
                        breakLoop = True

        self.__currStringTokens = sortByIndex(self.__currStringTokens)

    def __replace(self, word):
        word = re.sub('\(', '\(', word)
        word = re.sub('\)', '\)', word)
        word = re.sub('\[', '\[', word)
        word = re.sub('\{', '\{', word)
        word = re.sub('\?', '\?', word)
        word = re.sub('\*', '\*', word)
        word = re.sub('\+', '\+', word)
        word = re.sub('\^', '\^', word)
        word = re.sub('\|', '\|', word)
        word = re.sub('\.', '\.', word)
        word = re.sub('\$', '\$', word)

        return word

    def printTokens(self):
        print("----- Sequence of tokens from source code -----")
        for token in self.__tokens:
            print("     " + token.toString())


if __name__ == '__main__':
    string = '"How many rows for your multiplication table?"'

    if re.search(r'"How many rows for your multiplication table?"', string) is None:
        print(1)
    else:
        print(2)

    for i in range(0, 5):
        print(i)

