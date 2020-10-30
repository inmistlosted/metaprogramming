class WithinSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def IndexAccessBrackets(self):
        return self.__settings["IndexAccessBrackets"]

    def GroupingParentheses(self):
        return self.__settings["GroupingParentheses"]

    def FunctionDeclarationParentheses(self):
        return self.__settings["FunctionDeclarationParentheses"]

    def FunctionCallParentheses(self):
        return self.__settings["FunctionCallParentheses"]

    def IfParentheses(self):
        return self.__settings["IfParentheses"]

    def ForParentheses(self):
        return self.__settings["ForParentheses"]

    def WhileParentheses(self):
        return self.__settings["WhileParentheses"]

    def SwitchParentheses(self):
        return self.__settings["SwitchParentheses"]

    def CatchParentheses(self):
        return self.__settings["CatchParentheses"]

    def ObjectLiteralBraces(self):
        return self.__settings["ObjectLiteralBraces"]

    def ES6ImportExportBraces(self):
        return self.__settings["ES6ImportExportBraces"]

    def ArrayBraces(self):
        return self.__settings["ArrayBraces"]

    def InterpolationExpressions(self):
        return self.__settings["InterpolationExpressions"]