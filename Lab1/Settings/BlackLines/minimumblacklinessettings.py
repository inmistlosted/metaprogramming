class MinimumBlackLinesSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def AfterImports(self):
        return self.__settings["AfterImports"]

    def AroundClass(self):
        return self.__settings["AroundClass"]

    def AroundField(self):
        return self.__settings["AroundField"]

    def AroundMethod(self):
        return self.__settings["AroundMethod"]

    def AroundFunction(self):
        return self.__settings["AroundFunction"]