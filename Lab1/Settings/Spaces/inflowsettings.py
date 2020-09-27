class InFlowSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def BeforeTypeReferenceColon(self):
        return self.__settings["BeforeTypeReferenceColon"]

    def AfterTypeReferenceColon(self):
        return self.__settings["AfterTypeReferenceColon"]

    def ObjectLiteralTypeBraces(self):
        return self.__settings["ObjectLiteralTypeBraces"]

    def UnionAndIntersectionTypes(self):
        return self.__settings["UnionAndIntersectionTypes"]