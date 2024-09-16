from enum import Enum
import sys
class Lexer: 
    def __init__(self, source):
        self.source = source + '\n'
        self.currChar = ''
        self.currPos = -1

        self.Lines = 1 #used to track the line number we are on, this will be useful to check if there is a comment on that line or not
        #if there is, the we store that comment and the corresponding line as a key value pair in our dictionary
        self.commentDict = {}
        self.nextChar()
        pass
    #Moves to the next character in the source  code 
    def nextChar(self):
        self.currPos += 1
        if self.currPos >= len(self.source): #check if current position exceeded the length of the source code, if it did that means we are at the end of the string or input
            self.currChar = '\0' #sets the current character equal to EOF character
        else:
            self.currChar = self.source[self.currPos] #if not at EOF then set the curent character equal to the character at the currPos in the source string
        return self.currChar
    #Looks at the next character but doesnt move currPos , used when i want to check what comes next
    def peek(self):
        if self.currPos + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.currPos + 1] #checks the next character
    #Handles errors, if it sees an invalid token, program exits
    def abort(self, message):
        sys.exit("Exiting....\n" + message)
        pass
    #Skips all the spaces and tabs until it finds a new line \n
    def skipWhiteSpace(self):
        while self.currChar == ' ' or self.currChar == '\t' or self.currChar == '\r':
            self.nextChar()
    #If lexer detects a comment, starting with " // " it will skip over the whole comment until it finds a newline
    def skipComment(self):
        if self.currChar == '@':
            if self.peek() == '@':
                self.nextChar()
                self.nextChar()
                startPosition = self.currPos #the current position is the first character after the second @, starting the comment
                while self.currChar != '\n':
                    self.nextChar()
                
                comment = ""
                for i in range(startPosition, self.currPos + 1):
                    comment = comment + self.source[i]
                
                self.commentDict[self.Lines] = comment.strip()

                print("Comment Line: " , self.Lines , ": Comment Text: " , comment.strip())

            else:
                self.abort("Unknown Token: " + self.peek())
    #Core function which will return the next token in the source code. Will be used to classify the current sequence of chars into different token types
    def getToken(self):
        self.skipWhiteSpace()
        self.skipComment()
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
                token = Token(self.currChar, TokenType.LESSTHAN)
        elif self.currChar == '!': #Not Equals
            if self.peek() == '=':
                previousChar = self.currChar
                nextChar  = self.nextChar()
                token = Token(previousChar + nextChar, TokenType.NOTEQUALS)
            else: 
                self.abort("Expected !=, but instead receive ! + " + self.peek())
        elif self.currChar == '*':#Asterisk
            token = Token(self.currChar, TokenType.ASTERISK)
        elif self.currChar == "/":#Slash
            token = Token(self.currChar, TokenType.SLASH)
        elif self.currChar == '\n': 
            token = Token(self.currChar, TokenType.NEWLINE)
            self.Lines += 1
            print("newline encountered: " ,self.Lines)
        elif self.currChar == '\0': #End of File
            token = Token(self.currChar, TokenType.EOF)
        #Printing a String
        elif self.currChar == '\"':
            #start reading the string
            self.nextChar() #in the string
            startPosition = self.currPos
            while self.currChar != "\"":
                if self.currChar == '\r' or self.currChar == '\n' or self.currChar == '\t' or self.currChar == '\\' or self.currChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()
            tokenText = ''
            for i in range(startPosition, self.currPos):
                tokenText += self.source[i]
            print("Token text: ", tokenText)
            token = Token(tokenText, TokenType.STRING)
        #Dealing with digits
        elif self.currChar.isdigit():
            startPosition = self.currPos
            while self.peek().isdigit():
                self.nextChar()

            if self.peek() == '.': #decimal
                self.nextChar()
                if not self.peek().isdigit():
                    self.abort("Chracter is not a number")
                while self.peek().isdigit():
                    self.nextChar()

            tokenText = ''
            for i in range(startPosition, self.currPos + 1):
                tokenText += self.source[i]
            token = Token(tokenText, TokenType.NUMBER)
        #Check whether text is an identifier or keyword ------------------------------------------------
        elif self.currChar.isalpha():
            #start looping here
            startPosition = self.currPos
            while( self.peek().isalpha() ):
                self.nextChar()
                #print("in: ",self.currChar)
            
            tokenText = ""
            for i in range( startPosition, self.currPos + 1): 
                tokenText += self.source[i]
                #print("Self source: " , "\n", self.source[i], "\n")
            
            is_a_keyword = Token.keywordCheck(tokenText)
            #print("is a keyword: ", is_a_keyword)
            if is_a_keyword == None:
                token = Token(tokenText, TokenType.IDENTIFIER)
            else:
                token = Token(tokenText, is_a_keyword) #returned the keyword TokenType.x
            #check whether joey is a keyword or not


        else:
            self.abort("Unknown Token: " + self.currChar)
        self.nextChar()
        #print("The token is: ", token.Type)
        return token

class Token: #every time this is used, I am creating an instance of the Token class
    def __init__(self, tokenText, tokenType): #constructor method that initialized each token object with a text and a Type
        self.text = tokenText 
        self.Type = tokenType #instance variable of the Token class and is set to the value passed in tokenType
    def keywordCheck(text):
        for x in TokenType:
            if x.name == text and x.value >= 50 and x.value <=59:
                #is a keyword
                print("Keyword: ", x.name)
                return x
        return None
    #In summary, an instance of a class is the actual object created from the class. In this case, token is an instance of the Token class, and it holds the attributes text and Type, which store information about the specific token.

class TokenType(Enum):
    #name = value
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENTIFIER = 2
    STRING = 3
    #Keywords
    PRINT = 50
    VAR = 51
    IF = 52
    THEREFORE = 53
    ELSE = 54
    ELSEIF = 55
    ENDIF = 56
    WHILE = 57
    DO = 58
    ENDWHILE = 59
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

