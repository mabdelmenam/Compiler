class Lexer: 
    def __init__(self, source):
        self.source = source + '\n'
        self.currChar = ''
        self.currPos = -1
        self.nextChar()
        pass
    #Moves to the next character in the source  code 
    def nextChar(self):
        pass
    #Looks at the next character but doesnt move currPos , used when i want to check what comes next
    def peek(self):
        pass
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
        pass
