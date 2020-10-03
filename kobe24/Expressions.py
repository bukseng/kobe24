from TokenType import TokenType
from Environment import Environment
from Errors import *
from Kobe import Kobe

cur_env = Environment()
kobes = []

def isTrue(bool):
	if bool == True:
		return True
	elif bool == False:
		return False
	elif bool is not None:
		return True
	else:
		return False
		
def copyVal(value):
	if isinstance(value, List) or isinstance(value, Map):
		return value.copy()
	else:
		return value
		
class SuperExpr:
	def setKobe(self, row_b, row_e, col_b, col_e, text):
		self.col_b = col_b
		self.col_e = col_e
		self.row_b = row_b
		self.row_e = row_e
		self.text = text

class BinaryExpr(SuperExpr):
	def __init__(self, left, oper, right):
		self.left = left
		self.oper = oper
		self.right = right
		
	def eval(self):
		left = self.left.eval()
		right = self.right.eval()
		value = None
		try:
			if self.oper.type == TokenType.ADD:
				if isinstance(left, str) or isinstance(right, str):
					value = str(left) + str(right)
				else:
					value = left + right
			elif self.oper.type == TokenType.SUB:
				value = left - right
			elif self.oper.type == TokenType.MUL:
				value = left * right
			elif self.oper.type == TokenType.FDIV:
				if right == 0:
					raise IllegalDivisionException(self.row_b, self.col_b)
				value = left // right
			elif self.oper.type == TokenType.DIV:
				if right == 0:
					raise IllegalDivisionException(self.row_b, self.col_b)
				value = left / right
			elif self.oper.type == TokenType.MOD:
				value = left % right
			elif self.oper.type == TokenType.POW:
				value = left ** right
			elif self.oper.type == TokenType.EQ:
				value = left == right
			elif self.oper.type == TokenType.NEQ:
				value = left != right
			elif self.oper.type == TokenType.GT:
				value = left > right
			elif self.oper.type == TokenType.LT:
				value = left < right
			elif self.oper.type == TokenType.GTE:
				value = left >= right
			elif self.oper.type == TokenType.LTE:
				value = left <= right
			elif self.oper.type == TokenType.OR:
				value = left or right
			elif self.oper.type == TokenType.AND:
				value = left and right
		except:
			raise InvalidOperationException(self.oper.text, self.oper.row_b, self.oper.col_b)
			
		return value
		
class UnaryExpr(SuperExpr):
	def __init__(self, oper, right):
		self.oper = oper
		self. right = right
		
	def eval(self):
		value = None
		right = self.right.eval()
		try:
			if self.oper.type == TokenType.SUB:
				value = -right
			elif self.oper.type == TokenType.NEG:
				value = not right	
		except:
			raise InvalidOperationException(self.oper.text, self.oper.row_b, self.oper.col_b)
			
		return value
	
class LiteralExpr(SuperExpr):
	def __init__(self, literal):
		self.literal = literal
		
	def eval(self):
		return self.literal
		
class MethodCall(SuperExpr):
	def __init__(self, name, indeces, fname, args):
		self.name = name
		self.indeces = indeces
		self.fname = fname
		self.args = args
	
	def eval(self):
		text = self.name.text
		argtext = []
		argvs = []
		for arg in self.args:
			argv = arg.eval()
			argvs.append(argv)
			argtext.append(str(argv))
		struct = cur_env.getValue(self.name)
		if len(self.indeces) > 0:
			for index in self.indeces:
				idx = index.eval()
				text += "[" + str(idx) + "]"
				struct = struct[idx]
				
		value = struct.call(self.fname, argvs)
		strval = str(value)
		if isinstance(value, List) or isinstance(value, Map):
			kobes.append(Kobe(self.text, strval, self.row_b, self.row_e, self.col_b, self.col_e, None, text + " = " + strval))
		else:
			kobes.append(Kobe(self.text, strval, self.row_b, self.row_e, self.col_b, self.col_e))
		return value
		
		
class ListStruct(SuperExpr):
	def __init__(self, elems):
		self.elems = elems
	
	def eval(self):
		vals = List()
		for e in self.elems:
			value = e.eval()
			vals.append(value)
		return vals
		
class MapStruct(SuperExpr):
	def __init__(self, klist, vlist):
		self.klist = klist
		self.vlist = vlist
	
	def eval(self):
		map = Map()
		n = len(self.klist)
		for i in range(0, n):
			key = self.klist[i].eval()
			value = self.vlist[i].eval()
			map[key] = value	
		return map
		
class GroupExpr(SuperExpr):
	def __init__(self, group):
		self.group = group
		
	def eval(self):
		return self.group.eval()
		
class NullExpr(SuperExpr):
	def eval(self):
		return None
		
class ReturnStmt(SuperExpr):
	def __init__(self, expr):
		self.expr = expr
		
	def eval(self):
		value = self.expr.eval()
		
		kobes.append(Kobe(self.text, str(value), self.row_b, self.row_e, self.col_b, self.col_e))
		raise Return(self.row_b, self.col_b, value)
		
class PrintStmt(SuperExpr):
	def __init__(self, expr):
		self.expr = expr
		
	def eval(self):
		value = self.expr.eval()
		strval = str(value)
		kobes.append(Kobe(self.text, strval, self.row_b, self.row_e, self.col_b, self.col_e, strval))

		

class PrintLnStmt(SuperExpr):
	def __init__(self, expr):
		self.expr = expr
		
	def eval(self):
		value = self.expr.eval()
		strval = str(value)
		kobes.append(Kobe(self.text, strval, self.row_b, self.row_e, self.col_b, self.col_e, strval+'\n'))
			
		
class GetExpr(SuperExpr):
	def __init__(self, name, indeces):
		self.name = name
		self.indeces = indeces
	
	def eval(self):
		value = copyVal(cur_env.getValue(self.name))
		if len(self.indeces) > 0:
			for index in self.indeces:
				idx = index.eval()
				try:
					value = value[idx]
				except:
					raise InvalidIndexException(idx, index.row_b, index.col_b)

		return value
				
class AssignStmt(SuperExpr):
	def __init__(self, name, expr, indeces):
		self.name = name
		self.expr = expr
		self.indeces = indeces
		self.vname = name.text
		
	def eval(self):
		self.value = self.expr.eval()
		strval = str(self.value)
		if len(self.indeces) == 0:
			kobes.append(Kobe(self.text, strval, self.row_b, self.row_e, self.col_b, self.col_e, None, self.vname + " = " + strval))
			cur_env.assign(self.name, self.value)
		else:
			current = cur_env.getValue(self.name)
			new = self.set(0, len(self.indeces), current)
			kobes.append(Kobe(self.text, strval, self.row_b, self.row_e, self.col_b, self.col_e, None, self.vname + " = " + strval))
			cur_env.assign(self.name, new)
		
	def set(self, i, n, struct):
		if i == n:
			return self.value
		idx = self.indeces[i].eval()
		self.vname += '[' + str(idx) + ']'
		if isinstance(struct, Map):
			if idx in struct:
				struct[idx] = self.set(i + 1, n, struct[idx])
			elif not(idx in struct):
				struct[idx] = self.set(i + 1, n, None)
			else:
				raise InvalidIndexException(idx, self.indeces[i].row_b, self.indeces[i].col_b)
		else:
			try:
				struct[idx] = self.set(i + 1, n, struct[idx])
			except:
				raise InvalidIndexException(idx, self.indeces[i].row_b, self.indeces[i].col_b)
		return struct
			
class BlockStmt:
	def __init__(self, stmts):
		self.stmts = stmts
		
	def eval(self):
		global cur_env
		env = Environment(cur_env)
		tmp = cur_env
		cur_env = env
		for s in self.stmts:
			s.eval()
		
		cur_env = tmp

class BreakStmt(SuperExpr):
	def __init__(self):
		self.value = "break"
		
	def eval(self):
		kobes.append(Kobe(self.text, str(self.value), self.row_b, self.row_e, self.col_b, self.col_e))
		raise Break(self.row_b, self.col_b)
		
class ContinueStmt(SuperExpr):
	def __init__(self):
		self.value = "next"
		
	def eval(self):
		kobes.append(Kobe(self.text, str(self.value), self.row_b, self.row_e, self.col_b, self.col_e))
		raise Continue(self.row_b, self.col_b)
		
class IfStmt:
	def __init__(self, cond, then, elsbr):
		self.cond = cond
		self.then = then
		self.elsbr = elsbr
		
	def eval(self):
		bool = self.cond.eval()
		kobes.append(Kobe(self.cond.text, str(True if bool else False), self.cond.row_b, self.cond.row_e, self.cond.col_b, self.cond.col_e))
		if isTrue(bool):
			self.then.eval()
		else:
			if self.elsbr != None:
				self.elsbr.eval()			
			
class WhileStmt:
	def __init__(self, cond, body):
		self.cond = cond
		self.body = body
		
	def eval(self):
		bool = self.cond.eval()
		stop = False
		while isTrue(bool):
			try:
				kobes.append(Kobe(self.cond.text, str(True if bool else False), self.cond.row_b, self.cond.row_e, self.cond.col_b, self.cond.col_e))	
				self.body.eval()
			except Break:
				stop = True
				break
			except Continue:
				bool = self.cond.eval()
				continue
			
			bool = self.cond.eval()
				
		if stop == False:
			kobes.append(Kobe(self.cond.text, str(True if bool else False), self.cond.row_b, self.cond.row_e, self.cond.col_b, self.cond.col_e))

class FunctionCall(SuperExpr):
	def __init__(self, name, args):
		self.name = name
		self.args = args
		
	def eval(self):
		funcName = self.name.text
		funcArgs = []
		funcArgsStr = []
		for arg in self.args:
			argv = arg.eval()
			funcArgs.append(argv)
			funcArgsStr.append(str(argv))
		func = cur_env.getValue(self.name)
		kobes.append(Kobe(self.text, funcName + "(" + ','.join(funcArgsStr) + ")", self.row_b, self.row_e, self.col_b, self.col_e))
		return func.call(funcArgs, self.name)
			
class FunctionStmt:
	def __init__(self, name, params, body):
		self.name = name
		self.params = params
		self.body = body
		
	def eval(self):
		cur_env.assign(self.name, Function(self.params, self.body))
								
class Function:
	def __init__(self, params, body):
		self.params = params
		self.body = body 
		
	def call(self, args, name):
		global cur_env
		fun_env = Environment(cur_env)
		plen = len(self.params)
		alen = len(args)
		if alen == plen:
			tmp = cur_env
			cur_env = fun_env
			fi = 0
			while fi < plen:
				param = self.params[fi]
				cur_env.define(param, args[fi])
				strval = str(args[fi])
				kobes.append(Kobe(param.text, strval, param.row_b, param.row_e, param.col_b, param.col_e, None, param.text + " = " + strval))
				fi += 1
			try:
				for stmt in self.body:
					stmt.eval()
			except Return as r:
				cur_env = tmp
				return r.getValue()	
						
			cur_env = tmp
		else:
			raise ArgumentNotMatchException(name.text, name.row_b, name.col_b, plen)

class List(list):
	methods = ["push", "pop", "insert", "size", "clear"]
	
	def call(self, method, args):
		if method.text in self.methods:
			if method.text == "push":
				return self.push(args, method)
			if method.text == "pop":
				return self._pop(args, method)
			if method.text == "insert":
				return self._insert(args, method)
			if method.text == "clear":
				return self._clear(args, method)
			if method.text == "size":
				return self.size(args, method)
		else:
			raise UndefinedMethodException(method.text, method.row_b, method.col_b)
				
	def push(self, args, method):
		if len(args) == 1:
			self.append(args[0])
			return self
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 1)
			
	def _pop(self, args, method):
		if len(args) == 0:
			self.pop()
			return self
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 0)
			
	def _insert(self, args, method):
		if len(args) == 2:
			self.insert(args[0], args[1])
			return self
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 2)
			
	def size(self, args, method):
		if len(args) == 0:
			return len(self)
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 0)
			
	def _clear(self, args, method):
		if len(args) == 0:
			self.clear()
			return self
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 0)
	
class Map(dict):
	methods = ["remove", "clear", "keys", "values", "size"]
	
	def call(self, method, args):
		if method.text in self.methods:
			if method.text == "remove":
				return self.remove(args, method)
			if method.text == "clear":
				return self._clear(args, method)
			if method.text == "keys":
				return self._keys(args, method)
			if method.text == "values":
				return self._values(args, method)
			if method.text == "size":
				return self.size(args, method)
		else:
			raise UndefinedMethodException(method.text, method.row_b, method.col_b)
			
	def remove(self, args, method):
		if len(args) == 1:
			self.pop(args[0])
			return self
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 1)
			
	def _clear(self, args, method):
		if len(args) == 0:
			self.clear()
			return self
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 0)

	def size(self, args, method):
		if len(args) == 0:
			return len(self)
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 0)
			
	def _keys(self, args, method):
		if len(args) == 0:
			return List(self.keys())
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 0)
			
	def _values(self, args, method):
		if len(args) == 0:
			return List(self.values())
		else:
			raise ArgumentNotMatchException(method.text, method.row_b, method.col_b, 0)
	