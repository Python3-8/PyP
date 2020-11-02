from codecs import decode
from string import digits

class Lexer:
	def __init__(self, code):
		self.code = code
		self.tokens = []
		self.escape = False
		self.funcs = ['writeLine']
	
	def lex(self):
		for line in self.code:
			chars = ''
			id = ''
			if line in '\n\t\r ':
				continue
			for char in line:
				if chars in self.funcs:
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
						self.tokens.append({'id': 'float', 'val': float(chars)})
					id = ''
					chars = ''
					if char == '<':
						self.tokens.append({'id': 'ang-brac', 'val': '<'})
						chars = ''
					elif char == '>':
						self.tokens.append({'id': 'ang-brac', 'val': '>'})
						chars = ''
					elif char == ',':
						self.tokens.append({'id': 'sep', 'val': ','})
						chars = ''
					elif char == ' ':
						pass
					elif char == '\n':
						self.tokens.append({'id': 'nl', 'val': '\n'})
					else:
						chars += char
					self.escape = False
					continue
				elif char == '<':
					self.tokens.append({'id': 'bpb', 'val': '<'}) # BPB stands for Brackets, Parenthesis, and Braces
					chars = ''
				elif char == '>':
					self.tokens.append({'id': 'bpb', 'val': '>'})
					chars = ''
				elif char == ',':
					self.tokens.append({'id': 'sep', 'val': ','})
					chars = ''
				elif char == '/':
					self.tokens.append({'id': 'op', 'val': '/'})
					chars = ''
				elif char == '*':
					self.tokens.append({'id': 'op', 'val': '*'})
					chars = ''
				elif char == '+':
					self.tokens.append({'id': 'op', 'val': '+'})
					chars = ''
				elif char == '-':
					self.tokens.append({'id': 'op', 'val': '-'})
					chars = ''
				elif char == ' ':
					pass
				elif char == '\n':
					self.tokens.append({'id': 'nl', 'val': '\n'})
				else:
					chars += char
				self.escape = False
		return self.tokens