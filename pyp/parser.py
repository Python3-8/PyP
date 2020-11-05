# CONTINUE: FIX ANGLE BRACKET ISSUE
from pyp.tokens import FUNCS, NL, LEFT_BPB, RIGHT_BPB, COMMA_SEP, OPS
from pyp.id_classes import obj, sep, op
from pyp.funcs import PYP_PY
from pyp.errors import InvalidSyntaxError, InvalidTypeError
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
        if line[ind + 1] != LEFT_BPB:
            return InvalidSyntaxError('expected \'<\' after ' + line[ind]['val'] + ' - line ' + str(ln))
        if line.count(LEFT_BPB) > 1:
            return InvalidSyntaxError('unexpected \'<\' - line ' + str(ln))
        if not RIGHT_BPB in line:
            return InvalidSyntaxError('missing \'>\' - line ' + str(ln))
        if line.count(RIGHT_BPB) > 1:
            return InvalidSyntaxError('unexpected \'>\' - line ' + str(ln))
        funcl_sepd = line[2:]
        rsplitd = self.split_list(funcl_sepd, RIGHT_BPB)
        rbpb_ind = line.index(RIGHT_BPB)
        last_type = None
        last_obj = {}
        in_op = False
        calc_ready = False
        calc = ''
        pyfunc = PYP_PY[line[ind]['val']]
        pyline = pyfunc[0]
        passed_vals = []
        for tkind, token in enumerate(rsplitd[0]):
            if tkind == len(rsplitd[0]) - 2 and last_type == obj and type(last_obj) in [int, float]:
                calc_ready = True if in_op else False
            if last_type == obj:
                if tkind != len(rsplitd[0]) and token != COMMA_SEP and not token in OPS:
                    return InvalidSyntaxError('expected \',\' or operator after ' + str(last_obj) + ' - line ' + str(ln))
                if token == COMMA_SEP:
                    last_type = sep
                    if type(last_obj) in [int, float]:
                        calc_ready = True if in_op else False
                elif token in OPS:
                    calc += (str(last_obj) + ' ') if not in_op else ''
                    # CONTINUE: FIX CALCULATIONS
                    last_type = op
                    in_op = last_obj
                last_obj = token
            elif last_type == sep:
                if not token['id'] in TYPES:
                    return InvalidSyntaxError('expected object after \',\' - line ' + str(ln))
                if tkind != len(rsplitd[0]) and not line[tkind + 1] in OPS:
                    passed_vals.append(repr(token['val']))
                last_obj = token['val'] if token['id'] != 'str' else (
                    '"' + token['val'] + '"')
                last_type = obj
            elif last_type == op:
                if not token['id'] in TYPES:
                    return InvalidSyntaxError('expected object after \'' + last_obj['val'] + '\' - line ' + str(ln))
                append_val = last_obj['val'] + ' ' + repr(token['val']) + ' '
                try:
                    eval(calc + append_val)
                except TypeError as err:
                    return InvalidTypeError(str(err))
                calc += append_val
                last_type = obj
                last_obj = token['val'] if token['id'] != 'str' else (
                    '"' + token['val'] + '"')
            elif not last_type:
                if not token['id'] in TYPES:
                    return InvalidSyntaxError('expected object after \',\' - line ' + str(ln))
                passed_vals.append(repr(token['val']))
                last_obj = token['val'] if token['id'] != 'str' else (
                    '"' + token['val'] + '"')
                last_type = obj
            if calc_ready:
                passed_vals.append(calc)
                calc_ready = False
                in_op = False
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
