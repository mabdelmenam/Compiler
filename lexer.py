from enum import Enum
class Lexer: 
    def __init__(self, source):
        self.source = source + '\n'
        self.currChar = ''
        self.currPos = -1
        self.nextChar()
        pass
    #Moves to the next character in the source  code 
    def nextChar(self):
        self.currPos += 1
        if self.currPos >= len(self.source): #check if current position exceeded the length of the source code, if it did that means we are at the end of the string or input
            self.currChar = '\0' #sets the current character equal to EOF character
        else:
            self.currChar = self.source[self.currPos] #if not at EOF then set the curent character equal to the character at the currPos in the source string
        pass
    #Looks at the next character but doesnt move currPos , used when i want to check what comes next
    def peek(self):
        if self.currPos + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.currPos + 1] #checks the next character
    #Handles errors, if it sees an invalid token, program exits
    def abort(self):
        pass
    #Skips all the spaces and tabs until it finds a new line \n
    def skipWhiteSpace(self):
        pass
    #If lexer detects a comment, starting with " // " it will skip over the whole comment until it finds a newline
    def skipComment(self):
        pass
    #Core function which will return the next token in the source code. Will be used to classify the current sequence of chars into different token types
    def getToken(self):
        token = None
        if self.currChar == '+': #PLUS
            token = Token(self.currChar, TokenType.PLUS)
        elif self.currChar == '-':#MINUS
            token = Token(self.currChar, TokenType.MINUS)
        elif self.currChar == '=':#EQUALS
            if self.peek() == '=':
                previousChar = self.currChar
                nextChar = self.nextChar()
                token = Token(previousChar + nextChar, TokenType.EqEq) #DOUBLE EQUALS
            else:
                token = Token(self.currChar, TokenType.EQUALS)
        elif self.currChar == '>':#Greater than and Greater than or Equals
            if self.peek() == '=':
                previousChar = self.currChar
                nextChar = self.nextChar()
                token = Token(previousChar + nextChar, TokenType.GREATERTHANEQ)
            else: 
                token = Token(self.currChar, TokenType.GREATERTHAN)
        elif self.currChar == '<': #Less than , and Less than or Equals
            if self.peek() == '=':
                previousChar = self.currChar
                nextChar = self.nextChar()
                token = Token(previousChar + nextChar, TokenType.LESSTHANEQ)
            else:
                token = Token(self.currChar)
        elif self.currChar == '*':#Asterisk
            token = Token(self.currChar, TokenType.ASTERISK)
        elif self.currChar == "/":#Slash
            token = Token(self.currChar, TokenType.SLASH)
        elif self.currChar == '\0': #End of File
            token = Token(self.currChar, TokenType.EOF)
        else:
            pass
        self.nextChar()
        return token

class Token:
    def __init__(self, tokenText, tokenType):
        self.text = tokenText
        self.Type = tokenType

class TokenType(Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENTIFIER = 2
    STRING = 3
    #Keywords
    label = 51
    goto = 52 
    #Operators
    EQUALS = 100
    PLUS = 101
    MINUS = 102
    ASTERISK = 103
    SLASH = 104
    EqEq = 105
    NOTEQUALS = 106
    LESSTHAN = 107
    LESSTHANEQ = 108
    GREATERTHAN = 109
    GREATERTHANEQ = 110

