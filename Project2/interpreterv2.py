from env_v1 import EnvironmentManager
from type_valuev1 import Type, Value, create_value, get_printable
from intbase import InterpreterBase, ErrorType
from brewparse import parse_program
import copy


# Main interpreter class
class Interpreter(InterpreterBase):
    # constants
    NIL_VALUE = create_value(InterpreterBase.NIL_DEF)
    BIN_OPS = {"+", "-", "*", "/"} #Added the next two bin_ops in * and /
    COM_OPS = {"<", ">", "<=", ">="} #Comparison operators
    LOG_OPS = {"!", "&&", "||"} #Logical operators
    EQU_OPS = {"==", "!="} #Equality Operators

    # methods
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.trace_output = trace_output
        self.__setup_ops()

    # run a program that's provided in a string
    # usese the provided Parser found in brewparse.py to parse the program
    # into an abstract syntax tree (ast)
    def run(self, program):
        ast = parse_program(program)
        self.__set_up_function_table(ast)
        main_func = self.__get_func_by_name(("main",0))
        curr_scope = EnvironmentManager()
        self.env = [curr_scope]
        statement_val = self.__run_statements(main_func.get("statements"))
        self.env.remove(curr_scope)
        return statement_val.value().value()


    def __set_up_function_table(self, ast):
        self.func_name_to_ast = {}
        for func_def in ast.get("functions"):
            self.func_name_to_ast[(func_def.get("name"),len(func_def.get("args")))] = func_def

    def __get_func_by_name(self, name):
        if name not in self.func_name_to_ast:
            super().error(ErrorType.NAME_ERROR, f"Function {name} not found")
        return self.func_name_to_ast[name]

    def __run_statements(self, statements):
        # all statements of a function are held in arg3 of the function AST node
        for statement in statements:
            if self.trace_output:
                print(statement)
            if statement.elem_type == InterpreterBase.FCALL_DEF:
                self.__call_func(statement)
            if statement.elem_type == "=":
                self.__assign(statement)
            if statement.elem_type == InterpreterBase.IF_DEF:
                if_value = self.__call_if(statement)
                if if_value is not None:
                    return if_value
            if statement.elem_type == InterpreterBase.WHILE_DEF:
                while_value = self.__call_while(statement)
                if while_value is not None:
                    return while_value
            if statement.elem_type == InterpreterBase.RETURN_DEF:
                return self.__call_ret(statement)


        return Value(Type.NIL,Value(Type.NIL, InterpreterBase.NIL_DEF)) 

    def __call_if(self, call_node):
        if_condition = call_node.get("condition")
        
        if if_condition.elem_type == InterpreterBase.VAR_DEF:
            evaluaed_var = self.__eval_expr(if_condition)
            if evaluaed_var.type() != Type.BOOL:
                super().error(ErrorType.TYPE_ERROR)

        if self.__eval_expr(if_condition).value():
            curr_scope = EnvironmentManager()
            self.env.append(curr_scope)
            return_value = self.__run_statements(call_node.get("statements"))
            self.env.remove(curr_scope)
            if(return_value.type() == Type.RET):
                return return_value
        elif call_node.get("else_statements") != None:
            curr_scope = EnvironmentManager()
            self.env.append(curr_scope)
            return_value = self.__run_statements(call_node.get("else_statements"))
            self.env.remove(curr_scope)
            if(return_value.type() == Type.RET):
                return return_value

    def __call_while(self, call_node):
        curr_scope = EnvironmentManager()
        self.env.append(curr_scope)

        #Same check as if and test_bad_cond1.br
        while_condition = call_node.get("condition")
        if while_condition.elem_type == InterpreterBase.VAR_DEF:
            super().error(ErrorType.TYPE_ERROR)
            
        loop_condition = self.__eval_expr(call_node.get("condition"))
        while loop_condition.value() and isinstance(loop_condition.value(), bool):
            return_value = self.__run_statements(call_node.get("statements"))
            if return_value.type() == Type.RET:
                self.env.remove(curr_scope)
                return return_value
            loop_condition = self.__eval_expr(call_node.get("condition"))
        self.env.remove(curr_scope)

    def __call_ret(self, call_node):
        return_val = Value(Type.NIL, InterpreterBase.NIL_DEF)
        if call_node.get("expression") != None:
            return_val = copy.deepcopy(self.__eval_expr(call_node.get("expression")))
        return Value(Type.RET, return_val)

    def __call_func(self, call_node):
        func_name = call_node.get("name")
        if func_name == "print":
            return self.__call_print(call_node)
        if func_name == "inputi":
            return self.__call_input(call_node)
        if func_name == "inputs":
            return self.__call_input(call_node)

        #Handle other functions beside main -> user defined funtions
        func_args = call_node.get("args")
        if (func_name, len(func_args)) in self.func_name_to_ast:
            curr_scope = EnvironmentManager()
            func_def = self.__get_func_by_name((func_name, len(func_args)))
            for variable_name, variable_value in zip(func_def.get("args"), func_args):
                curr_scope.set(variable_name.get("name"), self.__eval_expr(variable_value))
            self.env.append(curr_scope)
            func_val = self.__run_statements(func_def.get("statements"))
            self.env.remove(curr_scope)
            return func_val.value()

        super().error(ErrorType.NAME_ERROR, f"Function {func_name} not found")

    def __call_print(self, call_ast):
        output = ""
        for arg in call_ast.get("args"):
            result = self.__eval_expr(arg)  # result is a Value object
            output = output + get_printable(result)
        super().output(output)
        return Interpreter.NIL_VALUE

    def __call_input(self, call_ast):
        args = call_ast.get("args")
        if args is not None and len(args) == 1:
            result = self.__eval_expr(args[0])
            super().output(get_printable(result))
        elif args is not None and len(args) > 1:
            super().error(
                ErrorType.NAME_ERROR, "No inputi() function that takes > 1 parameter"
            )
        inp = super().get_input()
        if call_ast.get("name") == "inputi":
            return Value(Type.INT, int(inp))
        # we can support inputs here later
        #Inputs()
        elif call_ast.get("name") == "inputs":
            return Value(Type.STRING, str(inp).split()[0])


    def __assign(self, assign_ast):
        var_name = assign_ast.get("name")
        value_obj = self.__eval_expr(assign_ast.get("expression"))
        scope_dict = self.env[-1]
        
        #Handle scoping
        for variable in reversed(self.env):
            if variable.get(var_name) != None:
                scope_dict = variable
                break
        scope_dict.set(var_name, value_obj)


    def __eval_expr(self, expr_ast):
        if expr_ast.elem_type == InterpreterBase.INT_DEF:
            return Value(Type.INT, expr_ast.get("val"))
        if expr_ast.elem_type == InterpreterBase.STRING_DEF:
            return Value(Type.STRING, expr_ast.get("val"))
        if expr_ast.elem_type == InterpreterBase.BOOL_DEF: #Handle Booleans
            return Value(Type.BOOL, expr_ast.get("val"))
        if expr_ast.elem_type == InterpreterBase.NIL_DEF: #Handle nil type
            return Value(Type.NIL, expr_ast.get("val"))
        #Arithmetic Negation
        if expr_ast.elem_type == InterpreterBase.NEG_DEF:
            temp1 = self.__eval_expr(expr_ast.get("op1"))
            if temp1.type() != Type.INT:
                super().error(ErrorType.TYPE_ERROR)
            temp2 = temp1.value()
            return Value(Type.INT, temp2 * (-1))
        #Boolean Negation
        if expr_ast.elem_type == Interpreter.NOT_DEF:
            temp1 = self.__eval_expr(expr_ast.get("op1"))
            if temp1.type() != Type.BOOL:
                super().error(ErrorType.TYPE_ERROR)
            temp2 = temp1.value()
            return Value(Type.BOOL, not temp2)
            
        if expr_ast.elem_type == InterpreterBase.VAR_DEF:
            var_name = expr_ast.get("name")
            val = None
            for variable in reversed(self.env):
                if variable.get(var_name) != None:
                    return variable.get(var_name)
            if val is None:
                super().error(ErrorType.NAME_ERROR, f"Variable {var_name} not found")
        if expr_ast.elem_type == InterpreterBase.FCALL_DEF:
            return self.__call_func(expr_ast)
        if expr_ast.elem_type in Interpreter.BIN_OPS: # +, -, *, /
            return self.__eval_op(expr_ast)
        if expr_ast.elem_type in Interpreter.COM_OPS: # <, >, <=, >=
            return self.__eval_comp(expr_ast)
        if expr_ast.elem_type in Interpreter.EQU_OPS: # ==, != 
            return self.__eval_equality(expr_ast)
        if expr_ast.elem_type in Interpreter.LOG_OPS: # &&, ||
            return self.__eval_log_op(expr_ast)

    def __eval_op(self, arith_ast):
        #Get the expression
        left_value_obj = self.__eval_expr(arith_ast.get("op1"))
        right_value_obj = self.__eval_expr(arith_ast.get("op2"))
        
        if left_value_obj.type() != right_value_obj.type():
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible types for {arith_ast.elem_type} operation",
            )
        if arith_ast.elem_type not in self.op_to_lambda[left_value_obj.type()]:
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible operator {arith_ast.get_type} for type {left_value_obj.type()}",
            )
        f = self.op_to_lambda[left_value_obj.type()][arith_ast.elem_type]
        return f(left_value_obj, right_value_obj)

    #handling comparisons is different than the binary operations, so define a separate function.
    def __eval_comp(self, arith_ast):
        left_value_obj = self.__eval_expr(arith_ast.get("op1"))
        right_value_obj = self.__eval_expr(arith_ast.get("op2"))

        #If trying to compare non-integers, throw an error
        if left_value_obj.type() != Type.INT:
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible types for {arith_ast.elem_type} operation",
            )
        if right_value_obj.type() != Type.INT:
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible types for {arith_ast.elem_type} operation",
            )

        #If the types aren't the same, throw an error
        if left_value_obj.type() != right_value_obj.type():
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible types for {arith_ast.elem_type} operation",
            )
        f = self.op_to_lambda[left_value_obj.type()][arith_ast.elem_type]
        return f(left_value_obj, right_value_obj)

    #handling equality is also different since something like: x = 5; y = "5"; -> this returns false if you say x == y
    def __eval_equality(self, arith_ast):
        left_value_obj = self.__eval_expr(arith_ast.get("op1"))
        right_value_obj = self.__eval_expr(arith_ast.get("op2"))

        #Equality of different types always equate to true false. Inequality of different types always equates to true.
        if arith_ast.elem_type == "==":
            if left_value_obj.type() != right_value_obj.type():
                return Value(Type.BOOL, False)
            #Special Case of NIL:
            if left_value_obj.type() == Type.NIL and right_value_obj.type() == Type.NIL:
                return Value(Type.BOOL, True)
        if arith_ast.elem_type == "!=":
            if left_value_obj.type() != right_value_obj.type():
                return Value(Type.BOOL, True)
            if left_value_obj.type() == Type.NIL and right_value_obj.type() == Type.NIL:
                return Value(Type.BOOL, False)
            

        #If both types are the same, then we can process to the lambda
        f = self.op_to_lambda[left_value_obj.type()][arith_ast.elem_type]
        return f(left_value_obj, right_value_obj)
    
    def __eval_log_op(self, arith_ast):
        left_value_obj = self.__eval_expr(arith_ast.get("op1"))
        right_value_obj = self.__eval_expr(arith_ast.get("op2"))

        if left_value_obj.type() != Type.BOOL:
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible types for {arith_ast.elem_type} operation",
            )
        if right_value_obj.type() != Type.BOOL:
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible types for {arith_ast.elem_type} operation",
            )

        #If the types aren't the same, throw an error
        if left_value_obj.type() != right_value_obj.type():
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible types for {arith_ast.elem_type} operation",
            )
        f = self.op_to_lambda[left_value_obj.type()][arith_ast.elem_type]
        return f(left_value_obj, right_value_obj)



    def __setup_ops(self):
        self.op_to_lambda = {}
        # set up operations on integers, strings, booleans
        self.op_to_lambda[Type.INT] = {}
        self.op_to_lambda[Type.STRING] = {}
        self.op_to_lambda[Type.BOOL] = {}
        self.op_to_lambda[Type.NIL] = {}
        
        #Basic integer arithemtic
        self.op_to_lambda[Type.INT]["+"] = lambda x, y: Value(
            x.type(), x.value() + y.value()
        )
        self.op_to_lambda[Type.INT]["-"] = lambda x, y: Value(
            x.type(), x.value() - y.value()
        )
        self.op_to_lambda[Type.INT]["*"] = lambda x, y: Value(
            x.type(), x.value() * y.value()
        )
        self.op_to_lambda[Type.INT]["/"] = lambda x, y: Value(
            x.type(), x.value() // y.value()
        )
        #String Concatenation
        self.op_to_lambda[Type.STRING]["+"] = lambda x, y: Value(
            x.type(), x.value() + y.value()
        )
        #Equality and Inequality
        self.op_to_lambda[Type.STRING]["=="] = lambda x, y: Value(
            Type.BOOL, x.value() == y.value()
        )
        self.op_to_lambda[Type.INT]["=="] = lambda x, y: Value(
            Type.BOOL, x.value() == y.value()
        )
        self.op_to_lambda[Type.BOOL]["=="] = lambda x, y: Value(
            Type.BOOL, x.value() == y.value()
        )
        self.op_to_lambda[Type.NIL]["=="] = lambda x, y: Value(
            Type.BOOL, x.value() == y.value()
        )
        self.op_to_lambda[Type.STRING]["!="] = lambda x, y: Value(
            Type.BOOL, x.value() != y.value()
        )
        self.op_to_lambda[Type.INT]["!="] = lambda x, y: Value(
            Type.BOOL, x.value() != y.value()
        )
        self.op_to_lambda[Type.BOOL]["!="] = lambda x, y: Value(
            Type.BOOL, x.value() != y.value()
        )
        self.op_to_lambda[Type.NIL]["!="] = lambda x, y: Value(
            Type.BOOL, x.value() != y.value()
        )
        #Comparison
        self.op_to_lambda[Type.INT]["<"] = lambda x, y: Value(
            Type.BOOL, x.value() < y.value()
        )
        self.op_to_lambda[Type.INT][">"] = lambda x, y: Value(
            Type.BOOL, x.value() > y.value()
        )
        self.op_to_lambda[Type.INT]["<="] = lambda x, y: Value(
            Type.BOOL, x.value() <= y.value()
        )
        self.op_to_lambda[Type.INT][">="] = lambda x, y: Value(
            Type.BOOL, x.value() >= y.value()
        )
        #Logical operations:
        self.op_to_lambda[Type.BOOL]["&&"] = lambda x, y: Value(
            Type.BOOL, x.value() and y.value()
        )
        self.op_to_lambda[Type.BOOL]["||"] = lambda x, y: Value(
            Type.BOOL, x.value() or y.value()
        )