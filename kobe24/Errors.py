
class UnexpectedCharacterError(Exception):
	pass
	
class UnterminatedStringError(Exception):
	pass
	
class ExpectedTokenError(Exception):
	pass
	
class Return(Exception):
	def __init__(self, value):
		self.value = value
		
	def getValue(self):
		return self.value
		
class Continue(Exception):
	pass
	
class Break(Exception):
	pass