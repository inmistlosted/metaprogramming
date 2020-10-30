class BeforeKeywordsSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def ElseKeyword(self):
        return self.__settings["ElseKeyword"]

    def WhileKeyword(self):
        return self.__settings["WhileKeyword"]

    def CatchKeyword(self):
        return self.__settings["CatchKeyword"]

    def FinallyKeyword(self):
        return self.__settings["FinallyKeyword"]