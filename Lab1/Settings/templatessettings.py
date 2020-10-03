import json
from Settings.TabsAndIndents.tabsandindents import TabsAndIndentsSettings
from Settings.Spaces.spacessettings import SpacesSettings
from Settings.BlackLines.blacklinessettings import BlackLinesSettings
from Settings.Punktuation.punctuationsettings import PunctuationSettings


class TemplatesSettings(object):
    def __init__(self):
        with open("resources/templates-settings.json", "r") as settingsFile:
            settings = json.load(settingsFile)
            self.__tabsAndIndentsSettings = TabsAndIndentsSettings(settings["TabsAndIndents"])
            self.__spacesSettings = SpacesSettings(settings["Spaces"])
            self.__blackLinesSettings = BlackLinesSettings(settings["BlankLines"])
            self.__punctuationSettings = PunctuationSettings(settings["Punctuation"])

    def TabsAndIndentsSettings(self):
        return self.__tabsAndIndentsSettings

    def SpacesSettings(self):
        return self.__spacesSettings

    def BlackLinesSettings(self):
        return self.__blackLinesSettings

    def PunctuationSettings(self):
        return self.__punctuationSettings


if __name__ == '__main__':
    sets = TemplatesSettings()

    print(sets.TabsAndIndentsSettings().TabSize())
