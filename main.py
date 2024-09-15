from lexer import *
from parser import *

def main():
    #source = 'VAR x = 5'

    if len(sys.argv) != 2 :
        sys.exit("Expected 2 arguments, please include source file as arugment.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    lexer = Lexer(source)
    parser = Parser(lexer)
    #token = lexer.getToken()
    parser.program()
    print("Parsing Complete")
    # 
    """  token = lexer.getToken()
    while( token.Type != TokenType.EOF ):
        print(token.text)
        print(token.Type)     
        token = lexer.getToken()   """

main()