class AroundOperatorsSettings(object):
    def __init__(self, settings):
        self.__settings = settings

    def AssignmentOperators(self):
        return self.__settings["AssignmentOperators"]

    def LogicalOperators(self):
        return self.__settings["LogicalOperators"]

    def EqualityOperators(self):
        return self.__settings["EqualityOperators"]

    def RelationOperators(self):
        return self.__settings["RelationOperators"]

    def BitwiseOperators(self):
        return self.__settings["BitwiseOperators"]

    def AdditiveOperators(self):
        return self.__settings["AdditiveOperators"]

    def MultiplicativeOperators(self):
        return self.__settings["MultiplicativeOperators"]

    def ShiftOperators(self):
        return self.__settings["ShiftOperators"]

    def UnaryAdditiveOperators(self):
        return self.__settings["UnaryAdditiveOperators"]

    def ArrowFunction(self):
        return self.__settings["ArrowFunction"]

    def BeforeUnaryNot(self):
        return self.__settings["BeforeUnaryNot"]

    def AfterUnaryNot(self):
        return self.__settings["AfterUnaryNot"]