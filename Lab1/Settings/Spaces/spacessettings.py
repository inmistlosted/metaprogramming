from Settings.Spaces.beforeleftbracesettings import BeforeLeftBraceSettings
from Settings.Spaces.withinsettings import WithinSettings
from Settings.Spaces.aroundoperatorssettings import AroundOperatorsSettings
from Settings.Spaces.beforekeywordssettings import BeforeKeywordsSettings
from Settings.Spaces.internaryoperatorsettings import InTernaryOperatorSettings
from Settings.Spaces.othersettings import OtherSettings
from Settings.Spaces.beforeparenthesessettings import BeforeParenthesesSettings


class SpacesSettings(object):
    def __init__(self, settings):
        self.__aroundOperatorsSettings = AroundOperatorsSettings(settings["AroundOperators"])
        self.__beforeParenthesesSettings = BeforeParenthesesSettings(settings["BeforeParentheses"])
        self.__beforeLeftBraceSettings = BeforeLeftBraceSettings(settings["BeforeLeftBrace"])
        self.__beforeKeywordsSettings = BeforeKeywordsSettings(settings["BeforeKeywords"])
        self.__withinSettings = WithinSettings(settings["Within"])
        self.__inTernaryOperatorSettings = InTernaryOperatorSettings(settings["InTernaryOperator"])
        self.__otherSettings = OtherSettings(settings["Other"])

    def AroundOperators(self):
        return self.__aroundOperatorsSettings

    def BeforeParentheses(self):
        return self.__beforeParenthesesSettings

    def BeforeLeftBrace(self):
        return self.__beforeLeftBraceSettings

    def BeforeKeywords(self):
        return self.__beforeKeywordsSettings

    def Within(self):
        return self.__withinSettings

    def InTernaryOperator(self):
        return self.__inTernaryOperatorSettings

    def Other(self):
        return self.__otherSettings
