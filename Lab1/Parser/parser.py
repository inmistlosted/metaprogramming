from Lexer.token1 import Token
from Parser.parsertoken import ParserToken
from Settings.templatessettings import TemplatesSettings


class Parser(object):
    def __init__(self, tokens):
        self.__lexerTokens = tokens
        self.__settings = TemplatesSettings()
        self.__tokens = []
        self.__getParserTokens()

    def execute(self):
        self.__applyIndents()

        result = ""

        for token in self.__tokens:
            tokenIndent = self.__getIndentView(token.getIndent(), token.getContIndent())

            tokenValue = list(token.getValue())

            for i in range(0, len(tokenValue)):
                if tokenValue[i] == '#':
                    tokenValue[i] = '\n' + tokenIndent

            tokenString = ''
            tokenString = tokenString.join(tokenValue)
            tokenResult = tokenString

            result += tokenResult

        return result

    def __applyIndents(self):
        indentLevel = 0
        contIndent = 0
        skipped = False
        isChained = False
        isGroupChained = False

        for i in range(0, len(self.__tokens)):
            self.__tokens[i].setIndent(indentLevel)
            self.__tokens[i].setContIndent(contIndent)

            if isChained and self.__settings.TabsAndIndentsSettings().IndentChainedMethod():
                self.__tokens[i].setIndent(indentLevel+1)
                if self.__tokens[i].getValue() == ";":
                    isChained = False

            if isGroupChained and skipped:
                self.__tokens[i].setIndent(indentLevel+1)
            else:
                isGroupChained = False

            if i != len(self.__tokens)-1 and self.__tokens[i].getGroupName() == "new line" and self.__tokens[i+1].getGroupName() == "new line":
                if not self.__settings.TabsAndIndentsSettings().KeepIndentsOnEmptyLines():
                    self.__tokens[i].setIndent(0)
                    self.__tokens[i].setContIndent(0)

            if self.__tokens[i].getValue() == "(":
                if i != len(self.__tokens)-1 and self.__tokens[i+1].getValue() == "{":
                    skipped = True
                    if self.__settings.TabsAndIndentsSettings().IndentAllChainedCallsInAGroup():
                        isGroupChained = True
                else:
                    contIndent += 1
            elif self.__tokens[i].getValue() == ")":
                if not skipped:
                    contIndent -= 1
                    if contIndent >= 0:
                        self.__tokens[i].setContIndent(contIndent)
                        self.__tokens[i - 1].setContIndent(contIndent)

                    if self.__hasChainedMethod(i):
                        isChained = True
                else:
                    skipped = False
                    isChained = True
            elif self.__tokens[i].getValue() == "{":
                indentLevel += 1
            elif self.__tokens[i].getValue() == "}":
                indentLevel -= 1
                if indentLevel >= 0:
                    self.__tokens[i].setIndent(indentLevel)
                    if not isGroupChained:
                        self.__tokens[i - 1].setIndent(indentLevel)
                    else:
                        self.__tokens[i - 1].setIndent(indentLevel+1)

            if indentLevel < 0:
                print("Syntacsis error")

            if contIndent < 0:
                print("Syntacsis error")

    def __getParserTokens(self):
        for i in range(0, len(self.__lexerTokens)):
            added = False
            if i != len(self.__lexerTokens) - 1:
                if self.__isFunctionCall(self.__lexerTokens[i], self.__lexerTokens[i + 1]):
                    self.__tokens.append(ParserToken(self.__lexerTokens[i], "function"))
                    added = True
            if not added:
                self.__tokens.append(ParserToken(self.__lexerTokens[i]))

    @staticmethod
    def __isFunctionCall(token, nextToken):
        if token.getGroupName() == "identifier" and nextToken.getValue() == "(":
            return True
        return False

    def __hasChainedMethod(self, index):
        for i in range(index, len(self.__tokens)):
            if i != 0 and self.__tokens[i-1].getGroupName() == "new line" and self.__tokens[i].getValue() == ".":
                return True
            elif i != 0 and self.__tokens[i-1].getGroupName() == "new line" and self.__tokens[i].getValue() != ".":
                return False
            elif self.__tokens[i].getValue() == ";":
                return False
        return False

    def __getIndentView(self, indent, contIndent):
        tokenIndent = ''
        indentViewSymbol = '-' if self.__settings.TabsAndIndentsSettings().UseTabsCharacter() else ' '
        defaultViewSymbol = ' '
        indentSize = contIndent * self.__settings.TabsAndIndentsSettings().ContinuationIndent() + indent * self.__settings.TabsAndIndentsSettings().Indent()

        for i in range(0, indentSize):
            if i < (
                    indentSize // self.__settings.TabsAndIndentsSettings().TabSize()) * self.__settings.TabsAndIndentsSettings().TabSize():
                tokenIndent += indentViewSymbol
            else:
                tokenIndent += defaultViewSymbol

        return tokenIndent
