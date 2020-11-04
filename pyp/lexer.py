from codecs import decode
from pyp.tokens import FUNCS, NL, LEFT_BPB, RIGHT_BPB, COMMA_SEP, DIV_OP, MULT_OP, ADD_OP, SUB_OP
from string import digits


class Lexer:
	def __init__(self, code):
		self.code = code
		self.tokens = []
		self.escape = False

	def lex(self):
		for line in self.code:
			chars = ''
			id = ''
			if line in '\n\t\r ':
				continue
			for char in line:
				if chars in FUNCS:
					self.tokens.append({'id': 'func', 'val': chars})
					chars = ''
				if char == '"' and id == '':
					id = 'str'
				elif char == '\\':
					self.escape = True
					continue
				elif char == '"' and id == 'str' and self.escape:
					chars += '"'
					self.escape = False
				elif char and id == 'str' and self.escape:
					chars += decode('\\' + char, 'unicode_escape')
					self.escape
				elif char != '"' and id == 'str':
					chars += char
				elif char == '"' and id == 'str':
					self.tokens.append({'id': id, 'val': chars})
					chars = ''
					id = ''
				elif char in digits and id != 'num':
					id = 'num'
					chars += char
				elif char in digits and id == 'num':
					chars += char
				elif char == '.' and id == 'num':
					chars += '.'
				elif char not in digits and id == 'num':
					try:
						self.tokens.append({'id': 'int', 'val': int(chars)})
					except:
						self.tokens.append(
							{'id': 'float', 'val': float(chars)})
					id = ''
					chars = ''
					if char == '<':
						# BPB stands for Brackets, Parenthesis, and Braces
						self.tokens.append(LEFT_BPB)
						chars = ''
					elif char == '>':
						self.tokens.append(RIGHT_BPB)
						chars = ''
					elif char == ',':
						self.tokens.append(COMMA_SEP)
						chars = ''
					elif char == '/':
						self.tokens.append(DIV_OP)
						chars = ''
					elif char == '*':
						self.tokens.append(MULT_OP)
						chars = ''
					elif char == '+':
						self.tokens.append(ADD_OP)
						chars = ''
					elif char == '-':
						self.tokens.append(SUB_OP)
						chars = ''
					elif char == ' ':
						pass
					elif char == '\n':
						self.tokens.append(NL)
					else:
						chars += char
					self.escape = False
					continue
				elif char == '<':
					# BPB stands for Brackets, Parenthesis, and Braces
					self.tokens.append(LEFT_BPB)
					chars = ''
				elif char == '>':
					self.tokens.append(RIGHT_BPB)
					chars = ''
				elif char == ',':
					self.tokens.append(COMMA_SEP)
					chars = ''
				elif char == '/':
					self.tokens.append(DIV_OP)
					chars = ''
				elif char == '*':
					self.tokens.append(MULT_OP)
					chars = ''
				elif char == '+':
					self.tokens.append(ADD_OP)
					chars = ''
				elif char == '-':
					self.tokens.append(SUB_OP)
					chars = ''
				elif char == ' ':
					pass
				elif char == '\n':
					self.tokens.append(NL)
				else:
					chars += char
				self.escape = False
		return self.tokens
