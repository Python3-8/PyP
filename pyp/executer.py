class Executer:
    def __init__(self, ast):
        self.ast = ast

    def execute(self):
        exec(self.ast.py)
