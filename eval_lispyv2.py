#!/usr/bin/env python3
'''Lisp interpreter using python3'''

import os
import re
from functools import reduce
# from collections import deque
from lisp_repl import repl
from lisp_globals import (lisp_env)
from lisp_evaluation import eval_comparision


GLOBAL_ENV, OP_ENV, MATH_ENV = lisp_env()
# LOCAL_ENV = {}
LAMBDA_ENV = {}


# class ENV(dict):
#     "An environment: a dict of {'var': val} pairs, with an outer Env."
#     def __init__(self, parms=(), args=(), genv=None):
#         self.update(zip(parms, args))
#         self.genv = genv
#     def find(self, var):
#         "Find the innermost Env where var appears."
#         return self if (var in self) else self.genv.find(var)


class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, params, body):
        self.params, self.body = params, body

    def __call__(self, *args):
        LAMBDA_ENV.update(zip(self.params, args))
        return lisp_evaluator(lisp_evaluator(self.body))

def bool_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[:2] == "#t" or lisp_str[:2] == "#f":
        return lisp_str[:2], lisp_str[2:].strip()
    return None

def symbol_parser(lisp_str):
    re_symbol = re.match(r'[^ \t\n\r\f\v()]+', lisp_str)
    # re_symbol = re.match(r'^\s*[+-]?[\w-]+|[><+-/*%]?\s*', lisp_str)
    if re_symbol:
        symbol, lisp_str = re_symbol.group().strip(), lisp_str[re_symbol.end():].strip()
    else:
        return None

    try:
        symbol = float(symbol)
    except ValueError:
        pass
    try:
        symbol = int(symbol)
    except ValueError:
        pass
    return symbol, lisp_str

def expression_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    exp_list = []
    sub_parsers = [bool_parser, symbol_parser, ]
    while lisp_str and lisp_str.strip()[0] != ")":
        for sub_parser in sub_parsers:
            sub_parsed = sub_parser(lisp_str)
            if sub_parsed and sub_parsed[0]:
                parsed, lisp_str = sub_parsed
                exp_list.append(parsed)

        if lisp_str[0] == '(':
            nested_exp = expression_parser(lisp_str[1:])
            parsed, lisp_str = nested_exp[0], nested_exp[1].strip()
            exp_list.append(parsed)
    return exp_list, lisp_str[1:]

def input_parser(lisp_str):
    lisp_str = lisp_str.strip()
    if lisp_str[0] == "(":
        lisp_str = lisp_str[1:]
    else:
        return None
    parsed_lists = []
    while expression_parser(lisp_str):
        expression_parsed, lisp_str = expression_parser(lisp_str)
        if expression_parsed:
            parsed_lists.extend(expression_parsed)
    # print(parsed_lists, lisp_str)
    return parsed_lists, lisp_str

def lisp_interpreter(lisp_str):
    lisp_str = lisp_str.strip()
    if not lisp_str:
        return None
    lisp_parsed = input_parser(lisp_str)
    if lisp_parsed and lisp_parsed[0]:
        parsed, _ = input_parser(lisp_str)
        print(parsed)
        return parsed
    return None

def get_value(key):
    value = LAMBDA_ENV.get(key, False) or GLOBAL_ENV.get(key, False)
    return value

def lisp_evaluator(parsed):
    keywords = ['define', 'if', 'lambda', 'quote', 'list', 'range', ]
    if not parsed:
        return None

    if isinstance(parsed, (int, float)):
        return parsed

    if isinstance(parsed, str):
        return get_value(parsed)

    operation, *arguments = parsed

    if operation in keywords:
        return keyword_eval(operation, arguments)

    if operation in OP_ENV or MATH_ENV:
        return eval_math(operation, arguments)


    # math_procedure = eval_math(operation, arguments)
    # if math_procedure:
    #     return math_procedure

    if operation == 'define':
        variable, exp = arguments
        if variable in GLOBAL_ENV:
            print("\ncant define variable.. its standard.. Dont mess with standards\n ")
            return None
        GLOBAL_ENV[variable] = lisp_evaluator(exp)
        return "OK"


    print(arguments)
    if operation == 'if':
        condition, output, alt_output = arguments
        return lisp_evaluator(output if lisp_evaluator(condition) else alt_output)
    if operation == 'quote':
        return arguments[0]
    if operation == 'lambda':
        parameters, body = arguments
        # parameters = [lisp_evaluator(param) for param in parameters]
        return Procedure(parameters, body)
    if operation == "range":
        arg_list = [lisp_evaluator(argument) for argument in arguments]
        return tuple(reduce(range, arg_list))
    if operation == 'list':
        return [lisp_evaluator(argument) for argument in arguments]

    proc = get_value(operation)
    if operation in ["<", ">", "<=", ">=",]:
        arg_list = [lisp_evaluator(argument) for argument in arguments]
        return OP_ENV[eval_comparision(proc, arg_list)]

    if operation in OP_ENV:
        arg_list = [lisp_evaluator(argument) for argument in arguments]
        print(arg_list)
        return reduce(proc, arg_list)
    if operation in MATH_ENV:
        if len(arguments) == 1:
            return proc(arguments[0])
        arg1, arg2 = arguments
        return proc(arg1, arg2)

    return None

def keyword_eval(keyword, arguments):
    if keyword == 'define':
        variable, exp = arguments
        if variable in GLOBAL_ENV:
            print("\ncant define variable.. its standard.. Dont mess with standards\n ")
            return None
        GLOBAL_ENV[variable] = lisp_evaluator(exp)
        return "OK"

    if keyword == 'if':
        condition, output, alt_output = arguments
        return lisp_evaluator(output if lisp_evaluator(condition) else alt_output)
    if keyword == 'quote':
        return arguments[0]
    if keyword == 'lambda':
        parameters, body = arguments
        # parameters = [lisp_evaluator(param) for param in parameters]
        return Procedure(parameters, body)
    if keyword == "range":
        arg_list = [lisp_evaluator(argument) for argument in arguments]
        return tuple(reduce(range, arg_list))
    if keyword == 'list':
        return [lisp_evaluator(argument) for argument in arguments]

def eval_math(operation, arguments):
    procedure = GLOBAL_ENV.get(operation, False)
    if  not procedure:
        return None

    if operation in ["<", ">", "<=", ">=",]:
        arguments = [lisp_evaluator(argument) for argument in arguments]
        return OP_ENV[eval_comparision(procedure, arguments)]

    if operation in OP_ENV:
        arguments = [lisp_evaluator(argument) for argument in arguments]
        print(arguments)
        return reduce(procedure, arguments)

    if operation in MATH_ENV:
        arguments = [lisp_evaluator(argument) for argument in arguments]
        if len(arguments) == 1:
            return procedure(arguments[0])
        arg1, arg2 = arguments
        return procedure(arg1, arg2)
    return None


def main():
    try:
        os.system("clear||cls")
        while True:
            output = lisp_evaluator(lisp_interpreter(repl()))
            if output:
                print(output)
            # else:
            #     print("\nsyntax error\n")
    except KeyboardInterrupt:
        print("\n\n\tExiting Lisp interpreter..\n\n")
    # except:
    #     print("\nSyntax error\n")
    #     os.sys.exit()

if __name__ == '__main__':
    main()
