# CONTINUE: FIX ANGLE BRACKET ISSUE
from pyp.tokens import FUNCS, NL, LEFT_BPB, RIGHT_BPB, COMMA_SEP
from pyp.needed_classes import obj, sep
from pyp.funcs import PYP_PY
from pyp.errors import InvalidSyntaxError
from pyp.types import TYPES
from pyp.ast import AST


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.in_ = ()
        self.lines = self.split_list(self.tokens, NL)
        self.ast = AST()

    def parse(self):
        for ln_, line in enumerate(self.lines):
            ln = ln_ + 1
            for ind, token in enumerate(line):
                if token['val'] in FUNCS:
                    res = self.func(ind, line, ln)
                    if res:
                        self.in_ = 'func', res[1]
                        self.ast += res[0]
                    else:
                        return res
                elif 'func' in self.in_ and token['val']:
                    if ind == self.in_[1]:
                        self.in_ = ()
        return self.ast

    def func(self, ind, line, ln):
        if not line[ind + 1] == LEFT_BPB:
            return InvalidSyntaxError('expected \'<\' after ' + line[ind]['val'] + ' - line ' + str(ln))
        if not RIGHT_BPB in line:
            return InvalidSyntaxError('missing \'>\' - line ' + str(ln))
        funcl_sepd = line[2:]
        rsplitd = self.split_list(funcl_sepd, RIGHT_BPB)
        rbpb_ind = line.index(RIGHT_BPB)
        last_type = None
        last_obj = None
        pyfunc = PYP_PY[line[ind]['val']]
        pyline = pyfunc[0]
        passed_vals = []
        for tkind, token in enumerate(rsplitd[0]):
            if last_type == obj:
                if tkind != len(rsplitd) and token != COMMA_SEP:
                    return InvalidSyntaxError('expected \',\' after ' + str(last_obj) + ' - line ' + str(ln))
                last_type = sep
            elif last_type == sep:
                if not token['id'] in TYPES:
                    return InvalidSyntaxError('expected object after \',\' - line ' + str(ln))
                passed_vals.append(repr(token['val']))
                last_obj = token['val'] if token['id'] != 'str' else (
                    '"' + token['val'] + '"')
                last_type = obj
            elif not last_type:
                if not token['id'] in TYPES:
                    return InvalidSyntaxError('expected object after \',\' - line ' + str(ln))
                passed_vals.append(repr(token['val']))
                last_obj = token['val'] if token['id'] != 'str' else (
                    '"' + token['val'] + '"')
                last_type = obj
        pyline += ', '.join(passed_vals) + pyfunc[1]
        return pyline, rbpb_ind

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
