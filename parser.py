from lexer import *
from emitter import *
import sys

class Parser: 
    def __init__(self,lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter
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
        
        self.curr_Token = self.peek_Token
        self.peek_Token = self.lexer.getToken()

    #-------------------------Grammar Rules-------------------------
    def program(self):
        print("entered program")
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")
        while self.checkToken(TokenType.NEWLINE):
            
            self.nextToken()
        
        while not self.checkToken(TokenType.EOF):
            self.statement()
        
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")
    def statement(self): #Includes all the different statement parsing rules
        #statement -> "print" (expression | string) nl
        if self.checkToken(TokenType.PRINT):
            print("PRINT-STATEMENT")
            self.nextToken()
            
            if self.checkToken(TokenType.STRING):
                self.emitter.emitLine("printf(\"" + self.curr_Token.text + "\\n\");")
                #print("STRING")
                self.nextToken()
            else: 
                #expression, print result as a float
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")

            #print("expecting a NEWLINE after PRINT")
            #self.newline()
        #if" comparison "therefore" nl statement* ("else if" comparison "therefore" nl statement*)* ("else" nl statement*)? "endif" nl
        elif self.checkToken(TokenType.IF):
            print("IF")
            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()

            self.match(TokenType.THEREFORE)
            #print("THEREFORE")
            self.newline()
            self.emitter.emitLine("){")

            while not (self.checkToken(TokenType.ELSEIF) or self.checkToken(TokenType.ELSE) or self.checkToken(TokenType.ENDIF)): #if" comparison "therefore" nl statement*
                print("Processing statements in IF block")
                self.statement()
                #print("after")
            self.emitter.emitLine("}")
            
            #print("exit")
            while self.checkToken(TokenType.ELSEIF): #("else if" comparison "therefore" nl statement*)*
                print("ELSE IF")
                self.nextToken()
                self.emitter.emit("else if(")
                self.comparison()

                self.match(TokenType.THEREFORE)
                print("THEREFORE")
                self.newline()
                self.emitter.emitLine("){")

                while not (self.checkToken(TokenType.ELSE) or self.checkToken(TokenType.ENDIF)): #Parse statements in the ELSE IF BLOCK
                    print("Processing statements in ELSE IF block")
                    self.statement()
                
                self.emitter.emitLine("}")
            
            if self.checkToken(TokenType.ELSE): #("else" nl statement*)? Optional Else block
                print("ELSE")
                self.nextToken()
                print("Expecting a NEWLINE after ELSE")
                self.emitter.emit("else{")
                self.newline()
                while not self.checkToken(TokenType.ENDIF): #Parse statements in ELSE block
                    print("Processing statements in ELSE block")
                    self.statement()
                self.emitter.emitLine("}")
            
            self.match(TokenType.ENDIF)
        
        #"while" comparison "do" nl statement* "endwhile" nl
        elif self.checkToken(TokenType.WHILE):
            print("WHILE")
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()

            self.match(TokenType.DO)
            self.newline()
            self.emitter.emitLine("){")

            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            
            self.emitter.emitLine("}")
            self.match(TokenType.ENDWHILE)


        #var" ident ("=" expression)? nl
        elif self.checkToken(TokenType.VAR):
            print("VAR")
            self.nextToken()
            variable_name = self.curr_Token.text

            if self.curr_Token.text not in self.variables:
                self.variables[variable_name] = None #declaring but not initialzing
                
                self.emitter.headerLine("float " + variable_name + ";")
            else:
                sys.exit(f"Variable '{variable_name} already declared.")
        
            self.match(TokenType.IDENTIFIER)

            # Deaks with a variable being declared and initialized at the same time
            if self.checkToken(TokenType.EQUALS):
                self.match(TokenType.EQUALS)
                #print("EQUALS")
                
                self.emitter.emit(variable_name + " = ")
                self.expression()
                
                self.emitter.emitLine(";")
        
        #Purpose: When a variable has already been declared and is now being assigned a new value
        # ident "=" expression nl
        elif self.checkToken(TokenType.IDENTIFIER):
            variable_name = self.curr_Token.text
            if variable_name not in self.variables:
                sys.exit("Variable " + variable_name + " not does not exist.")
            else:
                print("Updating variable: " , variable_name)
            
            self.nextToken()
            self.emitter.emit(variable_name + " = ")
            self.match(TokenType.EQUALS)

            self.expression()
            self.emitter.emitLine(";")

            
        self.newline() #Signifies the end of a statement, without doing this the parser will continue parsing even though it should stop at the end of the current line

    #comparison -> expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    # a + b 
    def comparison(self):
        print("Comparison")
        self.expression()

        if self.checkToken(TokenType.EqEq) or self.checkToken(TokenType.NOTEQUALS) or self.checkToken(TokenType.GREATERTHAN) \
        or self.checkToken(TokenType.GREATERTHANEQ) or self.checkToken(TokenType.LESSTHAN) or self.checkToken(TokenType.LESSTHANEQ): #if a > b and b < c
            self.emitter.emit(self.curr_Token.text)
            self.nextToken()
            self.expression()
        else:
            sys.exit("Expected a comparison operator and receieved " + self.curr_Token.text)
        
        while self.checkToken(TokenType.EqEq) or self.checkToken(TokenType.NOTEQUALS) or self.checkToken(TokenType.GREATERTHAN) \
        or self.checkToken(TokenType.GREATERTHANEQ) or self.checkToken(TokenType.LESSTHAN) or self.checkToken(TokenType.LESSTHANEQ): #look up explanation
            self.emitter.emit(self.curr_Token.text)
            self.nextToken()
            self.expression()

    def expression(self):
        #expression -> term (("-" | "+") term)*
        self.term()

        while( self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS)):
            if self.checkToken(TokenType.PLUS):
                self.emitter.emit(self.curr_Token.text)
                self.match(TokenType.PLUS)
                
            elif self.checkToken(TokenType.MINUS):
                self.emitter.emit(self.curr_Token.text)
                self.match(TokenType.MINUS)
                
            self.term()
    def term(self):
        #term -> unary (("/" | "*") unary)*
        self.unary()

        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            if self.checkToken(TokenType.ASTERISK):
                self.emitter.emit(self.curr_Token.text)
                self.match(TokenType.ASTERISK)
                
            elif self.checkToken(TokenType.SLASH):
                self.emitter.emit(self.curr_Token.text)
                self.match(TokenType.SLASH)
                
                
            self.unary()
    def unary(self):
        #unary -> ("+" | "-")? primary
        print("UNARY")

        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            if self.checkToken(TokenType.PLUS):
                self.emitter.emit(self.curr_Token.text)
                
            elif self.checkToken(TokenType.MINUS):
                self.emitter.emit(self.curr_Token.text)
                
            self.nextToken()

        self.primary()
    def primary(self):
        #primary -> number | ident
        print("PRIMARY")

        #print("Current Token in Primary: ", self.curr_Token.Type, " Value: ", self.curr_Token.text)
        if self.checkToken(TokenType.NUMBER):
            self.emitter.emit(self.curr_Token.text)
            
            self.nextToken()
        elif self.checkToken(TokenType.IDENTIFIER):
            if self.curr_Token.text not in self.variables: #checks if the current identifier or variable being used has first been declared
                sys.exit("Variable " + self.curr_Token.text + " has not been declared.")
            
            self.emitter.emit(self.curr_Token.text)
            self.nextToken() #proceed to next token after confirming that an identifier is valid
        else:
            sys.exit("Unexpected token:  " + self.curr_Token.text)
    def newline(self):
        print("NEWLINE")
        #nl -> '\n'+
        self.match(TokenType.NEWLINE)

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
    

        