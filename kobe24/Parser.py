from TokenType import TokenType
from Expressions import *
from Errors import UnexpectedTokenError, ArgumentNotMatchException

class Parser:

	def __init__(self, tokens):
		self.tokens = tokens
		self.i = 0
		self.exprs = []
		
	def parse(self):
		while self.current().type != TokenType.EOF:
			self.exprs.append(self.declaration())
		return self.exprs
	
	def match(self, mtoks):
		for tok in mtoks:
			if self.current().type == tok:
				self.advance()
				return True
		return False
		 
	def expect(self, tok):
		if self.current().type == tok:
			return self.advance()
		
		raise UnexpectedTokenError(self.current().text, self.current().row_b, self.current().col_b) 

	def advance(self):
		if self.current().type != TokenType.EOF:
			self.i += 1
		return self.previous()
		
	def current(self):
		return self.tokens[self.i]
		
	def previous(self):
		return self.tokens[self.i - 1]
		
	def next(self):
		if self.tokens[self.i].type == TokenType.EOF:
			return current()
		else:
			return self.tokens[self.i + 1]
		
	def declaration(self):
		if self.match([TokenType.FUN]):
			return self.funDef()
		
		return self.statement()
			
	def statement(self):
		if self.match([TokenType.WRITE, TokenType.WRTLN]):
			return self.printStmt()
		if self.match([TokenType.RET]):
			return self.returnStmt()
		if self.match([TokenType.BRK]):
			return self.breakStmt()
		if self.match([TokenType.CON]):
			return self.continueStmt()
		if self.match([TokenType.IF]):
			return self.ifStmt();
		if self.match([TokenType.LCUR]):
			return self.block()
		if self.match([TokenType.WHILE]):
		    return self.whileStmt()
		return self.expression()
		
	def returnStmt(self):
		prev = self.previous()		
		value = self.expression()
		col_e = value.col_e
		row_e = value.row_e
		text = prev.text + " " + value.text
			
		ret = ReturnStmt(value)
		ret.setKobe(prev.row_b, row_e, prev.col_b, col_e, text)
		return ret
		
	def breakStmt(self):
		prev = self.previous()
		ret = BreakStmt()
		ret.setKobe(prev.row_b, prev.row_e, prev.col_b, prev.col_e, prev.text)
		return ret

	def continueStmt(self):
		prev = self.previous()
		ret = ContinueStmt()
		ret.setKobe(prev.row_b, prev.row_e, prev.col_b, prev.col_e, prev.text)
		return ret	

	def block(self):
		stmts = []
		while self.current().type != TokenType.RCUR and self.current().type != TokenType.EOF:
			stmts.append(self.statement())
			
		self.expect(TokenType.RCUR)
		return BlockStmt(stmts)
	
	def whileStmt(self):
		self.expect(TokenType.LPAR)
		cond = self.expression()
		self.expect(TokenType.RPAR)
		body = self.statement()
		return WhileStmt(cond, body)
				
	def ifStmt(self):
		self.expect(TokenType.LPAR)
		cond = self.expression()
		self.expect(TokenType.RPAR)

		then = self.statement()
		
		elsbr = None
		if self.match([TokenType.ELSE]):
			elsbr = self.statement()
			
		return IfStmt(cond, then, elsbr)
				
	def printStmt(self):
		prev = self.previous()
		self.expect(TokenType.LPAR);
		if self.current().type == TokenType.RPAR:
			raise ArgumentNotMatchException(prev.text, prev.row_b, prev.col_b, 1)
		expr = self.expression()
		self.expect(TokenType.RPAR);
		row_b = expr.row_b
		row_e = expr.row_e
		col_b = expr.col_b
		col_e = expr.col_e
		ret = None
		if prev.type == TokenType.WRITE:
			ret = PrintStmt(expr)
		else:
			ret = PrintLnStmt(expr)
		ret.setKobe(row_b, row_e, col_b, col_e, expr.text)
		return ret
	
	def expression(self):
		return self.orLogic()
		
	
	def orLogic(self):
		expr = self.andLogic()
		
		while self.match([TokenType.OR]):
			oper = self.previous()
			right = self.andLogic()
			left = expr
			expr = BinaryExpr(left, oper, right)
			expr.setKobe(left.row_b, right.row_e, left.col_b, right.col_e, left.text + oper.text + right.text)
			
		return expr
	
	def andLogic(self):
		expr = self.equality()
		
		while self.match([TokenType.AND]):
			oper = self.previous()
			right = self.equality()
			left = expr
			expr = BinaryExpr(left, oper, right)
			expr.setKobe(left.row_b, right.row_e, left.col_b, right.col_e, left.text + oper.text + right.text)
			
		return expr
		
	def equality(self):
		expr = self.comparison()
		while self.match([TokenType.EQ, TokenType.NEQ]):
			oper = self.previous()
			right = self.comparison()
			left = expr
			expr = BinaryExpr(left, oper, right)
			expr.setKobe(left.row_b, right.row_e, left.col_b, right.col_e, left.text + oper.text + right.text)
			
		return expr
		
	def comparison(self):
		expr = self.addsub()
		
		while self.match([TokenType.GT, TokenType.GTE, TokenType.LT, TokenType.LTE]):
			oper = self.previous()
			right = self.addsub()
			left = expr
			expr = BinaryExpr(left, oper, right)
			expr.setKobe(left.row_b, right.row_e, left.col_b, right.col_e, left.text + oper.text + right.text)
			
		return expr
		
	def addsub(self):
		expr = self.muldiv()
		
		while self.match([TokenType.ADD, TokenType.SUB]):
			oper = self.previous()
			right = self.muldiv()
			left = expr
			expr = BinaryExpr(left, oper, right)
			expr.setKobe(left.row_b, right.row_e, left.col_b, right.col_e, left.text + oper.text + right.text)
			
		return expr
		
	
	def muldiv(self):
		expr = self.power()
		
		while self.match([TokenType.MUL, TokenType.DIV, TokenType.MOD, TokenType.FDIV]):
			oper = self.previous()
			right = self.power()
			left = expr
			expr = BinaryExpr(left, oper, right)
			expr.setKobe(left.row_b, right.row_e, left.col_b, right.col_e, left.text + oper.text + right.text)
		
		return expr

	def power(self):
		expr = self.unary()
		
		while self.match([TokenType.POW]):
			oper = self.previous()
			right = self.unary()
			left = expr
			expr = BinaryExpr(left, oper, right)
			expr.setKobe(left.row_b, right.row_e, left.col_b, right.col_e, left.text + oper.text + right.text)
		
		return expr
		
	def unary(self):
		if self.match([TokenType.SUB, TokenType.NEG]):
			oper = self.previous()
			right = self.unary()
			ret = UnaryExpr(oper, right)
			ret.setKobe(oper.row_b, right.row_e, oper.col_b, right.col_e, oper.text + right.text);
			return ret;
		return self.funCall()
		
	def funCall(self):
		expr = self.primary()
		
		if self.match([TokenType.LPAR]):
			expr = self.funArgs(expr.name, expr.row_b, expr.col_b)
		
		return expr
				
	def funArgs(self, name, row_b, col_b):
		args = []
		argTxt = name.text + "("
		if self.current().type != TokenType.RPAR:
			arg = self.expression()
			argTxt += arg.text
			args.append(arg)
			while self.match([TokenType.COM]):
				arg = self.expression()
				argTxt += ", " + arg.text
				args.append(arg)
		end = self.expect(TokenType.RPAR)
		argTxt += end.text
		ret = FunctionCall(name, args)
		ret.setKobe(row_b, end.row_e, col_b, end.col_e, argTxt)
		return ret
		
	def funDef(self):
		name = self.expect(TokenType.VAR)
		params = []
		body = []
		self.expect(TokenType.LPAR)
		if self.current().type != TokenType.RPAR:
			params.append(self.expect(TokenType.VAR))
			while self.match([TokenType.COM]):
				params.append(self.expect(TokenType.VAR))
			
		self.expect(TokenType.RPAR)
		self.expect(TokenType.LCUR)
		while self.current().type != TokenType.RCUR:
			body.append(self.statement())
		self.expect(TokenType.RCUR)
		return FunctionStmt(name, params, body)
	
	def listStruct(self):
		prev = self.previous()
		text = prev.text
		self.expect(TokenType.LPAR)
		text += '('
		elems = []
		if self.current().type != TokenType.RPAR:
			elem = self.expression()
			elems.append(elem)
			text += elem.text
			while self.match([TokenType.COM]):
				text += ', '
				elem = self.expression()
				elems.append(elem)
				text += elem.text
							
		end = self.expect(TokenType.RPAR)
		text += ')'
		ret = ListStruct(elems)
		ret.setKobe(prev.row_b, end.row_e, prev.col_b, end.col_e, text)
		return ret
		
	def mapStruct(self):
		prev = self.previous()
		text = prev.text
		self.expect(TokenType.LPAR)
		text += '('
		klist = []
		vlist = []
		if self.current().type != TokenType.RPAR:
			key = self.expression()
			klist.append(key)
			self.expect(TokenType.COL)
			value = self.expression()
			vlist.append(value)
			text += key.text + ':' + value.text
			while self.match([TokenType.COM]):
				text += ', '
				key = self.expression()
				klist.append(key)
				self.expect(TokenType.COL)
				value = self.expression()
				vlist.append(value)
				text += key.text + ':' + value.text
							
		end = self.expect(TokenType.RPAR)
		text += ')'
		ret = MapStruct(klist, vlist)
		ret.setKobe(prev.row_b, end.row_e, prev.col_b, end.col_e, text)
		return ret
	
	def methodCall(self):
		text = "."
		fname = self.expect(TokenType.VAR)
		text += fname.text
		self.expect(TokenType.LPAR)
		text += "("
		args = []
		if self.current().type != TokenType.RPAR:
			arg = self.expression()
			text += arg.text
			args.append(arg)
			while self.match([TokenType.COM]):
				arg = self.expression()
				text += ", " + arg.text
				args.append(arg)
		end = self.expect(TokenType.RPAR)
		text += end.text
		return {"fname":fname, "args":args, "text":text, "end":end}


	def primary(self):
		if self.match([TokenType.NUM, TokenType.STR, TokenType.TRUE, TokenType.FALSE]):
			lit = self.previous()
			ret = LiteralExpr(lit.literal)
			ret.setKobe(lit.row_b, lit.row_e, lit.col_b, lit.col_e, lit.text)
			return ret
		elif self.match([TokenType.VAR]):
			name = self.previous()
			if self.match([TokenType.LBRC]):
				text = name.text
				indeces = []
				index = self.expression()
				indeces.append(index)
				end = self.expect(TokenType.RBRC)
				text += '[' + index.text + ']'
				while self.match([TokenType.LBRC]):
					index = self.expression()
					indeces.append(index)
					end = self.expect(TokenType.RBRC)
					text += '[' + index.text + ']'

				if self.match([TokenType.ASGN]):
					right = self.expression()
					ret = AssignStmt(name, right, indeces)
					ret.setKobe(right.row_b, right.row_e, right.col_b, right.col_e, right.text)
					return ret
				elif self.match([TokenType.DOT]):
					meta = self.methodCall()
					ret = MethodCall(name, indeces, meta["fname"], meta["args"])
					ret.setKobe(name.row_b, meta["end"].row_e, name.col_b, meta["end"].col_e, text+meta["text"])
					return ret
					 	
				ret = GetExpr(name, indeces)
				ret.setKobe(name.row_b, end.row_e, name.col_b, end.col_e, text)
				return ret
			elif self.match([TokenType.DOT]):
				meta = self.methodCall()
				ret = MethodCall(name, [], meta["fname"], meta["args"])
				ret.setKobe(name.row_b, meta["end"].row_e, name.col_b, meta["end"].col_e, name.text+meta["text"])
				return ret
			elif self.match([TokenType.ASGN]):
				right = self.expression()
				ret = AssignStmt(name, right, [])
				ret.setKobe(right.row_b, right.row_e, right.col_b, right.col_e, right.text)
				return ret			
			else:
				ret = GetExpr(name, [])
				ret.setKobe(name.row_b, name.row_e, name.col_b, name.col_e, name.text)
				return ret	
		elif self.match([TokenType.LPAR]):
			left = self.previous()
			expr = self.expression()
			right = self.expect(TokenType.RPAR)
			ret = GroupExpr(expr)
			ret.setKobe(left.row_b, right.row_e, left.col_b, right.col_e, left.text + expr.text + right.text)
			return ret
		elif self.match([TokenType.LST]):
			return self.listStruct()
		elif self.match([TokenType.MAP]):
			return self.mapStruct()
		elif self.match([TokenType.NULL]):
			prev =  self.previous()
			ret = NullExpr()
			ret.setKobe(prev.row_b, prev.row_e, prev.col_b, prev.col_e, prev.text)
			return ret
		else:
			raise UnexpectedTokenError(self.current().text, self.current().row_b, self.current().col_b)
	
