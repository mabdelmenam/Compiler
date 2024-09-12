from lexer import *
from parser import *

def main():
    source = 'PRINT x'

    lexer = Lexer(source)
    parser = Parser(lexer)
    #token = lexer.getToken()
    parser.program()
    # 
    """  token = lexer.getToken()
    while( token.Type != TokenType.EOF ):
        print(token.text)
        print(token.Type)     
        token = lexer.getToken()   """

main()