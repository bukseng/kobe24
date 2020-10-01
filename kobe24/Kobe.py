
class Kobe:
	
	def __init__(self, text, value, row_b, row_e, col_b, col_e, write=None, variable=None):
		self.text = text
		self.value = value
		self.row_b = row_b
		self.row_e = row_e
		self.col_b = col_b
		self.col_e = col_e
		self.write = write
		self.variable = variable
		
	def __repr__(self):
		return self.value
		
	def __str__(self):
		return self.text + ' >> ' + str(self.value) + ' loc: ' + str(self.row_b) + ',' + str(self.row_e) + ',' + str(self.col_b) + ',' + str(self.col_e)  
		