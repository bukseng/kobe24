
class Token:

	def __init__(self, type, text, literal, row_b, row_e, col_b, col_e):
		self.type = type
		self.text = text
		self.literal = literal
		self.row_b = row_b
		self.row_e = row_e
		self.col_b = col_b
		self.col_e = col_e
		
	def __str__(self):
		return self.text + ' - ' + str(self.row_b) + ',' + str(self.row_e) + ',' + str(self.col_b) + ',' + str(self.col_e)

	def __repr__(self):
		return self.text
		