from lexer import *

class Parser: 
    def __init__(self,lexer):
        self.lexer = lexer
        print("SELF LEXER: ", self.lexer.__dict__)
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
        #if" comparison "therefore" nl statement* ("else" nl statement*)? "endif" nl
        #elif self.checkToken(TokenType.IF):
         #   self.nextToken()
          #  self.comparison
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
        else:
            sys.exit("Unexpected token:  " + self.curr_Token.text)
    def newline(self):
        #nl -> '\n'+
        self.match(TokenType.NEWLINE)

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
    

        