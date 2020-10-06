class SuperException(Exception):
	def getLocation(self):
		return " at line " + str(self.line) + ", column " + str(self.col)

class UnexpectedCharacterError(SuperException):
	def __init__(self, char, line, col):
		self.line = line
		self.col = col
		self.char = char	
		
	def getMessage(self):
		return "Unexpected character '" + self.char + "'" + self.getLocation()
	
class UnterminatedStringError(SuperException):
	def __init__(self, line, col):
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Unterminated string starting" + self.getLocation()
	
class UnexpectedTokenError(SuperException):
	def __init__(self, text, line, col):
		self.text = text
		self.line = line
		self.col = col
	
	def getMessage(self):
		return "Unexpected token '" + self.text + "'" + self.getLocation()
	
class UndefinedException(SuperException):
	def __init__(self, name, line, col):
		self.name = name
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Undefined '" + self.name + "'" + self.getLocation()
	
class InvalidIndexException(SuperException):
	def __init__(self, index, line, col):
		self.index = index
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Invalid index '" + str(self.index) + "'" + self.getLocation()
		
class UndefinedMethodException(SuperException):
	def __init__(self, name, line, col):
		self.name = name
		self.line = line
		self.col = col
	
	def getMessage(self):
		return "Undefined method '" + self.name + "'" + self.getLocation()

class ArgumentNotMatchException(SuperException):
	def __init__(self, name, line, col, exp):
		self.name = name
		self.line = line
		self.col = col
		self.exp = exp
		
	def getMessage(self):
		return "Method/Function '" + self.name + "'" + self.getLocation() + " expects " + str(self.exp) + " argument(s)"
	
class IllegalDivisionException(SuperException):
	def __init__(self, line, col):
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Illegal division by zero" + self.getLocation()

class InvalidOperationException(SuperException):
	def __init__(self, text, line, col):
		self.text = text
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Invalid operation '" + self.text + "'" + self.getLocation()

class Return(SuperException):
	def __init__(self, line, col, value):
		self.line = line
		self.col = col
		self.value = value
		
	def getValue(self):
		return self.value
		
	def getMessage(self):
		return "Invalid command 'return'" + self.getLocation()
		
class Continue(SuperException):
	def __init__(self, line, col):
		self.line = line
		self.col = col
	
	def getMessage(self):
		return "Invalid command 'next'" + self.getLocation()
		
class Break(SuperException):
	def __init__(self, line, col):
		self.line = line
		self.col = col
		
	def getMessage(self):
		return "Invalid command 'break'" + self.getLocation() 
		
class ExpectedArgCount(Exception):
	def __init__(self, expc):
		self.expc = expc
		
	def getExpCount(self):
		return self.expc
