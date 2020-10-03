class BeforeLeftBraceSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def FunctionLeftBrace(self):
        return self.__settings["FunctionLeftBrace"]

    def IfLeftBrace(self):
        return self.__settings["IfLeftBrace"]

    def ElseLeftBrace(self):
        return self.__settings["ElseLeftBrace"]

    def ForLeftBrace(self):
        return self.__settings["ForLeftBrace"]

    def WhileLeftBrace(self):
        return self.__settings["WhileLeftBrace"]

    def DoLeftBrace(self):
        return self.__settings["DoLeftBrace"]

    def SwitchLeftBrace(self):
        return self.__settings["SwitchLeftBrace"]

    def TryLeftBrace(self):
        return self.__settings["TryLeftBrace"]

    def CatchLeftBrace(self):
        return self.__settings["CatchLeftBrace"]

    def FinallyLeftBrace(self):
        return self.__settings["FinallyLeftBrace"]

    def ClassLeftBrace(self):
        return self.__settings["ClassLeftBrace"]