class SemicolonStatementsSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def Use(self):
        return self.__settings["Use"]
