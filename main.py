from lexer import *
from parser import *
from emitter import *

def main():
    #source = 'VAR x = 5'

    if len(sys.argv) != 2 :
        sys.exit("Expected 2 arguments, please include source file as arugment.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    lexer = Lexer(source)
    emitter = Emitter("mycode.c")
    parser = Parser(lexer, emitter)
    
    parser.program()
    emitter.writeFile()
    print("Parsing Complete")

main()