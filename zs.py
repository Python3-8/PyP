from lexer import Lexer

def main(filename):
    with open(filename, 'r') as file:
        code = file.read()
    lexer = Lexer(code)
    tokens = lexer.lex()
    print(tokens)

if __name__ == '__main__':
    main('ex.zs')