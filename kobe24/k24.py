from Scanner import Scanner
from Parser import Parser
from Errors import *
from tkinter import *
import Expressions
import sys

codebase = ""
sourcecode = sys.argv[1]

with open(sourcecode) as rf:
	line = rf.readline()
	while line:
		codebase += line
		line = rf.readline()

codebase = codebase.replace('\t', '    ')

def convertEscChar(string):
	string = string.replace('\\t', '\t')
	string = string.replace('\\n', '\n')
	string = string.replace('\\f', '\f')
	string = string.replace('\\r', '\r')
	string = string.replace('\\b', '\b')
	string = string.replace('\\"', '\"')
	string = string.replace("\\'", "\'")
	string = string.replace('\\\\', '\\')
	return string

try:	
	scanner = Scanner()
	tokens = scanner.scan(codebase);
	parser = Parser(tokens)
	exprs =  parser.parse()

	for expr in exprs:
		expr.eval()
	
	kobes = Expressions.kobes
	n = len(kobes)
	kpointer = -1

	console = []
	varlogs = []
	display = ""
	vlog = ""
	for k in kobes:
		if k.write != None:
			display += k.write
		console.append(convertEscChar(display))
	
		if k.variable != None:
			vlog += k.variable + '\n'
		varlogs.append(convertEscChar(vlog))

	#gui	
	window = Tk()
	w_width = window.winfo_screenwidth()
	w_height = window.winfo_screenheight()
	w_unit = w_width // 57
	h_unit = w_height // 32
	window.title("Kobe24")
	window.geometry(str(w_width) + 'x' + str(w_height))
	window.resizable(0,0)
	codeframe = Frame(window)
	codeframe.place(x=w_unit, y=h_unit, anchor="nw", width=w_width/2, height=w_height-(h_unit * 5))
	codebox = Text(codeframe, wrap=NONE, font=("Consolas", 15))
	cvsb = Scrollbar(codeframe, command=codebox.yview)
	chsb = Scrollbar(codeframe, orient=HORIZONTAL, command=codebox.xview)
	codebox['yscrollcommand'] = cvsb.set
	codebox['xscrollcommand'] = chsb.set
	codebox.insert(END, codebase)
	codebox.config(state=DISABLED)
	cvsb.pack(side=RIGHT, fill=Y)
	chsb.pack(side=BOTTOM, fill=X)
	codebox.pack(side=LEFT, fill=BOTH)

	outframe = Frame(window)
	outframe.place(x=w_width/2 + (w_unit * 2), y=h_unit, anchor="nw", width=w_width/2 - (w_unit * 5), height=h_unit * 7)
	outlbl = Label(outframe, text="Console:", font=("Verdana", 15)).pack()
	outtxt = Text(outframe, font=("Consolas", 15))
	outtxt.config(state=DISABLED)
	osb = Scrollbar(outframe, command=outtxt.yview)
	outtxt['yscrollcommand'] = osb.set
	osb.pack(side=RIGHT, fill=Y)
	outtxt.pack(side=LEFT, fill=BOTH)

	def first():
		global kpointer
		kpointer = 0
		update()
	def prev():
		global kpointer
		if kpointer > 0:
			kpointer -= 1
			update()
	def next():
		global kpointer
		if kpointer < n - 1:
			kpointer += 1
			update()
	def last():
		global kpointer
		kpointer = n - 1
		update()	

	btnframe = Frame(window)
	btnframe.place(x=w_width/4 - (w_unit*4), y=w_height-(h_unit * 5) + (h_unit * 3), anchor="sw", width=w_width/2, height=h_unit * 2)
	firstbtn = Button(btnframe, text="First", font=("Verdana", 15), command=first).pack(side=LEFT)
	prevbtn = Button(btnframe, text="Prev", font=("Verdana", 15), command=prev).pack(side=LEFT)
	nextbtn = Button(btnframe, text="Next", font=("Verdana", 15), command=next).pack(side=LEFT)
	lastbtn = Button(btnframe, text="Last", font=("Verdana", 15), command=last).pack(side=LEFT)

	rawframe = Frame(window)
	rawframe.place(x=w_width/2 + (w_unit * 2), y=h_unit * 9, anchor="nw", width=w_width/2 - (w_unit * 5), height=h_unit * 2) 
	rawlabel = Label(rawframe, text="Raw:", font=("Verdana", 14)).pack(side=LEFT)
	rawtxt = Text(rawframe, wrap=NONE, font=("Consolas", 15))
	rawtxt.config(state=DISABLED)
	rhsb = Scrollbar(rawframe, orient=HORIZONTAL, command=rawtxt.xview)
	rvsb = Scrollbar(rawframe, command=rawtxt.yview)
	rawtxt['xscrollcommand'] = rhsb.set
	rawtxt['yscrollcommand'] = rvsb.set
	rvsb.pack(side=RIGHT, fill=Y)
	rhsb.pack(side=BOTTOM, fill=X)
	rawtxt.pack(side=LEFT, fill=BOTH)

	valueframe = Frame(window)
	valueframe.place(x=w_width/2 + (w_unit * 2), y=h_unit * 12, anchor="nw", width=w_width/2 - (w_unit * 5), height=h_unit * 2) 
	valuelabel = Label(valueframe, text="Value:", font=("Verdana", 14)).pack(side=LEFT)
	valuetxt = Text(valueframe, wrap=NONE, font=("Consolas", 15))
	valuetxt.config(state=DISABLED)
	vhsb = Scrollbar(valueframe, orient=HORIZONTAL, command=valuetxt.xview)
	vvsb = Scrollbar(valueframe, command=valuetxt.yview)
	valuetxt['xscrollcommand'] = vhsb.set
	valuetxt['yscrollcommand'] = vvsb.set
	vvsb.pack(side=RIGHT, fill=Y)
	vhsb.pack(side=BOTTOM, fill=X)
	valuetxt.pack(side=LEFT, fill=BOTH)

	logframe = Frame(window)
	logframe.place(x=w_width/2 + (w_unit * 2), y=h_unit * 14, anchor="nw", width=w_width/2 - (w_unit * 5), height=h_unit * 16)
	loglbl = Label(logframe, text="Variable Logs:", font=("Verdana", 15)).pack()
	logtxt = Text(logframe, wrap=NONE, font=("Consolas", 15))
	logtxt.config(state=DISABLED)
	lvsb = Scrollbar(logframe, command=logtxt.yview)
	lhsb = Scrollbar(logframe, orient=HORIZONTAL, command=logtxt.xview)
	logtxt['yscrollcommand'] = lvsb.set
	logtxt['xscrollcommand'] = lhsb.set
	lvsb.pack(side=RIGHT, fill=Y)
	lhsb.pack(side=BOTTOM, fill=X)
	logtxt.pack(side=LEFT, fill=BOTH)	

	def update():
		global pk
		global codebox
		global kpointer
		global rawtxt
		global valuetxt
		global outtxt
		global logtxt
		codebox.tag_config('tag', background="white")
		codebox.tag_delete('tag')
		kobe = kobes[kpointer]
		logtxt.config(state=NORMAL)
		logtxt.delete(1.0, END)
		logtxt.insert(END, varlogs[kpointer])
		logtxt.config(state=DISABLED)
		outtxt.config(state=NORMAL)
		outtxt.delete(1.0, END)
		outtxt.insert(END, console[kpointer])
		outtxt.config(state=DISABLED)				
		rawtxt.config(state=NORMAL)
		rawtxt.delete(1.0, END)
		rawtxt.insert(END, kobe.text)
		rawtxt.config(state=DISABLED)
		valuetxt.config(state=NORMAL)
		valuetxt.delete(1.0, END)
		valuetxt.insert(END, convertEscChar(kobe.value))
		valuetxt.config(state=DISABLED)
		start = str(kobe.row_b) + '.' + str(kobe.col_b - 1)
		end = str(kobe.row_e) + '.' + str(kobe.col_e)
		codebox.tag_add('tag', start, end)
		codebox.tag_config('tag', background="yellow")
		
	window.mainloop()

except Exception as e:
	try:
		print(e.getMessage())
	except:
		print("Unknown Error")
	


