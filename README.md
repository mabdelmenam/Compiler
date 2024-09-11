#### Small compiler built with Python, used to compiler our own custom programming language and compile the code to C.

1) **Defining the Tokens:**

--------------------------------------------------------------------------------------------------------------------------------------------

Tokens are the words of the programming langauge, the elements that the language will recognize. 

The Tokens will include *keywords*, *operators*, *identifiers*, *numbers*, and *special symbols* like __=  ==  !=  >  <  >=  <=__

***All of the Token types are located in the ***TokenType*** class in *lexer.py*. ***

--------------------------------------------------------------------------------------------------------------------------------------------
2) **Building the Lexer:** (*Lexical Analyzer* or *Lexical Analysis* )

--------------------------------------------------------------------------------------------------------------------------------------------
The Lexer is responsible for reading the source code and converting it into a stream of tokens. It processes the code character by character
into our predefined token types in our ***TokenType*** class, Types such as *keywords*, *operators*, *identifiers*..etc.

It also removes white spaces, tabs, comments, which are irrelevant to the programs logic.

--------------------------------------------------------------------------------------------------------------------------------------------
3) **Define the Grammar:** The rules for the structure of the language

--------------------------------------------------------------------------------------------------------------------------------------------
```
**program -> statement*** A program consists of zero or more statements  

**statement -> "PRINT" (expression | string) nl**  : A statement can be a PRINT command followed by an *expression* or *string*, then a newline  
    **| "IF" comparison "THEREFORE" nl statement* "ENDIF" nl**  A statement can be a IF condition followed by THEREFORE, a block of statements, and an ENDIF followed by a newline.  
    **| "WHILE" comparison "REPEAT" nl statement* "ENDWHILE" nl**  
    **| "LABEL" ident nl**  
    **| "GOTO" ident nl**  
    **| "LET" ident "=" expression nl**  
    **| "INPUT" ident nl**

**comparison -> expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+**

**expression -> term (("-" | "+") term)**

**term -> unary (("/" | "*") unary)**

**unary -> ("+" | "-")? primary**

**primary -> number | ident**

**nl -> '\n'+**
```


--------------------------------------------------------------------------------------------------------------------------------------------

Why Use Terms, Unary, and Primary?

Primary: Can be either a number or an identifier, the most basic element of the grammar rules.

Unary: Handles optional unary operators (+, -) in front of primary expressions. **Example: -5 or +x, x just being a primary**

Term: A term is a combination of unary expressions connected by multiplication or division (* or /). This builds on top of unary and primary to allow more complex mathematical operations.

Expression: An expression combines terms using addition and subtraction (+, -). This gives a full range of arithmetic expressions like  ( x + 5 - y * 3 ) .

***All of the grammar rules build on top of each other, higher-level rules like __expressions__ rely on lower-level rules like __term__ , which relies on even more lower-level rules like __unary__ and __primary__***


2) Create the Parser: The parser will make sure that the structure of the tokens is correct, it will match the input tokens against the grammar rules, ensuring that the code is valid.

Will use a recursive descent parser using a top down approach