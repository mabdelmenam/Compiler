Small compiler built with Python, used to compiler our own custom programming language and compile the code to C.

1) Define the Grammar : The rules for the structure of the language
Example grammar: 
statement  -> IF expression THEN block ENDIF
           |  LET IDENT = expression
           |  PRINT expression
expression -> IDENT | NUMBER | expression + expression

statement -> let_statement | if_statement | print_statement
let_statement -> LET IDENT = expression
if_statement -> IF condition THEN block ENDIF
expression -> IDENT | NUMBER | expression + expression

2) Create the Parser: The parser will make sure that the structure of the tokens is correct, it will match the input tokens against the grammar rules, ensuring that the code is valid.