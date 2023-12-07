from intbase import InterpreterBase
from brewparse import parse_program
from intbase import ErrorType

class Interpreter(InterpreterBase):

    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)

    #This actually runs our program
    def run(self, program_node):
        ast = parse_program(program_node) #Being by parsing the program node into the AST
        self.map = {}  # Initialize the variable map
        functions = ast.get('functions') #use .get() using the key 'functions' to obtain all possible function nodes from AST, for Proj1 only main will exist
        
        #Run the functions created by the AST     
        self.run_func(functions)

    #We pass the list of possible functions into run_func which will process and run the functions that came from the program node dictionary.
    def run_func(self, function_node):
        #Find the main function to run
        for functions in function_node:
            if(functions.get('name') == 'main'):
                self.run_statement(functions)
            else: #If a main() function does not exist. We return an error code
                super().error(ErrorType.NAME_ERROR, "No main() found.")

    #Every statement node points to either an assignment or function call. Retrieve all the statements in the statement node by using the .get() using the key 'statements'
    #Our statements variable now holds a list of all possible statements and their two possible elem_types which are '=' and 'fcall'. Now we check for which one we are dealing with.
    def run_statement(self, statement_node):
        for statements in statement_node.get('statements'):
            if statements.elem_type == '=':
                self.do_assignment(statements) #If the elem_type is '=', we are dealing with an assignment. Handle accordingly using the right functions -> do_assignment. Ex: x = 5
            elif statements.elem_type == 'fcall': 
                self.do_func_call(statements) #If the elem_type is 'fcall', we are calling a function. Handle accordingly using the right functions -> do_func_call. Ex: foo()

    #Assigning a value to a variable's name. Ex: x = 5. x would be the assignment_node.get() where the key 'name' would return x. 5 would be the assignment_node.get() where the key is 'expression'
    def do_assignment(self, assignment_node):
        #Create a variable to store the value of the expression
        value = self.do_evaluate_expression(assignment_node.get('expression'))
        #As long as the name of the variable is defined properly -> aka the .get('name') exists -> we can map the name to said value
        if (assignment_node.get('name') != None):
            self.map[assignment_node.get('name')] = value

    #Function calls from the statement node contain a list pointing to possibly a Expression node, Variable node, or Value node
    def do_func_call(self, function_node):
        #Handle Print
        #Expresion = elem_type +, -, fcall
        #Value = elem_type int
        #Variable = elem_type var
        if(function_node.get('name') == 'print'):
            print_line = ""
            for statements in function_node.get('args'):
                if statements.elem_type == 'string':
                    print_line = print_line + statements.get('val')
                elif statements.elem_type == 'int':
                    print_line = print_line + str(statements.get('val'))
                elif statements.elem_type == 'fcall':
                    print_line = print_line + str(self.do_func_call(statements))
                elif statements.elem_type == '+':
                    print_line = print_line + str(self.do_evaluate_expression(statements))
                elif statements.elem_type == '-':
                    print_line = print_line + str(self.do_evaluate_expression(statements))
                elif statements.elem_type == 'var':
                    print_line = print_line + str(self.do_evaluate_expression(statements))
            super().output(print_line)
        #Handle Input
        elif(function_node.get('name') == 'inputi'):
            #Check for only 1 input into inputi()
            arguments = function_node.get('args')
            if len(arguments) > 1:
                super().error(ErrorType.NAME_ERROR, f"Too many inputs")
            for statements in function_node.get('args'):
                return_val = 0
                super().output(statements.get('val'))
            return_val = int(self.get_input()) #The get_input() method returns a string regardless of what the user types in, so you'll need to convert the result to an integer yourself.
            if type(return_val) != int:
                super().error(ErrorType.NAME_ERROR, f"Incorrect input")
            else:
                return return_val
        elif(function_node.get('name') == 'intpui' and len(function_node.get('args')) > 1):
            super().error(ErrorType.NAME_ERROR, f"Too many inputs")
        elif type(function_node.get('arg')) != int:
            super().error(ErrorType.NAME_ERROR, f"Incorrect input")
        else:
            super().error(ErrorType.NAME_ERROR, f"Unknown function call",)


    #+ or - are the possible elem_type and the dict contains op1, op2
    def do_evaluate_expression(self, expression_node):
        if expression_node.get('val') != None:
            #If it's a value, just return the value
            return expression_node.get('val')
        elif expression_node.elem_type == 'fcall':
            #If it's a functional call, call do_func_call
            return self.do_func_call(expression_node)
            #Elaborate the algebraic expression either addition or subtraction
        elif expression_node.elem_type == '+' or expression_node.elem_type == '-':
            arg1 = self.do_evaluate_expression(expression_node.get('op1'))
            arg2 = self.do_evaluate_expression(expression_node.get('op2'))
            if(type(arg1) == int and type(arg2) == int):
                if expression_node.elem_type == '+':
                    result = arg1 + arg2
                    return result
                elif expression_node.elem_type == '-':
                    result = arg1 - arg2
                    return result
            else:
                super().error(ErrorType.TYPE_ERROR, "Invalid Operands")
        elif expression_node.elem_type == 'var':
            if not(expression_node.get('name') in self.map):
                super().error(ErrorType.NAME_ERROR, "Variable not found.")
            else:
                return self.map[expression_node.get('name')]
        else:
            super().error(ErrorType.NAME_ERROR,f"Variable has not been defined",)
