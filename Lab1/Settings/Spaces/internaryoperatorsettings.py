class InTernaryOperatorSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def BeforeQuestionMark(self):
        return self.__settings["BeforeQuestionMark"]

    def AfterQuestionMark(self):
        return self.__settings["AfterQuestionMark"]

    def BeforeDoublePoints(self):
        return self.__settings["BeforeDoublePoints"]

    def AfterDoublePoints(self):
        return self.__settings["AfterDoublePoints"]