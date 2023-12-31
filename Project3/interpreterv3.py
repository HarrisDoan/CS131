import copy
from enum import Enum

from brewparse import parse_program
from env_v2 import EnvironmentManager
from intbase import InterpreterBase, ErrorType
from type_valuev2 import Type, Value, create_value, get_printable


class ExecStatus(Enum):
    CONTINUE = 1
    RETURN = 2

#Create a class to store my pre-coercion state for my variables to make undoing the coercion easier
#Used ChatGPT here to figure out how to effectively store the original value and type before the type coercion:
class PreCoercionState:
    def __init__(self, value_obj):
        self.original_type = value_obj.type()
        self.original_value = value_obj.value()

# Main interpreter class
class Interpreter(InterpreterBase):
    # constants
    NIL_VALUE = create_value(InterpreterBase.NIL_DEF)
    TRUE_VALUE = create_value(InterpreterBase.TRUE_DEF)
    BIN_OPS = {"+", "-", "*", "/", "==", "!=", ">", ">=", "<", "<=", "||", "&&"}
    ARITH_OPS = {"+", "-", "*", "/", "!="}
    LOG_OPS = {"==", "||", "&&"}

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
        self.env = EnvironmentManager()
        main_func = self.__get_func_by_name("main", 0)
        self.__run_statements(main_func.get("statements"))

    def __set_up_function_table(self, ast):
        self.func_name_to_ast = {}
        for func_def in ast.get("functions"):
            func_name = func_def.get("name")
            num_params = len(func_def.get("args"))
            if func_name not in self.func_name_to_ast:
                self.func_name_to_ast[func_name] = {}
            self.func_name_to_ast[func_name][num_params] = func_def
        

    def __get_func_by_name(self, name, num_params):
        if name not in self.func_name_to_ast and self.env.get(name) == None:
            super().error(ErrorType.NAME_ERROR, f"Function {name} not found")
        if name in self.func_name_to_ast:
            candidate_funcs = self.func_name_to_ast[name]
        else:
            candidate_funcs = self.env.get(name)
            if candidate_funcs.type() == Type.FUNCTION:
                return candidate_funcs
            elif candidate_funcs.type() != Type.FUNCTION:
                super().error(ErrorType.TYPE_ERROR, f"Variable {name} is not of a type 'function'",)
        if num_params == None:
            if len(self.func_name_to_ast[name]) == 1:
                param = list(self.func_name_to_ast[name].keys())[0]
                return self.func_name_to_ast[name][param]
            else:
                super().error(ErrorType.NAME_ERROR, f"Function {name} not found.")
        elif num_params not in candidate_funcs:
            super().error(ErrorType.NAME_ERROR, f"Function {name} with {num_params} params not found")
        return candidate_funcs[num_params]

    def __run_statements(self, statements):
        self.env.push()
        for statement in statements:
            if self.trace_output:
                print(statement)
            status = ExecStatus.CONTINUE
            if statement.elem_type == InterpreterBase.FCALL_DEF:
                self.__call_func(statement)
            elif statement.elem_type == "=":
                self.__assign(statement)
            elif statement.elem_type == InterpreterBase.RETURN_DEF:
                status, return_val = self.__do_return(statement)
            elif statement.elem_type == Interpreter.IF_DEF:
                status, return_val = self.__do_if(statement)
            elif statement.elem_type == Interpreter.WHILE_DEF:
                status, return_val = self.__do_while(statement)

            if status == ExecStatus.RETURN:
                self.env.pop()
                return (status, return_val)

        self.env.pop()
        return (ExecStatus.CONTINUE, Interpreter.NIL_VALUE)

    def __call_func(self, call_node):
        func_name = call_node.get("name")
        if func_name == "print":
            return self.__call_print(call_node)
        if func_name == "inputi":
            return self.__call_input(call_node)
        if func_name == "inputs":
            return self.__call_input(call_node)

        actual_args = call_node.get("args")
        func_ast = self.__get_func_by_name(func_name, len(actual_args))
        if type(func_ast) == Value:
            if(func_ast.value().elem_type == InterpreterBase.LAMBDA_DEF):
                original_env = self.env
                self.env = func_ast.get_env()
            #Set lambda flag to true
            lambda_flag = True
            func_ast = func_ast.value()
        formal_args = func_ast.get("args")
        if len(actual_args) != len(formal_args):
            if lambda_flag == True:
                super().error(ErrorType.TYPE_ERROR, f"Function {func_ast.get('name')} with {len(actual_args)} args not found",)
        self.env.push()

        #Handle lambdas, lambdas pass-by-ref
        for formal_ast, actual_ast in zip(formal_args, actual_args):
            #Case: != ref
            if formal_ast.elem_type != InterpreterBase.REFARG_DEF:
                result = copy.deepcopy(self.__eval_expr(actual_ast))
                result.ref_flag = False
            #Case: ref, lambda
            elif formal_ast.elem_type == InterpreterBase.REFARG_DEF and func_ast.elem_type == InterpreterBase.LAMBDA_DEF:
                result = original_env.get(actual_ast.get("name"))
            #Case: ref, != lambda
            elif formal_ast.elem_type == InterpreterBase.REFARG_DEF and func_ast.elem_type != InterpreterBase.LAMBDA_DEF:
                result = self.env.get(actual_ast.get("name"))
                result.ref_flag = True
            else:
                super().error(ErrorType.TYPE_ERROR)
            arg_name = formal_ast.get("name")
            self.env.create(arg_name, result)

        _, return_val = self.__run_statements(func_ast.get("statements"))

        if(func_ast.elem_type == InterpreterBase.LAMBDA_DEF):
            self.env.pop()
            self.env = original_env
        else:
            self.env.pop()
        return return_val


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
        if call_ast.get("name") == "inputs":
            return Value(Type.STRING, inp)

    def __assign(self, assign_ast):
        var_name = assign_ast.get("name")
        value_obj = self.__eval_expr(assign_ast.get("expression"))
        self.env.set(var_name, value_obj)

    def __eval_expr(self, expr_ast):
        if expr_ast.elem_type == InterpreterBase.NIL_DEF:
            return Interpreter.NIL_VALUE
        if expr_ast.elem_type == InterpreterBase.INT_DEF:
            return Value(Type.INT, expr_ast.get("val"))
        if expr_ast.elem_type == InterpreterBase.STRING_DEF:
            return Value(Type.STRING, expr_ast.get("val"))
        if expr_ast.elem_type == InterpreterBase.BOOL_DEF:
            return Value(Type.BOOL, expr_ast.get("val"))
        if expr_ast.elem_type == InterpreterBase.VAR_DEF:
            var_name = expr_ast.get("name")
            val = self.env.get(var_name)
            if val is None:
                func_name = self.__get_func_by_name(var_name, None)
                val = Value(Type.FUNCTION, func_name)
            if val is None and var_name is not None:
                super().error(ErrorType.NAME_ERROR, f"Variable {var_name} not found")
            return val
        if expr_ast.elem_type == InterpreterBase.FCALL_DEF:
            return self.__call_func(expr_ast)
        if expr_ast.elem_type == InterpreterBase.LAMBDA_DEF:
            return self.__do_lambda(expr_ast)
        if expr_ast.elem_type in Interpreter.BIN_OPS:
            return self.__eval_op(expr_ast)
        if expr_ast.elem_type == Interpreter.NEG_DEF:
            return self.__eval_unary(expr_ast, Type.INT, lambda x: -1 * x)
        if expr_ast.elem_type == Interpreter.NOT_DEF:
            return self.__eval_unary(expr_ast, Type.BOOL, lambda x: not x)

    def __eval_op(self, arith_ast):
        left_value_obj = self.__eval_expr(arith_ast.get("op1"))
        right_value_obj = self.__eval_expr(arith_ast.get("op2"))
        operation = arith_ast.elem_type

        og_left_value_obj = PreCoercionState(left_value_obj)
        og_right_value_obj = PreCoercionState(right_value_obj)

        #Perform coercion -> won't afect values if they don't apply to the coercion 
        left_value_obj, right_value_obj = self.__do_coercion(left_value_obj, right_value_obj, operation)
        
        if not self.__compatible_types(arith_ast.elem_type, left_value_obj, right_value_obj):
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible types for {arith_ast.elem_type} operation",
            )
        if arith_ast.elem_type not in self.op_to_lambda[left_value_obj.type()]:
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible operator {arith_ast.elem_type} for type {left_value_obj.type()}",
            )
        f = self.op_to_lambda[left_value_obj.type()][arith_ast.elem_type]
        result = f(left_value_obj, right_value_obj)

        #Undo coercion:
        #See comment at PreCoercionState class for citation:
        left_value_obj.t = og_left_value_obj.original_type
        left_value_obj.v = og_left_value_obj.original_value
        right_value_obj.t = og_right_value_obj.original_type
        right_value_obj.v = og_right_value_obj.original_value

        return result

    def __compatible_types(self, oper, obj1, obj2):
        # DOCUMENT: allow comparisons ==/!= of anything against anything
        if oper in ["==", "!="]:
            return True
        return obj1.type() == obj2.type()

    def __eval_unary(self, arith_ast, t, f):
        value_obj = self.__eval_expr(arith_ast.get("op1"))
        if arith_ast.elem_type == "!" and value_obj.type() == Type.INT:
            value_obj = self.__int_to_bool(value_obj)
        if arith_ast.elem_type == "-" and value_obj.type() == Type.BOOL:
            value_obj = self.__bool_to_int(value_obj)
        if value_obj.type() != t:
            super().error(ErrorType.TYPE_ERROR, f"Incompatible type for {arith_ast.elem_type} operation")
        return Value(t, f(value_obj.value()))

    def __setup_ops(self):
        self.op_to_lambda = {}
        # set up operations on integers
        self.op_to_lambda[Type.INT] = {}
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
        self.op_to_lambda[Type.INT]["=="] = lambda x, y: Value(
            Type.BOOL, x.type() == y.type() and x.value() == y.value()
        )
        self.op_to_lambda[Type.INT]["!="] = lambda x, y: Value(
            Type.BOOL, x.type() != y.type() or x.value() != y.value()
        )
        self.op_to_lambda[Type.INT]["<"] = lambda x, y: Value(
            Type.BOOL, x.value() < y.value()
        )
        self.op_to_lambda[Type.INT]["<="] = lambda x, y: Value(
            Type.BOOL, x.value() <= y.value()
        )
        self.op_to_lambda[Type.INT][">"] = lambda x, y: Value(
            Type.BOOL, x.value() > y.value()
        )
        self.op_to_lambda[Type.INT][">="] = lambda x, y: Value(
            Type.BOOL, x.value() >= y.value()
        )
        #  set up operations on strings
        self.op_to_lambda[Type.STRING] = {}
        self.op_to_lambda[Type.STRING]["+"] = lambda x, y: Value(
            x.type(), x.value() + y.value()
        )
        self.op_to_lambda[Type.STRING]["=="] = lambda x, y: Value(
            Type.BOOL, x.value() == y.value()
        )
        self.op_to_lambda[Type.STRING]["!="] = lambda x, y: Value(
            Type.BOOL, x.value() != y.value()
        )
        #  set up operations on bools
        self.op_to_lambda[Type.BOOL] = {}
        self.op_to_lambda[Type.BOOL]["&&"] = lambda x, y: Value(
            x.type(), x.value() and y.value()
        )
        self.op_to_lambda[Type.BOOL]["||"] = lambda x, y: Value(
            x.type(), x.value() or y.value()
        )
        self.op_to_lambda[Type.BOOL]["=="] = lambda x, y: Value(
            Type.BOOL, x.type() == y.type() and x.value() == y.value()
        )
        self.op_to_lambda[Type.BOOL]["!="] = lambda x, y: Value(
            Type.BOOL, x.type() != y.type() or x.value() != y.value()
        )
        #  set up operations on nil
        self.op_to_lambda[Type.NIL] = {}
        self.op_to_lambda[Type.NIL]["=="] = lambda x, y: Value(
            Type.BOOL, x.type() == y.type() and x.value() == y.value()
        )
        self.op_to_lambda[Type.NIL]["!="] = lambda x, y: Value(
            Type.BOOL, x.type() != y.type() or x.value() != y.value()
        )
        # set up operations on functions
        self.op_to_lambda[Type.FUNCTION] = {}
        self.op_to_lambda[Type.FUNCTION]["!="] = lambda x, y: Value(
            Type.BOOL, x.type() != y.type() or x.value() != y.value()
        )
        self.op_to_lambda[Type.FUNCTION]["=="] = lambda x, y: Value(
            Type.BOOL, x.type() == y.type() and x.value() == y.value()
        )

    def __do_if(self, if_ast):
        cond_ast = if_ast.get("condition")
        result = self.__eval_expr(cond_ast)
        if result.type() == Type.INT:
            result = self.__int_to_bool(result)
        if result.type() != Type.BOOL:
            super().error(
                ErrorType.TYPE_ERROR,
                "Incompatible type for if condition",
            )
        if result.value():
            statements = if_ast.get("statements")
            status, return_val = self.__run_statements(statements)
            return (status, return_val)
        else:
            else_statements = if_ast.get("else_statements")
            if else_statements is not None:
                status, return_val = self.__run_statements(else_statements)
                return (status, return_val)

        return (ExecStatus.CONTINUE, Interpreter.NIL_VALUE)

    def __do_while(self, while_ast):
        cond_ast = while_ast.get("condition")
        run_while = Interpreter.TRUE_VALUE
        while run_while.value():
            run_while = self.__eval_expr(cond_ast)
            if run_while.type() == Type.INT:
                run_while = self.__int_to_bool(run_while)
            if run_while.type() != Type.BOOL:
                super().error(
                    ErrorType.TYPE_ERROR,
                    "Incompatible type for while condition",
                )
            if run_while.value():
                statements = while_ast.get("statements")
                status, return_val = self.__run_statements(statements)
                if status == ExecStatus.RETURN:
                    return status, return_val

        return (ExecStatus.CONTINUE, Interpreter.NIL_VALUE)

    def __do_return(self, return_ast):
        expr_ast = return_ast.get("expression")
        if expr_ast is None:
            return (ExecStatus.RETURN, Interpreter.NIL_VALUE)
        value_obj = copy.deepcopy(self.__eval_expr(expr_ast))
        return (ExecStatus.RETURN, value_obj)

    #This isn't handling lambdas correctly, exp: test_lambda_non_capture from the GitHub public test cases. It doesn't recognize a or x.
    def __do_lambda(self, lambda_ast):
        lambda_val = Value(Type.FUNCTION, lambda_ast)
        lambda_val.set_env(copy.deepcopy(self.env))
        return lambda_val


    def __do_coercion(self, left_value_obj, right_value_obj, operation):
        if operation in Interpreter.ARITH_OPS:
            if left_value_obj.type() == Type.BOOL:
                left_value_obj = self.__bool_to_int(left_value_obj)
            if right_value_obj.type() == Type.BOOL:
                right_value_obj = self.__bool_to_int(right_value_obj)
        elif operation in Interpreter.LOG_OPS:
            if left_value_obj.type() == Type.INT:
                left_value_obj = self.__int_to_bool(left_value_obj)
            if right_value_obj.type() == Type.INT:
                right_value_obj = self.__int_to_bool(right_value_obj)
        return left_value_obj, right_value_obj
        
    def __bool_to_int(self, value_obj):
        if value_obj.type() == Type.BOOL:
            coerced_type = Type.INT
            if value_obj.value() == True:
                coerced_value = 1
            else:
                coerced_value = 0
            return Value(coerced_type, coerced_value)
        return value_obj

    def __int_to_bool(self, value_obj):
        if value_obj.type() == Type.INT:
            coerced_type = Type.BOOL
            if value_obj.value() == 0:
                coerced_value = False
            else:
                coerced_value = True
            return Value(coerced_type, coerced_value)
        return value_obj