class Lexer:
	def __init__(self, code):
		self.code = code
		self.tokens = []
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
				elif char == '\n':
					self.tokens.append({'id': 'nl', 'val': '\n'})
				else:
					chars += char
		return self.tokens