from pprint import pprint
from pyp.lexer import Lexer
from pyp.parser import *

def main(filename):
    with open(filename, 'r') as file:
        code = file.readlines()
    lexer = Lexer(code)
    tokens = lexer.lex()
    pprint(tokens)

if __name__ == '__main__':
    main('code.pyp')