class FormatterToken(object):
    def __init__(self, token, helpGroupName:str=None):
        if helpGroupName is not None:
            self.__helpGroupName = helpGroupName
        else:
            self.__helpGroupName = ""

        self.__value = token.getValue()
        self.__index = token.getIndex()
        self.__groupName = token.getGroupName()
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

    def getHelpGroupName(self):
        return self.__helpGroupName

    def setHelpGroupName(self, helpGroupName):
        self.__helpGroupName = helpGroupName