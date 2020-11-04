class AST:
    def __init__(self, py=''):
        self.py = py

    def __add__(self, code):
        return AST(self.py + code + '\n')
