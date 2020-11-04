from pyp.lexer import Lexer
from pyp.parser import Parser


def main(filename):
    with open(filename, 'r') as file:
        code = file.readlines()
    lexer = Lexer(code)
    tokens = lexer.lex()
    parser = Parser(tokens)
    ast = parser.parse()
    if not ast:
        ast.raise_()


if __name__ == '__main__':
    main('code.pyp')
