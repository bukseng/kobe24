
class Environment:
    		
	def __init__(self, env=None):
		self.values = {}
		self.outer = env
		
	def assign(self, name, value):
		if name in self.values:
			self.values[name] = value
		elif self.checkOuter(name) == True:
			self.outer.assign(name, value)
		else:
			self.values[name] = value
			
	def define(self, name, value):
		self.values[name] = value
			
	def checkOuter(self, name):
		if self.outer is not None:
			if name in self.outer.values:
				return True
			else:
				return self.outer.checkOuter(name)
		else:
			return False
		
	def getValue(self, name):
		if name in self.values:
			return self.values[name]
			
		if self.outer is not None:
			return self.outer.getValue(name)
		
		raise Exception