import random
from Errors import ExpectedArgCount

class RandInt:	
	def call(self, args):
		if len(args) == 2:
			return random.randint(args[0], args[1])
		else:
			raise ExpectedArgCount(2)
			
			
class RandFloat:
	def call(self, args):
		if len(args) == 2:
			return random.uniform(args[0], args[1])
		else:
			raise ExpectedArgCount(2)
