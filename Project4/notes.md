Changes to the AST Structure

**Statement Node**
A Statement node represents an individual statement (e.g., print(5+6);), and it contains the details about the specific type of statement (in project #1, this will be either an assignment or a function call):

A Statement node representing an assignment will have the following fields:
self.elem_type whose value is '=' 
self.dict which holds two keys
'name' which maps to a string holding the name of the variable on the left-hand side of the assignment (e.g., the string 'bar' for bar = 10 + 5;); *the left-hand side variable may use dot notation so you may now refer to object fields (e.g., x.bar = 10 + 5;); only a single dot is allowed (e.g., a.b.c = 5; is not allowed, nor does your interpreter need to check for this case)*
'expression' which maps to either an Expression node (e.g., for bar = 10+5;), a Variable node (e.g., for bar = bletch;) or a Value node (for bar = 5; or bar = "hello";)

**A Statement node representing a method call will have the following fields:**
self.elem_type whose value is 'mcall' 
self.dict which holds three keys:
- 'objref' which maps to the variable name on the left-hand-side of the dot.  For example, in bar.foo(), objref would map to the string 'bar'. This field could hold a variable name or the "this" keyword.
- 'name' which maps to the name of the function that is to be called in this statement (e.g., the string 'print', or 'foo' as in bar.foo())
- 'args' which maps to a list containing zero or more Expression nodes, Variable nodes or Value nodes that represent arguments to the function call


**Expression Node**
An Expression node represents an individual expression, and it contains the expression operation (e.g. '+', '-', '*', '/','==', '<', '<=', '>', '>=', '!=', 'neg', '!', etc.) and the argument(s) to the expression. There are three types of expression nodes you need to be able to interpret:

**An Expression node representing a method call (e.g. bar.foo(7)) will have the following fields:**
self.elem_type whose value is 'mcall'  
self.dict which holds three keys:
- 'objref' which maps to the variable name on the left-hand-side of the dot.  For example, in bar.foo(), objref would map to the string 'bar'. You may also use the "this" keyword for your objref
- 'name' which maps to the name of the function being called, e.g. 'factorial', or in the case of bar.foo() it would be 'foo'
- 'args' which maps to a list containing zero or more Expression nodes, Variable nodes or Value nodes that represent arguments to the function call

**An Expression node representing instantiation of a new object will have a single field:**
self.elem_type whose value is '@'
There are no other fields/dictionaries in this node

**Variable Node**
A Variable node represents an individual variable that's referred to in an expression or statement. It may also refer to a field or method inside an object (e.g., x.field_name, x.method_name):

An Variable node will have the following fields:
self.elem_type whose value is 'var'  
self.dict which holds one key  
*'name' which maps to the variable's name (e.g., 'x' or 'x.y' to access field y inside object x)*
