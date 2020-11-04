from pyp.tokens import FUNCS, NL, LEFT_BPB, RIGHT_BPB
from pyp.errors import InvalidSyntaxError
from pprint import pprint
from pyp.ast import AST


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.in_ = None
        self.lines = self.split_list(self.tokens, NL)
        self.ast = AST()

    def parse(self):
        for ln_, line in enumerate(self.lines):
            ln = ln_ + 1
            for ind, token in enumerate(line):
                if token['val'] in FUNCS:
                    res = self.func(ind, line, ln)
                    if res:
                        self.ind_ = 'func'
                    else:
                        return res
                elif self.in_ == 'func' and token['val']:
                    pass
        return self.ast

    def func(self, ind, line, ln):
        if not line[ind + 1] == LEFT_BPB:
            return InvalidSyntaxError('expected \'<\' after \'' + line[ind]['val'] + '\' - line ' + str(ln))
        if not RIGHT_BPB in line:
            return InvalidSyntaxError('missing \'>\' - line ' + str(ln))
        funcl_sepd = line[2:]
        rsplitd = self.split_list(funcl_sepd, RIGHT_BPB)
        pprint(rsplitd)  # CONTINUE HERE
        return True

    def split_list(self, lst, by):
        major = []
        minor = []
        for val in lst:
            if val == by:
                major.append(minor)
                minor = []
            else:
                minor.append(val)
        major.append(minor)
        return major
