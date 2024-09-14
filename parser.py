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
        if self.checkToken(tokenType) is not True:
            sys.exit("Expected ${self.text} but returned ${self.curr_Token.name}")
        self.nextToken()
        #moves over to the next token
    def nextToken(self):
        print("in nextToken")
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
    def statement(self):
        #statement -> "print" (expression | string) nl
        if self.checkToken(TokenType.PRINT):
            print("PRINT-STATEMENT")
            self.nextToken()
            
            if self.checkToken(TokenType.STRING):
                print("STRING")
                self.nextToken()
            else: 
                self.expression()
        #if" comparison "therefore" nl statement* ("else if" comparison "therefore" nl statement*)* ("else" nl statement*)? "endif" nl
        elif self.checkToken(TokenType.IF):
            print("IF")
            self.nextToken()
            self.comparison()

            self.match(TokenType.THEREFORE)
            self.newline()

            while not self.checkToken(TokenType.ELSE_IF) or not self.checkToken(TokenType.ELSE) or not self.checkToken(TokenType.ENDIF): #if" comparison "therefore" nl statement*
                self.statement()
            
            while self.checkToken(TokenType.ELSE_IF): #("else if" comparison "therefore" nl statement*)*
                print("ELSE IF")
                self.nextToken()
                self.comparison()

                self.match(TokenType.THEREFORE)
                self.newline()

                while not self.checkToken(TokenType.ELSE) or not self.checkToken(TokenType.ENDIF):
                        self.statement()
            
            if self.checkToken(TokenType.ELSE): #("else" nl statement*)?
                self.nextToken()
                self.newline()
                while not self.checkToken(TokenType.ENDIF):
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
            
            self.match(TokenType.IDENTIFIER)

            if self.checkPeekToken(TokenType.EQUALS):
                self.match(TokenType.EQUALS)
                print("EQUALS")
                print(f"{variable_name}")
                self.expression()
                print(";")

            self.match()
            
    
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
            self.nextToken()
            self.term()
    def term(self):
        #term -> unary (("/" | "*") unary)*
        self.unary()

        while ( self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH)):
            self.nextToken()
            self.unary()
    def unary(self):
        #unary -> ("+" | "-")? primary
        print("UNARY")

        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.primary()
        self.primary()
    def primary(self):
        #primary -> number | ident
        print("PRIMARY")

        if self.checkToken(TokenType.NUMBER):
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
    

        