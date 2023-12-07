Final Update: I give up. I'll take what I can get. "all good!"       
   
   
    Notes:

        func main() {
        x = lambda(ref f, ref g) {
            print(f == g);
            print(a == b);
            f = g;
            print(f == g);
            print(a == b);
        };
        a = 5;
        b = 10;
        x(a, b);
        print(a == b);

        /*
        *OUT*
        false
        false
        true
        true
        true
        *OUT*
        */
        }

    """

    This one test case keeps failing and I am trying to figure out why. I've modified it to:

    func main() {
        x = lambda(ref f, ref g) {
            print(f);
            print(g);
            print(f == g);
            print("I made it past the first");
            print(a == b);
            print("I made it past the second");
            f = g;
            print(f == g);
            print(a == b);
        };
        a = 5;
        b = 10;
        x(a, b);
        print(a == b);

        /*
        *OUT*
        false
        false
        true
        true
        true
        *OUT*
        */
    }

    """

    - The continual point of failure seems to be the interpreter is recognizing 'a' as a function instead of a value. Possible places the error is occuring:

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
            self.__assign_param_value(formal_ast, actual_ast, func_ast, formal_args, actual_args)

        _, return_val = self.__run_statements(func_ast.get("statements"))

        if(func_ast.elem_type == InterpreterBase.LAMBDA_DEF):
            self.env.pop()
            self.env = original_env
        else:
            self.env.pop()
        return return_val
    
    def __assign_param_value(self, formal_ast, actual_ast, func_ast, formal_args, actual_args):
        original_env = self.env
        if formal_ast.elem_type == InterpreterBase.REFARG_DEF:
            if func_ast.elem_type == InterpreterBase.LAMBDA_DEF:
                result = original_env.get(actual_ast.get("name"))
            else:
                result = self.env.get(actual_ast.get("name"))
            result.ref_flag = True
        else:
            result = copy.deepcopy(self.__eval_expr(actual_ast))
        arg_name = formal_ast.get("name")
        self.env.create(arg_name, result)
        return

    or it could be at:

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

    since the error I get when I run python3 test.py is -> super().error(ErrorType.NAME_ERROR, f"Function {name} not found") where {name} is 'a'. It could be here or
    it could be during variable assignment.

    This is where I have variable assignment:

    def __assign(self, assign_ast):
        var_name = assign_ast.get("name")
        value_obj = self.__eval_expr(assign_ast.get("expression"))
        self.env.set(var_name, value_obj)


        #Handle lambdas, lambdas pass-by-ref
        for formal_ast, actual_ast in zip(formal_args, actual_args):
            #Case: It is a reference, but not with a lambda
            if formal_ast.elem_type != InterpreterBase.REFARG_DEF:
                result = copy.deepcopy(self.__eval_expr(actual_ast))
                result.ref_flag = True
            #Case: It is a refernce, but is also with a lambda
            elif formal_ast.elem_type == InterpreterBase.REFARG_DEF and func_ast.elem_type == InterpreterBase.LAMBDA_DEF:
                result = original_env.get(actual_ast.get("name"))
            #Case: It is a reference, but not with a lambda
            elif formal_ast.elem_type == InterpreterBase.REFARG_DEF and func_ast.elem_type != InterpreterBase.LAMBDA_DEF:
                result = self.env.get(actual_ast.get("name"))
            else:
                super().error(ErrorType.TYPE_ERROR)
            result.ref_flag = True
            arg_name = formal_ast.get("name")
            self.env.create(arg_name, result)

        (base) harrisdoan@Harris-MacBook-Pro fall-23-autograder % python3 test.py
true -> it prints true once, this is the print(f==g) line. However, it doesn't continue.
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/test.py", line 36, in <module>
    main()
  File "/Users/harrisdoan/CS131/fall-23-autograder/test.py", line 32, in main
    interpreter.run(program1)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 44, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 84, in __run_statements
    self.__call_func(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 145, in __call_func
    _, return_val = self.__run_statements(func_ast.get("statements"))
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 84, in __run_statements
    self.__call_func(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 104, in __call_func
    return self.__call_print(call_node)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 158, in __call_print
    result = self.__eval_expr(arg)  # result is a Value object
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 206, in __eval_expr
    return self.__eval_op(expr_ast)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 213, in __eval_op
    left_value_obj = self.__eval_expr(arith_ast.get("op1"))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 196, in __eval_expr
    func_name = self.__get_func_by_name(var_name, None)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 58, in __get_func_by_name
    super().error(ErrorType.NAME_ERROR, f"Function {name} not found")
  File "/Users/harrisdoan/CS131/fall-23-autograder/intbase.py", line 74, in error
    raise Exception(f"{error_type}{description}")
Exception: ErrorType.NAME_ERROR: Function a not found

I think these modifications are putting me on the right track. 