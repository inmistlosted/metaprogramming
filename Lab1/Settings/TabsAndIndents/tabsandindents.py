class TabsAndIndentsSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def UseTabsCharacter(self):
        return self.__settings["UseTabsCharacter"]

    def TabSize(self):
        return self.__settings["TabSize"]

    def Indent(self):
        return self.__settings["Indent"]

    def ContinuationIndent(self):
        return self.__settings["ContinuationIndent"]

    def KeepIndentsOnEmptyLines(self):
        return self.__settings["KeepIndentsOnEmptyLines"]

    def IndentChainedMethod(self):
        return self.__settings["IndentChainedMethod"]

    def IndentAllChainedCallsInAGroup(self):
        return self.__settings["IndentAllChainedCallsInAGroup"]
