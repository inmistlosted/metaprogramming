import json
from Settings.TabsAndIndents.tabsandindents import TabsAndIndentsSettings
from Settings.Spaces.spacessettings import SpacesSettings

class TemplatesSettings(object):
    def __init__(self):
        with open("resources/templates-settings.json", "r") as settingsFile:
            settings = json.load(settingsFile)
            self.__tabsAndIndentsSettings = TabsAndIndentsSettings(settings["TabsAndIndents"])
            self.__spacesSettings = SpacesSettings(settings["Spaces"])

    def TabsAndIndentsSettings(self):
        return self.__tabsAndIndentsSettings

    def SpacesSettings(self):
        return self.__spacesSettings


if __name__ == '__main__':
    sets = TemplatesSettings()

    print(sets.TabsAndIndentsSettings().TabSize())
