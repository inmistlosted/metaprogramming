from Lexer.token1 import Token
from Parser.parsertoken import ParserToken
from Settings.templatessettings import TemplatesSettings


class Parser(object):
    def __init__(self, tokens, templateName):
        self.__lexerTokens = tokens
        self.__settings = TemplatesSettings()
        self.__tokens = []
        self.__getParserTokens()
        self.__templateName = templateName

    def execute(self):
        if self.__templateName == "TabsAndIndents":
            self.__applyIndents()
        elif self.__templateName == "Spaces":
            self.__applySpaces()



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

            if indentLevel < 0:
                print("Syntacsis error")

            if contIndent < 0:
                print("Syntacsis error")

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

    def __getParserTokens(self):
        for i in range(0, len(self.__lexerTokens)):
            # added = False
            # if self.__isFunctionCall(i):
            #     self.__tokens.append(ParserToken(self.__lexerTokens[i], "function call"))
            # elif self.__isFunctionDeclaration(i):
            #     self.__tokens.append(ParserToken(self.__lexerTokens[i], "function declaration"))
            #
            #
            #     self.__tokens.append(ParserToken(self.__lexerTokens[i], "function"))
            #     added = True
            # if not added:
            self.__tokens.append(ParserToken(self.__lexerTokens[i]))

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
                        print("error")
                        break
            elif self.__tokens[index].getValue() == "{":
                back = index - 1
                while back != -1:
                    if self.__tokens[back].getGroupName() == "new line":
                        back -= 1
                    elif self.__tokens[back].getValue() == "=" or self.__tokens[back].getGroupName() == "punctuation mark":
                        self.__tokens[index].setHelpGroupName("object literal braces")
                        break
                    elif self.__tokens[back].getValue() == "import" or self.__tokens[back].getValue() == "export":
                        self.__tokens[index].setHelpGroupName("import export braces")
                        break
                    else:
                        print("error")
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
                        else:
                            bracesLevel -= 1
                    i -= 1
            elif self.__tokens[index].getValue() == ")":
                i = index - 1
                parenthesesLevel = 0
                while i != -1:
                    if self.__tokens[i].getValue() == ")":
                        parenthesesLevel += 1
                    elif self.__tokens[i].getValue() == "(":
                        if parenthesesLevel == 0:
                            self.__tokens[index].setHelpGroupName("back " + self.__tokens[i].getHelpGroupName())
                        else:
                            parenthesesLevel -= 1
                    i -= 1
            elif self.__tokens[index].getValue() == "]":
                i = index - 1
                bracketsLevel = 0
                while i != -1:
                    if self.__tokens[i].getValue() == "]":
                        bracketsLevel += 1
                    elif self.__tokens[i].getValue() == "[":
                        if bracketsLevel == 0:
                            self.__tokens[index].setHelpGroupName("back " + self.__tokens[i].getHelpGroupName())
                        else:
                            bracketsLevel -= 1
                    i -= 1







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
