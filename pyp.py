from pprint import pprint
from lexer import Lexer

def main(filename):
    with open(filename, 'r') as file:
        code = file.readlines()
    lexer = Lexer(code)
    tokens = lexer.lex()
    pprint(tokens)

if __name__ == '__main__':
    main('ex.pyp')