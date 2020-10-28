from Token import Token
from TokenType import TokenType
from Errors import UnexpectedCharacterError, UnterminatedStringError

class Scanner:	
	keywords = {
		'write' : TokenType.WRITE,
		'writeln' : TokenType.WRTLN,
		'true' : TokenType.TRUE,
		'false' : TokenType.FALSE,
		'if' : TokenType.IF,
		'else' : TokenType.ELSE,
		'while' : TokenType.WHILE,
		'or': TokenType.OR,
		'and': TokenType.AND,
		'function' : TokenType.FUN,
		'return' : TokenType.RET,
		'next' : TokenType.CON,
		'break' : TokenType.BRK,
		'list': TokenType.LST,
		'map': TokenType.MAP,
		'null': TokenType.NULL
	}

	def __init__(self):
		self.tokens = []
		self.row = 1
		self.col = 1
		self.i = 0
		

	def scan(self, codebase):
		self.codebase = codebase
		self.code_len = len(self.codebase)
		while self.i < self.code_len:
			ch = self.codebase[self.i]
			nxt = self.peekNext()
			if ch.isalpha() or ch == '_':
				self.processAlpha()
			elif ch.isnumeric():
				self.processNumber()
			elif ch == ':':
				self.addToken(TokenType.COL, ch)
			elif ch == '.':
				self.addToken(TokenType.DOT, ch)
			elif ch == '{':
				self.addToken(TokenType.LCUR, ch)
			elif ch == '}':
				self.addToken(TokenType.RCUR, ch)
			elif ch == '[':
				self.addToken(TokenType.LBRC, ch)
			elif ch == ']':
				self.addToken(TokenType.RBRC, ch)
			elif ch == '+':
				self.addToken(TokenType.ADD, ch)
			elif ch == '-':
				self.addToken(TokenType.SUB, ch)
			elif ch == '%':
				self.addToken(TokenType.MOD, ch)
			elif ch == '*':
				if nxt == '*':
					self.addToken(TokenType.POW, ch + nxt)
				else:
					self.addToken(TokenType.MUL,ch)
			elif ch == '/':
				if nxt == '/':
					self.addToken(TokenType.FDIV, ch + nxt)
				else:
					self.addToken(TokenType.DIV, ch)
			elif ch == '(':
			    self.addToken(TokenType.LPAR, ch)
			elif ch == ')':
				self.addToken(TokenType.RPAR, ch)
			elif ch == '=':
				if nxt == '=':
					self.addToken(TokenType.EQ, ch + nxt)
				else:
					self.addToken(TokenType.ASGN, ch)
			elif ch == '!':
				if nxt == '=':
					self.addToken(TokenType.NEQ, ch + nxt)
				else:
					self.addToken(TokenType.NEG, ch)
			elif ch == '<':
				if nxt == '=':
					self.addToken(TokenType.LTE, ch + nxt)
				elif nxt == '<':
					self.addToken(TokenType.BSL, ch + nxt)
				else:
					self.addToken(TokenType.LT, ch)
			elif ch == '>':
				if nxt == '=':
					self.addToken(TokenType.GTE, ch + nxt)
				elif nxt == '>':
					self.addToken(TokenType.BSR, ch + nxt)
				else:
					self.addToken(TokenType.GT, ch)
			elif ch == '&':
				self.addToken(TokenType.BAND, ch)
			elif ch == '|':
				self.addToken(TokenType.BOR, ch)
			elif ch == '^':
				self.addToken(TokenType.BXOR, ch)
			elif ch == '~':
				self.addToken(TokenType.BOC, ch)
			elif ch == '"':
				self.processString()
			elif ch == ',':
				self.addToken(TokenType.COM, ch)
			elif ch == '\n':
				self.row += 1
				self.col = 1
				self.i += 1
			elif ch.isspace():
				self.i += 1
				self.col += 1
			else:
				raise UnexpectedCharacterError(self.codebase[self.i], self.row, self.col)
		
		self.addToken(TokenType.EOF, '$') 
		return self.tokens
		
	def peekNext(self):
		if self.i + 1 < self.code_len:
			return self.codebase[self.i + 1]
		return None
		
	def addToken(self, type, text, literal=None):
		tlen = len(text)
		self.tokens.append(Token(type, text, literal, self.row, self.row, self.col, self.col+tlen-1))
		self.col += tlen
		self.i += tlen

	def processString(self):
		cur_i = self.i + 1
		row = self.row
		col = self.col
		while cur_i < self.code_len and self.codebase[cur_i] != '"':
			if self.codebase[cur_i] == '\\':
				cur_i += 1
				self.col += 1
			if self.codebase[cur_i] == '\n':
				self.row += 1
				self.col = 0
			cur_i += 1
			self.col += 1
			

		if cur_i == self.code_len:
			raise UnterminatedStringError(row, col)
		else:
			text = self.codebase[self.i:cur_i + 1]
			literal = self.codebase[self.i + 1:cur_i]
			literal = literal.replace('\\n', '\n')
			self.col += 1
			self.tokens.append(Token(TokenType.STR, text, literal, row, self.row, col, self.col))
			self.col += 1
			self.i = cur_i + 1
					
	def processNumber(self):
		cur_i = self.i
		while cur_i < self.code_len and self.codebase[cur_i].isnumeric():
			cur_i += 1
		
		if cur_i < self.code_len and self.codebase[cur_i] == '.':
			cur_i += 1
			while cur_i < self.code_len and self.codebase[cur_i].isnumeric():
				cur_i += 1
				
		text = self.codebase[self.i:cur_i]
		literal = None
		if "." in text:
			literal = float(text)
		else:
			literal = int(text)
		self.addToken(TokenType.NUM, text, literal)
		
	def processAlpha(self):
		cur_i = self.i
		while cur_i < self.code_len and (self.codebase[cur_i].isalnum() or self.codebase[cur_i] == '_'):
			cur_i += 1
		text = self.codebase[self.i:cur_i]
		cur_type = None
		if text in Scanner.keywords:
			cur_type = Scanner.keywords[text]
		else:
			cur_type = TokenType.VAR
		
		if text == "true":
			self.addToken(cur_type, text, True)
		elif text == "false":
			self.addToken(cur_type, text, False)
		else:
			self.addToken(cur_type, text)
		
		
	 
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	