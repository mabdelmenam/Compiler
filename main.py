from lexer import *

def main():
    source = "=-"

    lexer = Lexer(source)
    token = lexer.getToken()

    while( token.Type != TokenType.EOF ):
        print(lexer.currChar)
        print("\n", token.Type)     
        token = lexer.getToken()   

main()