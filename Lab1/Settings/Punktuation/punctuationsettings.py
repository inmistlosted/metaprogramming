from Settings.Punktuation.semicolonstatementssettings import SemicolonStatementsSettings
from Settings.Punktuation.quotessettings import QuotesSettings


class PunctuationSettings(object):
    def __init__(self, settings):
        self.__semicolonStatementsSettings = SemicolonStatementsSettings(settings["SemicolonToTerminateStatements"])
        self.__quotesSettings = QuotesSettings(settings["Quotes"])
        self.__trailingComma = settings["TrailingComma"]

    def SemicolonStatementsSettings(self):
        return self.__semicolonStatementsSettings

    def QuotesSettings(self):
        return self.__quotesSettings

    def TrailingComma(self):
        return self.__trailingComma
