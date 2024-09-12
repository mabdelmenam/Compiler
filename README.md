### Small compiler built with Python, used to compiler our own custom programming language and compile the code to C.

--------------------------------------------------------------------------------------------------------------------------------------------

1) **Defining the Tokens:**

--------------------------------------------------------------------------------------------------------------------------------------------

Tokens are the words of the programming langauge, the elements that the language will recognize. 

The Tokens will include *keywords*, *operators*, *identifiers*, *numbers*, and *special symbols* like __=  ==  !=  >  <  >=  <=__

___All of the Token types are located in the `TokenType` class in *lexer.py*.___

--------------------------------------------------------------------------------------------------------------------------------------------
2) **Building the Lexer:** (*Lexical Analyzer* or *Lexical Analysis* )

--------------------------------------------------------------------------------------------------------------------------------------------
The Lexer is responsible for reading the source code and converting it into a stream of tokens. It processes the code character by character
into our predefined token types in our ***TokenType*** class, Types such as *keywords*, *operators*, *identifiers*..etc.

It also removes white spaces, tabs, comments, which are irrelevant to the programs logic.

--------------------------------------------------------------------------------------------------------------------------------------------
3) **Define the Grammar:** The rules for the structure of the language

--------------------------------------------------------------------------------------------------------------------------------------------
`program -> statement*`

`statement -> "print" (expression | string) nl` : A statement can be a PRINT command followed by an 
*expression* or *string*, then a newline

&nbsp;`| "if" comparison "therefore" nl statement* ("else" nl statement*)? "endif" nl` : A statement can be a IF condition followed by THEREFORE, a block of statements, and an ENDIF followed by a newline.  

&nbsp;`| "while" comparison "do" nl statement* "endwhile" nl` : A statement can be a WHILE loop with a condition, followed by a block of statements inside the loop, and ending with ENDWHILE.

&nbsp;`| "var" ident "=" expression nl` : A statement can assign an expression to a variable using ' var ' followed by a newline.

&nbsp;`| "input" ident nl` : A statement can prompt for user input and assign it to a variable (identifier), followed by a newline.

`end statement`

`comparison -> expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+` : two or more expressions compared using relational operators

`expression -> term (("-" | "+") term)*` : An expression consists of one or more terms combined by + or -. Which allows for expressions such as: $${\color{lightgreen}(x + 5 - y * 3)}$$	

`term -> unary (("/" | "*") unary)*` : A term consists of one or more unary expressions combined by * or /.  This builds on top of unary and primary to allow more complex mathematical operations.

`unary -> ("+" | "-")? primary` : A unary expression can optionally have a + or - sign followed by a primary expression. **Example: -5 or +x, x just being a primary**

`primary -> number | ident` : A primary expression is either a number or an identifier (variable).

`nl -> '\n'+` : One or more newline characters

###### ***All of the grammar rules build on top of each other, higher-level rules like __expressions__ rely on lower-level rules like __term__ , which relies on even more lower-level rules like __unary__ and __primary__***

--------------------------------------------------------------------------------------------------------------------------------------------

4) **Create the Parser**: The parser will make sure that the structure of the tokens is correct, it will match the input tokens against the grammar rules, ensuring that the code is valid.

Will use a recursive descent parser using a top down approach

5) Semantic Analysis