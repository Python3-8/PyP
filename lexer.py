class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.funcs = ['writeLine']
    
    def lex(self):
        for line in self.code:
            chars = ''
            id = ''
            for char in line:
                print(chars)
                if chars in self.funcs:
                    self.tokens.append({'id': 'func', 'val': chars})
                    chars = ''
                elif char == '"' and id == '':
                    id = 'str'
                elif char != '"' and id == 'str':
                    chars += char
                elif char == '"' and id == 'str':
                    self.tokens.append({'id': id, 'val': chars})
                    chars = ''
                    id = ''
                elif char == ':':
                    self.tokens.append({'id': 'op', 'val': ':'})
                    chars = ''
                elif char == ' ':
                    pass
                else:
                    chars += char
        return self.tokens