from Lexer.token1 import Token


class ParserToken(object):
    def __init__(self, token, groupName:str=None):
        if groupName is not None:
            self.__groupName = groupName
        else:
            self.__groupName = token.getGroupName()

        self.__value = token.getValue()
        self.__index = token.getIndex()
        self.__indent = 0
        self.__contIndent = 0

    def getGroupName(self):
        return self.__groupName

    def getValue(self):
        return self.__value

    def setValue(self, value):
        self.__value = value

    def getIndex(self):
        return self.__index

    def setIndex(self, index):
        self.__index = index

    def getIndent(self):
        return self.__indent

    def setIndent(self, indent):
        self.__indent = indent

    def getContIndent(self):
        return self.__contIndent

    def setContIndent(self, contIndent):
        self.__contIndent = contIndent

if __name__ == '__main__':
    token = Token("sdfs", "shfh")

    p = ParserToken(token)
    p2 = ParserToken(token, "popo")

    o = 0