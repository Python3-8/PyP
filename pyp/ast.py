class AST:
    def __init__(self):
        self.py = ''

    def __add__(self, code):
        return self.py + code + '\n'
