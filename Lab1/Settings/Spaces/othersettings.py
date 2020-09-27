class OtherSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def BeforeComma(self):
        return self.__settings["BeforeComma"]

    def AfterComma(self):
        return self.__settings["AfterComma"]

    def BeforeForSemicolon(self):
        return self.__settings["BeforeForSemicolon"]

    def BeforePropertyNameValueSeparator(self):
        return self.__settings["BeforePropertyNameValueSeparator"]

    def AfterPropertyNameValueSeparator(self):
        return self.__settings["AfterPropertyNameValueSeparator"]

    def AfterTriplePointsInRestSpread(self):
        return self.__settings["AfterTriplePointsInRestSpread"]

    def BeforeMultiplicationInGenerator(self):
        return self.__settings["BeforeMultiplicationInGenerator"]

    def AfterMultiplicationInGenerator(self):
        return self.__settings["AfterMultiplicationInGenerator"]