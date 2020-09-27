class Token(object):
    def __init__(self, groupName, value):
        self.__groupName = groupName
        self.__value = value
        self.__index = 0

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

    def toString(self):
        return "{" + "'" + self.__groupName + "'" + " : '" + self.__value + "'" + "}"