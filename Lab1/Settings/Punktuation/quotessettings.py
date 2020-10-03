class QuotesSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def Single(self):
        return self.__settings["Single"]

    def Always(self):
        return self.__settings["Always"]