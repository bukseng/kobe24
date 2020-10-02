from Errors import UndefinedException

class Environment:
    		
	def __init__(self, env=None):
		self.values = {}
		self.outer = env
		
	def assign(self, name, value):
		if name.text in self.values:
			self.values[name.text] = value
		elif self.checkOuter(name.text) == True:
			self.outer.assign(name, value)
		else:
			self.values[name.text] = value
			
	def define(self, name, value):
		self.values[name.text] = value
			
	def checkOuter(self, name):
		if self.outer is not None:
			if name in self.outer.values:
				return True
			else:
				return self.outer.checkOuter(name)
		else:
			return False
		
	def getValue(self, name):
		if name.text in self.values:
			return self.values[name.text]
			
		if self.checkOuter(name.text) == True:
			return self.outer.getValue(name)
			
		raise UndefinedException(name.text, name.row_b, name.col_b)