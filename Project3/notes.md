me:

(base) harrisdoan@Harris-MacBook-Pro fall-23-autograder % python3 tester.py 3
Running 9 tests...
Running v3/tests/test_func_with_val2.br... 
Exception: 
ErrorType.NAME_ERROR: Variable bar not found
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 44, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 91, in __run_statements
    self.__assign(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 182, in __assign
    value_obj = self.__eval_expr(assign_ast.get("expression"))
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 201, in __eval_expr
    return self.__call_func(expr_ast)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 148, in __call_func
    _, return_val = self.__run_statements(func_ast.get("statements"))
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 93, in __run_statements
    status, return_val = self.__do_return(statement)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 381, in __do_return
    value_obj = copy.deepcopy(self.__eval_expr(expr_ast))
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 198, in __eval_expr
    super().error(ErrorType.NAME_ERROR, f"Variable {var_name} not found")
  File "/Users/harrisdoan/CS131/fall-23-autograder/intbase.py", line 74, in error
    raise Exception(f"{error_type}{description}")
Exception: ErrorType.NAME_ERROR: Variable bar not found
 FAILED
Running v3/tests/test_promo1.br...  PASSED
Running v3/tests/test_ref2.br... 
Expected output:
['16']

Actual output:
['5']
 FAILED
Running v3/tests/test_func_comp1.br... 
Exception: 
ErrorType.NAME_ERROR: Variable foo not found
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 44, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 91, in __run_statements
    self.__assign(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 182, in __assign
    value_obj = self.__eval_expr(assign_ast.get("expression"))
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 198, in __eval_expr
    super().error(ErrorType.NAME_ERROR, f"Variable {var_name} not found")
  File "/Users/harrisdoan/CS131/fall-23-autograder/intbase.py", line 74, in error
    raise Exception(f"{error_type}{description}")
Exception: ErrorType.NAME_ERROR: Variable foo not found
 FAILED
Running v3/tests/test_lambda_shadow7.br...  PASSED
Running v3/tests/test_lambda_with_val1.br...  PASSED
Running v3/fails/test_bad_func_ops1.br... 
Expected error:
['ErrorType.TYPE_ERROR']

Received error:
['ErrorType.NAME_ERROR']

Exception: 
ErrorType.NAME_ERROR: Variable main not found
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 44, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 91, in __run_statements
    self.__assign(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 182, in __assign
    value_obj = self.__eval_expr(assign_ast.get("expression"))
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 198, in __eval_expr
    super().error(ErrorType.NAME_ERROR, f"Variable {var_name} not found")
  File "/Users/harrisdoan/CS131/fall-23-autograder/intbase.py", line 74, in error
    raise Exception(f"{error_type}{description}")
Exception: ErrorType.NAME_ERROR: Variable main not found
 FAILED
Running v3/fails/test_bad_func1.br...  PASSED
Running v3/fails/test_overload2.br...  PASSED
5/9 tests passed.
Total Score:     55.56%




me 2:
(base) harrisdoan@Harris-MacBook-Pro fall-23-autograder % python3 tester.py 3
Running 9 tests...
Running v3/tests/test_func_with_val2.br... =: name: a, expression: [fcall: name: foo, args: []]
0
0
return: expression: [var: name: bar]
fcall: name: a, args: [int: val: 10, int: val: 20]
2
2
fcall: name: print, args: [var: name: a, var: name: b]
 PASSED
Running v3/tests/test_promo1.br... =: name: b, expression: [+: op1: [bool: val: True], op2: [int: val: 123]]
fcall: name: print, args: [var: name: b]
=: name: b, expression: [+: op1: [int: val: 123], op2: [bool: val: True]]
fcall: name: print, args: [var: name: b]
=: name: b, expression: [+: op1: [int: val: 123], op2: [bool: val: False]]
fcall: name: print, args: [var: name: b]
=: name: c, expression: [+: op1: [bool: val: True], op2: [bool: val: True]]
fcall: name: print, args: [var: name: c]
=: name: d, expression: [+: op1: [bool: val: False], op2: [bool: val: True]]
fcall: name: print, args: [var: name: d]
 PASSED
Running v3/tests/test_ref2.br... =: name: b, expression: [int: val: 5]
fcall: name: foo, args: [var: name: b]
1
1
else statemetn
=: name: a, expression: [+: op1: [var: name: a], op2: [int: val: 10]]
fcall: name: bar, args: [var: name: a]
1
1
else statemetn
=: name: c, expression: [+: op1: [var: name: c], op2: [int: val: 1]]
fcall: name: print, args: [var: name: b]

Expected output:
['16']

Actual output:
['5']
 FAILED
Running v3/tests/test_func_comp1.br... =: name: a, expression: [var: name: foo]
if: condition: [!=: op1: [var: name: a], op2: [nil]], statements: [fcall: name: print, args: [string: val: Good]], else_statements: None
fcall: name: print, args: [string: val: Good]
if: condition: [!=: op1: [var: name: foo], op2: [nil]], statements: [fcall: name: print, args: [string: val: Good]], else_statements: None
fcall: name: print, args: [string: val: Good]
if: condition: [!=: op1: [nil], op2: [var: name: a]], statements: [fcall: name: print, args: [string: val: Good]], else_statements: None
fcall: name: print, args: [string: val: Good]
if: condition: [!=: op1: [nil], op2: [var: name: foo]], statements: [fcall: name: print, args: [string: val: Good]], else_statements: None
fcall: name: print, args: [string: val: Good]
 PASSED
Running v3/tests/test_lambda_shadow7.br... =: name: b, expression: [int: val: 0]
=: name: f, expression: [lambda: args: [], statements: [=: name: b, expression: [+: op1: [var: name: b], op2: [int: val: 1]], fcall: name: print, args: [var: name: b]]]

Exception: 
'Value' object has no attribute 'env_setup'
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 36, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 84, in __run_statements
    self.__assign(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 179, in __assign
    value_obj = self.__eval_expr(assign_ast.get("expression"))
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 217, in __eval_expr
    return self.__do_lambda(expr_ast)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 405, in __do_lambda
    ret.env_setup(copy.deepcopy(self.env))
    ^^^^^^^^^^^^^
AttributeError: 'Value' object has no attribute 'env_setup'
 FAILED
Running v3/tests/test_lambda_with_val1.br... =: name: a, expression: [int: val: 10]
=: name: b, expression: [lambda: args: [arg: name: a], statements: [fcall: name: print, args: [var: name: a]]]

Exception: 
'Value' object has no attribute 'env_setup'
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 36, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 84, in __run_statements
    self.__assign(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 179, in __assign
    value_obj = self.__eval_expr(assign_ast.get("expression"))
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 217, in __eval_expr
    return self.__do_lambda(expr_ast)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv3.py", line 405, in __do_lambda
    ret.env_setup(copy.deepcopy(self.env))
    ^^^^^^^^^^^^^
AttributeError: 'Value' object has no attribute 'env_setup'
 FAILED
Running v3/fails/test_bad_func_ops1.br... =: name: f, expression: [var: name: main]
if: condition: [>: op1: [var: name: f], op2: [int: val: 10]], statements: [fcall: name: printf, args: [string: val: hi]], else_statements: None
 PASSED
Running v3/fails/test_bad_func1.br... =: name: f, expression: [int: val: 5]
fcall: name: f, args: [int: val: 20]
 PASSED
Running v3/fails/test_overload2.br... fcall: name: bar, args: [var: name: foo]
1
1
 PASSED
6/9 tests passed.
Total Score:     66.67%