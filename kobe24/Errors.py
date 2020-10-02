
class UnexpectedCharacterError(Exception):
	def __init__(self, char, line, col):
		self.line = line
		self.col = col
		self.char = char	
		
	def getMessage(self):
		return "Unexpected character '" + self.char + "' at line " + str(self.line) + ", column " + str(self.col)
	
class UnterminatedStringError(Exception):
	def __init__(self, line, col):
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Unterminated string starting at line " + str(self.line) + ", column " + str(self.col)
	
class UnexpectedTokenError(Exception):
	def __init__(self, text, line, col):
		self.text = text
		self.line = line
		self.col = col
	
	def getMessage(self):
		return "Unexpected token '" + self.text + "' at line " + str(self.line) + ", column " + str(self.col)
	
class UndefinedException(Exception):
	def __init__(self, name, line, col):
		self.name = name
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Undefined '" + self.name + "' at line " +str(self.line) + ", column " + str(self.col)
	
class InvalidIndexException(Exception):
	def __init__(self, index, line, col):
		self.index = index
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Invalid index '" + str(self.index) + "' at line " + str(self.line) + ", column " + str(self.col)
		
class UndefinedMethodException(Exception):
	def __init__(self, name, line, col):
		self.name = name
		self.line = line
		self.col = col
	
	def getMessage(self):
		return "Undefined method '" + self.name + "' at line " + str(self.line) + ", column " + str(self.col)

class ArgumentNotMatchException(Exception):
	def __init__(self, name, line, col, exp):
		self.name = name
		self.line = line
		self.col = col
		self.exp = exp
		
	def getMessage(self):
		return "Method/Function '" + self.name + "' at line " + str(self.line) + ", column " + str(self.col) + " expects " + str(self.exp) + " argument(s)"
	
class IllegalDivisionException(Exception):
	def __init__(self, line, col):
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Illegal division by zero at line " + str(self.line) + ", column " + str(self.col)

class InvalidOperationException(Exception):
	def __init__(self, text, line, col):
		self.text = text
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Invalid operation '" + self.text + "' at line " + str(self.line) + ", column " + str(self.col)

class Return(Exception):
	def __init__(self, line, col, value):
		self.line = line
		self.col = col
		self.value = value
		
	def getValue(self):
		return self.value
		
	def getMessage(self):
		return "Invalid command 'return' at line " + str(self.line) + ", column " + str(self.col) 
		
class Continue(Exception):
	def __init__(self, line, col):
		self.line = line
		self.col = col
	
	def getMessage(self):
		return "Invalid command 'next' at line " + str(self.line) + ", column " + str(self.col) 
		
class Break(Exception):
	def __init__(self, line, col):
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Invalid command 'break' at line " + str(self.line) + ", column " + str(self.col) 
