# Guide:

### Variables
* no need to specify type and dynamically typed
* variable name must start with _ or [a-zA-z] and can only contain _ and alphanumeric characters
* variable must always be initialized
* strings are contained in ""
```
	x = null
	y = "hello"
```
### Conditional Statement
* same with C++ and Java
```
  if(x< 0){

  }else if(x > 0){

  }else{

  }
```

### Iteration Statement
* as of now, only while loop is supported and it is same with C++ and Java
```
	while(x < 0){

	}
```
* use 'break' to terminate the iteration
* use 'next' to skip an iteration
* be careful of infinite loop; just terminate the process in terminal when encountered 

### Function
* can only be defined globally
* arguments are always passed by value
* use 'function' to define one
* use 'return' to return a value
* function overloading is not supported
```
  function sum(a, b){
  	return a + b
  }
  x = sum(3,4)
```

### Data Structures
* supports list and map
```
	x = list(1,2,3)
	y = map("k3": 3, 4:"v4")
	x[0] = 0
	x.pop()
	y[4] = "world"
	z = y.size()
```
* see Structures.py for more details

### Built-in Functions
* support write, writeln, randi and randf functions
* write and writeln always expects an argument
```
	write("hello")
	writeln("world")
	x = randi(0, 10)
	y = randf(0, 10)
```
* see Functions.py for randi and randf details
* functions in Functions.py can be overriden

### Operators
* logical operators   and, or, !
* unary operators   !, -, ~
* arithmetic operators   +, -, %, //, /, *, **
* bitwise operators   &, |, ^, ~, <<, >>
* relational operators   ==, !=, <, >, <=, >=
* assignment operator   =
* grouping operator   ()
* operator precedence is same with python

### Block
* use {} to create a block







