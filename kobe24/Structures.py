from Errors import ExpectedArgCount, ArgumentNotMatchException, UndefinedMethodException

class List(list):
	methods = ["push", "pop", "insert", "size", "clear"]
	
	def call(self, method, args):
		if method.text in self.methods:
			try:
				if method.text == "push":
					return self.push(args)
				if method.text == "pop":
					return self._pop(args)
				if method.text == "insert":
					return self._insert(args)
				if method.text == "clear":
					return self._clear(args)
				if method.text == "size":
					return self.size(args)
			except ExpectedArgCount as expc:
				raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, expc.getExpCount())
		else:
			raise UndefinedMethodException(method.text, method.row_b, method.col_b)
				
	def push(self, args):
		if len(args) == 1:
			self.append(args[0])
			return self
		else:
			raise ExpectedArgCount(1)
			
	def _pop(self, args):
		if len(args) == 0:
			self.pop()
			return self
		else:
			raise ExpectedArgCount(0)
			
	def _insert(self, args):
		if len(args) == 2:
			self.insert(args[0], args[1])
			return self
		else:
			raise ExpectedArgCount(2)
			
	def size(self, args):
		if len(args) == 0:
			return len(self)
		else:
			raise ExpectedArgCount(0)
			
	def _clear(self, args):
		if len(args) == 0:
			self.clear()
			return self
		else:
			raise ExpectedArgCount(0)
	
class Map(dict):
	methods = ["remove", "clear", "keys", "values", "size", "contains"]
	
	def call(self, method, args):
		if method.text in self.methods:
			try:
				if method.text == "remove":
					return self.remove(args)
				if method.text == "clear":
					return self._clear(args)
				if method.text == "keys":
					return self._keys(args)
				if method.text == "values":
					return self._values(args)
				if method.text == "size":
					return self.size(args)
				if method.text == "contains":
					return self.contains(args)
			except ExpectedArgCount as expc:
				raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, expc.getExpCount())
		else:
			raise UndefinedMethodException(method.text, method.row_b, method.col_b)
			
	def contains(self, args):
		if len(args) == 1:
			if args[0] in self:
				return True
			return False
		else:
			raise ExpectedArgCount(1)	
			
	def remove(self, args):
		if len(args) == 1:
			self.pop(args[0])
			return self
		else:
			raise ExpectedArgCount(1)
			
	def _clear(self, args):
		if len(args) == 0:
			self.clear()
			return self
		else:
			raise ExpectedArgCount(0)

	def size(self, args):
		if len(args) == 0:
			return len(self)
		else:
			raise ExpectedArgCount(0)
			
	def _keys(self, args):
		if len(args) == 0:
			return List(self.keys())
		else:
			raise ExpectedArgCount(0)
			
	def _values(self, args):
		if len(args) == 0:
			return List(self.values())
		else:
			raise ExpectedArgCount(0)
	
class String(str):
	methods = ["size"]
	
	def call(self, method, args):
		if method.text in self.methods:
			try:
				if method.text == "size":
					return self.size(args)
			except ExpectedArgCount as expc:
				raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, expc.getExpCount())
		else:
			raise UndefinedMethodException(method.text, method.row_b, method.col_b)	
	
	def size(self, args):
		if len(args) == 0:
			return len(self)
		else:
			raise ExpectedArgCount(0)
		