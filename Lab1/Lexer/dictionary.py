class Dictionary(object):
    __dictionaryFileName = 'resources/dictionary.txt'

    def __init__(self):
        self.__initDictionary()

    def __initDictionary(self):
        dictionary = open(self.__dictionaryFileName, 'r')

        while True:
            line = dictionary.readline()
            if not line:
                break

            settings = line.split(":")
            if settings[0] == "keywords":
                self.__keywords = settings[1].split(",")
            elif settings[0] == "operators":
                self.__operators = settings[1].split(",")

    def getKeyWords(self):
        return self.__keywords

    def getOperators(self):
        return self.__operators