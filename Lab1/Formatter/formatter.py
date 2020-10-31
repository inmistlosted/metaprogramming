from Lexer.lexertoken import Token
from Formatter.formattertoken import FormatterToken
from Settings.templatessettings import TemplatesSettings
from datetime import datetime


class Formatter(object):
    def __init__(self, type, tokens, fileName, templateName:str=None):
        self.__lexerTokens = tokens
        self.__type = type
        self.__settings = TemplatesSettings(templateName)
        self.__tokens = []
        self.__getFormatterTokens()
        self.__templateName = templateName
        self.__fileName = fileName

    def execute(self):
        if self.__type == "Formatting":
            self.__applyNewLines()
            self.__applyIndents()
            self.__applySpaces()
            self.__applyPunctuation()

            result = ""

            for token in self.__tokens:
                tokenIndent = self.__getIndentView(token.getIndent(), token.getContIndent())

                tokenValue = list(token.getValue())

                for i in range(0, len(tokenValue)):
                    if tokenValue[i] == '#':
                        tokenValue[i] = '\n' + tokenIndent

                tokenString = ''
                tokenString = tokenString.join(tokenValue)
                tokenResult = tokenString

                result += tokenResult

            return result

        else:
            with open("resources/logfile.txt", "a") as logFile:
                now = datetime.now()
                logFile.write("---------- file name: " + self.__fileName + " ---- analysis time: " + now.strftime("%m/%d/%Y, %H:%M:%S") + " ----------\n")
            self.__getMistakes()
            self.__getParenthesesTypes()
            self.__getBracesTypes()
            self.__getKeywordsTypes()
            self.__getOperatorsTypes()
            self.__getOtherTypes()
            self.__getClosingTypes()
            self.__getPunktMarksTypes()
            return ""







    def __applyIndents(self):
        indentLevel = 0
        contIndent = 0
        skipped = False
        isChained = False
        isGroupChained = False

        for i in range(0, len(self.__tokens)):
            self.__tokens[i].setIndent(indentLevel)
            self.__tokens[i].setContIndent(contIndent)

            if isChained and self.__settings.TabsAndIndentsSettings().IndentChainedMethod():
                self.__tokens[i].setIndent(indentLevel+1)
                if self.__tokens[i].getValue() == ";":
                    isChained = False

            if isGroupChained and skipped:
                self.__tokens[i].setIndent(indentLevel+1)
            else:
                isGroupChained = False

            if i != len(self.__tokens)-1 and self.__tokens[i].getGroupName() == "new line" and self.__tokens[i+1].getGroupName() == "new line":
                if not self.__settings.TabsAndIndentsSettings().KeepIndentsOnEmptyLines():
                    self.__tokens[i].setIndent(0)
                    self.__tokens[i].setContIndent(0)

            if self.__tokens[i].getValue() == "(":
                if i != len(self.__tokens)-1 and self.__tokens[i+1].getValue() == "{":
                    skipped = True
                    if self.__settings.TabsAndIndentsSettings().IndentAllChainedCallsInAGroup():
                        isGroupChained = True
                else:
                    contIndent += 1
            elif self.__tokens[i].getValue() == ")":
                if not skipped:
                    contIndent -= 1
                    if contIndent >= 0:
                        self.__tokens[i].setContIndent(contIndent)
                        self.__tokens[i - 1].setContIndent(contIndent)

                    if self.__hasChainedMethod(i):
                        isChained = True
                else:
                    skipped = False
                    isChained = True
            elif self.__tokens[i].getValue() == "{":
                indentLevel += 1
            elif self.__tokens[i].getValue() == "}":
                indentLevel -= 1
                if indentLevel >= 0:
                    self.__tokens[i].setIndent(indentLevel)
                    if not isGroupChained:
                        self.__tokens[i - 1].setIndent(indentLevel)
                    else:
                        self.__tokens[i - 1].setIndent(indentLevel+1)

    def __applySpaces(self):
        self.__getParenthesesTypes()
        self.__getBracesTypes()
        self.__getKeywordsTypes()
        self.__getOperatorsTypes()
        self.__getOtherTypes()
        self.__getClosingTypes()
        self.__getPunktMarksTypes()

        for i in range(0, len(self.__tokens)):
            if self.__tokens[i].getHelpGroupName() == "function declaration parentheses":
                if self.__settings.SpacesSettings().BeforeParentheses().FunctionDeclarationParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Within().FunctionDeclarationParentheses():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "function call parentheses":
                if self.__settings.SpacesSettings().BeforeParentheses().FunctionCallParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Within().FunctionCallParentheses():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "if parentheses":
                if self.__settings.SpacesSettings().BeforeParentheses().IfParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Within().IfParentheses():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "for parentheses":
                if self.__settings.SpacesSettings().BeforeParentheses().ForParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Within().ForParentheses():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "while parentheses":
                if self.__settings.SpacesSettings().BeforeParentheses().WhileParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Within().WhileParentheses():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "switch parentheses":
                if self.__settings.SpacesSettings().BeforeParentheses().SwitchParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Within().SwitchParentheses():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "catch parentheses":
                if self.__settings.SpacesSettings().BeforeParentheses().CatchParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Within().CatchParentheses():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "function expression parentheses":
                if self.__settings.SpacesSettings().BeforeParentheses().InFunctionExpression():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "async arrow function parentheses":
                if self.__settings.SpacesSettings().BeforeParentheses().InAsyncArrowFunction():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "assignment operator":
                if self.__settings.SpacesSettings().AroundOperators().AssignmentOperators():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "logical operator":
                if self.__settings.SpacesSettings().AroundOperators().LogicalOperators():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "equality operator":
                if self.__settings.SpacesSettings().AroundOperators().EqualityOperators():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "relational operator":
                if self.__settings.SpacesSettings().AroundOperators().RelationOperators():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "bitwise operator":
                if self.__settings.SpacesSettings().AroundOperators().BitwiseOperators():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "additive operator":
                if self.__settings.SpacesSettings().AroundOperators().AdditiveOperators():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "multiplicative operator":
                if self.__settings.SpacesSettings().AroundOperators().MultiplicativeOperators():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "shift operator":
                if self.__settings.SpacesSettings().AroundOperators().ShiftOperators():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "unary additive operator":
                if self.__settings.SpacesSettings().AroundOperators().UnaryAdditiveOperators():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "arrow function":
                if self.__settings.SpacesSettings().AroundOperators().ArrowFunction():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "unary not operator":
                if self.__settings.SpacesSettings().AroundOperators().BeforeUnaryNot():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().AroundOperators().AfterUnaryNot():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "function left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().FunctionLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "if left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().IfLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "else left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().ElseLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "for left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().ForLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "while left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().WhileLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "do left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().DoLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "switch left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().SwitchLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "try left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().TryLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "catch left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().CatchLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "finally left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().FinallyLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "class left brace":
                if self.__settings.SpacesSettings().BeforeLeftBrace().ClassLeftBrace():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "else keyword":
                if self.__settings.SpacesSettings().BeforeKeywords().ElseKeyword():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "while keyword":
                if self.__settings.SpacesSettings().BeforeKeywords().WhileKeyword():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "catch keyword":
                if self.__settings.SpacesSettings().BeforeKeywords().CatchKeyword():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "finally keyword":
                if self.__settings.SpacesSettings().BeforeKeywords().FinallyKeyword():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "index access brackets":
                if self.__settings.SpacesSettings().Within().IndexAccessBrackets():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "grouping parentheses":
                if self.__settings.SpacesSettings().Within().GroupingParentheses():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "object literal braces":
                if self.__settings.SpacesSettings().Within().ObjectLiteralBraces():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "import export braces":
                if self.__settings.SpacesSettings().Within().ES6ImportExportBraces():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "array brackets":
                if self.__settings.SpacesSettings().Within().ArrayBraces():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "back index access brackets":
                if self.__settings.SpacesSettings().Within().IndexAccessBrackets():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back grouping parentheses":
                if self.__settings.SpacesSettings().Within().GroupingParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            if self.__tokens[i].getHelpGroupName() == "back function declaration parentheses":
                if self.__settings.SpacesSettings().Within().FunctionDeclarationParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back function call parentheses":
                if self.__settings.SpacesSettings().Within().FunctionCallParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back if parentheses":
                if self.__settings.SpacesSettings().Within().IfParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back for parentheses":
                if self.__settings.SpacesSettings().Within().ForParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back while parentheses":
                if self.__settings.SpacesSettings().Within().WhileParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back switch parentheses":
                if self.__settings.SpacesSettings().Within().SwitchParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back catch parentheses":
                if self.__settings.SpacesSettings().Within().CatchParentheses():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back object literal braces":
                if self.__settings.SpacesSettings().Within().ObjectLiteralBraces():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back import export braces":
                if self.__settings.SpacesSettings().Within().ES6ImportExportBraces():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "back array brackets":
                if self.__settings.SpacesSettings().Within().ArrayBraces():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "ternary if operator":
                if self.__settings.SpacesSettings().InTernaryOperator().BeforeQuestionMark():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().InTernaryOperator().AfterQuestionMark():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "ternary else operator":
                if self.__settings.SpacesSettings().InTernaryOperator().BeforeDoublePoints():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().InTernaryOperator().AfterDoublePoints():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "comma":
                if self.__settings.SpacesSettings().Other().BeforeComma():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Other().AfterComma():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "for semicolon":
                if self.__settings.SpacesSettings().Other().BeforeForSemicolon():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
            elif self.__tokens[i].getHelpGroupName() == "property name-value separator":
                if self.__settings.SpacesSettings().Other().BeforePropertyNameValueSeparator():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Other().AfterPropertyNameValueSeparator():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getHelpGroupName() == "generator sign":
                if self.__settings.SpacesSettings().Other().BeforeMultiplicationInGenerator():
                    self.__tokens[i].setValue(" " + self.__tokens[i].getValue())
                if self.__settings.SpacesSettings().Other().AfterMultiplicationInGenerator():
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")
            elif self.__tokens[i].getGroupName() == "keyword" or self.__tokens[i].getGroupName() == "identifier" or self.__tokens[i].getGroupName() == "symbolic constant" or self.__tokens[i].getGroupName() == "literal":
                if i + 1 < len(self.__tokens) and (self.__tokens[i+1].getGroupName() == "keyword" or self.__tokens[i+1].getGroupName() == "identifier" or self.__tokens[i+1].getGroupName() == "symbolic constant" or self.__tokens[i+1].getGroupName() == "literal"):
                    self.__tokens[i].setValue(self.__tokens[i].getValue() + " ")

    def __getFormatterTokens(self):
        for i in range(0, len(self.__lexerTokens)):
            self.__tokens.append(FormatterToken(self.__lexerTokens[i]))

    def __getParenthesesTypes(self):
        for index in range(0, len(self.__tokens)):
            if self.__tokens[index].getValue() == "(":
                i = index - 1
                while i != -1:
                    if self.__tokens[i].getGroupName() == "new line":
                        i -= 1
                    elif self.__tokens[i].getGroupName() == "identifier":
                        j = i - 1
                        while j != -1:
                            if self.__tokens[j].getGroupName() == "new line":
                                j -= 1
                            elif self.__tokens[j].getGroupName() == "keyword" and self.__tokens[j].getValue() == "function":
                                self.__tokens[index].setHelpGroupName("function declaration parentheses")
                                break
                            else:
                                self.__tokens[index].setHelpGroupName("function call parentheses")
                                break
                        break
                    elif self.__tokens[i].getGroupName() == "keyword":
                        if self.__tokens[i].getValue() == "if":
                            self.__tokens[index].setHelpGroupName("if parentheses")
                            break
                        elif self.__tokens[i].getValue() == "for":
                            self.__tokens[index].setHelpGroupName("for parentheses")
                            break
                        elif self.__tokens[i].getValue() == "while":
                            self.__tokens[index].setHelpGroupName("while parentheses")
                            break
                        elif self.__tokens[i].getValue() == "switch":
                            self.__tokens[index].setHelpGroupName("switch parentheses")
                            break
                        elif self.__tokens[i].getValue() == "catch":
                            self.__tokens[index].setHelpGroupName("catch parentheses")
                            break
                        elif self.__tokens[i].getValue() == "function":
                            self.__tokens[index].setHelpGroupName("function expression parentheses")
                            break
                        elif self.__tokens[i].getValue() == "async":
                            self.__tokens[index].setHelpGroupName("async arrow function parentheses")
                            break
                        else:
                            break
                    else:
                        self.__tokens[index].setHelpGroupName("grouping parentheses")
                        break

    def __getBracesTypes(self):
        for index in range(0, len(self.__tokens)):
            if self.__tokens[index].getValue() == "{":
                i = index - 1
                while i != -1:
                    if self.__tokens[i].getGroupName() == "new line":
                        i -= 1
                    elif self.__tokens[i].getValue() == ")":
                        j = i - 1
                        parenthesesLevel = 0
                        while j != -1:
                            if self.__tokens[j].getValue() == ")":
                                parenthesesLevel += 1
                            elif self.__tokens[j].getValue() == "(":
                                if self.__tokens[j].getHelpGroupName() == "function declaration parentheses" and parenthesesLevel == 0:
                                    self.__tokens[index].setHelpGroupName("function left brace")
                                    break
                                elif self.__tokens[j].getHelpGroupName() == "if parentheses" and parenthesesLevel == 0:
                                    self.__tokens[index].setHelpGroupName("if left brace")
                                    break
                                elif self.__tokens[j].getHelpGroupName() == "for parentheses" and parenthesesLevel == 0:
                                    self.__tokens[index].setHelpGroupName("for left brace")
                                    break
                                elif self.__tokens[j].getHelpGroupName() == "while parentheses" and parenthesesLevel == 0:
                                    self.__tokens[index].setHelpGroupName("while left brace")
                                    break
                                elif self.__tokens[j].getHelpGroupName() == "switch parentheses" and parenthesesLevel == 0:
                                    self.__tokens[index].setHelpGroupName("switch left brace")
                                    break
                                elif self.__tokens[j].getHelpGroupName() == "catch parentheses" and parenthesesLevel == 0:
                                    self.__tokens[index].setHelpGroupName("catch left brace")
                                    break
                                else:
                                    parenthesesLevel -= 1
                            j -= 1
                        break
                    elif self.__tokens[i].getGroupName() == "keyword":
                        if self.__tokens[i].getValue() == "else":
                            self.__tokens[index].setHelpGroupName("else left brace")
                            break
                        elif self.__tokens[i].getValue() == "do":
                            self.__tokens[index].setHelpGroupName("do left brace")
                            break
                        elif self.__tokens[i].getValue() == "try":
                            self.__tokens[index].setHelpGroupName("try left brace")
                            break
                        elif self.__tokens[i].getValue() == "finally":
                            self.__tokens[index].setHelpGroupName("finally left brace")
                            break
                        else:
                            break
                    elif self.__tokens[i].getGroupName() == "identifier":
                        self.__tokens[index].setHelpGroupName("class left brace")
                        break
                    else:
                        break

    def __getKeywordsTypes(self):
        for index in range(0, len(self.__tokens)):
            if self.__tokens[index].getGroupName() == "keyword":
                if self.__tokens[index].getValue() == "else":
                    self.__tokens[index].setHelpGroupName("else keyword")
                elif self.__tokens[index].getValue() == "while":
                    self.__tokens[index].setHelpGroupName("while keyword")
                elif self.__tokens[index].getValue() == "catch":
                    self.__tokens[index].setHelpGroupName("catch keyword")
                elif self.__tokens[index].getValue() == "finally":
                    self.__tokens[index].setHelpGroupName("finally keyword")

    def __getOperatorsTypes(self):
        for index in range(0, len(self.__tokens)):
            if self.__tokens[index].getGroupName() == "operator":
                if self.__tokens[index].getValue() == "=" or self.__tokens[index].getValue() == "+=" or self.__tokens[index].getValue() == "-=" or self.__tokens[index].getValue() == "/=" or self.__tokens[index].getValue() == "*=" or self.__tokens[index].getValue() == "%=":
                    self.__tokens[index].setHelpGroupName("assignment operator")
                elif self.__tokens[index].getValue() == "&&" or self.__tokens[index].getValue() == "||":
                    self.__tokens[index].setHelpGroupName("logical operator")
                elif self.__tokens[index].getValue() == "==" or self.__tokens[index].getValue() == "!=":
                    self.__tokens[index].setHelpGroupName("equality operator")
                elif self.__tokens[index].getValue() == "<" or self.__tokens[index].getValue() == ">" or self.__tokens[index].getValue() == ">=" or self.__tokens[index].getValue() == "<=":
                    self.__tokens[index].setHelpGroupName("relational operator")
                elif self.__tokens[index].getValue() == "&" or self.__tokens[index].getValue() == "|" or self.__tokens[index].getValue() == "^":
                    self.__tokens[index].setHelpGroupName("bitwise operator")
                elif self.__tokens[index].getValue() == "+" or self.__tokens[index].getValue() == "-":
                    self.__tokens[index].setHelpGroupName("additive operator")
                elif self.__tokens[index].getValue() == "*" or self.__tokens[index].getValue() == "/" or self.__tokens[index].getValue() == "%":
                    self.__tokens[index].setHelpGroupName("multiplicative operator")
                elif self.__tokens[index].getValue() == "<<" or self.__tokens[index].getValue() == ">>" or self.__tokens[index].getValue() == ">>>":
                    self.__tokens[index].setHelpGroupName("shift operator")
                elif self.__tokens[index].getValue() == "++" or self.__tokens[index].getValue() == "--":
                    self.__tokens[index].setHelpGroupName("unary additive operator")
                elif self.__tokens[index].getValue() == "=>":
                    self.__tokens[index].setHelpGroupName("arrow function")
                elif self.__tokens[index].getValue() == "!" or self.__tokens[index].getValue() == "!!":
                    self.__tokens[index].setHelpGroupName("unary not operator")

    def __getOtherTypes(self):
        for index in range(0, len(self.__tokens)):
            if self.__tokens[index].getValue() == "[":
                back = index - 1
                while back != -1:
                    if self.__tokens[back].getGroupName() == "new line":
                        back -= 1
                    elif self.__tokens[back].getGroupName() == "identifier":
                        self.__tokens[index].setHelpGroupName("index access brackets")
                        break
                    elif self.__tokens[back].getValue() == "=" or self.__tokens[back].getGroupName() == "punctuation mark":
                        self.__tokens[index].setHelpGroupName("array brackets")
                        break
                    else:
                        break
            elif self.__tokens[index].getValue() == "{":
                back = index - 1
                while back != -1:
                    if self.__tokens[back].getGroupName() == "new line":
                        back -= 1
                    elif self.__tokens[back].getValue() == "=" or (self.__tokens[back].getGroupName() == "punctuation mark" and self.__tokens[back].getValue() != ")"):
                        self.__tokens[index].setHelpGroupName("object literal braces")
                        break
                    elif self.__tokens[back].getValue() == "import" or self.__tokens[back].getValue() == "export":
                        self.__tokens[index].setHelpGroupName("import export braces")
                        break
                    else:
                        break
            elif self.__tokens[index].getGroupName() == "literal" or self.__tokens[index].getGroupName() == "symbolic constant":
                if self.__settings.SpacesSettings().Within().InterpolationExpressions():
                    letters = list(self.__tokens[index].getValue())
                    for i in range(0, len(letters)):
                        if i + 1 != len(letters) and letters[i] == '$' and letters[i+1] == '{':
                            j = i + 1
                            while j != len(letters)-1:
                                if letters[j] == '}':
                                    letters[i + 1] = '{ '
                                    letters[j] = ' }'
                                    break
                                j += 1
                    self.__tokens[index].setValue(''.join(letters))

    def __getPunktMarksTypes(self):
        for index in range(0, len(self.__tokens)):
            if self.__tokens[index].getValue() == ",":
                self.__tokens[index].setHelpGroupName("comma")
            elif self.__tokens[index].getValue() == "?":
                self.__tokens[index].setHelpGroupName("ternary if operator")
            elif self.__tokens[index].getValue() == ":":
                i = index - 1
                while i != -1:
                    if self.__tokens[i].getGroupName() == "new line":
                        i -= 1
                    elif self.__tokens[i].getValue() == "}" and self.__tokens[i].getHelpGroupName() == "object literal braces":
                        break
                    elif self.__tokens[i].getValue() == "{" and self.__tokens[i].getHelpGroupName() == "object literal braces":
                        self.__tokens[index].setHelpGroupName("property name-value separator")
                        break
                    elif self.__tokens[i].getValue() == "?" and self.__tokens[i].getHelpGroupName() == "ternary if operator":
                        self.__tokens[index].setHelpGroupName("ternary else operator")
                        break
                    i -= 1
            elif self.__tokens[index].getValue() == ";":
                i = index - 1
                while i != -1:
                    if self.__tokens[i].getGroupName() == "new line":
                        i -= 1
                    elif self.__tokens[i].getValue() == ")" and self.__tokens[i].getHelpGroupName() == "back for parentheses":
                        break
                    elif self.__tokens[i].getValue() == "(" and self.__tokens[i].getHelpGroupName() == "for parentheses":
                        self.__tokens[index].setHelpGroupName("for semicolon")
                        break
                    i -= 1
            elif self.__tokens[index].getValue() == "*":
                i = index - 1
                while i != -1:
                    if self.__tokens[i].getGroupName() == "new line":
                        i -= 1
                    elif self.__tokens[i].getValue() == "function" or self.__tokens[i].getValue() == "yield":
                        self.__tokens[index].setHelpGroupName("generator sign")
                        break
                    i -= 1

    def __getClosingTypes(self):
        for index in range(0, len(self.__tokens)):
            if self.__tokens[index].getValue() == "}":
                i = index - 1
                bracesLevel = 0
                while i != -1:
                    if self.__tokens[i].getValue() == "}":
                        bracesLevel += 1
                    elif self.__tokens[i].getValue() == "{":
                        if bracesLevel == 0:
                            self.__tokens[index].setHelpGroupName("back " + self.__tokens[i].getHelpGroupName())
                            break
                        else:
                            bracesLevel -= 1
                    i -= 1
                if bracesLevel < 0:
                    self.__printError(index, "Wrong '{' position")
                elif bracesLevel > 0:
                    self.__printError(index, "Wrong '}' position")
            elif self.__tokens[index].getValue() == ")":
                i = index - 1
                parenthesesLevel = 0
                while i != -1:
                    if self.__tokens[i].getValue() == ")":
                        parenthesesLevel += 1
                    elif self.__tokens[i].getValue() == "(":
                        if parenthesesLevel == 0:
                            self.__tokens[index].setHelpGroupName("back " + self.__tokens[i].getHelpGroupName())
                            break
                        else:
                            parenthesesLevel -= 1
                    i -= 1
                if parenthesesLevel < 0:
                    self.__printError(index, "Wrong '(' position")
                elif parenthesesLevel > 0:
                    self.__printError(index, "Wrong ')' position")
            elif self.__tokens[index].getValue() == "]":
                i = index - 1
                bracketsLevel = 0
                while i != -1:
                    if self.__tokens[i].getValue() == "]":
                        bracketsLevel += 1
                    elif self.__tokens[i].getValue() == "[":
                        if bracketsLevel == 0:
                            self.__tokens[index].setHelpGroupName("back " + self.__tokens[i].getHelpGroupName())
                            break
                        else:
                            bracketsLevel -= 1
                    i -= 1
                if bracketsLevel < 0:
                    self.__printError(index, "Wrong '[' position")
                elif bracketsLevel > 0:
                    self.__printError(index, "Wrong ']' position")







    def __hasChainedMethod(self, index):
        for i in range(index, len(self.__tokens)):
            if i != 0 and self.__tokens[i-1].getGroupName() == "new line" and self.__tokens[i].getValue() == ".":
                return True
            elif i != 0 and self.__tokens[i-1].getGroupName() == "new line" and self.__tokens[i].getValue() != ".":
                return False
            elif self.__tokens[i].getValue() == ";":
                return False
        return False

    def __getIndentView(self, indent, contIndent):
        tokenIndent = ''
        indentViewSymbol = '-' if self.__settings.TabsAndIndentsSettings().UseTabsCharacter() else ' '
        defaultViewSymbol = ' '
        indentSize = contIndent * self.__settings.TabsAndIndentsSettings().ContinuationIndent() + indent * self.__settings.TabsAndIndentsSettings().Indent()

        for i in range(0, indentSize):
            if i < (
                    indentSize // self.__settings.TabsAndIndentsSettings().TabSize()) * self.__settings.TabsAndIndentsSettings().TabSize():
                tokenIndent += indentViewSymbol
            else:
                tokenIndent += defaultViewSymbol

        return tokenIndent

    def __setElementsBlackLines(self):
        self.__getParenthesesTypes()
        self.__getBracesTypes()
        self.__getKeywordsTypes()
        self.__getOperatorsTypes()
        self.__getOtherTypes()
        self.__getClosingTypes()
        self.__getPunktMarksTypes()

        self.__setImportBlackLines()
        self.__setClassStartBlackLines()
        self.__setClassEndBlackLines()


    def __setImportBlackLines(self):
        toBreak = 0
        startPos = 0

        while toBreak != len(self.__tokens)-1:
            blackLinesCount = 0
            blackLinesStart = 0

            for i in range(startPos, len(self.__tokens)):
                if self.__tokens[i].getGroupName() == "keyword" and self.__tokens[i].getValue() == "import":
                    j = i + 1
                    while j != len(self.__tokens):
                        if self.__tokens[j].getValue() == ";":
                            if j + 1 != len(self.__tokens):
                                blackLinesStart = j + 1
                            l = j + 1
                            while l != len(self.__tokens) and self.__tokens[l].getGroupName() == "new line":
                                blackLinesCount += 1
                                l += 1
                            break
                        j += 1
                    break
                toBreak = i

            if toBreak != len(self.__tokens)-1:
                del self.__tokens[blackLinesStart:blackLinesStart+blackLinesCount]
                for i in range (blackLinesStart, blackLinesStart + self.__settings.BlackLinesSettings().MinimumBlackLinesSettings().AfterImports()+1):
                    self.__tokens.insert(i, FormatterToken(Token("new line", "#")))
                startPos = blackLinesStart+blackLinesCount

    def __setClassStartBlackLines(self):
        toBreak = 0
        startPos = 0

        while toBreak != len(self.__tokens)-1:
            blackLinesCount = 0
            blackLinesStart = 0

            for i in range(startPos, len(self.__tokens)):
                if self.__tokens[i].getHelpGroupName() == "class left brace":
                    j = i - 1
                    while j != -1:
                        if self.__tokens[j].getGroupName() == "new line":
                            if j - 1 != -1:
                                blackLinesStart = j - 1
                            l = j - 1
                            while l != -1 and self.__tokens[l].getGroupName() == "new line":
                                blackLinesCount += 1
                                l -= 1
                            startPos = i+1
                            break
                        j -= 1
                    break
                toBreak = i

            if toBreak != len(self.__tokens) - 1:
                del self.__tokens[blackLinesStart-blackLinesCount:blackLinesStart]
                for i in range (blackLinesStart-blackLinesCount, blackLinesStart-blackLinesCount + self.__settings.BlackLinesSettings().MinimumBlackLinesSettings().AroundClass()):
                    self.__tokens.insert(i, FormatterToken(Token("new line", "#")))

    def __setClassEndBlackLines(self):
        toBreak = 0
        startPos = 0

        while toBreak != len(self.__tokens)-1:
            blackLinesCount = 0
            blackLinesStart = 0

            for i in range(startPos, len(self.__tokens)):
                if self.__tokens[i].getHelpGroupName() == "back class left brace":
                    j = i + 1
                    while j != len(self.__tokens):
                        if self.__tokens[j].getGroupName() == "new line":
                            if j + 1 != len(self.__tokens):
                                blackLinesStart = j + 1
                            l = j + 1
                            while l != len(self.__tokens) and self.__tokens[l].getGroupName() == "new line":
                                blackLinesCount += 1
                                l += 1
                            break
                        j += 1
                    break
                toBreak = i

            if toBreak != len(self.__tokens) - 1:
                del self.__tokens[blackLinesStart:blackLinesStart + blackLinesCount]
                for i in range(blackLinesStart,
                               blackLinesStart + self.__settings.BlackLinesSettings().MinimumBlackLinesSettings().AroundClass()):
                    self.__tokens.insert(i, FormatterToken(Token("new line", "#")))
                startPos = blackLinesStart + blackLinesCount

    def __setFieldStartBlackLines(self):
        while True:
            blackLinesCount = 0
            blackLinesStart = 0

            for i in range(0, len(self.__tokens)):
                if self.__tokens[i].getHelpGroupName() == "class left brace":
                    j = i - 1
                    while j != -1:
                        if self.__tokens[j].getGroupName() == "new line":
                            if j - 1 != -1:
                                blackLinesStart = j - 1
                            l = j - 1
                            while l != -1 and self.__tokens[l].getGroupName() == "new line":
                                blackLinesCount += 1
                                l -= 1
                            break
                        j -= 1
                    break

            del self.__tokens[blackLinesStart-blackLinesCount:blackLinesStart]
            for i in range (blackLinesStart-blackLinesCount, blackLinesStart-blackLinesCount + self.__settings.BlackLinesSettings().MinimumBlackLinesSettings().AroundClass()):
                self.__tokens.insert(i, FormatterToken(Token("new line", "#")))

    def __setFieldEndBlackLines(self):
        while True:
            blackLinesCount = 0
            blackLinesStart = 0

            for i in range(0, len(self.__tokens)):
                if self.__tokens[i].getHelpGroupName() == "back class left brace":
                    j = i + 1
                    while j != len(self.__tokens):
                        if self.__tokens[j].getGroupName() == "new line":
                            if j + 1 != len(self.__tokens):
                                blackLinesStart = j + 1
                            l = j + 1
                            while l != len(self.__tokens) and self.__tokens[l].getGroupName() == "new line":
                                blackLinesCount += 1
                                l += 1
                            break
                        j += 1
                    break

            del self.__tokens[blackLinesStart:blackLinesStart + blackLinesCount]
            for i in range(blackLinesStart,
                           blackLinesStart + self.__settings.BlackLinesSettings().MinimumBlackLinesSettings().AroundClass()):
                self.__tokens.insert(i, FormatterToken(Token("new line", "#")))


    def __applyPunctuation(self):
        self.__getParenthesesTypes()
        self.__getBracesTypes()
        self.__getKeywordsTypes()
        self.__getOperatorsTypes()
        self.__getOtherTypes()
        self.__getClosingTypes()
        self.__getPunktMarksTypes()

        self.__removeCommasPunctuation()
        self.__addCommasPunctuation()

    def __removeCommasPunctuation(self):
        indicesToRemove = []

        for i in range(0, len(self.__tokens)):
            if self.__tokens[i].getGroupName() == "literal" or self.__tokens[i].getGroupName() == "symbolic constant":
                value = list(self.__tokens[i].getValue())
                if self.__settings.PunctuationSettings().QuotesSettings().Single():
                    value[0] = "'"
                    value[len(value) - 1] = "'"
                else:
                    value[0] = '"'
                    value[len(value) - 1] = '"'
                self.__tokens[i].setValue("".join(value))
            elif self.__tokens[i].getValue() == ";":
                if self.__settings.PunctuationSettings().SemicolonStatementsSettings().Use():
                    self.__tokens[i].setValue(";")
                else:
                    self.__tokens[i].setValue("")
            elif self.__tokens[i].getValue() == "," or self.__tokens[i].getValue() == ", " or self.__tokens[
                i].getValue() == " ," or self.__tokens[i].getValue() == " , ":
                j = i + 1
                while j != len(self.__tokens):
                    if self.__tokens[j].getGroupName() == "new line":
                        j += 1
                    elif self.__tokens[j].getHelpGroupName() == "back array brackets" or self.__tokens[
                        j].getHelpGroupName() == "back object literal braces":
                        if self.__settings.PunctuationSettings().TrailingComma() == "Remove":
                            indicesToRemove.append(i)
                        break
                    else:
                        break

        diff = 0
        for index in indicesToRemove:
            del self.__tokens[index - diff:index - diff + 1]
            diff += 1

    def __addCommasPunctuation(self):
        indicesToAdd = []

        for i in range(0, len(self.__tokens)):
            if self.__tokens[i].getHelpGroupName() == "back array brackets" or self.__tokens[i].getHelpGroupName() == "back object literal braces":
                if i - 1 >= 0 and self.__tokens[i - 1].getGroupName() == "new line" and self.__settings.PunctuationSettings().TrailingComma() == "Add when multiline":
                    j = i - 1
                    while j != -1:
                        if self.__tokens[j].getGroupName() == "new line":
                            j -= 1
                        elif self.__tokens[j].getValue() != "," and self.__tokens[j].getValue() != ", " and self.__tokens[j].getValue() != " ," and self.__tokens[j].getValue() != " , ":
                            indicesToAdd.append(j+1)
                            break
                        else:
                            break
        diff = 0
        for index in indicesToAdd:
            self.__tokens.insert(index+diff, FormatterToken(Token("punctuation mark", ",")))
            diff += 1

    def __getMistakes(self):
        for i in range(0, len(self.__tokens)):
            if self.__tokens[i].getGroupName() == "keyword":
                j = i + 1
                while j != len(self.__tokens):
                    if self.__tokens[j].getGroupName() == "new line":
                        j += 1

                    elif self.__tokens[i].getValue() == "break" and self.__tokens[j].getValue() != ";":
                        self.__printError(j, "Missing ; after break")
                        break
                    elif self.__tokens[i].getValue() == "case" and self.__tokens[j].getGroupName() != "literal" and self.__tokens[j].getGroupName() != "symbolic constant" and self.__tokens[j].getGroupName() != "numeric constant" and self.__tokens[j].getValue() != "false" and self.__tokens[j].getValue() != "true":
                        self.__printError(j, "Wrong value after case")
                        break
                    elif self.__tokens[i].getValue() == "catch" and self.__tokens[j].getValue() != "(":
                        self.__printError(j, "Missing ( after catch")
                        break
                    elif self.__tokens[i].getValue() == "delete" and self.__tokens[j].getGroupName() != "identifier":
                        self.__printError(j, "Wrong value after delete")
                        break
                    elif self.__tokens[i].getValue() == "else" and self.__tokens[j].getValue() != "{" and self.__tokens[j].getValue() != "if":
                        self.__printError(j, "Missing { after else")
                        break
                    elif self.__tokens[i].getValue() == "finally" and self.__tokens[j].getValue() != "{":
                        self.__printError(j, "Missing { after finally")
                        break
                    elif self.__tokens[i].getValue() == "for" and self.__tokens[j].getValue() != "(":
                        self.__printError(j, "Missing ( after for")
                        break
                    elif self.__tokens[i].getValue() == "function" and self.__tokens[j].getValue() != "(" and self.__tokens[j].getGroupName() != "identifier":
                        self.__printError(j, "Wrong value after function")
                        break
                    elif self.__tokens[i].getValue() == "if" and self.__tokens[j].getValue() != "(":
                        self.__printError(j, "Missing ( after if")
                        break
                    elif self.__tokens[i].getValue() == "let" and self.__tokens[j].getGroupName() != "identifier":
                        self.__printError(j, "Wrong type after let")
                        break
                    elif self.__tokens[i].getValue() == "const" and self.__tokens[j].getGroupName() != "identifier":
                        self.__printError(j, "Wrong type after const")
                        break
                    elif self.__tokens[i].getValue() == "new" and self.__tokens[j].getGroupName() != "identifier":
                        self.__printError(j, "Wrong type after new")
                        break
                    elif self.__tokens[i].getValue() == "class" and self.__tokens[j].getGroupName() != "identifier":
                        self.__printError(j, "Wrong type after class")
                        break
                    elif self.__tokens[i].getValue() == "switch" and self.__tokens[j].getValue() != "(":
                        self.__printError(j, "Missing ( after switch")
                        break
                    elif self.__tokens[i].getValue() == "try" and self.__tokens[j].getValue() != "{":
                        self.__printError(j, "Missing { after try")
                        break
                    elif self.__tokens[i].getValue() == "while" and self.__tokens[j].getValue() != "(":
                        self.__printError(j, "Missing ( after while")
                        break
                    elif self.__tokens[i].getValue() == "var" and self.__tokens[j].getGroupName() != "identifier":
                        self.__printError(j, "Wrong type after var")
                        break
                    elif self.__tokens[j].getGroupName() == "numeric constant" and self.__tokens[j].getGroupName() == "literal" and self.__tokens[j].getGroupName() == "symbolic constant" and self.__tokens[j].getGroupName() == "operator":
                        self.__printError(j, "Wrong value after keyword")
                        break
                    else:
                        break
                l = i - 1
                while l != -1:
                    if self.__tokens[l].getGroupName() == "new line":
                        l -= 1

                    elif self.__tokens[i].getValue() == "break" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getGroupName() != "comments" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{":
                        self.__printError(i, "Wrong value before break")
                        break
                    elif self.__tokens[i].getValue() == "case" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before case")
                        break
                    elif self.__tokens[i].getValue() == "catch" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before catch")
                        break
                    elif self.__tokens[i].getValue() == "delete" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before delete")
                        break
                    elif self.__tokens[i].getValue() == "else" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before else")
                        break
                    elif self.__tokens[i].getValue() == "finally" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before finally")
                        break
                    elif self.__tokens[i].getValue() == "for" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before for")
                        break
                    elif self.__tokens[i].getValue() == "function" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getValue() != "," and self.__tokens[l].getValue() != "=" and self.__tokens[l].getGroupName() != "comments" and self.__tokens[l].getValue() != ":" and self.__tokens[l].getValue() != "(" and self.__tokens[l].getValue() != "return":
                        self.__printError(i, "Wrong value before function")
                        break
                    elif self.__tokens[i].getValue() == "if" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getValue() != "(" and self.__tokens[l].getGroupName() != "comments" and self.__tokens[l].getValue() != "else":
                        self.__printError(i, "Wrong value before if")
                        break
                    elif self.__tokens[i].getValue() == "let" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before let")
                        break
                    elif self.__tokens[i].getValue() == "const" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before const")
                        break
                    elif self.__tokens[i].getValue() == "switch" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before switch")
                        break
                    elif self.__tokens[i].getValue() == "try" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before try")
                        break
                    elif self.__tokens[i].getValue() == "class" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getValue() != "export" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before class")
                        break
                    elif self.__tokens[i].getValue() == "while" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before while")
                        break
                    elif self.__tokens[i].getValue() == "var" and self.__tokens[l].getValue() != ";" and self.__tokens[l].getValue() != "}" and self.__tokens[l].getValue() != "{" and self.__tokens[l].getValue() != "(" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before var")
                        break
                    elif self.__tokens[l].getGroupName() == "numeric constant" and self.__tokens[l].getGroupName() == "literal" and self.__tokens[l].getGroupName() == "symbolic constant" and self.__tokens[l].getGroupName() == "operator" and self.__tokens[l].getGroupName() != "comments":
                        self.__printError(i, "Wrong value before keyword")
                        break
                    else:
                        break
            elif self.__tokens[i].getGroupName() == "identifier":
                j = i + 1
                while j != len(self.__tokens):
                    if self.__tokens[j].getGroupName() == "new line":
                        j += 1
                    elif self.__tokens[j].getGroupName() == "numeric constant" or self.__tokens[j].getGroupName() == "literal" or self.__tokens[j].getGroupName() == "symbolic constant" or self.__tokens[j].getGroupName() == "identifier":
                        self.__printError(j, "Wrong value after identifier")
                        break
                    else:
                        break
                l = i - 1
                while l != len(self.__tokens):
                    if self.__tokens[l].getGroupName() == "new line":
                        l -= 1
                    elif self.__tokens[l].getGroupName() == "numeric constant" or self.__tokens[l].getGroupName() == "literal" or self.__tokens[l].getGroupName() == "symbolic constant":
                        self.__printError(i, "Wrong value before identifier")
                        break
                    else:
                        break
            elif self.__tokens[i].getGroupName() == "literal":
                j = i + 1
                while j != len(self.__tokens):
                    if self.__tokens[j].getGroupName() == "new line":
                        j += 1
                    elif self.__tokens[j].getGroupName() == "numeric constant" or self.__tokens[j].getGroupName() == "literal" or self.__tokens[j].getGroupName() == "symbolic constant":
                        self.__printError(j, "Wrong value after literal")
                        break
                    else:
                        break
                l = i - 1
                while l != len(self.__tokens):
                    if self.__tokens[l].getGroupName() == "new line":
                        l -= 1
                    elif self.__tokens[l].getGroupName() == "numeric constant" or self.__tokens[l].getGroupName() == "symbolic constant":
                        self.__printError(i, "Wrong value before literal")
                        break
                    else:
                        break
            elif self.__tokens[i].getGroupName() == "symbolic constant":
                j = i + 1
                while j != len(self.__tokens):
                    if self.__tokens[j].getGroupName() == "new line":
                        j += 1
                    elif self.__tokens[j].getGroupName() == "numeric constant" or self.__tokens[j].getGroupName() == "symbolic constant":
                        self.__printError(j, "Wrong value after symbolic constant")
                        break
                    else:
                        break
                l = i - 1
                while l != len(self.__tokens):
                    if self.__tokens[l].getGroupName() == "new line":
                        l -= 1
                    elif self.__tokens[l].getGroupName() == "numeric constant":
                        self.__printError(i, "Wrong value before symbolic constant")
                        break
                    else:
                        break
            elif self.__tokens[i].getGroupName() == "numeric constant":
                j = i + 1
                while j != len(self.__tokens):
                    if self.__tokens[j].getGroupName() == "new line":
                        j += 1
                    elif self.__tokens[j].getGroupName() == "numeric constant":
                        self.__printError(j, "Wrong value after operator")
                        break
                    else:
                        break
            elif self.__tokens[i].getGroupName() == "operator":
                j = i + 1
                while j != len(self.__tokens):
                    if self.__tokens[j].getGroupName() == "new line":
                        j += 1
                    elif (self.__tokens[j].getGroupName() == "operator" and self.__tokens[j].getValue() != "-") or ((self.__tokens[j].getGroupName() == "punctuation mark" and self.__tokens[j].getValue() != "{") and ((self.__tokens[i].getValue() == "++" or self.__tokens[i].getValue() == "--") and self.__tokens[j].getValue() != ")" and self.__tokens[j].getValue() != ";")):
                        self.__printError(j, "Wrong value after operator")
                        break
                    else:
                        break
                l = i - 1
                while l != len(self.__tokens):
                    if self.__tokens[l].getGroupName() == "new line":
                        l -= 1
                    elif self.__tokens[l].getGroupName() == "punctuation mark":
                        if self.__tokens[i].getValue() != "=>" and self.__tokens[l].getValue() != ")" and self.__tokens[l].getValue() != "(" and self.__tokens[i].getValue() != "!" and self.__tokens[l].getValue() != "]":
                            self.__printError(i, "Wrong value before operator")
                        break
                    else:
                        break

    def __printError(self, index, value):
        lineCount = 1

        for i in range(0, index):
            if self.__tokens[i].getGroupName() == "new line":
                lineCount += 1
            elif self.__tokens[i].getGroupName() == "comments":
                commValue = list(self.__tokens[i].getValue())
                for symbol in commValue:
                    if symbol == "#":
                        lineCount += 1

        with open("resources/logfile.txt", "a") as logFile:
            errorView = value + "(line: " + str(lineCount) + ", index: " + str(index) + ")\n"
            logFile.write(errorView)

    def __applyNewLines(self):
        newLineIndices = []

        for i in range(0, len(self.__tokens)):
            if self.__tokens[i].getValue() == ";" and i + 1 != len(self.__tokens) and self.__tokens[i+1].getGroupName() != "new line" and self.__tokens[i+1].getGroupName() != "comment":
                newLineIndices.append(i+1)
            elif self.__tokens[i].getValue() == "{" and i + 1 != len(self.__tokens) and self.__tokens[i+1].getGroupName() != "new line" and self.__tokens[i+1].getGroupName() != "comment":
                newLineIndices.append(i + 1)
            elif self.__tokens[i].getValue() == "}" and i + 1 != len(self.__tokens) and self.__tokens[i+1].getGroupName() != "new line" and self.__tokens[i+1].getGroupName() != "comment":
                if i != 0 and self.__tokens[i - 1].getGroupName() != "new line" and self.__tokens[i-1].getValue() != ";":
                    newLineIndices.append(i)
                if i + 1 != len(self.__tokens) and self.__tokens[i+1].getGroupName() != "new line" and self.__tokens[i+1].getGroupName() != "comment":
                    newLineIndices.append(i + 1)

        diff = 0
        for index in newLineIndices:
            self.__tokens.insert(index + diff, FormatterToken(Token("new line", "#")))
            diff += 1

