class BeforeParenthesesSettings(object):
    def __init__(self, settings):
        self.__settings = settings

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

    def InFunctionExpression(self):
        return self.__settings["InFunctionExpression"]

    def InAsyncArrowFunction(self):
        return self.__settings["InAsyncArrowFunction"]