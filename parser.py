from lexer import *

class Parser: 
    def __init__(self,lexer):
        self.lexer =  lexer
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
        self.curr_Token = self.peek_Token
        self.peek_Token = self.lexer.getToken()
        #Grammar


        