class Emitter:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""
    #write the header (variable declarations, includes)
    def headerLine(self, code):
        self.header += code + '\n'
    def addComment(self, comment):
        self.code += "/* " + comment + " */\n"
    #write code to main body of C file
    def emit(self,code):
        self.code +=code
    #Adds last piece of code and a newline
    def emitLine( self, code ):
        self.code += code + '\n'
    def writeFile(self):
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)