Notes:

(base) harrisdoan@Harris-MacBook-Pro fall-23-autograder % python3 tester.py 2
Running 15 tests...
Running v2/tests/test_overload.br... 
Exception: 
ErrorType.NAME_ERROR: Variable b not found
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 30, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 49, in __run_statements
    self.__call_func(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 138, in __call_func
    result = self.__run_statements(func_def.get("statements"))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 49, in __run_statements
    self.__call_func(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 111, in __call_func
    return self.__call_print(call_node)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 158, in __call_print
    result = self.__eval_expr(arg)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 209, in __eval_expr
    super().error(ErrorType.NAME_ERROR, f"Variable {var_name} not found")
  File "/Users/harrisdoan/CS131/fall-23-autograder/intbase.py", line 74, in error
    raise Exception(f"{error_type}{description}")
Exception: ErrorType.NAME_ERROR: Variable b not found
 FAILED
Running v2/tests/test_nested_expr.br...  PASSED
Running v2/tests/test_and_or.br...  PASSED
Running v2/tests/test_shadow2.br... 
Exception: 
'NoneType' object has no attribute 'get'
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 30, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 49, in __run_statements
    self.__call_func(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 111, in __call_func
    return self.__call_print(call_node)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 158, in __call_print
    result = self.__eval_expr(arg)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 207, in __eval_expr
    val = self.env.get(var_name)
          ^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
 FAILED
Running v2/tests/test_recur3.br... 
Expected output:
['5']

Actual output:
['']
 FAILED
Running v2/tests/test_concat_str.br...  PASSED
Running v2/tests/test_call2.br...  PASSED
Running v2/tests/test_nested_ret.br... 
Exception: 
'NoneType' object has no attribute 'get'
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 30, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 49, in __run_statements
    self.__call_func(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 111, in __call_func
    return self.__call_print(call_node)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 158, in __call_print
    result = self.__eval_expr(arg)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 207, in __eval_expr
    val = self.env.get(var_name)
          ^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
 FAILED
Running v2/tests/test_recur1.br... 
Exception: 
'NoneType' object is not iterable
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 30, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 49, in __run_statements
    self.__call_func(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 111, in __call_func
    return self.__call_print(call_node)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 152, in __call_print
    result = self.__call_func(arg)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 138, in __call_func
    result = self.__run_statements(func_def.get("statements"))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 51, in __run_statements
    self.__call_if(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 76, in __call_if
    for statements in else_statement:
TypeError: 'NoneType' object is not iterable
 FAILED
Running v2/tests/test_dynamic_scoping2.br...  PASSED
Running v2/fails/test_bad_call1.br...  PASSED
Running v2/fails/test_dynamic_scoping1.br... 
Expected error:
['ErrorType.NAME_ERROR']

Received error:
['None']

Exception: 
'NoneType' object has no attribute 'get'
Traceback (most recent call last):
  File "/Users/harrisdoan/CS131/fall-23-autograder/tester.py", line 52, in run_test_case
    interpreter.run(program)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 30, in run
    self.__run_statements(main_func.get("statements"))
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 49, in __run_statements
    self.__call_func(statement)
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 111, in __call_func
    return self.__call_print(call_node)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 158, in __call_print
    result = self.__eval_expr(arg)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/harrisdoan/CS131/fall-23-autograder/interpreterv2.py", line 207, in __eval_expr
    val = self.env.get(var_name)
          ^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
 FAILED
Running v2/fails/test_bad_expr5.br...  PASSED
Running v2/fails/test_bad_expr2.br...  PASSED
Running v2/fails/test_bad_cond1.br... 
Expected error:
['ErrorType.TYPE_ERROR']

Actual output:
[]
 FAILED
8/15 tests passed.
Total Score:     53.33%

Fails:
- test_bad_call1.br -- PASSED
- test_bad_cond1.br -- PASSED
- test_bad_expr2.br -- PASSED
- test_bad_expr5.br -- PASSED
- test_dynamic_scoping1.br -- FAILED

Tests:
- test_and_or.br -- PASSED
- test_call2.br -- PASSED
- test_concat_str.br -- PASSED
- test_dynamic_scoping2.br -- PASSED
- test_nested_expr.br -- PASSED
- test_nested_ret.br -- FAILED
- test_overload.br -- FAILED
- test_recur1.br -- FAILED
_ test_recur3.br -- FAILED
- test_shadow2.br -- FAILED


After my nearly 40 submissions to the Gradescope tester, I realized that using that as a check every time was gonna make it really hard to focus on a single problem. So as I went to solve one issue, it would cause four new issues to arise. And now there was 4 problems instead of 1. So I started using the auto-grader and eventually I realized how useful the other test cases were. Using the name of the test cases in the auto-grader I was able to figure out that problem in my code. Once, I realize the logic and how the enviornment manager was supposed to be use in terms of scoping, everything started to come together. Comparing the solution code to my own code in interpreterv1.py, I realized how easy a modular code was. Instead of just doing everything within an if block or else block, I can create a function to handle it all. This overall cleaned up my code nicely and made it 10000x easier to figure out what my problem was. Biggest error for my was modifying anything in the env_v1.py file. I was thinking to just copy the enviornment at each function call and append that to the stack, almost like a function call stack like we learned in CS33. But I came to realize the implementation was extremely flawed and wasn't going to work how I wanted it to. Thats when I moved to the scope being a list of environments that we could be working on. We could append and remove from the list as we process user-defined functions. One of the biggest things that kept throwing me off was the "for statement in statements:" I would mess up by writing statements instead of statements, so that was the most frustrating, hair pulling debugging process of my life. The other error that kept making me fail basic cases were the NOT_DEF and NEG_DEF. I didn't have a line to check to make sure the thing passed in is able to be negated or logical not. I had to check for anything in the NOT_DEF that the type was an actual bool and not something like an int. And then the same thing applied to the NEG_DEF. So...after 40+ tries, all good! 

(base) harrisdoan@Harris-MacBook-Pro fall-23-autograder % python3 tester.py 2
Running 15 tests...
Running v2/tests/test_overload.br...  PASSED
Running v2/tests/test_nested_expr.br...  PASSED
Running v2/tests/test_and_or.br...  PASSED
Running v2/tests/test_shadow2.br...  PASSED
Running v2/tests/test_recur3.br...  PASSED
Running v2/tests/test_concat_str.br...  PASSED
Running v2/tests/test_call2.br...  PASSED
Running v2/tests/test_nested_ret.br...  PASSED
Running v2/tests/test_recur1.br...  PASSED
Running v2/tests/test_dynamic_scoping2.br...  PASSED
Running v2/fails/test_bad_call1.br...  PASSED
Running v2/fails/test_dynamic_scoping1.br...  PASSED
Running v2/fails/test_bad_expr5.br...  PASSED
Running v2/fails/test_bad_expr2.br...  PASSED
Running v2/fails/test_bad_cond1.br...  PASSED
15/15 tests passed.
Total Score:    100.00%


(base) harrisdoan@Harris-MacBook-Pro MORE-TESTS---131-Fall-2023 % python3 tester.py 2
Running 47 tests...
Running v2/tests/test_unaries.br...  PASSED
Running v2/tests/test_ret_in_condition.br...  PASSED
Running v2/tests/basic_int_compare.br...  PASSED
Running v2/tests/test_cond.br...  PASSED
Running v2/tests/test_and_or_2.br...  PASSED
Running v2/tests/test_overload.br...  PASSED
Running v2/tests/test_nested_expr.br...  PASSED
Running v2/tests/test_nil.br...  PASSED
Running v2/tests/test_call.br...  PASSED
Running v2/tests/test_and_or.br...  PASSED
Running v2/tests/test_ret2.br...  PASSED
Running v2/tests/test_weird_equality.br...  PASSED
Running v2/tests/test_types.br...  PASSED
Running v2/tests/test_shadow2.br...  PASSED
Running v2/tests/test_inputi.br...  PASSED
Running v2/tests/compare_int_return.br...  PASSED
Running v2/tests/test_recur3.br...  PASSED
Running v2/tests/test_concat_str.br...  PASSED
Running v2/tests/func_execution_compare.br...  PASSED
Running v2/tests/test_print.br...  PASSED
Running v2/tests/test_call2.br...  PASSED
Running v2/tests/test_nested_ret.br...  PASSED
Running v2/tests/test_premature_while_ret.br...  PASSED
Running v2/tests/test_recur1.br...  PASSED
Running v2/tests/while_loop_compare.br...  PASSED
Running v2/tests/recursive_compare.br...  PASSED
Running v2/tests/test_ret1.br...  PASSED
Running v2/tests/test_while.br...  PASSED
Running v2/tests/if_stmt_compare.br...  PASSED
Running v2/tests/test_inputs.br...  PASSED
Running v2/tests/test_cmp1.br...  PASSED
Running v2/tests/test_str_cmp.br...  PASSED
Running v2/tests/test_dynamic_scoping2.br...  PASSED
Running v2/tests/test_bool_cmp.br...  PASSED
Running v2/tests/test_int_cmp.br...  PASSED
Running v2/tests/test_ret_nil_.br...  PASSED
Running v2/tests/int_compare_vars.br...  PASSED
Running v2/fails/test_bad_call1.br...  PASSED
Running v2/fails/test_dynamic_scoping1.br...  PASSED
Running v2/fails/test_bad_expr5.br...  PASSED
Running v2/fails/test_bad_expr_n.br...  PASSED
Running v2/fails/invalid_dynamic_scoping3.br...  PASSED
Running v2/fails/invalid_arithmetic.br...  PASSED
Running v2/fails/invalid_dynamic_scoping2.br...  PASSED
Running v2/fails/invalid_arithmetic_2.br...  PASSED
Running v2/fails/test_bad_expr2.br...  PASSED
Running v2/fails/test_bad_cond1.br...  PASSED
47/47 tests passed.
Total Score:    100.00%



ALL GOOD!