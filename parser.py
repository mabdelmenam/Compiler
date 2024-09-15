from lexer import *
import sys

class Parser: 
    def __init__(self,lexer):
        self.lexer = lexer
        print("SELF LEXER: ", self.lexer.__dict__)

        self.variables = {} #dictionary holding key: variable names or identifiers and the corresponding values
        self.curr_Token = None
        self.peek_Token = None
        self.nextToken() #nextToken() is called twice in order to push the curr and peek Tokens over to the next Token in line, used to initialize current and peek
        self.nextToken()
        #returns true if the current token matches
    def checkToken(self, tokenType):
        if tokenType == self.curr_Token.Type:
            return True
        else:
            return False
        #returns true if the next token(peek) matches
    def checkPeekToken(self, tokenType):
        if tokenType == self.peek_Token.Type:
            return True
        else:
            return False
        #checks if the current token matches, if it does move to the next
    def match(self, tokenType):
        if not self.checkToken(tokenType):
            print(tokenType.__dict__)
            sys.exit("Expected " + tokenType.name + " but returned: " + self.curr_Token.text)
        self.nextToken()
        #moves over to the next token
    def nextToken(self):
        #print("in nextToken")
        self.curr_Token = self.peek_Token
        self.peek_Token = self.lexer.getToken()
        #Grammar
    def program(self):
        print("entered program")
        while self.checkToken(TokenType.NEWLINE):
            print("in here1")
            self.nextToken()
        
        while not self.checkToken(TokenType.EOF):
            self.statement()
    def statement(self): #Includes all the different statement parsing rules
        #statement -> "print" (expression | string) nl
        if self.checkToken(TokenType.PRINT):
            print("PRINT-STATEMENT")
            self.nextToken()
            
            if self.checkToken(TokenType.STRING):
                #print("STRING")
                self.nextToken()
            else: 
                self.expression()

            #print("expecting a NEWLINE after PRINT")
            #self.newline()
        #if" comparison "therefore" nl statement* ("else if" comparison "therefore" nl statement*)* ("else" nl statement*)? "endif" nl
        elif self.checkToken(TokenType.IF):
            print("IF")
            self.nextToken()
            self.comparison()

            self.match(TokenType.THEREFORE)
            #print("THEREFORE")
            self.newline()

            while not (self.checkToken(TokenType.ELSE_IF) or self.checkToken(TokenType.ELSE) or self.checkToken(TokenType.ENDIF)): #if" comparison "therefore" nl statement*
                print("Processing statements in IF block")
                self.statement()
                #print("after")
            
            #print("exit")
            while self.checkToken(TokenType.ELSE_IF): #("else if" comparison "therefore" nl statement*)*
                print("ELSE IF")
                self.nextToken()
                self.comparison()

                self.match(TokenType.THEREFORE)
                print("THEREFORE")
                self.newline()

                while not self.checkToken(TokenType.ELSE) or not self.checkToken(TokenType.ENDIF): #Parse statements in the ELSE IF BLOCK
                    print("Processing statements in ELSE IF block")
                    self.statement()
            
            if self.checkToken(TokenType.ELSE): #("else" nl statement*)? Optional Else block
                print("ELSE")
                self.nextToken()
                print("Expecting a NEWLINE after ELSE")
                self.newline()
                while not self.checkToken(TokenType.ENDIF): #Parse statements in ELSE block
                    print("Processing statements in ELSE block")
                    self.statement()
            
            self.match(TokenType.ENDIF)
            
            """ while not self.checkToken(TokenType.ENDIF):
                self.statement()
                if self.checkToken(TokenType.ELSE_IF):
                    self.nextToken()
                    self.comparison()

                    self.match(TokenType.THEREFORE)
                    self.newline()
                    while not self.checkToken(TokenType.ELSE) or not self.checkToken(TokenType.ENDIF):
                        self.statement()
                elif self.checkToken(TokenType.ELSE):
                    self.nextToken()
                    self.newline()
                    while not self.checkToken(TokenType.ENDIF):
                        self.statement() """
        
        #"while" comparison "do" nl statement* "endwhile" nl
        elif self.checkToken(TokenType.WHILE):
            print("WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokenType.DO)
            self.newline()

            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            
            self.match(TokenType.ENDWHILE)


        #var" ident ("=" expression)? nl
        elif self.checkToken(TokenType.VAR):
            print("VAR")
            self.nextToken()
            variable_name = self.curr_Token.text

            if self.curr_Token.text not in self.variables:
                self.variables[variable_name] = None #declaring but not initialzing
                print(f"Declared variable: float {variable_name};")
            else:
                sys.exit(f"Variable '{variable_name} already declared.")
            
            #print("Current token before: ", self.curr_Token.Type)
            self.match(TokenType.IDENTIFIER)
            #print("Identified!!")
            #print("Current Token after: ", self.curr_Token.Type)

            #print("Peeked token is: ", self.peek_Token.Type)
            if self.checkToken(TokenType.EQUALS):
                self.match(TokenType.EQUALS)
                #print("EQUALS")
                print(f"{variable_name} \n", end="") #where is the equals sign like this  self.emitter.emit(self.curToken.text + " = ")
                self.expression()
                print(";")
        #UPDATING IDENTIFIER (VAR), initializing
        # ident "=" expression nl
        elif self.checkToken(TokenType.IDENTIFIER):
            variable_name = self.curr_Token.text
            if variable_name not in self.variables:
                sys.exit("Variable " + variable_name + " not does not exist.")
            else:
                print("Updating variable: " , variable_name)
            
            self.nextToken()
            self.match(TokenType.EQUALS)

            self.expression()


            
        self.newline() #Important!!! Signifies the end of a statement, without doing this the parser will continue parsing even though it should stop at the end of the current line

    #comparison -> expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    # a + b 
    def comparison(self):
        print("Comparison")
        self.expression()

        if self.checkToken(TokenType.EqEq) or self.checkToken(TokenType.NOTEQUALS) or self.checkToken(TokenType.GREATERTHAN) \
        or self.checkToken(TokenType.GREATERTHANEQ) or self.checkToken(TokenType.LESSTHAN) or self.checkToken(TokenType.LESSTHANEQ): #if a > b and b < c
            self.nextToken()
            self.expression()
        else:
            sys.exit("Expected a comparison operator and receieved " + self.curr_Token.text)
        
        while self.checkToken(TokenType.EqEq) or self.checkToken(TokenType.NOTEQUALS) or self.checkToken(TokenType.GREATERTHAN) \
        or self.checkToken(TokenType.GREATERTHANEQ) or self.checkToken(TokenType.LESSTHAN) or self.checkToken(TokenType.LESSTHANEQ): #look up explanation
            self.nextToken()
            self.expression()

    def expression(self):
        #expression -> term (("-" | "+") term)*
        self.term()

        while( self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS)):
            if self.checkToken(TokenType.PLUS):
                self.match(TokenType.PLUS)
                print(" + ", end="")
            elif self.checkToken(TokenType.MINUS):
                self.match(TokenType.MINUS)
                print(" - ", end="")
            self.term()
    def term(self):
        #term -> unary (("/" | "*") unary)*
        self.unary()

        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            if self.checkToken(TokenType.ASTERISK):
                self.match(TokenType.ASTERISK)
                print(" * ", end="")
            elif self.checkToken(TokenType.SLASH):
                self.match(TokenType.SLASH)
                print(" / ", end="")
                
            self.unary()
    def unary(self):
        #unary -> ("+" | "-")? primary
        print("UNARY")

        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            if self.checkToken(TokenType.PLUS):
                print(" +", end="")
            elif self.checkToken(TokenType.MINUS):
                print(" -", end="")
            self.nextToken()

        self.primary()
    def primary(self):
        #primary -> number | ident
        print("PRIMARY")

        print("Current Token in Primary: ", self.curr_Token.Type, " Value: ", self.curr_Token.text)
        if self.checkToken(TokenType.NUMBER):
            print(self.curr_Token.text, "\n", end="")
            self.nextToken()
        elif self.checkToken(TokenType.IDENTIFIER):
            if self.curr_Token.text not in self.variables: #checks if the current identifier or variable being used has first been declared,
                #A user may attempt to PRINT x as an example, while x has not yet been declared, which is impossible as x does not yet exist, thus we must exit the program
                sys.exit("Variable " + self.curr_Token.text + " has not been declared.")
            self.nextToken() #proceed to next token after confirming that an identifier is valid
        else:
            sys.exit("Unexpected token:  " + self.curr_Token.text)
    def newline(self):
        print("NEWLINE")
        #nl -> '\n'+
        self.match(TokenType.NEWLINE)

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
    

        